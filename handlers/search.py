"""FSM and result navigation for lead searches."""

from __future__ import annotations

import asyncio
import html
import logging
import time
from collections import Counter
from dataclasses import dataclass

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import lead_collector as collector
from lead_scorer import LEAD_TYPES
from locations import TOP_LOCATIONS
from services.instagram_enrichment import InstagramEnrichmentService
from services.lead_pipeline import (
    LeadPipeline,
    SearchAlreadyRunningError,
    SearchTimeoutError,
    SearchResult,
)
from services.presentation import make_page

router = Router(name=__name__)
logger = logging.getLogger(__name__)
background_tasks: set[asyncio.Task[None]] = set()
NEW_SEARCH_DEBOUNCE_SECONDS = 2.0

LEAD_TYPE_LABELS = {
    "NO_WEBSITE": "Без сайту",
    "INSTAGRAM_ONLY": "Instagram",
    "GOOGLE_MAPS_ONLY": "Google Maps",
    "BUSINESS_SITE": "Business Site",
    "SOCIAL_ONLY": "Соцмережі",
    "HTTP_WEBSITE": "HTTP",
    "MODERN_WEBSITE": "HTTPS",
    "UNKNOWN": "Невідомо",
}


class SearchForm(StatesGroup):
    country = State()
    region = State()
    cities = State()
    niche = State()
    limit = State()
    instagram_only = State()
    confirm = State()


@dataclass(slots=True)
class ViewState:
    page: int = 0
    high_only: bool = False
    lead_type: str | None = None


view_states: dict[int, ViewState] = {}


class NewSearchDebouncer:
    def __init__(self, cooldown_seconds: float) -> None:
        self.cooldown_seconds = cooldown_seconds
        self._last_click: dict[int, float] = {}

    def accept(self, user_id: int, now: float | None = None) -> bool:
        current = time.monotonic() if now is None else now
        previous = self._last_click.get(user_id)
        if previous is not None and current - previous < self.cooldown_seconds:
            return False
        self._last_click[user_id] = current
        return True

    def reset(self, user_id: int) -> None:
        self._last_click.pop(user_id, None)


new_search_debouncer = NewSearchDebouncer(NEW_SEARCH_DEBOUNCE_SECONDS)


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Новий пошук")]],
        resize_keyboard=True,
    )


def cities_keyboard(
    country_code: str | None = None, regions: list[str] | None = None
) -> ReplyKeyboardMarkup:
    buttons: list[KeyboardButton] = []
    reg_list = [r for r in (regions or []) if r]
    if country_code and country_code in TOP_LOCATIONS and reg_list:
        country_regions = TOP_LOCATIONS[country_code]
        seen_cities: set[str] = set()
        for r_name in reg_list:
            cities_list = country_regions.get(r_name)
            if not cities_list:
                for reg_key, c_list in country_regions.items():
                    if reg_key.lower() == r_name.lower():
                        cities_list = c_list
                        break
            if cities_list:
                for city in cities_list:
                    if city not in seen_cities:
                        seen_cities.add(city)
                        buttons.append(KeyboardButton(text=city))

    keyboard: list[list[KeyboardButton]] = [
        buttons[i : i + 2] for i in range(0, len(buttons), 2)
    ]
    if reg_list:
        keyboard.append([KeyboardButton(text="Шукати по обраних регіонах")])
        keyboard.append([KeyboardButton(text="Шукати по всій країні")])
    else:
        keyboard.append([KeyboardButton(text="Шукати по всій країні")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def country_keyboard() -> ReplyKeyboardMarkup:
    countries = [KeyboardButton(text=name) for name in collector.country_options()]
    return ReplyKeyboardMarkup(
        keyboard=[
            countries[index : index + 2] for index in range(0, len(countries), 2)
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def region_keyboard(
    country_code: str | None = None, selected_regions: list[str] | None = None
) -> ReplyKeyboardMarkup:
    selected = set(selected_regions or [])
    buttons: list[KeyboardButton] = []
    if country_code and country_code in TOP_LOCATIONS:
        for reg in TOP_LOCATIONS[country_code].keys():
            marker = "✅ " if reg in selected else ""
            buttons.append(KeyboardButton(text=f"{marker}{reg}"))

    keyboard: list[list[KeyboardButton]] = [
        buttons[i : i + 2] for i in range(0, len(buttons), 2)
    ]
    if selected:
        keyboard.append(
            [KeyboardButton(text=f"➡️ Продовжити з обраними ({len(selected)})")]
        )
        keyboard.append([KeyboardButton(text="Скинути вибір / Пропустити")])
    else:
        keyboard.append([KeyboardButton(text="Пропустити регіон")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def instagram_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Всі компанії"),
                KeyboardButton(text="Тільки з Instagram"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Запустити", callback_data="search:run")],
            [InlineKeyboardButton(text="Новий пошук", callback_data="search:new")],
        ]
    )


def new_search_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Новий пошук", callback_data="search:new")]
        ]
    )


def results_keyboard(
    result: SearchResult | None = None,
    view: ViewState | None = None,
) -> InlineKeyboardMarkup:
    current_view = view or ViewState()
    counts = (
        Counter(row.get("lead_type", "UNKNOWN") for row in result.rows)
        if result
        else Counter()
    )
    type_buttons = [
        InlineKeyboardButton(
            text=(
                f"{'✓ ' if current_view.lead_type is None else ''}"
                f"Усі типи{f' · {result.total}' if result else ''}"
            ),
            callback_data="results:type:ALL",
        )
    ]
    for lead_type in LEAD_TYPES:
        count = counts[lead_type]
        if result is not None and count == 0:
            continue
        marker = "✓ " if current_view.lead_type == lead_type else ""
        suffix = f" · {count}" if result is not None else ""
        type_buttons.append(
            InlineKeyboardButton(
                text=f"{marker}{LEAD_TYPE_LABELS[lead_type]}{suffix}",
                callback_data=f"results:type:{lead_type}",
            )
        )

    type_rows = [
        type_buttons[index : index + 2] for index in range(0, len(type_buttons), 2)
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Попередні 10", callback_data="results:previous"
                ),
                InlineKeyboardButton(text="Наступні 10", callback_data="results:next"),
            ],
            [
                InlineKeyboardButton(
                    text="Усі priority" if current_view.high_only else "Тільки HIGH",
                    callback_data="results:high",
                )
            ],
            *type_rows,
            [InlineKeyboardButton(text="Завантажити CSV", callback_data="results:csv")],
            [InlineKeyboardButton(text="Новий пошук", callback_data="search:new")],
        ]
    )


async def begin_search(
    message: Message,
    state: FSMContext,
    pipeline: LeadPipeline,
    user_id: int | None = None,
) -> None:
    effective_user_id = user_id or (message.from_user.id if message.from_user else None)
    if effective_user_id is not None and await pipeline.is_running(effective_user_id):
        await message.answer("Поточний пошук ще виконується. Дочекайтеся завершення.")
        return
    await state.clear()
    await state.set_state(SearchForm.country)
    await message.answer("Оберіть країну.", reply_markup=country_keyboard())


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(
        "Бот збирає компанії через Overture Maps і виконує локальний скоринг.",
        reply_markup=main_keyboard(),
    )


@router.message(F.text == "Новий пошук")
async def new_search_message(
    message: Message, state: FSMContext, pipeline: LeadPipeline
) -> None:
    user_id = message.from_user.id if message.from_user else None
    if user_id is not None and not new_search_debouncer.accept(user_id):
        await message.answer("Новий пошук уже відкрито.")
        return
    await begin_search(message, state, pipeline, user_id=user_id)


@router.callback_query(F.data == "search:new")
async def new_search_callback(
    callback: CallbackQuery, state: FSMContext, pipeline: LeadPipeline
) -> None:
    user_id = callback.from_user.id
    if not new_search_debouncer.accept(user_id):
        await callback.answer("Новий пошук уже відкрито.")
        return
    await callback.answer()
    if callback.message:
        await begin_search(
            callback.message,
            state,
            pipeline,
            user_id=user_id,
        )


@router.message(SearchForm.country)
async def receive_country(message: Message, state: FSMContext) -> None:
    try:
        country = collector.parse_country(message.text or "")
    except ValueError as error:
        await message.answer(f"Некоректна країна: {error}")
        return
    await state.update_data(
        country_code=country.code,
        country_name=country.name,
        regions=[],
    )
    await state.set_state(SearchForm.region)
    await message.answer(
        "Оберіть один або кілька штатів/регіонів (клікайте по кнопках або введіть через кому).\n"
        "Або натисніть «Пропустити регіон».",
        reply_markup=region_keyboard(country.code),
    )


@router.message(SearchForm.region)
async def receive_region(message: Message, state: FSMContext) -> None:
    raw_text = (message.text or "").strip()
    data = await state.get_data()
    country_code = data.get("country_code")
    current_regions: list[str] = list(data.get("regions") or [])

    if raw_text in {"Пропустити регіон", "Скинути вибір / Пропустити"}:
        await state.update_data(regions=[])
        await state.set_state(SearchForm.cities)
        await message.answer(
            "Регіони пропущено.\n"
            "Введіть міста через кому або натисніть «Шукати по всій країні».",
            reply_markup=cities_keyboard(country_code, []),
        )
        return

    if raw_text.startswith("➡️ Продовжити"):
        await state.set_state(SearchForm.cities)
        regions_display = ", ".join(current_regions)
        await message.answer(
            f"Обрано регіони: {regions_display}.\n"
            "Оберіть місто з кнопок нижче, введіть свої через кому, або натисніть «Шукати по обраних регіонах».",
            reply_markup=cities_keyboard(country_code, current_regions),
        )
        return

    clean_text = raw_text.removeprefix("✅ ").strip()
    known_regions = TOP_LOCATIONS.get(country_code, {}) if country_code else {}
    matched_region = None
    for r_name in known_regions.keys():
        if r_name.lower() == clean_text.lower():
            matched_region = r_name
            break

    if matched_region:
        if matched_region in current_regions:
            current_regions.remove(matched_region)
        else:
            current_regions.append(matched_region)
        await state.update_data(regions=current_regions)
        count = len(current_regions)
        status_text = (
            f"Обрано ({count}): {', '.join(current_regions)}.\n"
            "Можете обрати ще один регіон, або натисніть «➡️ Продовжити з обраними»."
            if count
            else "Вибір очищено. Оберіть регіон або натисніть «Пропустити регіон»."
        )
        await message.answer(
            status_text,
            reply_markup=region_keyboard(country_code, current_regions),
        )
        return

    typed_regions = [r.strip() for r in raw_text.split(",") if r.strip()]
    if typed_regions:
        await state.update_data(regions=typed_regions)
        await state.set_state(SearchForm.cities)
        await message.answer(
            f"Обрано регіони: {', '.join(typed_regions)}.\n"
            "Оберіть місто з кнопок нижче, введіть свої через кому, або натисніть «Шукати по обраних регіонах».",
            reply_markup=cities_keyboard(country_code, typed_regions),
        )
        return

    await message.answer(
        "Оберіть регіон зі списку або введіть назву.",
        reply_markup=region_keyboard(country_code, current_regions),
    )


@router.message(SearchForm.cities)
async def receive_cities(message: Message, state: FSMContext) -> None:
    raw_cities = (message.text or "").strip()
    data = await state.get_data()

    if raw_cities in {
        "Шукати по всій країні",
        "Уся країна",
        collector.WHOLE_COUNTRY_SCOPE_NAME,
    }:
        cities: list[str] = []
        await state.update_data(regions=[])
    elif raw_cities in {
        "Шукати по обраних регіонах",
        "Пропустити міста",
    }:
        cities = []
    else:
        try:
            cities = collector.parse_cities(raw_cities)
            if cities == [collector.WHOLE_COUNTRY_SCOPE_NAME]:
                cities = []
                await state.update_data(regions=[])
        except ValueError as error:
            await message.answer(f"Некоректний список міст: {error}")
            return

    await state.update_data(cities=cities)
    await state.set_state(SearchForm.niche)
    await message.answer(
        "Введіть нішу, наприклад: Dental або автосервіс.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(SearchForm.niche)
async def receive_niche(message: Message, state: FSMContext) -> None:
    niche = (message.text or "").strip()
    if not niche:
        await message.answer("Ніша не може бути порожньою. Спробуйте ще раз.")
        return
    try:
        collector.niche_filter(niche)
    except ValueError as error:
        await message.answer(f"Не вдалося розпізнати нішу: {error}")
        return
    await state.update_data(niche=niche)
    await state.set_state(SearchForm.limit)
    await message.answer("Введіть потрібну кількість компаній.")


@router.message(SearchForm.limit)
async def receive_limit(message: Message, state: FSMContext) -> None:
    try:
        limit = collector.positive_int((message.text or "").strip())
    except (ValueError, TypeError):
        await message.answer("Ліміт має бути цілим числом, більшим за нуль.")
        return

    await state.update_data(limit=limit)
    await state.set_state(SearchForm.instagram_only)
    await message.answer(
        "Шукати тільки компанії з Instagram чи показувати всі?",
        reply_markup=instagram_keyboard(),
    )


@router.message(SearchForm.instagram_only)
async def receive_instagram_only(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip().lower()
    instagram_only = "тільки з instagram" in text or ("instagram" in text and "всі" not in text)
    await state.update_data(instagram_only=instagram_only)
    data = await state.get_data()
    await state.set_state(SearchForm.confirm)
    regions: list[str] = list(data.get("regions") or [])
    cities: list[str] = list(data.get("cities") or [])
    if cities:
        scope_display = ", ".join(cities)
    elif regions:
        scope_display = f"усі в регіонах: {', '.join(regions)}"
    else:
        scope_display = f"уся країна ({data['country_name']})"

    regions_display = ", ".join(regions) if regions else "— (вся країна)"
    ig_filter_display = "Тільки з Instagram" if instagram_only else "Всі компанії"
    await message.answer(
        "<b>Перевірте параметри</b>\n"
        f"Країна: {html.escape(data['country_name'])}\n"
        f"Регіони: {html.escape(regions_display)}\n"
        f"Scope: {html.escape(scope_display)}\n"
        f"Ніша: {html.escape(data['niche'])}\n"
        f"Фільтр: {ig_filter_display}\n"
        f"Ліміт: {data['limit']}",
        reply_markup=confirm_keyboard(),
    )


async def refresh_instagram_enrichment(
    result_message: Message,
    result: SearchResult,
    instagram_enrichment: InstagramEnrichmentService,
) -> None:
    try:
        await instagram_enrichment.enrich_rows(result.rows)
        view = view_states.get(result.user_id, ViewState())
        page = make_page(result, view.page, view.high_only, view.lead_type)
        await result_message.edit_text(
            page.text,
            reply_markup=results_keyboard(result, view),
        )
    except Exception:
        logger.exception("Could not refresh Instagram enrichment")


async def send_search_result(
    message: Message,
    result: SearchResult,
    instagram_enrichment: InstagramEnrichmentService,
) -> None:
    view = ViewState()
    view_states[result.user_id] = view
    instagram_profiles = instagram_enrichment.prepare_rows(result.rows)
    page = make_page(result, page=0, high_only=False, lead_type=None)
    coverage_warning = collector.niche_coverage_warning(result.niche)
    if coverage_warning:
        await message.answer(coverage_warning)
    result_message = await message.answer(
        page.text,
        reply_markup=results_keyboard(result, view),
    )
    await message.answer_document(
        FSInputFile(result.csv_path, filename="scored_leads.csv"),
        caption="Повний scored_leads.csv",
        reply_markup=new_search_keyboard(),
    )
    if instagram_profiles and instagram_enrichment.enabled:
        task = asyncio.create_task(
            refresh_instagram_enrichment(
                result_message,
                result,
                instagram_enrichment,
            )
        )
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)


async def run_search_in_background(
    message: Message,
    pipeline: LeadPipeline,
    user_id: int,
    niche: str,
    cities: list[str],
    limit: int,
    instagram_enrichment: InstagramEnrichmentService,
    country_code: str | None = None,
    country_name: str = "",
    regions: list[str] | None = None,
    instagram_only: bool = False,
) -> None:
    try:
        result = await pipeline.run(
            user_id,
            niche,
            cities,
            limit,
            country_code=country_code,
            country_name=country_name,
            regions=regions,
            instagram_only=instagram_only,
        )
        await send_search_result(message, result, instagram_enrichment)
    except SearchAlreadyRunningError:
        await message.answer(
            "Пошук уже виконується. Дочекайтеся завершення.",
            reply_markup=new_search_keyboard(),
        )
    except SearchTimeoutError as error:
        await message.answer(
            str(error),
            reply_markup=new_search_keyboard(),
        )
    except Exception:
        logger.exception("Lead search failed for user %s", user_id)
        await message.answer(
            "Не вдалося завершити пошук. Перевірте мережу та параметри й спробуйте ще раз.",
            reply_markup=new_search_keyboard(),
        )


@router.callback_query(SearchForm.confirm, F.data == "search:run")
async def run_search(
    callback: CallbackQuery,
    state: FSMContext,
    pipeline: LeadPipeline,
    instagram_enrichment: InstagramEnrichmentService,
) -> None:
    if not callback.from_user or not callback.message:
        await callback.answer()
        return
    if await pipeline.is_running(callback.from_user.id):
        await callback.answer("Пошук уже виконується.", show_alert=True)
        return

    data = await state.get_data()
    required = {"country_code", "country_name", "niche", "cities", "limit"}
    if not required.issubset(data):
        await callback.answer(
            "Параметри застаріли. Почніть новий пошук.", show_alert=True
        )
        return

    await callback.answer()
    await state.clear()
    await callback.message.answer("Пошук запущено. Це може зайняти кілька хвилин.")
    regions = list(data.get("regions") or [])
    task = asyncio.create_task(
        run_search_in_background(
            callback.message,
            pipeline,
            callback.from_user.id,
            data["niche"],
            data["cities"],
            data["limit"],
            instagram_enrichment,
            country_code=data["country_code"],
            country_name=data["country_name"],
            regions=regions,
            instagram_only=data.get("instagram_only", False),
        )
    )
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)


async def update_result_message(
    callback: CallbackQuery, pipeline: LeadPipeline, action: str
) -> None:
    user_id = callback.from_user.id
    result = pipeline.get_result(user_id)
    if result is None or not callback.message:
        await callback.answer("Немає активного результату.", show_alert=True)
        return

    view = view_states.setdefault(user_id, ViewState())
    previous_page = view.page
    previous_high_only = view.high_only
    previous_lead_type = view.lead_type
    if action == "next":
        view.page += 1
    elif action == "previous":
        view.page -= 1
    elif action == "high":
        view.high_only = not view.high_only
        view.page = 0
    elif action.startswith("type:"):
        selected_type = action.partition(":")[2]
        view.lead_type = None if selected_type == "ALL" else selected_type
        view.page = 0

    page = make_page(result, view.page, view.high_only, view.lead_type)
    view.page = page.number
    if (
        view.page == previous_page
        and view.high_only == previous_high_only
        and view.lead_type == previous_lead_type
    ):
        await callback.answer("Інших сторінок немає.")
        return
    await callback.message.edit_text(
        page.text,
        reply_markup=results_keyboard(result, view),
    )
    await callback.answer()


@router.callback_query(F.data.in_({"results:next", "results:previous", "results:high"}))
async def navigate_results(callback: CallbackQuery, pipeline: LeadPipeline) -> None:
    action = (callback.data or "").partition(":")[2]
    await update_result_message(callback, pipeline, action)


@router.callback_query(F.data.startswith("results:type:"))
async def filter_results_by_type(
    callback: CallbackQuery, pipeline: LeadPipeline
) -> None:
    action = (callback.data or "").partition("results:")[2]
    selected_type = action.partition(":")[2]
    if selected_type != "ALL" and selected_type not in LEAD_TYPES:
        await callback.answer("Невідомий тип ліда.", show_alert=True)
        return
    await update_result_message(callback, pipeline, action)


@router.callback_query(F.data == "results:csv")
async def download_csv(callback: CallbackQuery, pipeline: LeadPipeline) -> None:
    result = pipeline.get_result(callback.from_user.id)
    if result is None or not result.csv_path.exists() or not callback.message:
        await callback.answer(
            "CSV більше недоступний. Запустіть новий пошук.", show_alert=True
        )
        return
    await callback.answer()
    await callback.message.answer_document(
        FSInputFile(result.csv_path, filename="scored_leads.csv")
    )

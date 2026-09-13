"""Non-blocking orchestration of the existing collector and scorer modules."""

from __future__ import annotations

import asyncio
import logging
import shutil
import tempfile
import threading
import time
import uuid
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import lead_collector as collector
import lead_scorer as scorer
from locations import CITY_NAME_TRANSLATIONS, REGION_NAME_TRANSLATIONS

logger = logging.getLogger(__name__)


class SearchAlreadyRunningError(RuntimeError):
    """Raised when a user attempts to start a second simultaneous search."""


class SearchTimeoutError(RuntimeError):
    """Raised when a search exceeds the allowed time limit."""


# Maximum wall-clock time for one search run before it is cancelled.
SEARCH_TIMEOUT_SECONDS = 15 * 60  # 15 minutes


@dataclass(slots=True)
class SearchResult:
    user_id: int
    niche: str
    cities: list[str]
    requested_limit: int
    source_release: str
    rows: list[dict[str, str]]
    csv_path: Path
    run_dir: Path
    high: int
    medium: int
    low: int
    country_code: str = ""
    country_name: str = ""
    region: str = ""

    @property
    def total(self) -> int:
        return len(self.rows)


class LeadPipeline:
    """Run collection and scoring in a worker thread and manage run files."""

    def __init__(self, temp_root: Path | None = None, crm_db: 'CRMDatabase | None' = None) -> None:
        self.temp_root = temp_root or (
            Path(tempfile.gettempdir()) / "overture_lead_bot_runs"
        )
        self.crm_db = crm_db
        self._running_users: set[int] = set()
        self._sessions: dict[int, SearchResult] = {}
        self._cancel_events: dict[int, threading.Event] = {}
        self._state_lock = asyncio.Lock()
        self._geocode_lock = threading.Lock()
        self._last_geocode_at = 0.0

    async def is_running(self, user_id: int) -> bool:
        async with self._state_lock:
            return user_id in self._running_users

    def get_result(self, user_id: int) -> SearchResult | None:
        return self._sessions.get(user_id)

    async def run(
        self,
        user_id: int,
        niche: str,
        cities: list[str],
        limit: int,
        *,
        country_code: str | None = None,
        country_name: str = "",
        regions: list[str] | None = None,
        region: str = "",
        instagram_only: bool = False,
    ) -> SearchResult:
        async with self._state_lock:
            if user_id in self._running_users:
                raise SearchAlreadyRunningError(
                    "Для цього користувача пошук уже виконується."
                )
            self._running_users.add(user_id)

        cancel_event = threading.Event()
        self._cancel_events[user_id] = cancel_event
        try:
            try:
                result = await asyncio.wait_for(
                    asyncio.to_thread(
                        self._run_sync,
                        user_id,
                        niche,
                        cities,
                        limit,
                        country_code,
                        country_name,
                        regions,
                        region,
                        instagram_only=instagram_only,
                        cancel_event=cancel_event,
                    ),
                    timeout=SEARCH_TIMEOUT_SECONDS,
                )
            except asyncio.TimeoutError:
                cancel_event.set()
                raise SearchTimeoutError(
                    f"Пошук перевищив ліміт часу "
                    f"({SEARCH_TIMEOUT_SECONDS // 60} хв). "
                    f"Спробуйте зменшити кількість компаній або звузити "
                    f"область пошуку (конкретне місто замість всього штату)."
                )
            previous = self._sessions.get(user_id)
            self._sessions[user_id] = result
            if previous and previous.run_dir != result.run_dir:
                shutil.rmtree(previous.run_dir, ignore_errors=True)
            return result
        finally:
            self._cancel_events.pop(user_id, None)
            async with self._state_lock:
                self._running_users.discard(user_id)

    def _geocode_city(
        self,
        city: str,
        country_code: str | None = None,
        country_name: str = "",
        region: str = "",
    ) -> tuple[float, float, float, float]:
        # Translate localized city/region names to English for Nominatim
        city_en = CITY_NAME_TRANSLATIONS.get(city, city)
        region_en = REGION_NAME_TRANSLATIONS.get(region, region) if region else region
        # The public Nominatim policy permits at most one request per second.
        with self._geocode_lock:
            delay = 1.0 - (time.monotonic() - self._last_geocode_at)
            if delay > 0:
                time.sleep(delay)
            bounds = collector.geocode_city(
                city_en,
                country_code=country_code,
                country_name=country_name,
                region=region_en,
            )
            self._last_geocode_at = time.monotonic()
            return bounds

    def _geocode_region(
        self,
        region: str,
        country_code: str | None = None,
        country_name: str = "",
    ) -> tuple[float, float, float, float]:
        with self._geocode_lock:
            delay = 1.0 - (time.monotonic() - self._last_geocode_at)
            if delay > 0:
                time.sleep(delay)
            bounds = collector.geocode_region(
                region,
                country_code=country_code,
                country_name=country_name,
            )
            self._last_geocode_at = time.monotonic()
            return bounds

    def _run_sync(
        self,
        user_id: int,
        niche: str,
        cities: list[str],
        limit: int,
        country_code: str | None = None,
        country_name: str = "",
        regions: list[str] | None = None,
        region: str = "",
        instagram_only: bool = False,
        cancel_event: threading.Event | None = None,
    ) -> SearchResult:
        run_dir = self.temp_root / str(user_id) / uuid.uuid4().hex
        run_dir.mkdir(parents=True, exist_ok=False)
        raw_csv = run_dir / "leads.csv"
        scored_csv = run_dir / "scored_leads.csv"

        try:
            parsed_regions = [
                r.strip() for r in (regions or ([region] if region else [])) if r.strip()
            ]
            parsed_cities = collector.parse_cities(",".join(cities)) if cities else []
            exact_categories, category_patterns = collector.niche_filter(niche)
            collector.log_niche_resolution(niche, exact_categories, category_patterns)
            release = collector.latest_release()
            candidate_limit = max(limit * 2, 50)
            all_leads: list[dict[str, Any]] = []

            connection = collector.open_overture()
            try:
                if parsed_cities:
                    primary_region = (
                        parsed_regions[0] if len(parsed_regions) == 1 else ""
                    )
                    for city in parsed_cities:
                        if cancel_event and cancel_event.is_set():
                            logger.info("Search cancelled for user %d", user_id)
                            break
                        if (
                            country_code == collector.UKRAINE_COUNTRY_CODE
                            and collector.is_ukraine_scope(city)
                        ):
                            bounds = collector.UKRAINE_BOUNDS
                            query_country_code = country_code
                        elif country_code:
                            bounds = self._geocode_city(
                                city,
                                country_code=country_code,
                                country_name=country_name,
                                region=primary_region,
                            )
                            query_country_code = country_code
                        elif collector.is_ukraine_scope(city):
                            bounds = collector.UKRAINE_BOUNDS
                            query_country_code = collector.UKRAINE_COUNTRY_CODE
                        else:
                            bounds = self._geocode_city(city)
                            query_country_code = None

                        city_leads = collector.fetch_places(
                            connection,
                            release,
                            city,
                            bounds,
                            exact_categories,
                            category_patterns,
                            candidate_limit - len(all_leads),
                            country_code=query_country_code,
                            region=primary_region,
                            instagram_only=instagram_only,
                        )
                        logger.info(
                            "Lead search city complete: city=%r fetched=%d",
                            city,
                            len(city_leads),
                        )
                        all_leads.extend(city_leads)
                        if len(all_leads) >= candidate_limit:
                            break
                        # Reset connection to free DuckDB memory cache
                        connection.close()
                        connection = collector.open_overture()

                elif parsed_regions:
                    for reg in parsed_regions:
                        if cancel_event and cancel_event.is_set():
                            logger.info("Search cancelled for user %d", user_id)
                            break
                        if (
                            country_code == collector.UKRAINE_COUNTRY_CODE
                            and collector.is_ukraine_scope(reg)
                        ):
                            bounds = collector.UKRAINE_BOUNDS
                            query_country_code = country_code
                        elif country_code:
                            bounds = self._geocode_region(
                                reg,
                                country_code=country_code,
                                country_name=country_name,
                            )
                            query_country_code = country_code
                        elif collector.is_ukraine_scope(reg):
                            bounds = collector.UKRAINE_BOUNDS
                            query_country_code = collector.UKRAINE_COUNTRY_CODE
                        else:
                            bounds = self._geocode_region(reg)
                            query_country_code = None

                        reg_leads = collector.fetch_places(
                            connection,
                            release,
                            reg,
                            bounds,
                            exact_categories,
                            category_patterns,
                            candidate_limit - len(all_leads),
                            country_code=query_country_code,
                            region=reg,
                            instagram_only=instagram_only,
                        )
                        logger.info(
                            "Lead search region complete: region=%r fetched=%d",
                            reg,
                            len(reg_leads),
                        )
                        all_leads.extend(reg_leads)
                        if len(all_leads) >= candidate_limit:
                            break
                        # Reset connection to free DuckDB memory cache
                        connection.close()
                        connection = collector.open_overture()

                else:
                    area_name = country_name or country_code or ""
                    if country_code:
                        cb = collector.country_bounds(country_code)
                        if cb is None:
                            raise ValueError(
                                f"Немає захардкоджених меж для країни {country_code}."
                            )
                        bounds = cb
                        query_country_code = country_code
                    else:
                        bounds = collector.UKRAINE_BOUNDS
                        query_country_code = collector.UKRAINE_COUNTRY_CODE

                    country_leads = collector.fetch_places(
                        connection,
                        release,
                        area_name,
                        bounds,
                        exact_categories,
                        category_patterns,
                        candidate_limit,
                        country_code=query_country_code,
                        region="",
                        instagram_only=instagram_only,
                    )
                    logger.info(
                        "Lead search country complete: country=%r fetched=%d",
                        area_name,
                        len(country_leads),
                    )
                    all_leads.extend(country_leads)
            finally:
                connection.close()

            unique_leads = collector.deduplicate(all_leads)

            leads = collector.select_leads(unique_leads, limit)
            logger.info(
                "Lead search finalized: fetched=%d after_deduplication=%d "
                "after_limit=%d",
                len(all_leads),
                len(unique_leads),
                len(leads),
            )
            collector.write_csv(leads, raw_csv)

            scored_rows, fieldnames = scorer.read_and_score(raw_csv)
            scorer.write_scored(scored_csv, scored_rows, fieldnames)
            raw_csv.unlink(missing_ok=True)

            counts = Counter(row["priority"] for row in scored_rows)
            return SearchResult(
                user_id=user_id,
                niche=niche,
                cities=parsed_cities,
                requested_limit=limit,
                source_release=release,
                rows=scored_rows,
                csv_path=scored_csv,
                run_dir=run_dir,
                high=counts["HIGH"],
                medium=counts["MEDIUM"],
                low=counts["LOW"],
                country_code=country_code or "",
                country_name=country_name,
                region=region,
            )
        except Exception:
            shutil.rmtree(run_dir, ignore_errors=True)
            raise

    def cleanup_all(self) -> None:
        self._sessions.clear()
        shutil.rmtree(self.temp_root, ignore_errors=True)

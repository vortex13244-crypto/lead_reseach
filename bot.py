"""Telegram bot entry point."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from handlers import router
from handlers.middleware import WhitelistMiddleware
from services import LeadPipeline, build_instagram_enrichment
from services.crm_db import CRMDatabase


async def main() -> None:
    config = Config.from_env()

    from pathlib import Path
    crm_db = CRMDatabase(Path("crm_leads.db"))

    pipeline = LeadPipeline(crm_db=crm_db)
    pipeline.cleanup_all()
    instagram = config.instagram
    instagram_enrichment = build_instagram_enrichment(
        enabled=instagram.enabled,
        provider_name=instagram.provider,
        api_key=instagram.api_key,
        account_id=instagram.account_id,
        graph_api_version=instagram.graph_api_version,
        timeout_seconds=instagram.timeout_seconds,
        max_concurrency=instagram.max_concurrency,
        cache_ttl_seconds=instagram.cache_ttl_seconds,
        cache_path=instagram.cache_path,
    )

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(storage=MemoryStorage())
    router.message.outer_middleware(
        WhitelistMiddleware(config.allowed_user_ids)
    )
    router.callback_query.outer_middleware(
        WhitelistMiddleware(config.allowed_user_ids)
    )
    dispatcher.include_router(router)

    try:
        await dispatcher.start_polling(
            bot,
            pipeline=pipeline,
            instagram_enrichment=instagram_enrichment,
            crm_db=crm_db,
        )
    finally:
        from handlers.search import background_tasks
        for task in background_tasks:
            task.cancel()
        if background_tasks:
            await asyncio.gather(*background_tasks, return_exceptions=True)
        pipeline.cleanup_all()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    asyncio.run(main())

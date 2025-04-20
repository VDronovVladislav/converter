import asyncio
import logging
from fastapi import FastAPI

from .config import settings
from .logging_config import HTTPLoggerMiddleware
from .scheduler import periodic
from .fetcher import CBRCurrencyFetcher
from .storage import Storage
from .schemas import Amount
from .tasks import fetch_and_update, print_summary
from .routes import router

logger = logging.getLogger(__name__)


def create_app(period_minutes: int, initial_amount: Amount, debug: bool) -> FastAPI:
    """Функция создания приложения (фабрика)."""
    app = FastAPI(title=settings.app_title)

    if debug:
        app.add_middleware(HTTPLoggerMiddleware)

    @app.on_event("startup")
    async def on_startup():
        app.state.fetcher = CBRCurrencyFetcher()
        app.state.storage = Storage(initial_amount=initial_amount)

        logger.info(f"Начальный баланс: {initial_amount.dict()}")

        asyncio.create_task(periodic(period_minutes * 60, fetch_and_update, app))
        asyncio.create_task(periodic(60, print_summary, app))

    app.include_router(router)
    return app
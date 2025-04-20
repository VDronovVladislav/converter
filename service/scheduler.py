import asyncio
import logging


logger = logging.getLogger(__name__)


async def periodic(period_seconds: int, coro, *args):
    """Запускает coro(*args) в бесконечном цикле с паузой period_seconds."""
    while True:
        try:
            await coro(*args)
        except Exception as e:
            logger.warning(f"Ошибка в периодической задаче: {e}")
        await asyncio.sleep(period_seconds)
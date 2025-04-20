import logging
from fastapi import FastAPI

from .utils import sum_message


logger = logging.getLogger(__name__)


async def fetch_and_update(app: FastAPI):
    """Получает курсы и обновляет storage."""
    try:
        rates = await app.state.fetcher.fetch()
        if app.state.storage.check_changes() or not app.state.storage.current_rates:
            app.state.storage.update_rates(rates)
        logger.info(f"Успешно получили курсы: {rates.dict()}")
    except Exception as e:
        logger.warning(f"Не удалось получить курсы: {e}")

async def print_summary(app: FastAPI):
    """
    Выводит в консоль информационное сообщение, если что-то изменилось в суммах или курсе валюты.
    """
    storage = app.state.storage
    if storage.check_changes():
        amount = storage.current_amount
        rates = storage.current_rates
        total_rub, total_usd, total_eur = storage.calculate_totals()
        msg = sum_message(amount, rates, total_rub, total_usd, total_eur)
        logger.info(f"Данные изменились. Пересчет курсов или общей суммы: {msg}")
        storage.update_stages()
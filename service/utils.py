from fastapi import Request

from .storage import Storage


def parse_debug_flag(val: str) -> bool:
    """Функция парсинга строки с флагом debug."""
    return val.lower() in {"1", "true", "y", "True"}


def get_storage(request: Request) -> Storage:
    """Функция получения экземпляра Storage из контекста FastAPI."""
    return request.app.state.storage


def sum_message(amount, rates, total_rub, total_usd, total_eur):
    """Функция создания сообщения с валютами и суммой."""
    return (
        f"rub: {amount.rub}\n"
        f"usd: {amount.usd}\n"
        f"eur: {amount.eur}\n\n"
        f"rub-usd: {rates.usd:.2f}\n"
        f"rub-eur: {rates.eur:.2f}\n"
        f"usd-eur: {rates.eur/rates.usd:.2f}\n\n"
        f"sum: {total_rub:.2f} rub / {total_usd:.2f} usd / {total_eur:.2f} eur"
    )
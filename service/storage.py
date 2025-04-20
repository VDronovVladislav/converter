import copy
import logging

from fastapi import HTTPException

from .schemas import Amount, Rates

logger = logging.getLogger(__name__)


class Storage:
    """Класс для хранения текущего и предыдущего состояния курсов и баланса."""
    
    def __init__(self, initial_amount: Amount, initial_rates: Rates = None):
        self.current_amount = initial_amount
        self.previous_amount = None
        self.current_rates = initial_rates
        self.previous_rates = None

    def update_rates(self, new_rates: Rates):
        """Функция обновления курсов. Сохраняет прошлые и записывает новые."""
        self.previous_rates = copy.deepcopy(self.current_rates)
        self.current_rates = new_rates
        logger.info(f"Курсы валют обновлены: {self.current_rates.dict()}")
    
    def set_amount(self, new_amount: Amount):
        """Устанавливает баланс по переданным валютам."""
        self.previous_amount = copy.deepcopy(self.current_amount)
        for currency, amount in new_amount.dict().items():
            if amount is not None:
                setattr(self.current_amount, currency, amount)
        logger.info(f"Баланс установлен: {self.current_amount.dict()}")
    
    def modify_amount(self, **kwargs):
        """Добавляет (положительное) или вычитает (отрицательное) значения к текущему балансу."""
        self.previous_amount = copy.deepcopy(self.current_amount)
        for currency, amount in kwargs.items():
            if amount is not None:
                new_amount = getattr(self.current_amount, currency) + amount
                if new_amount < 0:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Баланс по {currency.upper()} не может стать отрицательным "
                            f"(текущее {self.current_amount.dict()[currency]}, новое {new_amount})"
                        )
                    )
                setattr(self.current_amount, currency, new_amount)
        logger.info(f"Баланс изменен: {self.current_amount.dict()}")

    def check_changes(self):
        """Функция проверки наличия изменений."""
        return (
            (self.previous_rates is not None and self.previous_rates != self.current_rates) or
            (self.previous_amount is not None and self.previous_amount != self.current_amount)
        )
    
    def update_stages(self):
        """Функция сброса предыдущего состояния и записи в него актуального."""
        self.previous_amount = copy.deepcopy(self.current_amount)
        self.previous_rates = copy.deepcopy(self.current_rates)
    
    def calculate_totals(self):
        """Считает общую сумму денег на балансе для каждой из трех валют."""
        amount = self.current_amount
        rates = self.current_rates
        total_rub = amount.rub + amount.usd * rates.usd + amount.eur * rates.eur
        total_usd = amount.rub / rates.usd  + amount.usd + amount.eur * rates.eur / rates.usd
        total_eur = amount.rub / rates.eur + amount.eur + amount.usd * rates.usd / rates.eur
        return total_rub, total_usd, total_eur
    

    

        
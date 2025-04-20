from typing import Optional

from pydantic import BaseModel, Field


class CurrencyBase(BaseModel):
    """Схема для выдачи валюты и суммы средств в этой валюте."""
    name: str
    value: float


class RateAmount(BaseModel):
    """Базовая схема для выдачи курса валюты и ее количества."""
    usd: float
    eur: float
    rub: float


class Rates(RateAmount):
    """Схема для курсов валют."""
    pass


class Amount(RateAmount):
    """Схема для хранения количества средств в каждой валюте."""
    pass


class AmountSetRequest(BaseModel):
    """
    Схема данных для запроса на POST /amount/set.
    Все поля опциональны — устанавливают новые значения для указанных валют.
    """
    usd: Optional[float] = Field(None, ge=0)
    eur: Optional[float] = Field(None, ge=0)
    rub: Optional[float] = Field(None, ge=0)


class ModifyRequest(BaseModel):
    """
    Схема данных для запроса на POST /modify.
    Все поля опциональны — добавляют (положительное) или вычитают (отрицательное) значения к текущим.
    """
    usd: Optional[float]
    eur: Optional[float]
    rub: Optional[float]

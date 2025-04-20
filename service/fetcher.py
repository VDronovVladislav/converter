import abc
import httpx

from .config import settings
from .schemas import Rates


class AbstractCurrencyFetcher(abc.ABC):
    """Абстрактный фетчер курсов валют."""
    @abc.abstractmethod
    async def fetch(self) -> Rates:
        pass


class CBRCurrencyFetcher(AbstractCurrencyFetcher):
    """Фетчер долларов и евро из cbr."""
    async def fetch(self) -> Rates:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.currency_url)
            response.raise_for_status()
            data = response.json()
        usd = data['Valute']['USD']['Value']
        eur = data['Valute']['EUR']['Value']
        return Rates(usd=usd, eur=eur, rub=1.0)

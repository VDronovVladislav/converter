from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from .storage import Storage
from .schemas import CurrencyBase, AmountSetRequest, ModifyRequest
from .utils import get_storage, sum_message


router = APIRouter()


@router.get("/rub/get", response_model=CurrencyBase, tags=["Currency"])
async def get_rub(storage: Storage = Depends(get_storage)):
    """Получение актуального количества рублей."""
    return CurrencyBase(name="RUB", value=storage.current_amount.rub)

@router.get("/usd/get", response_model=CurrencyBase, tags=["Currency"])
async def get_usd(storage: Storage = Depends(get_storage)):
    """Получение актуального количества долларов."""
    return CurrencyBase(name="USD", value=storage.current_amount.usd)

@router.get("/eur/get", response_model=CurrencyBase, tags=["Currency"])
async def get_eur(storage: Storage = Depends(get_storage)):
    """Получение актуального количества евро."""
    return CurrencyBase(name="EUR", value=storage.current_amount.eur)


@router.get("/amount/get", response_class=PlainTextResponse, tags=["Amount"])
async def get_amount(storage: Storage = Depends(get_storage)):
    """
    Получение актуального количества денег по каждой валюте, курсов валют 
    и общей суммы во всех валютах.
    """
    amount = storage.current_amount
    rates = storage.current_rates
    total_rub, total_usd, total_eur = storage.calculate_totals()
    return sum_message(amount, rates, total_rub, total_usd, total_eur)

@router.post("/amount/set", tags=["Amount"])
async def set_amount(body: AmountSetRequest, storage: Storage = Depends(get_storage)):
    """Установка актуального количества денег по валюте."""
    storage.set_amount(body)
    return {"status": "ok", "amount": storage.current_amount}

@router.post("/modify", tags=["Amount"])
async def modify_amount(body: ModifyRequest, storage: Storage = Depends(get_storage)):
    """Изменение актуального количества денег по валюте."""
    storage.modify_amount(**body.dict(exclude_none=True))
    return {"status": "ok", "amount": storage.current_amount}
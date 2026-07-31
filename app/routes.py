from pyexpat.errors import messages

from fastapi import Depends
from app.service import Service
from app.dependencies import get_service
from fastapi import APIRouter


router = APIRouter()


@router.get(path="/prices/", summary="Получение данных по указанной валюте")
async def get_prices_ticker(ticker: str, service: Service = Depends(get_service)):
    return await service.get_prices_ticker(ticker=ticker)

@router.get("/prices_latest/", summary="Получение последней цены валюты")
async def get_latest_prices(ticker: str, service: Service = Depends(get_service)):
    return await service.get_latest_price_ticker(ticker=ticker)

@router.get("/prices/by_date", summary="Получение цены валюты с фильтром по дате")
async def get_prices_by_period(ticker: str, from_ts: int, to_ts: int, service: Service = Depends(get_service)):
    return await service.get_price_ticker_by_period(ticker=ticker, from_ts=from_ts, to_ts=to_ts)





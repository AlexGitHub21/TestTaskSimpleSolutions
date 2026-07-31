from app.managers import Manager
from app.schemas import Price
from app.deribitclient import DeribitService

class Service:
    def __init__(self, manager: Manager, client: DeribitService) -> None:
        self.manager = manager
        self.client = client


    async def save_data(self, ticker: str):
        result = await self.client.get_ticker_data(ticker)

        data = result["result"]

        new_price = Price(
            ticker=ticker,
            price=float(data["index_price"]),
            timestamp=int(data["timestamp"]) // 1000)

        await self.manager.create_price(new_price)

    async def get_prices_ticker(self, ticker: str) -> list[Price] | None:
        return await self.manager.get_price_ticker(ticker=ticker)

    async def get_latest_price_ticker(self, ticker: str) -> Price | None:
        return await self.manager.get_latest_price_ticker(ticker=ticker)

    async def get_price_ticker_by_period(self, ticker: str, from_ts: int, to_ts: int) -> list[Price] | None:
        return await self.manager.get_price_ticker_by_period(ticker=ticker, from_ts=from_ts, to_ts=to_ts)

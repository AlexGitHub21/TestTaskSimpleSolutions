from core.db_dependency import DBDependency
from fastapi import HTTPException
from database.models import IndexPrices
from app.schemas import Price
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


class Manager:
    def __init__(self, db: DBDependency) -> None:
        self.db = db
        self.model = IndexPrices

    async def create_price(self, price: Price) -> bool:
        async with self.db.session_factory() as session:
            new_data_price = self.model(**price.model_dump())

            session.add(new_data_price)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Error")

            await session.refresh(new_data_price)
            return True

    async def get_price_ticker(self, ticker: str) -> list[Price] | None:
        async with self.db.session_factory() as session:
            query = select(
                self.model.ticker,
                self.model.price,
                self.model.timestamp
            ).where(self.model.ticker == ticker)

            result = await session.execute(query)
            prices_data = result.mappings().all()

            if prices_data:
                return [Price.model_validate(price) for price in prices_data]
            else:
                return None

    async def get_latest_price_ticker(self, ticker: str) -> Price | None:
        async with self.db.session_factory() as session:
            query = select(
                self.model.ticker,
                self.model.price,
                self.model.timestamp
            ).where(self.model.ticker == ticker).order_by(self.model.timestamp.desc()).limit(1)

            result = await session.execute(query)
            price_data = result.mappings().first()

            if price_data:
                return Price(**price_data)
            else:
                return None

    async def get_price_ticker_by_period(self, ticker: str, from_ts: int, to_ts: int) -> list[Price] | None:
        async with self.db.session_factory() as session:
            query = select(
                self.model.ticker,
                self.model.price,
                self.model.timestamp
            ).where(self.model.ticker == ticker,
                    self.model.timestamp >= from_ts,
                    self.model.timestamp <= to_ts)

            result = await session.execute(query)
            prices_data = result.mappings().all()

            if prices_data:
                return [Price.model_validate(price) for price in prices_data]
            else:
                return None
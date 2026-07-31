from app.celery_app import celery_app
from core.db_dependency import DBDependency
from app.managers import Manager
from app.service import Service
import asyncio
from app.deribitclient import DeribitService


@celery_app.task
def fetch_prices():
    async def runner():
        db = DBDependency()
        manager = Manager(db=db)
        client = DeribitService()
        service = Service(manager=manager, client=client)

        await service.save_data("BTC")
        await service.save_data("ETH")

    asyncio.run(runner())
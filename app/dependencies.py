from fastapi import Depends
from core.db_dependency import DBDependency
from app.managers import Manager
from app.service import Service
from app.deribitclient import DeribitService


db_dependency = DBDependency()
deribit_client = DeribitService()

def get_db() -> DBDependency:
    return db_dependency

def get_deribit_client() -> DeribitService:
    return deribit_client

def get_manager(db: DBDependency = Depends(get_db)) -> Manager:
    return Manager(db=db)

def get_service(manager: Manager = Depends(get_manager), client: DeribitService = Depends(get_deribit_client)) -> Service:
    return Service(manager=manager, client=client)
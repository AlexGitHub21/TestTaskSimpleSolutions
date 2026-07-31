from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.settings import *


class DBDependency:
    def __init__(self) -> None:
        self._engine = create_async_engine(
            url=db_settings.get_db_url, echo=db_settings.DB_ECHO
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False, autocommit=False
        )

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

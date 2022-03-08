from typing import Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.api.dependencies.settings import settings_provider
from src.core.settings import Settings


def sessionmaker_provider() -> Any:
    ...


def get_sessionmaker(settings: Settings = Depends(settings_provider)) -> sessionmaker:
    engine = create_async_engine(str(settings.database_dsn), future=True, echo=True)

    return sessionmaker(
        engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        class_=AsyncSession,
    )

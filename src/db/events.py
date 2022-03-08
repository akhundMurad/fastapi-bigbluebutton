from asyncpg import create_pool
from fastapi import FastAPI
from loguru import logger

from src.core.settings import Settings


async def connect_to_db(settings: Settings, app: FastAPI) -> None:
    logger.info("Connection to Postgres...")

    app.state.pool = await create_pool(dsn=settings.database_dsn)

    logger.info("Connection established.")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to Postgres...")

    await app.state.pool.close()

    logger.info("Connection closed.")


async def init_redis_pool(settings: Settings, app: FastAPI) -> None:
    logger.info("Creating redis pool...")
    redis = await create_pool(dsn=settings.redis_dsn)
    logger.info("Redis pool created.")
    app.state.redis = redis


async def close_redis_pool(app: FastAPI) -> None:
    logger.info("Closing redis pool...")
    await app.state.redis.close()
    logger.info("Redis pool closed.")

from aioredis import Redis, create_redis_pool

from core.settings import REDIS_URL, REDIS_PASSWORD, REDIS_DB


async def init_redis_pool() -> Redis:
    redis = await create_redis_pool(
        REDIS_URL,
        password=REDIS_PASSWORD or None,
        encoding="utf-8",
        db=REDIS_DB
    )
    return redis

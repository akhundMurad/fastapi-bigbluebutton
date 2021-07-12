from aioredis import Redis, create_redis_pool

from core.settings import REDIS_URL, REDIS_PASSWORD


async def init_redis_pool() -> Redis:
    redis = await create_redis_pool(
        REDIS_URL,
        password=REDIS_PASSWORD,
        encoding="utf-8",
    )
    return redis

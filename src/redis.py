from arq import create_pool, ArqRedis
from arq.connections import RedisSettings

from core import settings


RedisSettings(
    host=settings.REDIS_HOST,
    port=int(settings.REDIS_PORT),
    database=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD
)


async def init_redis_pool() -> ArqRedis:
    redis = await create_pool(RedisSettings())
    return redis

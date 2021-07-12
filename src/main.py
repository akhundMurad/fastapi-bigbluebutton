import uvicorn
from fastapi import FastAPI
from loguru import logger

from core.db import database
from redis import init_redis_pool
from views import auth, bigbluebutton

app = FastAPI()
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    app.state.redis = await init_redis_pool()

    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        logger.success('Connected to DB!')


@app.on_event("shutdown")
async def shutdown() -> None:
    app.state.redis.close()
    await app.state.redis.wait_closed()

    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
        logger.info('Disconnected from DB.')


app.include_router(auth.router)
app.include_router(bigbluebutton.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

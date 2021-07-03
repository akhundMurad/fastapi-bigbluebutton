import uvicorn

from loguru import logger
from fastapi import FastAPI
from core.db import database

app = FastAPI()
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        logger.success('Connected to DB!')


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
        logger.info('Disconnected from DB.')


@app.get("/")
def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

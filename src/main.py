import uvicorn
from fastapi import FastAPI

from src.db import events

from src.api.routers import schedule, auth, bigbluebutton

from src.api.dependencies.settings import get_settings, settings_provider
from src.api.dependencies.session import sessionmaker_provider, get_sessionmaker
from src.api.dependencies.jwtbearer import jwtbearer_provider, get_jwtbearer
from src.api.dependencies.user import current_user_provider, get_current_user


def get_app() -> FastAPI:
    application = FastAPI()

    application.dependency_overrides[settings_provider] = get_settings
    application.dependency_overrides[sessionmaker_provider] = get_sessionmaker
    application.dependency_overrides[jwtbearer_provider] = get_jwtbearer
    application.dependency_overrides[current_user_provider] = get_current_user

    application.add_event_handler("startup", events.connect_to_db)
    application.add_event_handler("shutdown", events.close_db_connection)
    application.add_event_handler("startup", events.init_redis_pool)
    application.add_event_handler("shutdown", events.close_redis_pool)

    application.include_router(auth.router)
    application.include_router(bigbluebutton.router)
    application.include_router(schedule.router)

    return application


app = get_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

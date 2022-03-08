from fastapi.security import HTTPBearer

from src.api.httpbearers.jwt import JWTBearer


def jwtbearer_provider() -> HTTPBearer:
    ...


def get_jwtbearer() -> JWTBearer:
    return JWTBearer()

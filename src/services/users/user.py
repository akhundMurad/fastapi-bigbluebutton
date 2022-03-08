import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker

from src.db.models import User
from src.api.dependencies.session import sessionmaker_provider
from src.api.dependencies.settings import settings_provider
from src.core import exceptions
from src.core.settings import Settings
from src.schemas.auth import UserCreate, UserRegister
from src.services.base.crud import CRUD
from src.utils.hashing import get_password_hash, verify_password
from src.services.base.result import ServiceResult, handle_result
from src.services.base.service import Service


class UserService(Service):
    def __init__(self, session_maker: sessionmaker = Depends(sessionmaker_provider)):
        self.crud = UserCRUD(session_maker())

    async def create(self, item: UserRegister) -> ServiceResult:
        user_data = item.dict()
        user_data["password"] = get_password_hash(user_data["raw_password1"])
        del user_data["raw_password1"]
        del user_data["raw_password2"]

        user = await self.crud.create(UserCreate(**user_data))
        if not user:
            return ServiceResult(exceptions.InvalidRequest())
        return ServiceResult(user)

    async def read(self, username: str) -> ServiceResult:
        user = await self.crud.read(username)
        if not user:
            return ServiceResult(exceptions.NotFound({"username": username}))
        return ServiceResult(user)


class UserCRUD(CRUD):
    async def create(self, item: UserCreate) -> User:
        user = User(
            username=item.username,
            first_name=item.first_name,
            last_name=item.last_name,
            role=item.role,
            password=item.password,
        )

        await self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def read(self, username: str) -> Optional[User]:
        user = await self.session.query(User).filter(User.username == username).first()
        return user


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    settings: Settings = Depends(settings_provider),
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str, settings: Settings = Depends(settings_provider)) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except JWTError:
        return {}


async def authenticate_user(username: str, password: str):
    result = await UserService().read(username)
    user = handle_result(result)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user


def verify_jwt(token: str) -> bool:
    payload = decode_token(token)
    return True if payload else False

from typing import Any, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker
from starlette import status

from src.api.dependencies.session import sessionmaker_provider
from src.api.dependencies.settings import get_settings
from src.core.settings import Settings
from src.schemas.auth import TokenData
from src.db.models import User
from src.services.users.user import UserCRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def current_user_provider() -> Any:
    ...


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
    session_maker: sessionmaker = Depends(sessionmaker_provider),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user: Optional[User] = await UserCRUD(session_maker()).read(token_data.username)
    if user is None:
        raise credentials_exception
    return user

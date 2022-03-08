from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.dependencies.settings import get_settings
from src.core.settings import Settings
from src.db.models import User
from src.services.base.result import handle_result
from src.services.users.user import create_access_token, UserService, authenticate_user
from src.schemas.auth import Token, UserRead, UserRegister
from src.api.dependencies.user import current_user_provider

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register/", response_model=UserRead, status_code=201)
async def register_user(user: UserRegister):
    result = await UserService().create(user)
    return UserRead(handle_result(result))


@router.get("/me/", response_model=UserRead)
async def get_user(current_user: User = Depends(current_user_provider)):
    return UserRead(current_user)


@router.post("/token/", response_model=Token, status_code=201)
async def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    settings: Settings = Depends(get_settings),
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

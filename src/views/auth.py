from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from core.schemas.auth import Token, UserCreateSchema, UserRetrieveSchema
from core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import get_current_user
from service import create_user
from utils.auth import authenticate_user
from utils.hashing import create_access_token, get_password_hash

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post(
    '/register/',
    response_model=UserRetrieveSchema,
    status_code=201
)
async def register_user(user: UserCreateSchema):
    user_data = user.dict()
    user_data['password'] = get_password_hash(user_data['raw_password1'])
    del user_data['raw_password1']
    del user_data['raw_password2']
    user = await create_user(**user_data)
    return UserRetrieveSchema(**user.dict())


@router.get("/me/", response_model=UserRetrieveSchema)
async def get_user(
        current_user: UserRetrieveSchema = Depends(get_current_user)
):
    return current_user


@router.post("/token/", response_model=Token, status_code=201)
async def create_token(
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

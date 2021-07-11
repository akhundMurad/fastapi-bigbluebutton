import time
from datetime import timedelta, datetime
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from core.settings import SECRET_KEY, ALGORITHM


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(*, plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY,
                                   algorithms=[ALGORITHM])
        return decoded_token if decoded_token[
                                    "exp"] >= time.time() else None
    except JWTError:
        return {}

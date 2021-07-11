from selector import get_user
from utils.hashing import verify_password, decode_token


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(
            plain_password=password,
            hashed_password=user.password
    ):
        return False
    return user


def verify_jwt(token: str) -> bool:
    payload = decode_token(token)
    return True if payload else False

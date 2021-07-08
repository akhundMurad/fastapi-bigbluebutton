from selector import get_user
from utils.hashing import verify_password


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

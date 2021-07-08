from core.models.users import User


async def get_user(username: str) -> User:
    return await User.objects.get(username=username)

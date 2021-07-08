from core.models.users import User


async def create_user(**data) -> User:
    user = await User.objects.create(**data)
    return user

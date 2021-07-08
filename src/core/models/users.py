import ormar
import enum

from core.db import metadata, database


class UserRoleChoices(enum.Enum):
    MODERATOR = 'moderator'
    ATTENDEE = 'attendee'

    @classmethod
    def values(cls) -> list:
        return [role.value for role in list(cls)]


class User(ormar.Model):
    class Meta:
        tablename = 'user'
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    username: str = ormar.String(unique=True, max_length=128)
    first_name: str = ormar.String(max_length=128)
    last_name: str = ormar.String(max_length=128)
    password: str = ormar.String(max_length=1024)
    role: str = ormar.String(max_length=9)

import enum


class UserRoleChoices(enum.Enum):
    MODERATOR = "moderator"
    ATTENDEE = "attendee"

    @classmethod
    def values(cls) -> list:
        return [role.value for role in list(cls)]

from typing import List

from core.models.schedule import Schedule
from core.models.users import User


async def create_user(**data) -> User:
    user = await User.objects.create(**data)
    return user


async def create_schedule(attendees: List[User]) -> Schedule:
    schedule = await Schedule.objects.create()
    for attendee in attendees:
        await schedule.attendee_list.add(attendee)
    await schedule.save()
    return schedule

from typing import List, NoReturn

from core.models.schedule import Schedule, ScheduleCell
from core.models.users import User


async def create_user(**data) -> User:
    user = await User.objects.create(**data)
    return user


async def create_schedule(attendees: List[User]) -> Schedule:
    schedule = await Schedule.objects.create()
    for attendee in attendees:
        await schedule.attendee_list.add(attendee)
    return schedule


async def create_meetings_by_cell(schedule_cell: ScheduleCell) -> NoReturn:
    async for meeting in schedule_cell.meetings.all():
        await meeting.api.create()

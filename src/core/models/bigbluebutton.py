from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import ormar

from core.db import database, metadata
from core.models.users import User


class Schedule(ormar.Model):
    class Meta:
        tablename = 'schedule'
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    attendee_list: Optional[List[User]] = ormar.ManyToMany(User)


class ScheduleCell(ormar.Model):
    class Meta:
        tablename = 'schedule_cell'
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    datetime_start: datetime = ormar.DateTime()
    datetime_end: datetime = ormar.DateTime()

    schedule: Schedule = ormar.ForeignKey(Schedule, related_name='cells')


class Meeting(ormar.Model):
    class Meta:
        tablename = 'meeting'
        metadata = metadata
        database = database

    id: str = ormar.UUID(primary_key=True, default=uuid4, unique=True,
                         uuid_format="string")
    name: str = ormar.String(max_length=512)

    welcome_message: Optional[str] = ormar.String(
        max_length=128, nullable=True
    )
    moderator_message: Optional[str] = ormar.String(
        max_length=128, nullable=True
    )
    record: bool = ormar.Boolean(default=False)
    auto_start_recording: bool = ormar.Boolean(default=False)
    allow_start_stop_recording: bool = ormar.Boolean(default=True)
    webcams_only_for_moderator: bool = ormar.Boolean(default=False)
    mute_on_start: bool = ormar.Boolean(default=False)
    allow_mods_to_unmute_users: bool = ormar.Boolean(default=False)
    max_participants: Optional[int] = ormar.Integer(maximum=50, nullable=True)
    duration: Optional[int] = ormar.Integer(nullable=True)

    schedule_cell: ScheduleCell = ormar.ForeignKey(ScheduleCell,
                                                   related_name='meetings')

    datetime_start: datetime = ormar.DateTime()
    datetime_end: datetime = ormar.DateTime()

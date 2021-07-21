from datetime import datetime
from typing import List, Optional

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

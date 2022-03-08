from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class ScheduleAttendeeCreate(BaseModel):
    attendee_id: UUID
    schedule_id: UUID


class ScheduleAttendeeRead(BaseModel):
    attendee_id: UUID


class ScheduleCreate(BaseModel):
    attendee_list: List[ScheduleAttendeeCreate]


class ScheduleRead(BaseModel):
    id: UUID
    attendee_list: List[ScheduleAttendeeRead]


class ScheduleReadMany(BaseModel):
    __root__: List[ScheduleRead]

    class Config:
        orm_mode = True


class ScheduleCellCreate(BaseModel):
    datetime_start: datetime
    datetime_end: datetime

    schedule_id: UUID


class ScheduleCellRead(BaseModel):
    id: UUID
    datetime_start: datetime
    datetime_end: datetime
    schedule_id: UUID


class ScheduleCellReadMany(BaseModel):
    __root__: List[ScheduleReadMany]

import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class BigbluebuttonServer(BaseModel):
    name: str
    url: str
    secret_key: str


class MeetingRead(BaseModel):
    id: uuid.UUID
    name: str
    welcome_message: Optional[str]
    moderator_message: str
    record: bool
    auto_start_recording: bool
    allow_start_stop_recording: bool
    webcams_only_for_moderator: bool
    mute_on_start: bool
    allow_mods_to_unmute_users: bool
    max_participants: Optional[int]
    duration: Optional[int]
    datetime_start: datetime
    datetime_end: datetime


class MeetingReadMany(BaseModel):
    __root__: List[MeetingRead]

    class Config:
        orm_mode = True


class MeetingCreate(BaseModel):
    name: str
    welcome_message: Optional[str]
    moderator_message: str
    record: bool
    auto_start_recording: bool
    allow_start_stop_recording: bool
    webcams_only_for_moderator: bool
    mute_on_start: bool
    allow_mods_to_unmute_users: bool
    max_participants: Optional[int]
    duration: Optional[int]
    datetime_start: datetime
    datetime_end: datetime
    schedule_cell_id: uuid.UUID

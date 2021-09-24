from datetime import datetime
from typing import Optional
from uuid import uuid4

import ormar

from bigbluebutton.api import MeetingAPI
from core.db import database, metadata
from core.models.schedule import ScheduleCell


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

    _api: Optional[MeetingAPI] = None

    @property
    def api(self) -> MeetingAPI:
        if self._api is None:
            self._api = MeetingAPI(meeting=self)
        return self._api

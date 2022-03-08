import sqlalchemy as sa

from datetime import datetime
from typing import Optional, List
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, registry


mapper_registry = registry()


@mapper_registry.mapped
class User:
    __tablename__ = "user"

    id: uuid.UUID = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: str = sa.Column(sa.String(length=128), unique=True)
    first_name: str = sa.Column(sa.String(length=128))
    last_name: str = sa.Column(sa.String(length=128))
    password: str = sa.Column(sa.String(length=1024))
    role: str = sa.Column(sa.String(length=9))

    schedules: List["ScheduleAttendee"] = relationship(
        "ScheduleAttendee", back_populates="attendee"
    )


@mapper_registry.mapped
class ScheduleAttendee:
    __tablename__ = "schedule_attendee"

    attendee_id: uuid.UUID = sa.Column(ForeignKey("user.id"), primary_key=True)
    schedule_id: uuid.UUID = sa.Column(ForeignKey("schedule.id"), primary_key=True)
    attendee: User = relationship(User, back_populates="schedules")
    schedule: "Schedule" = relationship("Schedule", back_populates="attendee_list")


@mapper_registry.mapped
class Schedule:
    __tablename__ = "schedule"

    id: uuid.UUID = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attendee_list: Optional[List[ScheduleAttendee]] = relationship(
        ScheduleAttendee, back_populates="schedule"
    )

    cells = relationship("ScheduleCell", back_populates="schedule")


@mapper_registry.mapped
class ScheduleCell:
    __tablename__ = "schedule_cell"

    id: uuid.UUID = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    datetime_start: datetime = sa.Column(sa.DateTime)
    datetime_end: datetime = sa.Column(sa.DateTime)

    schedule_id: uuid.UUID = sa.Column(UUID, ForeignKey("schedule.id"))
    schedule: Schedule = relationship(Schedule, back_populates="cells")
    meetings: List["Meeting"] = relationship("Meeting", back_populates="schedule_cell")


@mapper_registry.mapped
class Meeting:
    __tablename__ = "meetings"

    id: uuid.UUID = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = sa.Column(sa.String(length=256))

    welcome_message: Optional[str] = sa.Column(sa.String(length=128), nullable=True)
    moderator_message: Optional[str] = sa.Column(sa.String(length=128), nullable=False)
    record: bool = sa.Column(sa.Boolean, default=False)
    auto_start_recording: bool = sa.Column(sa.Boolean, default=False)
    allow_start_stop_recording: bool = sa.Column(sa.Boolean, default=True)
    webcams_only_for_moderator: bool = sa.Column(sa.Boolean, default=False)
    mute_on_start: bool = sa.Column(sa.Boolean, default=False)
    allow_mods_to_unmute_users: bool = sa.Column(sa.Boolean, default=False)
    max_participants: Optional[int] = sa.Column(sa.Integer, nullable=True)
    duration: Optional[int] = sa.Column(sa.Integer, nullable=True)

    datetime_start: datetime = sa.Column(sa.DateTime)
    datetime_end: datetime = sa.Column(sa.DateTime, nullable=True)

    schedule_cell_id: uuid.UUID = sa.Column(UUID, ForeignKey("schedule_cell.id"))
    schedule_cell: ScheduleCell = relationship(
        "ScheduleCell", back_populates="meetings"
    )

    _api = None

    @property
    def api(self):
        from src.bigbluebutton.api import MeetingAPI

        if self._api is None:
            self._api = MeetingAPI(meeting=self)
        return self._api

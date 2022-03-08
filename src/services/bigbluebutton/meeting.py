from typing import Optional, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from src.api.dependencies.session import sessionmaker_provider
from src.core import exceptions
from src.db.models import Meeting
from src.schemas.bigbluebutton import MeetingCreate
from src.services.base.crud import CRUD
from src.services.base.result import ServiceResult
from src.services.base.service import Service


class MeetingService(Service):
    def __init__(self, session_maker: sessionmaker = Depends(sessionmaker_provider)):
        self.crud = MeetingCRUD(session_maker())

    async def create(self, item: MeetingCreate) -> ServiceResult:
        meeting = await self.crud.create(item)
        if not meeting:
            return ServiceResult(exceptions.InvalidRequest())
        return ServiceResult(meeting)

    async def read(self, item_id: UUID) -> ServiceResult:
        meeting = await self.crud.read(item_id)
        if not meeting:
            return ServiceResult(exceptions.NotFound({"item_id": item_id}))
        return ServiceResult(meeting)

    async def read_all(self) -> ServiceResult:
        meetings = await self.crud.read_all()
        return ServiceResult(meetings)

    async def delete(self, item_id: UUID) -> ServiceResult:
        await self.crud.delete(item_id)
        return ServiceResult()


class MeetingCRUD(CRUD):
    async def create(self, item: MeetingCreate) -> Meeting:
        meeting = Meeting(
            name=item.name,
            welcome_message=item.welcome_message,
            moderator_message=item.moderator_message,
            record=item.record,
            auto_start_recording=item.auto_start_recording,
            allow_start_stop_recording=item.allow_start_stop_recording,
            webcams_only_for_moderator=item.webcams_only_for_moderator,
            mute_on_start=item.mute_on_start,
            allow_mods_to_unmute_users=item.allow_mods_to_unmute_users,
            max_participants=item.max_participants,
            duration=item.duration,
            datetime_start=item.datetime_start,
            datetime_end=item.datetime_end,
            schedule_cell_id=item.schedule_cell_id,
        )

        await self.session.add(meeting)
        await self.session.commit()
        await self.session.refresh(meeting)

        return meeting

    async def read(self, item_id: UUID) -> Optional[Meeting]:
        meeting = (
            await self.session.query(Meeting).filter(Meeting.id == item_id).first()
        )
        return meeting

    async def read_all(self) -> List[Meeting]:
        return await self.session.query(Meeting).all()

    async def delete(self, item_id: UUID) -> None:
        meeting = await self.read(item_id)
        self.session.delete(meeting)
        self.session.commit()

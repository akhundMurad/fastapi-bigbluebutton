from typing import Optional, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from src.api.dependencies.session import sessionmaker_provider
from src.core import exceptions
from src.db.models import Schedule, ScheduleAttendee
from src.schemas.schedule import ScheduleCreate
from src.services.base.crud import CRUD
from src.services.base.result import ServiceResult
from src.services.base.service import Service


class ScheduleService(Service):
    def __init__(self, session_maker: sessionmaker = Depends(sessionmaker_provider)):
        self.crud = ScheduleCRUD(session_maker())

    async def create(self, item: ScheduleCreate) -> ServiceResult:
        schedule = await self.crud.create(item)
        if not schedule:
            return ServiceResult(exceptions.InvalidRequest())
        return ServiceResult(schedule)

    async def read(self, item_id: UUID) -> ServiceResult:
        schedule = await self.crud.read(item_id)
        if not schedule:
            return ServiceResult(exceptions.NotFound({"item_id": item_id}))
        return ServiceResult(schedule)

    async def read_by_attendee(self, attendee_id: UUID) -> ServiceResult:
        schedules = await self.crud.read_by_attendee(attendee_id)
        return ServiceResult(schedules or [])

    async def delete(self, item_id: UUID) -> ServiceResult:
        await self.crud.delete(item_id)
        return ServiceResult()


class ScheduleCRUD(CRUD):
    async def create(self, item: ScheduleCreate) -> Schedule:
        schedule = Schedule()
        schedule.attendee_list.extend(
            [
                ScheduleAttendee(
                    attendee_id=schedule_attendee.attendee_id,
                    schedule_id=schedule_attendee.schedule_id,
                )
                for schedule_attendee in item.attendee_list
            ]
        )

        await self.session.add(schedule)
        await self.session.commit()
        await self.session.refresh(schedule)

        return schedule

    async def read(self, item_id: UUID) -> Optional[Schedule]:
        schedule = (
            await self.session.query(Schedule).filter(Schedule.id == item_id).first()
        )
        return schedule

    async def read_by_attendee(self, attendee_id: UUID) -> List[Schedule]:
        schedules = (
            await self.session.query(Schedule)
            .join(ScheduleAttendee)
            .filter(ScheduleAttendee.attendee_id == attendee_id)
            .all()
        )
        return schedules

    async def delete(self, item_id: UUID) -> None:
        schedule = await self.read(item_id)
        self.session.delete(schedule)
        self.session.commit()

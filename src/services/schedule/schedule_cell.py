from typing import Optional, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from src.api.dependencies.session import sessionmaker_provider
from src.core import exceptions
from src.db.models import Schedule, ScheduleAttendee, ScheduleCell
from src.schemas.schedule import ScheduleCellCreate
from src.services.base.crud import CRUD
from src.services.base.result import ServiceResult
from src.services.base.service import Service


class ScheduleCellService(Service):
    def __init__(self, session_maker: sessionmaker = Depends(sessionmaker_provider)):
        self.crud = ScheduleCellCRUD(session_maker())

    async def create(self, item: ScheduleCellCreate) -> ServiceResult:
        schedule_cell = await self.crud.create(item)
        if not schedule_cell:
            return ServiceResult(exceptions.InvalidRequest())
        return ServiceResult(schedule_cell)

    async def read(self, item_id: UUID) -> ServiceResult:
        schedule_cell = await self.crud.read(item_id)
        if not schedule_cell:
            return ServiceResult(exceptions.NotFound({"item_id": item_id}))
        return ServiceResult(schedule_cell)

    async def read_by_attendee(self, attendee_id: UUID) -> ServiceResult:
        schedule_cells = await self.crud.read_by_attendee(attendee_id)
        return ServiceResult(schedule_cells or [])

    async def read_by_schedule(self, schedule_id: UUID) -> ServiceResult:
        schedule_cells = await self.crud.read_by_schedule(schedule_id)
        return ServiceResult(schedule_cells or [])

    async def delete(self, item_id: UUID) -> ServiceResult:
        await self.crud.delete(item_id)
        return ServiceResult()


class ScheduleCellCRUD(CRUD):
    async def create(self, item: ScheduleCellCreate) -> ScheduleCell:
        scheduleCell = ScheduleCell(
            datetime_start=item.datetime_start,
            datetime_end=item.datetime_end,
            schedule_id=item.schedule_id,
        )

        await self.session.add(scheduleCell)
        await self.session.commit()
        await self.session.refresh(scheduleCell)

        return scheduleCell

    async def read(self, item_id: UUID) -> Optional[ScheduleCell]:
        schedule_cell = (
            await self.session.query(ScheduleCell)
            .filter(ScheduleCell.id == item_id)
            .first()
        )
        return schedule_cell

    async def read_by_attendee(self, attendee_id: UUID) -> List[ScheduleCell]:
        schedules_ids = (
            await self.session.query(Schedule)
            .join(ScheduleAttendee)
            .filter(ScheduleAttendee.attendee_id == attendee_id)
            .values("id")
        )
        schedules_ids = [schedule[0] for schedule in schedules_ids]

        schedule_cells = (
            await self.session.query(ScheduleCell)
            .join(Schedule)
            .filter(Schedule.id.in_(schedules_ids))
            .all()
        )
        return schedule_cells

    async def read_by_schedule(self, schedule_id: UUID) -> List[ScheduleCell]:
        schedule_cells = (
            await self.session.query(ScheduleCell)
            .join(Schedule)
            .filter(Schedule.id == schedule_id)
            .all
        )
        return schedule_cells

    async def delete(self, item_id: UUID) -> None:
        schedule_cell = await self.read(item_id)
        self.session.delete(schedule_cell)
        self.session.commit()

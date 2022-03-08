from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from starlette import status

from src.api.dependencies.jwtbearer import jwtbearer_provider
from src.db.models import User
from src.api.dependencies.user import current_user_provider
from src.services.base.result import handle_result
from src.services.schedule.schedule import ScheduleService
from src.services.schedule.schedule_cell import ScheduleCellService

from src.schemas.schedule import (
    ScheduleReadMany,
    ScheduleRead,
    ScheduleCellReadMany,
    ScheduleCreate,
    ScheduleCellRead,
    ScheduleCellCreate,
)

router = APIRouter(
    prefix="/schedule", tags=["schedule"], dependencies=[Depends(jwtbearer_provider)]
)


@router.get("/", response_model=ScheduleReadMany)
async def get_schedules(current_user: User = Depends(current_user_provider)):
    result = await ScheduleService().read_by_attendee(current_user.id)
    return ScheduleReadMany(handle_result(result))


@router.get("/{pk}", response_model=ScheduleRead)
async def get_schedule(pk: str):
    result = await ScheduleService().read(UUID(pk))
    return ScheduleRead(handle_result(result))


@router.get("/{pk}/cells", response_model=ScheduleCellReadMany)
async def get_cells_of_schedule(pk: str):
    result = await ScheduleCellService().read_by_schedule(UUID(pk))
    return ScheduleCellReadMany(handle_result(result))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ScheduleRead)
async def create_schedule(schedule: ScheduleCreate):
    result = await ScheduleService().create(schedule)
    return ScheduleCellReadMany(handle_result(result))


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(pk: str):
    await ScheduleService().delete(UUID(pk))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/cell/", response_model=ScheduleCellReadMany)
async def get_schedule_cells(current_user: User = Depends(current_user_provider)):
    result = await ScheduleCellService().read_by_attendee(current_user.id)
    return ScheduleCellReadMany(handle_result(result))


@router.get("/cell/{pk}", response_model=ScheduleCellRead)
async def get_schedule_cell(pk: str):
    result = await ScheduleCellService().read(UUID(pk))
    return ScheduleCellRead(handle_result(result))


@router.post(
    "/cell/", status_code=status.HTTP_201_CREATED, response_model=ScheduleCellCreate
)
async def create_schedule_cell(cell: ScheduleCellCreate):
    result = await ScheduleCellService().create(cell)
    return ScheduleCellRead(handle_result(result))


@router.delete("/cell/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule_cell(pk: str):
    await ScheduleCellService().delete(UUID(pk))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

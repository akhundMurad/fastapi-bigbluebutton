from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from starlette import status

import service

from core.models.schedule import Schedule, ScheduleCell
from core.models.users import User
from dependencies import JWTBearer


router = APIRouter(
    prefix='/schedule',
    tags=['schedule'],
    dependencies=[Depends(JWTBearer())]
)


@router.get(
    '/',
    response_model=List[Schedule]
)
async def get_schedules():
    schedules = await Schedule.objects.all()
    return schedules


@router.get(
    '/{pk}',
    response_model=Schedule
)
async def get_schedule(pk: int):
    schedule = await Schedule.objects.get(id=pk)
    return schedule


@router.get(
    '/{pk}/cells',
    response_model=List[ScheduleCell]
)
async def get_cells_of_schedule(pk: int):
    cell = await ScheduleCell.objects.get(schedule__id=pk)
    return cell


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=Schedule
)
async def create_schedule(attendees: List[User]):
    schedule = await service.create_schedule(attendees)
    return schedule


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(pk: int):
    schedule = await Schedule.objects.get(id=pk)
    await schedule.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/cell/',
    response_model=List[ScheduleCell]
)
async def get_schedule_cells():
    cells = await ScheduleCell.objects.all()
    return cells


@router.get(
    '/cell/{pk}',
    response_model=ScheduleCell
)
async def get_schedule_cell(pk: int):
    cell = await ScheduleCell.objects.get(id=pk)
    return cell


@router.post(
    '/cell/',
    status_code=status.HTTP_201_CREATED,
    response_model=ScheduleCell
)
async def create_schedule_cell(cell: ScheduleCell):
    await cell.save()
    return cell


@router.delete('/cell/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule_cell(pk: int):
    cell = await ScheduleCell.objects.get(id=pk)
    await cell.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


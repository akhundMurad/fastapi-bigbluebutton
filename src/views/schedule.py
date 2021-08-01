from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from starlette import status

import service

from core.models.schedule import Schedule, ScheduleCell
from core.models.users import User
from dependencies import JWTBearer, get_current_user

router = APIRouter(
    prefix='/schedule',
    tags=['schedule'],
    dependencies=[Depends(JWTBearer())]
)


@router.get(
    '/',
    response_model=List[Schedule]
)
async def get_schedules(current_user: User = Depends(get_current_user)):
    queryset = await Schedule.objects.prefetch_related(
        'attendee_list'
    ).filter(
        attendee_list__id__in=[current_user.id]
    ).all()

    return queryset


@router.get(
    '/{pk}',
    response_model=Schedule
)
async def get_schedule(
        pk: int,
        current_user: User = Depends(get_current_user)
):
    schedule = await Schedule.objects.prefetch_related(
        'attendee_list'
    ).get(id=pk)

    if current_user.id in schedule.attendee_list.values(['id']):
        return schedule
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    '/{pk}/cells',
    response_model=List[ScheduleCell]
)
async def get_cells_of_schedule(
        pk: int, 
        current_user: User = Depends(get_current_user)
):
    cell = await ScheduleCell.objects.prefetch_related(
        'schedule__attendee_list'
    ).get(schedule__id=pk)
    
    if current_user.id in cell.schedule.attendee_list.values(['id']):
        return cell
    return Response(status_code=status.HTTP_404_NOT_FOUND)


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
async def get_schedule_cells(current_user: User = Depends(get_current_user)):
    queryset = await ScheduleCell.objects.prefetch_related(
        'schedule__attendee_list'
    ).filter(
        schedule__attendee_list__id__in=[current_user.id]
    ).all()
    
    return queryset


@router.get(
    '/cell/{pk}',
    response_model=ScheduleCell
)
async def get_schedule_cell(
        pk: int,
        current_user: User = Depends(get_current_user)
):
    cell = await ScheduleCell.objects.get(id=pk)

    if current_user.id in cell.schedule.attendee_list.values(['id']):
        return cell
    return Response(status_code=status.HTTP_404_NOT_FOUND)


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

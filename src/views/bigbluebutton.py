from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from core.models.bigbluebutton import Meeting
from dependencies import JWTBearer

router = APIRouter(
    prefix='/bbb',
    tags=['bbb'],
    dependencies=[Depends(JWTBearer())]
)


@router.get(
    '/',
    response_model=List[Meeting]
)
async def get_meetings():
    meetings = await Meeting.objects.all()
    return meetings


@router.get(
    '/{pk}',
    response_model=Meeting
)
async def get_meeting(pk: str):
    meeting = await Meeting.objects.get(id=pk)
    return meeting


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=Meeting
)
async def create_meeting(
        meeting: Meeting.get_pydantic(exclude={'schedule_cell'})  # noqa: F821
):
    await Meeting(**meeting.dict()).save()
    return meeting

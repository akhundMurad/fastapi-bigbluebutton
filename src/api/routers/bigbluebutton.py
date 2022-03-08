from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from src.api.dependencies.jwtbearer import jwtbearer_provider
from src.schemas.bigbluebutton import MeetingCreate, MeetingRead, MeetingReadMany
from src.services.base.result import handle_result
from src.services.bigbluebutton.meeting import MeetingService

router = APIRouter(
    prefix="/bbb", tags=["bbb"], dependencies=[Depends(jwtbearer_provider)]
)


@router.get("/", response_model=MeetingReadMany)
async def get_meetings():
    result = await MeetingService().read_all()
    return MeetingReadMany(handle_result(result))


@router.get("/{pk}", response_model=MeetingRead)
async def get_meeting(pk: str):
    result = await MeetingService().read(UUID(pk))
    return MeetingRead(handle_result(result))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MeetingRead)
async def create_meeting(
    meeting: MeetingCreate,
):
    result = await MeetingService().create(meeting)
    return MeetingRead(handle_result(result))

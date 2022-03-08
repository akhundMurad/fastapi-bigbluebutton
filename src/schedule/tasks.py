from uuid import UUID

from src.services.schedule.schedule_cell import ScheduleCellService


async def create_meetings(ctx, schedule_cell_id: UUID) -> None:
    schedule_cell = await ScheduleCellService().read(schedule_cell_id)

    for meeting in schedule_cell.value.meetings:
        meeting.api.create()

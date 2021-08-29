from typing import NoReturn

from core.models.schedule import ScheduleCell


async def create_meetings(ctx, schedule_cell_id: int) -> NoReturn:
    from service import create_meetings_by_cell

    schedule_cell = await ScheduleCell.objects.get(id=schedule_cell_id)

    await create_meetings_by_cell(schedule_cell)

from ormar import post_save

from core.models.schedule import ScheduleCell


@post_save(ScheduleCell)
async def create_task(sender, instance, **kwargs):
    pass

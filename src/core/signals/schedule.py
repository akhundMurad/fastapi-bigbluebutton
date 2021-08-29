from datetime import timedelta

from ormar import post_save

from core.models.schedule import ScheduleCell

from main import app


@post_save(ScheduleCell)
async def create_task(sender, instance, **kwargs):
    await app.redis.enqueue_job(
        'create_meetings',
        instance.id,
        _defer_until=instance.datetime_start - timedelta(minutes=15)
    )

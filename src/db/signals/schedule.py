from datetime import timedelta

from sqlalchemy import event

from db.models import ScheduleCell
from main import app


@event.listens_for(ScheduleCell, "after_insert")
async def create_task(mapper, connection, target):
    if target.id is not None:
        await app.redis.enqueue_job(
            "create_meetings",
            target.id,
            _defer_until=target.datetime_start - timedelta(minutes=15),
        )

import asyncio
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

sys.path = ["", ".."] + sys.path[1:]

from src.api.dependencies.settings import get_settings

SETTINGS = get_settings()

config = context.config

fileConfig(config.config_file_name)

import src.db.models as models

target_metadata = models.mapper_registry.metadata


config.set_main_option("sqlalchemy.url", str(SETTINGS.database_dsn))


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


asyncio.run(run_migrations_online())

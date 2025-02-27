import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from config.settings import settings
from users.models.orm.user import User  # noqa: F401
from twots_bot.models.orm.message import Message  # noqa: F401
from twots_bot.models.orm.qr_data import QRData  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata
config.set_main_option("sqlalchemy.url", settings.dsn__database)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    context.configure(
       url=settings.dsn__database,
       target_metadata=target_metadata,
       literal_binds=True,
       dialect_opts={"paramstyle": "named"},
       )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.configure(
           connection=connection,
           target_metadata=target_metadata,
        )
        context.run_migrations()


async def run_migrations_online():
    config_section = config.get_section(config.config_ini_section)
    config_section["sqlalchemy.url"] = settings.dsn__database
    connectable = AsyncEngine(
       engine_from_config(
           config_section,
           prefix="sqlalchemy.",
           poolclass=pool.NullPool,
           future=True,
       ))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

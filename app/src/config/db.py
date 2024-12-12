from typing import AsyncIterator, Annotated

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession as AsynSessionSQLModel

from config.settings import settings

async_engine = create_async_engine(
    settings.dsn__database,
    pool_pre_ping=True,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
    class_=AsynSessionSQLModel,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        print(e)


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]

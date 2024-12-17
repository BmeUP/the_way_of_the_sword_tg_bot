from typing import TypeVar, Generic

from sqlmodel import SQLModel
from sqlalchemy import select

from config.db import AsyncSession


ModelClass = TypeVar('ModelClass', bound=SQLModel)


class BaseRepository(Generic[ModelClass]):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.entity: ModelClass | None = None
        self.data = None
        self.set_entity()

    def set_entity(self):
        raise NotImplementedError()

    def add_to_the_session(self, data):
        self.data = data
        self.session.add(self.data)

    async def get_object_by_params(self, **kwargs) -> ModelClass | None:
        statement = select(self.entity)

        for key, value in kwargs.items():
            statement = statement.where(self.entity.__table__.columns.get(key) == value) # noqa

        return await self.session.scalars(statement=statement)

    async def get_one_or_none_by_params(self, **kwargs):
        res = await self.get_object_by_params(**kwargs)
        return res.one_or_none()

    async def get_all_by_params(self, **kwargs):
        res = await self.get_object_by_params(**kwargs)
        return res.all()

    async def persist(self):
        try:
            await self.session.commit()
            await self.session.refresh(self.data)
            await self.session.close()
            return self.data
        except Exception:
            await self.session.rollback()

from config.db import AsyncSessionLocal
from common.repository import BaseRepository
from users.models.orm.user import User


class UserRepository(BaseRepository):
    def set_entity(self):
        self.entity = User


async def get_user_repo():
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        return user_repo

import asyncio

from config.settings import settings
from config.db import get_local_session
from users.models.repositories.user_repository import UserRepository
from users.models.orm.user import User
from admin_panel.utils import hash_password


async def create_admin():
    async with get_local_session() as session:
        user_repo = UserRepository(session=session)
        admin_user = User(username=settings.admin_username, password=hash_password(password=settings.admin_password))
        user_repo.add_to_the_session(data=admin_user)
        await user_repo.persist()


asyncio.run(main=create_admin())

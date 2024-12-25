import asyncio

from config.db import get_local_session
from users.models.repositories.user_repository import UserRepository
from users.models.orm.user import User
from admin_panel.utils import hash_password


async def create_admin():
    async with get_local_session() as session:
        user_repo = UserRepository(session=session)
        admin_user = User(username="admin", password=hash_password(password="admin_password_1"))
        user_repo.add_to_the_session(data=admin_user)
        await user_repo.persist()


asyncio.run(main=create_admin())

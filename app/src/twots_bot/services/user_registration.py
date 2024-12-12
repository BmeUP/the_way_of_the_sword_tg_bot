from aiogram.types import Message

from users.models.repositories.user_repository import UserRepository
from users.models.orm.user import User


class TGUserRegistration:
    def __init__(self, message, user_repo):
        self.__message: Message = message
        self.__user_repo: UserRepository = user_repo

    async def __save_initial_user_data(self):
        if not self.__user:
            self.__user_repo.add_to_the_session(data=User(first_name=self.__message.from_user.first_name,
                                                          last_name=self.__message.from_user.last_name,
                                                          telegram_user_id=self.__message.from_user.id))
            await self.__user_repo.persist()

    async def register(self):
        await self.__save_initial_user_data()

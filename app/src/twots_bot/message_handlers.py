from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from config.db import get_local_session
from users.models.repositories.user_repository import UserRepository
from users.models.orm.user import User
from twots_bot.services.user_data_filling import UserDataFilling
from twots_bot.services.user_registration import TGUserRegistration
from twots_bot.models.repositories.message_repository import MessageRepository
from twots_bot.models.orm.message import Message as DBMessage


twots_aiogram_router = Router()


@twots_aiogram_router.message(CommandStart())
async def start(message: Message) -> None:
    async with get_local_session() as session:
        user_repo = UserRepository(session=session)
        user: User | None = await user_repo.get_object_by_params(telegram_user_id=message.from_user.id)

        if not user:
            tg_user_registration = TGUserRegistration(message=message, user_repo=user_repo)
            await tg_user_registration.register()


@twots_aiogram_router.message()
async def echo(message: Message):
    async with get_local_session() as session:
        user_repo = UserRepository(session=session)
        user: User = await user_repo.get_object_by_params(telegram_user_id=message.from_user.id)

        if not user.is_manager:
            user_data_filling = UserDataFilling(message=message,
                                                user=user,
                                                user_repo=user_repo)
            await user_data_filling.fill_data()
            return

        message_repo = MessageRepository(session=session)
        message_repo.add_to_the_session(data=DBMessage(text=message.text))
        await message_repo.persist()

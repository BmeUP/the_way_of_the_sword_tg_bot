from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from twots_bot.services.user_registration import TGUserRegistration
from users.models.repositories.user_repository import get_user_repo


twots_aiogram_router = Router()


@twots_aiogram_router.message(CommandStart())
async def start(message: Message) -> None:
    user_repo = await get_user_repo()
    user = await user_repo.get_object_by_params(telegram_user_id=message.from_user.id)

    if not user:
        tg_user_registration = TGUserRegistration(message=message, user_repo=user_repo)
        await tg_user_registration.register()


@twots_aiogram_router.message()
async def echo(message: Message):
    user_repo = await get_user_repo()
    user = await user_repo.get_object_by_params(telegram_user_id=message.from_user.id)
    await message.answer(message.text)

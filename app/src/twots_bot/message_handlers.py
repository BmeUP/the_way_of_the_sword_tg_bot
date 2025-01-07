from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart

from config.db import get_local_session
from users.models.repositories.user_repository import UserRepository
from users.models.orm.user import User
from twots_bot.services.user_data_filling import UserDataFilling
from twots_bot.services.user_registration import TGUserRegistration
from twots_bot.models.repositories.message_repository import MessageRepository
from twots_bot.models.orm.message import Message as DBMessage
from twots_bot.services.user_qr import UserQR
from twots_bot.models.repositories.qr_data_repository import QRDataRepository
from twots_bot.services.downloads import DownloadMedia


twots_aiogram_router = Router()


@twots_aiogram_router.message(CommandStart())
async def start(message: Message) -> None:
    async with get_local_session() as session:
        user_repo = UserRepository(session=session)
        user: User | None = await user_repo.get_one_or_none_by_params(telegram_user_id=message.from_user.id)

        if not user:
            tg_user_registration = TGUserRegistration(message=message, user_repo=user_repo)
            await tg_user_registration.register()


@twots_aiogram_router.message()
async def echo(message: Message):
    async with get_local_session() as session:
        user_repo = UserRepository(session=session)
        user: User = await user_repo.get_one_or_none_by_params(telegram_user_id=message.from_user.id)

        if not user.is_manager:
            user_data_filling = UserDataFilling(message=message,
                                                user=user,
                                                user_repo=user_repo)
            await user_data_filling.fill_data()
            return

        download_media = DownloadMedia(message=message)
        text, file_path = await download_media.download_media()

        message_repo = MessageRepository(session=session)
        message_repo.add_to_the_session(data=DBMessage(text=text, file_path=file_path))
        await message_repo.persist()

        await message.answer("Сообщение сохранено. Закончите его настройку в админ панели.")


@twots_aiogram_router.callback_query(F.data == "get_qr")
async def get_qr(call: CallbackQuery):
    async with get_local_session() as session:
        user_repo = UserRepository(session=session)
        qr_data_repo = QRDataRepository(session=session)
        user_qr = UserQR(user_repository=user_repo,
                         qr_data_repository=qr_data_repo,
                         telegram_user_id=call.message.chat.id)
        await call.message.answer_photo(photo=BufferedInputFile(file=await user_qr.get_qr(), filename="qr.png"))

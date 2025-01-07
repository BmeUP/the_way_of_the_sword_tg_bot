from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile

from tiq import broker
from config.db import get_local_session
from twots_bot.models.repositories.message_repository import MessageRepository
from twots_bot.config import bot
from users.models.repositories.user_repository import UserRepository


@broker.task
async def send_message(message_id, user_tg_id):
    async with get_local_session() as session:
        message_repo = MessageRepository(session=session)
        message = await message_repo.get_one_or_none_by_params(id=message_id)
        keyboard = None
        photo = None

        if message.free_qr:
            big_button_1 = InlineKeyboardButton(text="Получить qr", callback_data="get_qr")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[big_button_1]])
        elif message.file_path:
            photo = FSInputFile(message.file_path)

        if photo:
            await bot.send_photo(chat_id=user_tg_id, photo=photo, caption=message.text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=user_tg_id, text=message.text,
                                   reply_markup=keyboard)


def check_date(message_send_at_date: datetime):
    if not message_send_at_date:
        return True

    now = datetime.now()
    if message_send_at_date.month == now.month and message_send_at_date.day == now.day and message_send_at_date.hour == now.hour:
        return True
    return False


@broker.task(schedule=[{"cron": "* * * * *"}])
async def find_messages_to_send():
    async with get_local_session() as session:
        message_repo = MessageRepository(session=session)
        user_repo = UserRepository(session=session)
        messages_to_send = await message_repo.get_all_by_params(is_sent=False, is_template=False)
        users = await user_repo.get_all_by_params(bot_is_banned=False, is_manager=False)

        for message in messages_to_send:
            if check_date(message_send_at_date=message.send_at):
                for user in users:
                    if user.telegram_user_id:
                        await send_message.kiq(message_id=message.id, user_tg_id=user.telegram_user_id)
                message.is_sent = True

        await message_repo.persist()

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config.settings import settings

bot = Bot(token=settings.bot_token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

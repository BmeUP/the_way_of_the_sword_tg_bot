from fastapi import APIRouter, Request
from aiogram.types import Update

from twots_bot.config import dp, bot


twtos_bot_router = APIRouter()


@twtos_bot_router.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)

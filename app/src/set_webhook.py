import asyncio

from twots_bot.config import bot, dp
from config.settings import settings


async def set_webhook():
    await bot.set_webhook(url=settings.webhook_domain + "/webhook",
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)


asyncio.run(set_webhook())

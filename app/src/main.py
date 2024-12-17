from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from tiq import broker
from config.settings import settings
from config.db import async_engine
from twots_bot.config import dp
from twots_bot.router import twtos_bot_router
from twots_bot.message_handlers import twots_aiogram_router
from admin_panel.user_view import UserAdmin
from admin_panel.authentication import AdminAuth
from admin_panel.message_view import MessageAdmin


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()

    yield

    if not broker.is_worker_process:
        await broker.shutdown()

app = FastAPI(lifespan=lifespan)
admin = Admin(app, async_engine, authentication_backend=AdminAuth(secret_key=settings.salt))


admin.add_view(UserAdmin)
admin.add_view(MessageAdmin)

app.include_router(twtos_bot_router)
dp.include_routers(twots_aiogram_router)

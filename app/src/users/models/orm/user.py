from sqlmodel import Field

from common.base import Base


class User(Base, table=True):
    first_name: str | None
    last_name: str | None
    username: str | None
    password: str | None
    telegram_user_id: int | None
    city: str | None
    full_name: str | None
    contact_phone: str | None
    is_manager: bool = Field(default=False)
    bot_is_banned: bool = Field(default=False)
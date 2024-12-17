from datetime import datetime

from sqlmodel import Field

from common.base import Base


class Message(Base, table=True):
    text: str
    payment_link: str | None
    qr_data: str | None
    is_sent: bool = Field(default=False)
    send_at: datetime | None
    is_template: bool = Field(default=True)

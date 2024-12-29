from datetime import datetime

from sqlmodel import Field

from common.base import Base


class Message(Base, table=True):
    text: str
    free_qr: bool = Field(default=False)
    is_sent: bool = Field(default=False)
    send_at: datetime | None
    is_template: bool = Field(default=True)
    file_path: str | None

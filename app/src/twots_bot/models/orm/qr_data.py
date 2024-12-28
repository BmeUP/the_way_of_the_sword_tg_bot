from sqlmodel import Field, Relationship

from common.base import Base
from users.models.orm.user import User


class QRData(Base, table=True):
    qr_data: str
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship()

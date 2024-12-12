from datetime import datetime

from sqlmodel import SQLModel, Field


class Base(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

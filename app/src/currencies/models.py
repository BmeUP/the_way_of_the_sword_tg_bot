import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, Enum
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import Field, Relationship

from common.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from currencies.enums import RateUpdateLogicEnum


class Currency(CreatedAtMixin, table=True):
    id: str = Field(max_length=16, primary_key=True)
    name: str = Field(max_length=32)
    is_active: bool = Field(default=True)

    rates_from: list["Rate"] = Relationship(
        back_populates="currency_from",
        sa_relationship_kwargs={"foreign_keys": "[Rate.currency_from_id]"}
    )
    rates_to: list["Rate"] = Relationship(
        back_populates="currency_to",
        sa_relationship_kwargs={"foreign_keys": "[Rate.currency_to_id]"}
    )


class Rate(CreatedAtMixin, table=True):
    currency_from_id: str = Field(max_length=16, foreign_key="currency.id", primary_key=True)
    currency_to_id: str = Field(max_length=16, foreign_key="currency.id", primary_key=True)
    rate: Decimal = Field(max_digits=8, decimal_places=2)
    update_logic: RateUpdateLogicEnum = Field(sa_column=Column(Enum(RateUpdateLogicEnum)), default=RateUpdateLogicEnum.BINANCE)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    currency_from: Currency = Relationship(
        back_populates="rates_from",
        sa_relationship_kwargs={"foreign_keys": "[Rate.currency_from_id]"}
    )
    currency_to: Currency = Relationship(
        back_populates="rates_to",
        sa_relationship_kwargs={"foreign_keys": "[Rate.currency_to_id]"}
    )

    @property
    def ticker(self) -> str:
        return f"{self.currency_from_id}{self.currency_to_id}"
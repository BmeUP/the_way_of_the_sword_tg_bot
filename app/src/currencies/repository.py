from decimal import Decimal

from sqlalchemy import update, func
from sqlalchemy.orm import aliased
from sqlmodel import select

from common.repository import BaseRepository
from config.db import AsyncSession
from currencies.enums import RateUpdateLogicEnum
from currencies.models import Rate, Currency


class CurrencyRateRepository(BaseRepository[Rate]):
    async def get_binance_rates(self) -> list[Rate]:
        currency1_alias = aliased(Currency, name="currency1")
        currency2_alias = aliased(Currency, name="currency2")
        async with self.session() as session:
            rates = (
                await session.exec(select(Rate)
                .join(currency1_alias, Rate.currency_to_id == currency1_alias.id)
                .join(currency2_alias, Rate.currency_from_id == currency2_alias.id)
                .where(Rate.update_logic == RateUpdateLogicEnum.BINANCE))
            ).all()
            return rates

    async def update_binance_rate(self, currency_from_id: str, currency_to_id: str, rate: str | Decimal) -> None:
        async with self.session() as session:
            await session.exec(
                update(Rate)
                .where(Rate.currency_from_id == currency_from_id, Rate.currency_to_id == currency_to_id)
                .values(rate=rate, updated_at=func.now())
            )
            await session.commit()

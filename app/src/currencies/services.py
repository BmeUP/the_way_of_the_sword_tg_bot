from fastapi import Depends
from sqlalchemy import func

from common.vednors.binance_api.api import BinanceAPI
from currencies.repository import CurrencyRateRepository


class CurrencyRateService:
    def __init__(self, rate_repository: CurrencyRateRepository = Depends(CurrencyRateRepository)):
        self.rate_repository = rate_repository

    async def update_binance_rate(self):
        rates = await self.rate_repository.get_binance_rates()
        binance_data = await BinanceAPI.get_all_currency_rates([x.ticker for x in rates])
        binance_data_dict = {x.symbol: x.price for x in binance_data}
        for rate in rates:
            symbol = f"{rate.currency_from_id}{rate.currency_to_id}"
            if symbol in binance_data_dict:
               await self.rate_repository.update_binance_rate(rate.currency_from_id, rate.currency_to_id, binance_data_dict[symbol])
        return binance_data

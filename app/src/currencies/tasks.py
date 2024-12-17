# from taskiq_dependencies import Depends

# from currencies.services import CurrencyRateService
# from tiq import broker


# @broker.task(schedule=[{"cron": "* * * * *"}])
# async def currency_rate_all(currency_rate_service: CurrencyRateService = Depends(CurrencyRateService)):
#     await currency_rate_service.update_binance_rate()

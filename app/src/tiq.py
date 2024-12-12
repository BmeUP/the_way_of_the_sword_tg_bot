import taskiq_fastapi
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from config.settings import settings

broker = AioPikaBroker(
    url=settings.dsn__rabbitmq
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

taskiq_fastapi.init(broker, 'main:app')

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dsn__database: str
    dsn__rabbitmq: str
    webhook_domain: str
    bot_token: str
    salt: str
    admin_username: str
    admin_password: str


settings = Settings()

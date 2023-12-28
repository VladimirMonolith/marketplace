from typing import Literal


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс для работы с переменными окружения."""

    MODE: Literal['DEV', 'TEST', 'PROD', 'INFO', 'DEBUG']
    LOG_LEVEL: str

    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    SECRET: str
    PASSWORD: str

    @property
    def DATABASE_URL(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
                f'{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}')

    # для локальной разработки
    model_config = SettingsConfigDict(env_file='.env')

    # для запуска в docker
    # model_config = SettingsConfigDict(env_file='.env-docker')


settings = Settings()

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        extra = "ignore"


class CacheSettings(BaseSettings):
    redis_url: str

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        extra = "ignore"


class CelerySettings(BaseSettings):
    celery_broker_url: str
    celery_result_backend: str

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        extra = "ignore"


class EmailSetting(BaseSettings):
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        extra = "ignore"


class Settings(BaseSettings):
    db: DbSettings = DbSettings()  # type: ignore
    celery: CelerySettings = CelerySettings()  # type: ignore
    email: EmailSetting = EmailSetting()  # type: ignore
    cache: CacheSettings = CacheSettings()  # type: ignore

    secret_key: str
    access_token_expire_minutes: int = Field(
        1440, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )  # type: ignore
    algorithm: str

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        extra = "ignore"


settings = Settings()  # type: ignore

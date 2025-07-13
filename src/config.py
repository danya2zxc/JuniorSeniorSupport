from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    MODE: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    model_config = SettingsConfigDict(extra="ignore")


class CacheSettings(BaseSettings):
    redis_url: str

    model_config = SettingsConfigDict(extra="ignore")


class CelerySettings(BaseSettings):
    celery_broker_url: str
    celery_result_backend: str

    model_config = SettingsConfigDict(extra="ignore")


class EmailSetting(BaseSettings):
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str

    model_config = SettingsConfigDict(extra="ignore")


class AISettings(BaseSettings):
    openai_api_key: str

    model_config = SettingsConfigDict(extra="ignore")


class Settings(BaseSettings):
    db: DbSettings = DbSettings()  # type: ignore
    celery: CelerySettings = CelerySettings()  # type: ignore
    email: EmailSetting = EmailSetting()  # type: ignore
    cache: CacheSettings = CacheSettings()  # type: ignore
    ai: AISettings = AISettings()  # type: ignore
    MODE: str

    secret_key: str
    access_token_expire_minutes: int = 1440
    algorithm: str

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()  # type: ignore

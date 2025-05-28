from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_name: str
    postgres_user: str
    postgres_pass: str

    class Config:
        env_file = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    db: DbSettings = DbSettings()  # type: ignore
    secret_key: str
    access_token_expire_minutes: int = Field(
        1440, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )  # type: ignore
    algorithm: str

    class Config:
        env_file = Path(__file__).resolve().parents[3] / ".env"


settings = Settings()  # type: ignore

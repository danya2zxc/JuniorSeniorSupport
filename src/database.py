from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from src.config import settings

DB_USER = settings.db.postgres_user
DB_PASS = settings.db.postgres_pass
DB_HOST = settings.db.postgres_host
DB_PORT = settings.db.postgres_port
DB_NAME = settings.db.postgres_name


DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

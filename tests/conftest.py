from typing import AsyncGenerator
from unittest.mock import patch

import pytest
import redis.asyncio as redis
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings
from src.database import Base, get_async_session
from src.main import app
from src.shared.security import get_password_hash
from src.users.enums import Role
from src.users.models import User

test_database_url = (
    f"postgresql+asyncpg://{settings.db.postgres_user}:{settings.db.postgres_password}"
    f"@localhost:{settings.db.postgres_port}/test_db_jss"
)
test_engine = create_async_engine(test_database_url)
test_async_session_maker = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
)


@pytest.fixture(autouse=True)
async def setup_test_db():
    async def override_get_async_session() -> AsyncGenerator:
        async with test_async_session_maker() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with test_engine.begin() as conn:
        print("\n--- Creating TEST database tables ---")
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        print("\n--- Dropping TEST database tables ---")
        await conn.run_sync(Base.metadata.drop_all)

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def override_redis_for_tests(monkeypatch):
    """
    Подменяет URL для Redis на localhost во время тестов.
    Это нужно, чтобы приложение внутри теста подключалось к локальному Redis,
    а не к 'cache', как в docker-compose.
    """
    monkeypatch.setattr(
        settings.cache, "redis_url", "redis://localhost:6379/1"
    )


@pytest.fixture(scope="session", autouse=True)
async def test_redis():
    redis_client = await redis.from_url("redis://localhost:6379/1")
    await redis_client.flushdb()
    yield

    await redis_client.aclose()


@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:  # noqa
        yield client


@pytest.fixture
@patch("src.mailing.tasks.send_activation_mail.delay")
async def test_user_junior(mock_send_email, ac: AsyncClient):
    data = {
        "email": "testuserjunior@example.com",
        "password": "testpass123",
        "role": "junior",
    }

    await ac.post("/api/users", data=data)

    mock_send_email.assert_called_once()

    return data


@pytest.fixture
async def test_junior_auth_token(ac: AsyncClient, test_user_junior):
    resp = await ac.post(
        "/api/auth/login",
        data={
            "username": test_user_junior["email"],
            "password": test_user_junior["password"],
        },
    )
    return resp.json()["access_token"]


@pytest.fixture
@patch("src.mailing.tasks.send_activation_mail.delay")
async def test_user_senior(mock_send_email, ac: AsyncClient):
    data = {
        "email": "testusersenior@example.com",
        "password": "testpass1234",
        "role": "senior",
    }

    await ac.post("/api/users", data=data)

    mock_send_email.assert_called_once()

    return data


@pytest.fixture
async def test_senior_auth_token(ac: AsyncClient, test_user_senior):
    resp = await ac.post(
        "/api/auth/login",
        data={
            "username": test_user_senior["email"],
            "password": test_user_senior["password"],
        },
    )

    return resp.json()["access_token"]


@pytest.fixture
@patch("src.mailing.tasks.send_activation_mail.delay")
async def test_user_senior_2(mock_send_email, ac: AsyncClient):
    data = {
        "email": "testusersenior2@example.com",
        "password": "testpass1234",
        "role": "senior",
    }

    await ac.post("/api/users", data=data)

    mock_send_email.assert_called_once()

    return data


@pytest.fixture
async def test_senior_auth_token_2(ac: AsyncClient, test_user_senior_2):
    resp = await ac.post(
        "/api/auth/login",
        data={
            "username": test_user_senior_2["email"],
            "password": test_user_senior_2["password"],
        },
    )

    return resp.json()["access_token"]


@pytest.fixture
async def test_user_admin():
    admin_data = {
        "email": "admin@example.com",
        "password": "adminpassword",
        "role": "admin",
    }

    user = User(
        email=admin_data["email"],
        hashed_password=get_password_hash(admin_data["password"]),
        role=Role.ADMIN,
        is_verified=True,
    )

    async with test_async_session_maker() as session:
        session.add(user)
        await session.commit()

    return admin_data


@pytest.fixture
async def test_admin_auth_token(ac: AsyncClient, test_user_admin):
    resp = await ac.post(
        "/api/auth/login",
        data={
            "username": test_user_admin["email"],
            "password": test_user_admin["password"],
        },
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


@pytest.fixture
async def test_issue(ac: AsyncClient, test_junior_auth_token):
    data = {"title": "testtitle", "body": "testbody"}
    resp = await ac.post(
        "/api/issues",
        data=data,
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
    )  # noqa

    issue = resp.json()

    return issue["id"]

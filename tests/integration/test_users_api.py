from unittest.mock import patch

import pytest
from httpx import AsyncClient
from tests.conftest import test_async_session_maker

from src.shared.security import get_password_hash
from src.users.enums import Role
from src.users.models import User


@pytest.mark.asyncio
@patch("src.mailing.tasks.send_activation_mail.delay")
async def test_create_user(mock_send_email, ac: AsyncClient):
    data = {
        "email": "johndoe@email.com",
        "password": 12345678,
        "role": "junior",
    }

    response = await ac.post("/api/users", data=data)

    result = response.json()

    assert response.status_code == 201
    assert result["email"] == data["email"]
    assert result["role"] == data["role"]

    mock_send_email.assert_called_once()


@pytest.mark.asyncio
@patch("src.mailing.tasks.send_activation_mail.delay")
async def test_create_registered_user(mock_send_email, ac: AsyncClient):
    data = {
        "email": "johndoe@email.com",
        "password": 12345678,
        "role": "junior",
    }

    await ac.post("/api/users", data=data)
    response = await ac.post("/api/users", data=data)

    result = response.json()
    print(result)

    assert response.status_code == 409

    assert result.get("detail", "") == "Email already registered"

    mock_send_email.assert_called_once()


@pytest.mark.asyncio
async def test_get_me(ac: AsyncClient, test_junior_auth_token):
    resp = await ac.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
    )

    assert resp.status_code == 200
    assert resp.json()["email"] == "testuserjunior@example.com"


@pytest.mark.asyncio
async def test_get_me_no_token(ac: AsyncClient):
    resp = await ac.get("/api/users/me")

    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_update_password(ac: AsyncClient, test_junior_auth_token):
    resp = await ac.patch(
        "/api/users/me/password",
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
        data={"old_password": "testpass123", "new_password": "testpass"},
    )

    assert resp.status_code == 200
    assert resp.json()["detail"] == "Password updated successfully"


@pytest.mark.asyncio
async def test_me_update_password_incorrect_old_password(
    ac: AsyncClient,
    test_junior_auth_token,
):
    resp = await ac.patch(
        "/api/users/me/password",
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
        data={"old_password": "testpass122", "new_password": "testpass"},
    )

    assert resp.status_code == 403
    assert resp.json()["detail"] == "Incorrect password"


@pytest.mark.asyncio
async def test_me_update_password_new_password_same_as_previous(
    ac: AsyncClient,
    test_junior_auth_token,
):
    resp = await ac.patch(
        "/api/users/me/password",
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
        data={"old_password": "testpass123", "new_password": "testpass123"},
    )

    assert resp.status_code == 400
    assert resp.json()["detail"] == (
        "New password must be different from old password"
    )


@pytest.mark.asyncio
async def test_me_update_password_not_authenticated(ac: AsyncClient):
    resp = await ac.patch(
        "/api/users/me/password",
        data={"old_password": "testpass123", "new_password": "testpass"},
    )

    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_users_list_by_junior(
    ac: AsyncClient,
    test_junior_auth_token,
):
    resp = await ac.get(
        "/api/users",
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
    )

    assert resp.status_code == 403
    assert resp.json()["detail"] == "Access denied"


@pytest.mark.asyncio
async def test_get_users_list_not_authenticated(ac: AsyncClient):
    resp = await ac.get("/api/users")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_users_list_by_admin_with_pagination(
    ac: AsyncClient,
    test_admin_auth_token,
):
    # --- phase prepare (Arrange) ---

    users_to_create = []
    for i in range(15):
        users_to_create.append(
            User(
                email=f"testuser{i}@example.com",
                hashed_password=get_password_hash("password"),
                role=Role.JUNIOR,
            )
        )

    async with test_async_session_maker() as session:
        session.add_all(users_to_create)
        await session.commit()

    # ---(Act) ---

    resp = await ac.get(
        "/api/users?skip=5&limit=5",
        headers={"Authorization": f"Bearer {test_admin_auth_token}"},
    )

    # --- (Assert) ---
    assert resp.status_code == 200

    result_data = resp.json()
    assert len(result_data) == 5

    assert result_data[0]["email"] == "testuser4@example.com"
    assert result_data[4]["email"] == "testuser8@example.com"


@pytest.mark.asyncio
async def test_user_delete_by_admin(ac: AsyncClient, test_admin_auth_token):
    resp = await ac.delete(
        "/api/users/1",
        headers={"Authorization": f"Bearer {test_admin_auth_token}"},
    )

    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_user_delete_by_not_admin(
    ac: AsyncClient,
    test_junior_auth_token,
):
    resp = await ac.delete(
        "/api/users/1",
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
    )

    assert resp.status_code == 403
    assert resp.json()["detail"] == "Access denied"


@pytest.mark.asyncio
async def test_user_delete_not_found(ac: AsyncClient, test_admin_auth_token):
    resp = await ac.delete(
        "/api/users/55",
        headers={"Authorization": f"Bearer {test_admin_auth_token}"},
    )

    assert resp.status_code == 404
    assert resp.json()["detail"] == "User not found"

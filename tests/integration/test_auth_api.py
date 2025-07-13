import pytest
from httpx import AsyncClient

from src.mailing.service import ActivationService


@pytest.mark.asyncio
async def test_login(ac: AsyncClient, test_user_junior):
    resp = await ac.post(
        "/api/auth/login",
        data={
            "username": test_user_junior["email"],
            "password": test_user_junior["password"],
        },
    )

    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_with_wrong_password(ac: AsyncClient, test_user_junior):
    resp = await ac.post(
        "/api/auth/login",
        data={"username": test_user_junior["email"], "password": 123},
    )

    assert resp.status_code == 401
    assert resp.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_complete_activation_successful(
    ac: AsyncClient,
    test_user_junior,
):
    # --- Prepare (Arrange) ---
    user_email = test_user_junior["email"]

    activation_service = ActivationService()

    token = activation_service.create_token(email=user_email)

    # --- Action (Act) ---
    resp = await ac.patch(f"/api/auth/complete-activation?token={token}")

    assert resp.status_code == 200
    assert resp.json()["message"] == f"User {user_email} verified"

    resp_retry = await ac.patch(f"/api/auth/complete-activation?token={token}")
    assert resp_retry.status_code == 404
    assert resp_retry.json()["detail"] == "Invalid or expired activation link"

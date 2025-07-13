import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_issues_list_empty(ac: AsyncClient):
    response = await ac.get("/api/issues")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_issue_create_not_authenticated(ac: AsyncClient):
    data = {"title": "testtitle", "body": "testbody"}
    resp = await ac.post("/api/issues", data=data)

    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_issue_create_by_senior(ac: AsyncClient, test_senior_auth_token):
    data = {"title": "testtitle", "body": "testbody"}
    resp = await ac.post(
        "/api/issues",
        data=data,
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    assert resp.status_code == 403
    assert resp.json()["detail"] == "Access denied"


@pytest.mark.asyncio
async def test_issue_take_by_senior_successfully(
    ac: AsyncClient,
    test_issue,
    test_senior_auth_token,
):
    resp = await ac.put(
        f"/api/issues/{test_issue}/take",
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    assert resp.status_code == 200
    assert resp.json()["status"] == "IN_PROGRESS"


@pytest.mark.asyncio
async def test_issue_close_by_senior(
    ac: AsyncClient,
    test_issue,
    test_senior_auth_token,
):
    await ac.put(
        f"/api/issues/{test_issue}/take",
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    resp = await ac.put(
        f"/api/issues/{test_issue}/close",
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    assert resp.status_code == 200
    assert resp.json()["status"] == "CLOSED"


@pytest.mark.asyncio
async def test_issue_close_by_another_senior(
    ac: AsyncClient,
    test_issue,
    test_senior_auth_token,
    test_senior_auth_token_2,
):
    await ac.put(
        f"/api/issues/{test_issue}/take",
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    resp = await ac.put(
        f"/api/issues/{test_issue}/close",
        headers={"Authorization": f"Bearer {test_senior_auth_token_2}"},
    )

    assert resp.status_code == 422
    assert resp.json()["detail"] == "Can't close this issue"


@pytest.mark.asyncio
async def test_issue_message_by_senior(
    ac: AsyncClient,
    test_issue,
    test_senior_auth_token,
):
    await ac.put(
        f"/api/issues/{test_issue}/take",
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    data = {
        "body": "testmessage",
    }

    resp = await ac.post(
        f"/api/issues/{test_issue}/messages",
        json=data,
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    assert resp.status_code == 200
    assert resp.json()["issue_id"] == test_issue


@pytest.mark.asyncio
async def test_issue_message_by_junior(
    ac: AsyncClient,
    test_issue,
    test_junior_auth_token,
    test_senior_auth_token,
):
    await ac.put(
        f"/api/issues/{test_issue}/take",
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    data = {
        "body": "testmessage",
    }

    resp = await ac.post(
        f"/api/issues/{test_issue}/messages",
        json=data,
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
    )

    assert resp.status_code == 200
    assert resp.json()["issue_id"] == test_issue


@pytest.mark.asyncio
async def test_issue_message_by_another_senior(
    ac: AsyncClient,
    test_issue,
    test_senior_auth_token_2,
    test_senior_auth_token,
):
    await ac.put(
        f"/api/issues/{test_issue}/take",
        headers={"Authorization": f"Bearer {test_senior_auth_token}"},
    )

    data = {
        "body": "testmessage",
    }

    resp = await ac.post(
        f"/api/issues/{test_issue}/messages",
        json=data,
        headers={"Authorization": f"Bearer {test_senior_auth_token_2}"},
    )

    assert resp.status_code == 403
    assert resp.json()["detail"] == "You are not a participant in this issue"


@pytest.mark.asyncio
async def test_issue_take_by_junior(
    ac: AsyncClient,
    test_issue,
    test_junior_auth_token,
):
    resp = await ac.put(
        f"/api/issues/{test_issue}/take",
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
    )

    assert resp.status_code == 403
    assert resp.json()["detail"] == "Access denied"


@pytest.mark.asyncio
async def test_issue_close_by_junior(
    ac: AsyncClient,
    test_issue,
    test_junior_auth_token,
):
    resp = await ac.put(
        f"/api/issues/{test_issue}/close",
        headers={"Authorization": f"Bearer {test_junior_auth_token}"},
    )

    assert resp.status_code == 403
    assert resp.json()["detail"] == "Access denied"


@pytest.mark.asyncio
async def test_issue_close_by_not_authenticated(ac: AsyncClient, test_issue):
    resp = await ac.put(f"/api/issues/{test_issue}/close")

    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_issue_take_by_not_authenticated(ac: AsyncClient, test_issue):
    resp = await ac.put(f"/api/issues/{test_issue}/take")

    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"

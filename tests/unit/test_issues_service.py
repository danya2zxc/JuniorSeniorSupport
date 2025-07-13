from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.issues.enums import Status
from src.issues.models import Issue
from src.issues.service import IssueCRUD


@pytest.mark.asyncio
async def test_issue_take_by_senior_success():
    mock_session = AsyncMock()

    test_issue = Issue(id=1, status=Status.OPENED, senior_id=None)

    crud_instance = IssueCRUD(mock_session)

    crud_instance.get_by_id = AsyncMock(return_value=test_issue)

    senior_id_to_assign = 10

    updated_issue = await crud_instance.assign_to_senior(
        issue_id=1,
        senior_id=senior_id_to_assign,
    )

    assert updated_issue.status == Status.IN_PROGRESS
    assert updated_issue.senior_id == senior_id_to_assign

    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_take_by_senior_fails_if_already_taken():
    mock_session = AsyncMock()

    test_issue = Issue(id=1, status=Status.IN_PROGRESS, senior_id=1)

    crud_instance = IssueCRUD(mock_session)
    crud_instance.get_by_id = AsyncMock(return_value=test_issue)

    with pytest.raises(HTTPException) as exc_info:
        await crud_instance.assign_to_senior(issue_id=1, senior_id=11)

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Can't take this issue"

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.auth.dependencies import get_current_user, optional_current_user
from src.issues.dependencies import get_issue_crud, get_message_crud
from src.issues.schemas import (
    IssueCreate,
    IssueResponse,
    MessageCreate,
    MessageResponse,
)
from src.issues.service import IssueBase, IssueCRUD, MessageCRUD
from src.shared.permissions import RoleChecker
from src.users.enums import Role
from src.users.models import User

router = APIRouter(prefix="/issues")


@router.get("", response_model=List[IssueResponse])
async def issues_list(
    skip: int = 0,
    limit: int = 100,
    issue_crud: IssueCRUD = Depends(get_issue_crud),
    user: User | None = Depends(optional_current_user),
):
    return await issue_crud.get_all_filtered(skip, limit, user)


@router.get("/{issue_id}", response_model=IssueResponse)
async def issue_get_by_id(
    issue_id: int,
    issue_crud: IssueCRUD = Depends(get_issue_crud),
    current_user: User = Depends(get_current_user),
):
    issue = await issue_crud.get_by_id(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.post("", response_model=IssueResponse)
async def issue_create(
    issue_data: IssueBase = Depends(IssueCreate.as_form),
    issue_crud: IssueCRUD = Depends(get_issue_crud),
    current_user: User = Depends(RoleChecker(Role.ADMIN, Role.JUNIOR)),
):
    return await issue_crud.create_issue(issue_data, junior_id=current_user.id)


@router.post("/random", response_model=IssueResponse)
async def issue_create_random(
    current_user: User = Depends(get_current_user),
    issue_crud: IssueCRUD = Depends(get_issue_crud),
):
    return await issue_crud.create_random_issue()


@router.patch("/{issue_id}", response_model=IssueResponse)
async def issue_update(
    issue_id: int,
    issue_data: IssueBase = Depends(IssueCreate.as_form),
    current_user: User = Depends(get_current_user),
    issue_crud: IssueCRUD = Depends(get_issue_crud),
):
    issue = await issue_crud.get_by_id(issue_id)
    if not issue:
        raise HTTPException(404, detail="Issue not found")

    if current_user.role == Role.SENIOR and issue.senior_id != current_user.id:
        raise HTTPException(403, detail="Not allowed to update this issue")

    if current_user.role not in [Role.SENIOR, Role.ADMIN]:
        raise HTTPException(403, detail="Only senior or admin can edit issues")

    return await issue_crud.update_issue(issue_id, issue_data)


@router.delete("/{issue_id}")
async def issue_delete(
    issue_id: int,
    issue_crud: IssueCRUD = Depends(get_issue_crud),
    current_user: User = Depends(RoleChecker(Role.ADMIN)),
):
    issue = await issue_crud.delete_issue(issue_id)
    if not issue:
        raise HTTPException(404, detail="Issue not found")
    return {"detail": f"Issue {issue_id} deleted"}


@router.put("/{issue_id}/take", response_model=IssueResponse)
async def issue_take(
    issue_id: int,
    issue_crud: IssueCRUD = Depends(get_issue_crud),
    current_user: User = Depends(RoleChecker(Role.SENIOR)),
):
    return await issue_crud.assign_to_senior(issue_id, current_user.id)


@router.get("/{issue_id}/messages", response_model=list[MessageResponse])
async def issue_messages_get(
    issue_id: int,
    message_crud: MessageCRUD = Depends(get_message_crud),
    current_user: User = Depends(get_current_user),
):
    return await message_crud.get_all_for_issue(issue_id, current_user)


@router.put("/{issue_id}/close", response_model=IssueResponse)
async def issue_close(
    issue_id: int,
    issue_crud: IssueCRUD = Depends(get_issue_crud),
    current_user: User = Depends(RoleChecker(Role.SENIOR)),
):
    return await issue_crud.close_issue(issue_id, current_user.id)


@router.post("/{issue_id}/messages", response_model=MessageResponse)
async def issue_message_post(
    issue_id: int,
    message_data: MessageCreate,
    message_crud: MessageCRUD = Depends(get_message_crud),
    current_user: User = Depends(get_current_user),
):
    return await message_crud.create_for_issue(
        issue_id, current_user, message_data
    )

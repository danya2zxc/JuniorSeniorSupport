from typing import List

from app.database import get_async_session
from crud.issue_crud import IssueCRUD
from fastapi import APIRouter, Depends, HTTPException
from schemas.issues_schema import IssueBase, IssueResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/issues")


@router.get("", response_model=List[IssueResponse])
async def get_issues(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_async_session)
):
    issues_crud = IssueCRUD(db)
    issues = await issues_crud.get_all(skip, limit)
    return issues


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(issue_id: int, db: Session = Depends(get_async_session)):
    issues_crud = IssueCRUD(db)
    issue = await issues_crud.get_by_id(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.post("", response_model=IssueResponse)
async def create_issue(
    issue_data: IssueBase, db: Session = Depends(get_async_session)
):
    issues_crud = IssueCRUD(db)
    new_issue = await issues_crud.create_issue(issue_data)
    return new_issue


@router.post("/create", response_model=IssueResponse)
async def create_random_issue(db: Session = Depends(get_async_session)):
    issues_crud = IssueCRUD(db)
    new_issue = await issues_crud.create_random_issue()
    return new_issue

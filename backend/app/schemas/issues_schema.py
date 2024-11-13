from datetime import datetime

from enums.status import Status
from pydantic import BaseModel


class IssueBase(BaseModel):
    title: str
    body: str
    status: Status = Status.OPENED

    class Config:
        orm_mode = True


class IssueResponse(IssueBase):
    id: int
    junior_id: int
    senior_id: int | None = None


class IssueCreate(IssueBase):
    pass


class IssueDetail(IssueBase):
    id: int
    junior_id: int
    senior_id: int
    created_at: datetime
    updated_at: datetime

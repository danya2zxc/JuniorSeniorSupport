from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field

from src.issues.enums import Status


class IssueBase(BaseModel):
    title: str
    body: str
    status: Status = Status.OPENED

    model_config = ConfigDict(from_attributes=True)


class IssueCreate(BaseModel):
    title: str
    body: str

    @classmethod
    def as_form(cls, title: str = Form(...), body: str = Form(...)):
        return cls(title=title, body=body)

    model_config = ConfigDict(from_attributes=True)


class IssueResponse(IssueBase):
    id: int
    junior_id: int
    senior_id: int | None = None


class IssueWithDates(IssueResponse):
    created_at: datetime
    updated_at: datetime


class IssuePreview(BaseModel):
    id: int
    title: str


class MessageBase(BaseModel):
    body: str = Field(..., max_length=1000)


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    timestamp: datetime
    user_id: int
    issue_id: int

    model_config = ConfigDict(from_attributes=True)

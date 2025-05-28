import random
import string

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.issues.enums import Status
from src.issues.models import Issue, Message
from src.issues.schemas import IssueBase, MessageCreate
from src.users.enums import Role
from src.users.models import User


def _random_string(length=10):
    return "".join(
        [random.choice(string.ascii_letters) for i in range(length)]
    )


class IssueCRUD:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_filtered(
        self, skip: int, limit: int, user: User | None = None
    ):
        query = select(Issue)

        if user is None:
            query = query.where(Issue.status == Status.CLOSED)
        elif user.role == Role.SENIOR:
            query = query.where(Issue.status == Status.IN_PROGRESS)
        elif user.role == Role.JUNIOR:
            query = query.where(Issue.junior_id == user.id)

        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, issue_id: int):
        query = select(Issue).filter(Issue.id == issue_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_issue(self, issue_data: IssueBase, junior_id: int):
        new_issue = Issue(
            **issue_data.model_dump(),
            status=Status.OPENED,
            junior_id=junior_id,
        )
        self.db.add(new_issue)
        await self.db.commit()
        await self.db.refresh(new_issue)
        return new_issue

    async def create_random_issue(self):
        new_issue = Issue(
            junior_id=1, title=_random_string(), body=_random_string()
        )
        self.db.add(new_issue)
        await self.db.commit()
        await self.db.refresh(new_issue)
        return new_issue

    async def update_issue(self, issue_id: int, data: IssueBase):
        issue = await self.get_by_id(issue_id)
        if issue is None:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(issue, field, value)
        await self.db.commit()
        await self.db.refresh(issue)
        return issue

    async def delete_issue(self, issue_id: int):
        issue = await self.get_by_id(issue_id)
        if issue is None:
            return None
        await self.db.delete(issue)
        await self.db.commit()
        return issue

    async def assign_to_senior(self, issue_id: int, senior_id: int):
        issue = await self.get_by_id(issue_id)
        if (
            not issue
            or issue.senior_id is not None
            or issue.status != Status.OPENED
        ):
            raise HTTPException(
                status_code=422, detail="Can't take this issue"
            )

        issue.senior_id = senior_id
        issue.status = Status.IN_PROGRESS
        await self.db.commit()
        await self.db.refresh(issue)
        return issue

    async def close_issue(self, issue_id: int, senior_id: int):
        issue = await self.get_by_id(issue_id)
        if (
            not issue
            or issue.senior_id != senior_id
            or issue.status != Status.IN_PROGRESS
        ):
            raise HTTPException(
                status_code=422, detail="Can't close this issue"
            )

        issue.status = Status.CLOSED
        await self.db.commit()
        await self.db.refresh(issue)
        return issue


class MessageCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_for_issue(self, issue_id: int, user: User):
        query = (
            select(Message)
            .where(
                (Message.issue_id == issue_id)
                & (
                    (Message.user_id == user.id)
                    | (
                        Issue.id == issue_id
                        and (
                            (Issue.junior_id == user.id)
                            | (Issue.senior_id == user.id)
                        )
                    )
                )
            )
            .order_by(Message.timestamp)
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_for_issue(
        self, issue_id: int, user: User, message_data: MessageCreate
    ):
        new_msg = Message(
            body=message_data.body,
            user_id=user.id,
            issue_id=issue_id,
        )
        self.db.add(new_msg)
        await self.db.commit()
        await self.db.refresh(new_msg)
        return new_msg

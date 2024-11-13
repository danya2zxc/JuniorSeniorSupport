import random
import string

from models.issues_models import Issue
from schemas.issues_schema import IssueBase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


def _random_string(length=10):
    return "".join(
        [random.choice(string.ascii_letters) for i in range(length)]
    )


class IssueCRUD:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100):
        query = select(Issue).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, issue_id: int):
        query = select(Issue).filter(Issue.id == issue_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_issue(self, issue_data: IssueBase):
        new_issue = Issue(**issue_data.dict())
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

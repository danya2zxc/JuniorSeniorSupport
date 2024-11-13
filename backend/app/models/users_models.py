from datetime import datetime

from app.database import Base
from enums.role import Role
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from models.types import intpk
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    first_name: Mapped[str] = mapped_column(
        String(15), nullable=True, index=True
    )
    last_name: Mapped[str] = mapped_column(
        String(50), nullable=True, index=True
    )

    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(
        String(15), nullable=False, default=Role.JUNIOR
    )

    data_joined: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        server_onupdate=text("TIMEZONE('utc', now())"),
    )
    junior_issues = relationship(
        "Issue", foreign_keys="[Issue.junior_id]", back_populates="junior"
    )
    senior_issues = relationship(
        "Issue", foreign_keys="[Issue.senior_id]", back_populates="senior"
    )

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.email
        )

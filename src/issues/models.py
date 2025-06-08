from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.issues.enums import Status
from src.shared.base_types import intpk


class Issue(Base):
    __tablename__ = "issues"
    __table_args__ = {"extend_existing": True}
    id: Mapped[intpk]
    junior_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    senior_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(30))
    body: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[Status] = mapped_column(default=Status.OPENED)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    junior = relationship(
        "User", back_populates="junior_issues", foreign_keys=[junior_id]
    )
    senior = relationship(
        "User", back_populates="senior_issues", foreign_keys=[senior_id]
    )

    messages = relationship("Message", back_populates="issue")

    def __repr__(self):
        return f"Issue[{self.id} {self.title[:10]}]"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[intpk]
    body: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    issue_id: Mapped[int] = mapped_column(ForeignKey("issues.id"))

    user = relationship("User")
    issue = relationship("Issue", back_populates="messages")

from app.database import Base
from enums.status import Status
from models.types import intpk
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


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

    junior = relationship(
        "User", back_populates="junior_issues", foreign_keys=[junior_id]
    )
    senior = relationship(
        "User", back_populates="senior_issues", foreign_keys=[senior_id]
    )

    def __repr__(self):
        return f"Issue[{self.id} {self.title[:10]}]"

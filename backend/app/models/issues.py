
# from database import Base
from database import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.users_model import intpk


class Issue(Base):
    __tablename__ = "issues"
    id: Mapped[intpk]
    junior_id: Mapped[int]
    senior_id: Mapped[int]
    title: Mapped[str] = mapped_column(String(30))
    body: Mapped[str] = mapped_column(Text)

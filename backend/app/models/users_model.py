from datetime import datetime
from typing import Annotated

from database import Base
from enums.role import Role
# from database import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    first_name: Mapped[str] = mapped_column(String(15), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)

    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(String(15), nullable=False, default=Role.JUNIOR)

    data_joined: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now
    )

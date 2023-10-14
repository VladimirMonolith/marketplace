from datetime import date
from typing import List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=50))
    first_name: Mapped[Optional[str]] = mapped_column(String(length=100))
    last_name: Mapped[Optional[str]] = mapped_column(String(length=150))
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    registrated: Mapped[date] = mapped_column(default=func.current_date())
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    purchases: Mapped[List['Purchase']] = relationship(
        back_populates='buyer', cascade='all, delete-orphan'
    )

    def __str__(self):
        return f'Пользователь:id - {self.id}, username - {self.username}'

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class Category(Base):
    """Модель категории."""

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=150))
    image_id: Mapped[int]
    subcategories: Mapped[List['Subcategory']] = relationship(
        back_populates='category'
    )
    # subcategories = relationship('Subcategory', back_populates='category')

    def __str__(self):
        return f'Категория:id - {self.id}, название - {self.name}'

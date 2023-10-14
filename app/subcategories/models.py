from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class Subcategory(Base):
    """Модель подкатегории."""

    __tablename__ = 'subcategories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=150))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    image_id: Mapped[int]
    # category = relationship('Category', back_populates='subcategories')
    category: Mapped['Category'] = relationship(back_populates='subcategories')
    goods: Mapped[List['Goods']] = relationship(back_populates='subcategory')
    # goods = relationship('Goods', back_populates='subcategory')

    def __str__(self):
        return f'Подкатегория:id - {self.id}, название - {self.name}'

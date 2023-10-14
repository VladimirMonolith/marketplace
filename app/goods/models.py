from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class Goods(Base):
    """Модель товара."""

    __tablename__ = 'goods'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=250))
    description: Mapped[Optional[str]] = mapped_column(String(length=500))
    price: Mapped[int]
    quantity: Mapped[int]
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategories.id'))
    image_id: Mapped[int]
    # subcategory = relationship('Subcategory', back_populates='goods')
    # purchases = relationship('Purchase', back_populates='goods')
    subcategory: Mapped['Subcategory'] = relationship(back_populates='goods')
    purchases: Mapped[List['Purchase']] = relationship(back_populates='goods')

    def __str__(self):
        return f'Товар:id - {self.id}, название - {self.name}'

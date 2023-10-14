from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Purchase(Base):
    """Модель покупки."""

    __tablename__ = 'purchases'

    id: Mapped[int] = mapped_column(primary_key=True)
    when: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    goods_id: Mapped[int] = mapped_column(ForeignKey('goods.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    buyer: Mapped['User'] = relationship(back_populates='purchases')
    goods: Mapped[List['Goods']] = relationship(back_populates='purchases')

    def __str__(self):
        return f'Покупка:id - {self.id}, совершена - {self.when}'

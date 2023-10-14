from datetime import datetime

from pydantic import BaseModel


class PurchaseRead(BaseModel):
    """Модель отображения покупки."""

    id: int
    when: datetime
    goods_id: int
    user_id: int


class PurchaseCreate(BaseModel):
    """Модель для добавления покупки."""

    goods_id: int

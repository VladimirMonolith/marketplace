from typing import Optional

from pydantic import BaseModel


class GoodsRead(BaseModel):
    """Модель отображения товара."""

    id: int
    name: str
    description: Optional[str] = None
    price: int
    quantity: int
    subcategory_id: int
    image_id: int


class GoodsCreate(BaseModel):
    """Модель для добавления товара."""

    name: str
    description: Optional[str] = None
    price: int
    quantity: int
    subcategory_id: int
    image_id: int


class GoodsUpdate(BaseModel):
    """Модель для обновления товара."""

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None
    subcategory_id: Optional[str] = None
    image_id: Optional[str] = None

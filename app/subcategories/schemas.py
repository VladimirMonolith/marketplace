from typing import Optional

from pydantic import BaseModel


class SubcategoryRead(BaseModel):
    """Модель отображения подкатегории."""

    id: int
    name: str
    category_id: int
    image_id: int


class SubcategoryCreate(BaseModel):
    """Модель для добавления подкатегории."""

    name: str
    category_id: int
    image_id: int


class SubcategoryUpdate(BaseModel):
    """Модель для обновления подкатегории."""

    name: Optional[str] = None
    category_id: Optional[str] = None
    image_id: Optional[int] = None


class SubcategoryGoodsRead(BaseModel):
    """Модель отображения товара подкатегории
    по заданным параметрам."""

    id: int
    name: str
    description: str
    price: int
    available_quantity: int
    image_id: int

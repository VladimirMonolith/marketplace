from typing import Optional

from pydantic import BaseModel


class CategoryRead(BaseModel):
    """Модель отображения категории."""

    id: int
    name: str
    image_id: int


class CategoryCreate(BaseModel):
    """Модель для добавления категории."""

    name: str
    image_id: int


class CategoryUpdate(BaseModel):
    """Модель для обновления категории."""

    name: Optional[str] = None
    image_id: Optional[int] = None

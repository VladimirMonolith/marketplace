from typing import List

from fastapi import APIRouter, Depends
from fastapi_versioning import version

from app.exceptions import (
    DatabaseErrorException,
    NotFoundException,
    ObjectAlreadyExistsException
)
from app.users.manager import current_superuser
from app.users.models import User

from .dao import CategoryDAO
from .schemas import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.post('')
@version(1)
async def create_category(
    data: CategoryCreate, user: User = Depends(current_superuser)
):
    """Позволяет добавить новую категорию."""
    category_exists = await CategoryDAO.get_object(name=data.name)

    if category_exists:
        raise ObjectAlreadyExistsException
    new_category = await CategoryDAO.add_object(**data.model_dump())

    if not new_category:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )
    return new_category


@router.get('', response_model=List[CategoryRead])
@version(1)
async def get_all_categories():
    """Возвращает все категории."""
    categories = await CategoryDAO.get_all_objects()

    if not categories:
        raise NotFoundException
    return categories


@router.get('/{category_id}', response_model=CategoryRead)
@version(1)
async def get_category(category_id: int):
    """Возвращает конкретную категорию."""
    category = await CategoryDAO.get_object(id=category_id)

    if not category:
        raise NotFoundException
    return category


@router.patch('/{category_id}', response_model=CategoryRead)
@version(1)
async def update_category(
    category_id: int,
    update_data: CategoryUpdate,
    user: User = Depends(current_superuser)
):
    """Позволяет обновить название категории."""
    category = await CategoryDAO.update_object(
        update_data=update_data, id=category_id
    )

    if not category:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return category


@router.delete('/{category_id}')
@version(1)
async def delete_category(
    category_id: int, user: User = Depends(current_superuser)
):
    """Позволяет удалить категорию."""
    result = await CategoryDAO.delete_object(id=category_id)

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result

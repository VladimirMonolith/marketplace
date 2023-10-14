from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from app.exceptions import (
    DatabaseErrorException,
    NotFoundException,
    ObjectAlreadyExistsException
)
from app.users.manager import current_superuser
from app.users.models import User

from .dao import SubcategoryDAO
from .schemas import (
    SubcategoryCreate,
    SubcategoryGoodsRead,
    SubcategoryRead,
    SubcategoryUpdate
)

router = APIRouter(
    prefix='/subcategories',
    tags=['subcategories']
)


@router.post('')
@version(1)
async def create_subcategory(
    data: SubcategoryCreate, user: User = Depends(current_superuser)
):
    """Позволяет добавить новую подкатегорию."""
    subcategory_exists = await SubcategoryDAO.get_object(name=data.name)

    if subcategory_exists:
        raise ObjectAlreadyExistsException
    new_subcategory = await SubcategoryDAO.add_object(**data.model_dump())

    if not new_subcategory:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )
    return new_subcategory


@router.get('', response_model=List[SubcategoryRead])
@version(1)
async def get_all_subcategories():
    """Возвращает все подкатегории."""
    subcategories = await SubcategoryDAO.get_all_objects()

    if not subcategories:
        raise NotFoundException
    return subcategories


@router.get('/{subcategory_id}', response_model=SubcategoryRead)
@version(1)
async def get_subcategory(subcategory_id: int):
    """Возвращает конкретную подкатегорию."""
    subcategory = await SubcategoryDAO.get_object(id=subcategory_id)

    if not subcategory:
        raise NotFoundException
    return subcategory


@router.patch('/{subcategory_id}', response_model=SubcategoryRead)
@version(1)
async def update_subcategory(
    subcategory_id: int,
    update_data: SubcategoryUpdate,
    user: User = Depends(current_superuser)
):
    """Позволяет обновить название подкатегории."""
    subcategory = await SubcategoryDAO.update_object(
        update_data=update_data, id=subcategory_id
    )

    if not subcategory:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return subcategory


@router.delete('/{subcategory_id}')
@version(1)
async def delete_subcategory(
    subcategory_id: int, user: User = Depends(current_superuser)
):
    """Позволяет удалить подкатегорию."""
    result = await SubcategoryDAO.delete_object(id=subcategory_id)

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result


@router.get('/{subcategory_id}/goods', response_model=List[SubcategoryGoodsRead])
@version(1)
@cache(expire=60)
async def get_all_subcategory_goods(
    subcategory_id: int,
    date: date = Query(
        ..., description=f'Например, {datetime.now().date()}.'
    ),
):
    """Возвращает список всех товаров категории."""
    subcategory_goods = await SubcategoryDAO.get_all_subcategory_goods_objects(
        subcategory_id=subcategory_id,
        date=date,
    )

    if not subcategory_goods:
        raise NotFoundException
    return subcategory_goods

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

from .dao import GoodsDAO
from .schemas import GoodsCreate, GoodsRead, GoodsUpdate

router = APIRouter(
    prefix='/goods',
    tags=['goods']
)


@router.post('')
@version(1)
async def create_goods(
    data: GoodsCreate, user: User = Depends(current_superuser)
):
    """Позволяет добавить новый товар."""
    goods_exists = await GoodsDAO.get_object(name=data.name)

    if goods_exists:
        raise ObjectAlreadyExistsException
    new_goods = await GoodsDAO.add_object(**data.model_dump())

    if not new_goods:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )
    return new_goods


@router.get('', response_model=List[GoodsRead])
@version(1)
async def get_goods():
    """Возвращает все товары."""
    goods = await GoodsDAO.get_all_objects()

    if not goods:
        raise NotFoundException
    return goods


@router.get('_all')
@version(1)
async def get_goods_all_information(
    user: User = Depends(current_superuser)
):
    """Возвращает все товары cо всей информацией."""
    goods = await GoodsDAO.get_goods_objects_all_information()

    if not goods:
        raise NotFoundException
    return goods


@router.get('/{goods_id}', response_model=GoodsRead)
@version(1)
async def get_good(goods_id: int):
    """Возвращает конкретный товар."""
    goods = await GoodsDAO.get_object(id=goods_id)
    if not goods:
        raise NotFoundException
    return goods


@router.patch('/{goods_id}', response_model=GoodsRead)
@version(1)
async def update_goods(
    goods_id: int,
    update_data: GoodsUpdate,
    user: User = Depends(current_superuser)
):
    """Позволяет обновить название товара."""
    goods = await GoodsDAO.update_object(
        update_data=update_data, id=goods_id
    )

    if not goods:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return goods


@router.delete('/{goods_id}')
@version(1)
async def delete_goods(
    goods_id: int, user: User = Depends(current_superuser)
):
    """Позволяет удалить товар."""
    result = await GoodsDAO.delete_object(id=goods_id)

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result

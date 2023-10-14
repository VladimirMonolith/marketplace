from typing import List

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pydantic import TypeAdapter

from app.exceptions import DatabaseErrorException, NotFoundException
from app.tasks.tasks import send_purchase_confirmation_email
from app.users.manager import current_active_user
from app.users.models import User

from .dao import PurchaseDAO
from .schemas import PurchaseCreate, PurchaseRead

router = APIRouter(
    prefix='/purchases',
    tags=['purchases']
)


@router.post('')
@version(1)
async def create_purchase(
    data: PurchaseCreate, user: User = Depends(current_active_user)
):
    """Позволяет добавить новую покупку."""
    purchase = await PurchaseDAO.add_purchase_object(
        goods_id=data.goods_id,
        user_id=user.id
    )

    if not purchase:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )

    purchase_dict = (
        TypeAdapter(PurchaseRead).validate_python(purchase).model_dump()
    )
    send_purchase_confirmation_email.delay(
        purchase=purchase_dict,
        username=user.username,
        email_to=user.email
    )
    return purchase


@router.get('', response_model=List[PurchaseRead])
@version(1)
async def get_all_purchases(user: User = Depends(current_active_user)):
    """Возвращает все покупки текущего пользователя."""
    purchases = await PurchaseDAO.get_all_objects(user_id=user.id)

    if not purchases:
        raise NotFoundException
    return purchases


@router.get('/{purchase_id}', response_model=PurchaseRead)
@version(1)
async def get_purchase(
    purchase_id: int, user: User = Depends(current_active_user)
):
    """Возвращает конкретную покупку текущего пользователя."""
    purchase = await PurchaseDAO.get_object(id=purchase_id, user_id=user.id)

    if not purchase:
        raise NotFoundException
    return purchase


@router.delete('/{purchase_id}')
@version(1)
async def delete_purchase(
    purchase_id: int, user: User = Depends(current_active_user)
):
    """Позволяет пользователю удалить/отменить покупку."""
    result = await PurchaseDAO.delete_object(
        id=purchase_id, user_id=user.id
    )

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result

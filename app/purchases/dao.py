from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import Purchase


class PurchaseDAO(BaseDAO):
    model = Purchase

    @classmethod
    async def add_purchase_object(
        cls,
        goods_id: int,
        user_id: int
    ):
        """Добавляет объект покупки в БД."""
        try:
            async with async_session_maker() as session:
                purchase = insert(Purchase).values(
                    goods_id=goods_id, user_id=user_id
                ).returning(
                    Purchase.id, Purchase.when,
                    Purchase.goods_id, Purchase.user_id
                )
                purchase = await session.execute(purchase)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return purchase.mappings().one()

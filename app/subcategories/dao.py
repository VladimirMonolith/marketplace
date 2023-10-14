from datetime import date, datetime

from fastapi import Query
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.goods.models import Goods
from app.logger import logger
from app.purchases.models import Purchase

from .models import Subcategory


class SubcategoryDAO(BaseDAO):
    model = Subcategory

    @classmethod
    async def get_all_subcategory_goods_objects(
        cls, subcategory_id: int,
        date: date = Query(
            ..., description=f'Например, {datetime.now().date()}.'
        ),
    ):
        """Возвращает список всех товаров подкатегории и их количество
        на конкретную дату."""
        try:
            async with async_session_maker() as session:
                purchased_goods = (
                    select(Purchase.goods_id, func.count(Purchase.goods_id)
                           .label('count_purchased_goods'))
                    .select_from(Purchase)
                    .where(Purchase.when <= date)
                    .group_by(Purchase.goods_id)
                    .cte('purchased_goods')
                )

                get_goods = (
                    select(
                        Goods.__table__.columns,
                        (Goods.quantity - func.coalesce(
                            purchased_goods.c.count_purchased_goods, 0
                        ))
                        .label('available_quantity')
                    )
                    .join(
                        purchased_goods,
                        purchased_goods.c.goods_id == Goods.id,
                        isouter=True)
                    .where(
                        Goods.subcategory_id == subcategory_id
                    )
                )

                all_subcategory_goods = await session.execute(get_goods)
                return all_subcategory_goods.mappings().all()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={
                    'subcategory_id': subcategory_id,
                    'date': date
                },
                exc_info=True
            )
            return None

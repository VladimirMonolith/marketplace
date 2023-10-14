from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import Goods


class GoodsDAO(BaseDAO):
    model = Goods

    @classmethod
    async def get_goods_objects_all_information(cls, **kwargs):
        """Возвращает все товары cо всей информацией."""
        try:
            async with async_session_maker() as session:
                goods = (
                    select(Goods)
                    .options(selectinload(Goods.purchases))
                    .options(joinedload(Goods.subcategory))
                )
                goods = await session.execute(goods)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return jsonable_encoder(goods.scalars().all())

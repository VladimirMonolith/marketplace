from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import async_session_maker
from app.logger import logger


class BaseDAO:
    """Класс для работы с объектами БД."""

    model = None

    @classmethod
    async def get_object(cls, **kwargs):
        """Возвращает объект модели."""
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__.columns).filter_by(**kwargs)
                result = await session.execute(query)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return result.mappings().one_or_none()

    @classmethod
    async def get_all_objects(cls, **kwargs):
        """Возвращает все объекты модели."""
        try:
            async with async_session_maker() as session:
                query = (select(cls.model.__table__.columns)
                         .filter_by(**kwargs)
                         .order_by(cls.model.id))
                result = await session.execute(query)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return result.mappings().all()

    @classmethod
    async def add_object(cls, **kwargs):
        """Добавляет объект в БД."""
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**kwargs)
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return 'Данные успешно добавлены.'

    @classmethod
    async def add_objects(cls, *data):
        """Добавляет объекты в БД."""
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(*data).returning(cls.model.id)
                result = await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return result.mappings().first()

    @classmethod
    async def update_object(cls, update_data, **kwargs):
        """Позволяет обновлять данные объекта."""
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                result = result.scalar_one_or_none()
                new_data = update_data.dict(exclude_unset=True)

                for key, value in new_data.items():
                    setattr(result, key, value)
                session.add(result)
                await session.commit()
                await session.refresh(result)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return result

    @classmethod
    async def delete_object(cls, **kwargs):
        """Удаляет объект из БД."""
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                result = result.scalar_one_or_none()
                await session.delete(result)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return 'Удаление успешно завершено.'

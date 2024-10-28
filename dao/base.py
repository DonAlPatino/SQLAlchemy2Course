from typing import List, Any, Dict

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None  # Устанавливается в дочернем классе

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        # Добавить одну запись
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[Dict[str, Any]]):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    @classmethod
    async def get_user_info(cls, session: AsyncSession, user_id: int):
        query = select(cls.model).filter_by(id=user_id)
        # query = select(cls.model).filter(cls.model.id == user_id)
        print(query)  # Выводим запрос для отладки
        result = await session.execute(query)
        user_info = result.scalar_one_or_none()
        return user_info

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

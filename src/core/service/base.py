from typing import Generic, TypeVar, Type
from abc import ABC, abstractmethod
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from traceback import print_exception
from sqlalchemy.future import select
from sqlalchemy import func
from src.conf.loging import log
from uuid import UUID

T = TypeVar('T')


class BaseService(ABC, Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session: AsyncSession = session
        self.model: Type[T] = model

    async def __handle_in_session(self, call_next, refresh: bool = False, *args, **kwargs ):
        try:
            result = await call_next(*args, **kwargs)
            await self.session.commit()
            if refresh:
                await self.session.refresh(result)
            return result
        except SQLAlchemyError as e:
            log.error(print_exception(e))
            raise HTTPException(
                detail="Something went wrong",
                status_code=500
            )

    async def _exec(self, call_next, fetch_one: bool = False, refresh: bool = False, *args, **kwargs):
        result = await self.__handle_in_session(call_next, refresh, *args, **kwargs)
        if refresh:
            return result
        if fetch_one:
            return result.scalars().first()
        return result.scalars().all()

    @abstractmethod
    async def before_add(self, instance: Type[T] = None, *args, **kwargs):
        pass

    async def add(self, *args, **kwargs):
        async def _add(*in_args, **in_kwargs):
            instance = self.model(**in_kwargs)
            await self.before_add(instance, *in_args, **in_kwargs)
            self.session.add(instance)
            return instance

        return await self._exec(_add, fetch_one=False, refresh=True, *args, **kwargs)

    async def get_all(self, offset: int = 0, limit: int = 10):
        async def _get_all(in_offset, in_limit):
            query = select(self.model).offset(offset=in_offset).limit(limit=in_limit)
            return await self.session.execute(query)

        return await self._exec(_get_all, in_offset=offset, in_limit=limit, refresh=False, fetch_one=False)

    async def get_count(self):
        async def _get_count():
            query = select(func.count()).select_from(self.model)
            return await self.session.execute(query)

        return await self._exec(_get_count, refresh=False, fetch_one=False)

    async def get_by_id(self, id: UUID):
        async def _get_by_id(in_id: UUID):
            query = select(self.model).where(self.model.id == in_id)
            return await self.session.execute(query)

        return await self._exec(_get_by_id, refresh=False, fetch_one=True, in_id=id)

from fastapi import (
    Depends,
    HTTPException,
    status
)
from src.conf.loging import log
from src.core.service.base import BaseService
from src.db.engine import get_async_session
from src.db.model.chat.chat import Chat

from sqlalchemy.future import select
from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Chat)

    async def check_if_exists(self, user1_id: UUID, user2_id: UUID):
        async def _check_if_exists(in_user1_id: UUID, in_user2_id: UUID):
            query = select(self.model).where(
                or_(
                    and_(
                        self.model.user1_id == in_user1_id,
                        self.model.user2_id == in_user2_id
                    ),
                    and_(
                        self.model.user1_id == in_user2_id,
                        self.model.user2_id == in_user1_id
                    )
                )
            )
            return await self.session.execute(query)

        result = await self._exec(_check_if_exists, in_user1_id=user1_id, in_user2_id=user2_id, fetch_one=True)
        if result:
            raise HTTPException(
                status_code=status.HTTP_308_PERMANENT_REDIRECT,
                detail={
                    "detail": "Chat already exists",
                    "chat_id": "{}".format(result.id)
                    }
            )
        return True

    async def before_add(self, instance=None, *args, **kwargs):
        proceed: bool = await self.check_if_exists(user1_id=kwargs.get("user1_id"), user2_id=kwargs.get('user2_id'))
        if proceed:
            return 1

def get_chat_service(session=Depends(get_async_session)) -> ChatService:
    return ChatService(session)
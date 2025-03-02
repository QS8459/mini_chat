from fastapi import Depends

from src.core.service.base import BaseService
from src.db.engine import get_async_session
from src.db.model.chat.chat import Chat

from sqlalchemy.ext.asyncio import AsyncSession


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Chat)

    async def before_add(self, instance=None, *args, **kwargs ):
        pass


def get_chat_service(session=Depends(get_async_session)) -> ChatService:
    return ChatService(session)
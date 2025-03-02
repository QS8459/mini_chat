from fastapi import Depends
from src.core.service.base import BaseService
from src.db.model.message.message import Messages
from src.db.engine import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Messages)

    async def before_add(self, instance=None, *args, **kwargs):
        pass


def get_message_service(session: AsyncSession = Depends(get_async_session)) -> MessageService:
    return MessageService(session)


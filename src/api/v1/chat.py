from fastapi import APIRouter, Depends, status
from src.core.service.chat.chat import (
    ChatService,
    get_chat_service
)
from src.core.service.auth.auth import get_current_user
from src.core.schema.chat import ChatAddSchema

chat_api: APIRouter = APIRouter(prefix='/chat', tags=['chat'])


@chat_api.post('/', status_code=status.HTTP_201_CREATED)
async def add_new_chat(
        schema: ChatAddSchema,
        service: ChatService = Depends(get_chat_service),
        current_user=Depends(get_current_user)
):
    return await service.add(**schema.dict())

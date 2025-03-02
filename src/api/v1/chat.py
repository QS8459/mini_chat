from fastapi import APIRouter, Depends, status
from src.core.service.chat.chat import (
    ChatService,
    get_chat_service
)
from src.core.service.auth.auth import get_current_user
from src.core.schema.responses import GlobalResponseSchema
from src.core.schema.chat import (
    ChatAddSchema,
    ChatResponseSchema
)

chat_api: APIRouter = APIRouter(prefix='/chat', tags=['chat'])


@chat_api.post('/', status_code=status.HTTP_201_CREATED, response_model=ChatResponseSchema)
async def add_new_chat(
        schema: ChatAddSchema,
        service: ChatService = Depends(get_chat_service),
        current_user=Depends(get_current_user)
):

    return await service.add(
        **schema.dict(),
        user1_id = current_user.id,
        created_by=current_user.id
    )


@chat_api.get('/list/', status_code=status.HTTP_200_OK, response_model=GlobalResponseSchema)
async def chat_list(
        service: ChatService = Depends(get_chat_service),
        current_user=Depends(get_current_user)
):
    count = await service.get_count()
    result = await service.get_all()
    return GlobalResponseSchema[ChatResponseSchema](
        count=count[0],
        result=result
    )

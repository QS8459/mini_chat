from fastapi import (
    APIRouter,
    Depends,
    status
)
from src.core.service.message.message import (
    get_message_service,
    MessageService
)
from src.core.service.auth.auth import get_current_user
from src.core.schema.message import (
    MessageAddSchema,
    MessageResponseSchema
)
from src.core.schema.responses import GlobalResponseSchema

message_api: APIRouter = APIRouter(prefix='/message', tags=['message'])


@message_api.post(
    '/send/',
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponseSchema
)
async def send_message(
    schema: MessageAddSchema,
    service: MessageService = Depends(get_message_service),
    current_user=Depends(get_current_user)
):
    return await service.add(
        **schema.dict(),
        created_by=current_user.id
    )


@message_api.get(
    '/all/messages/',
    status_code=status.HTTP_200_OK,
    response_model=GlobalResponseSchema
)
async def messages_list(
        service: MessageService = Depends(get_message_service),
        current_user=Depends(get_current_user)
):
    count = await service.get_count()
    result = await service.get_all()
    return GlobalResponseSchema[MessageResponseSchema](
        count=count[0],
        result=result
    )
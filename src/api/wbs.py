from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Query,
    WebSocketException,
    status,
    Depends,
    HTTPException
)
from src.core.service.account.account import (
    get_account_service,
    AccountService
)
from src.core.service.message.message import (
    get_message_service,
    MessageService
)
from src.core.service.auth.auth import get_current_user
from src.core.wb_manager import manager
from src.conf.loging import log
from uuid import UUID


websocket_api: APIRouter = APIRouter(prefix='/ws', tags=['ws'])


@websocket_api.websocket('/{chat_id}/')
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id:UUID,
        acc_service: AccountService = Depends(get_account_service),
        msg_service: MessageService = Depends(get_message_service)

):
    await manager.connect(websocket)
    try:

        log.info("WebSocket connection established")
        token = websocket.headers.get('Authorization').split(' ')[1]
        user = await get_current_user(token=token, acc_service=acc_service)
        if user:

            data = await websocket.receive_text()
            await msg_service.add(
                created_by=user.id,
                msg=data,
                chat_id=chat_id
            )
            await manager.send_personal_message(f"You wrote {data}", websocket)
        else:
            raise WebSocketException(
                reason="Authentication Error",
                code=status.WS_1013_TRY_AGAIN_LATER
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_personal_message('Client Has Left', websocket)
    except HTTPException as e:
        await manager.send_personal_message("Client Has Left", websocket)

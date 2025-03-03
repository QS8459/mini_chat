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
from src.core.service.account.account import get_account_service
from src.core.service.auth.auth import get_current_user
from src.core.wb_manager import manager
from src.conf.loging import log


websocket_api: APIRouter = APIRouter(prefix='/ws', tags=['ws'])


@websocket_api.websocket('/')
async def websocket_endpoint(
        websocket: WebSocket,
        token: str = Query(...),
        acc_service=Depends(get_account_service)

):
    await manager.connect(websocket)
    try:

        log.info("WebSocket connection established")
        user = await get_current_user(token=token, acc_service=acc_service)
        log.info(user.id)
        if user:

            log.info(f"User id is {user.id}")

            log.info(websocket.headers)
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote nothing", websocket)
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

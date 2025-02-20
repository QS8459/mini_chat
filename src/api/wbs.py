from fastapi import WebSocket, APIRouter
from src.conf.conf import log

ws: APIRouter = APIRouter(prefix='/webs')


@ws.websocket('/ws/with_client')
async def message(websocket: WebSocket):
    log.info("Connection is set")
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        log.info(data)
        await websocket.send_json(data)

# from fastapi import WebSocket, FastAPI
# from fastapi.responses import HTMLResponse
# from src.api.wbs import ws
# from src.api import api
#
# app = FastAPI()
#
# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var ws = new WebSocket("ws://127.0.0.1:8090/webs/ws/with_client");
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(JSON.parse(event.data).message + "my custom message")
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(JSON.stringify({message:input.value}))
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """
#
# # app.include_router(ws)
#
# @app.get("/")
# async def home():
#     return HTMLResponse(html)
#
# app.include_router(api)


# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from src.middleware.loging import logger
from src.api import api


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        from src.conf.db_connection import engine
        yield
        await engine.dispose()
    except Exception as e:
        raise e


app = FastAPI(
    lifespane=lifespan,
    title="Mini Chat",
    version="0.0.1",
    description="Mini chat",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify a list of allowed origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware('http')(logger)
app.include_router(api)


# WebSocket manager to handle connected clients
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#
#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#
#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)
#
#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)
#
#
# manager = ConnectionManager()


# @app.websocket("/ws/chat/{chat_id}")
# async def websocket_endpoint(websocket: WebSocket, chat_id: int, db: Session = Depends(get_db)):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Process the received message (parse JSON, extract fields, etc.)
#             message_data = json.loads(data)
#             msg_text = message_data.get("msg")
#             owner_id = message_data.get("owner_id")
#
#             # Create a new message and save it to the database
#             db_message = models.Messages(
#                 chat_id=chat_id,
#                 msg=msg_text,
#                 owner_id=owner_id
#             )
#             db.add(db_message)
#             db.commit()
#             db.refresh(db_message)
#
#             # Broadcast the message to all connected clients
#             await manager.broadcast(f"Chat {chat_id}: {msg_text}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Chat {chat_id}: Client disconnected")

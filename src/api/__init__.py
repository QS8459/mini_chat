from fastapi import APIRouter
from src.api.account import router as api_router
from src.api.chat import router as chat_router
from src.api.message import router as message_router

api: APIRouter = APIRouter(prefix='/api')

api.include_router(api_router)
api.include_router(chat_router)
api.include_router(message_router)


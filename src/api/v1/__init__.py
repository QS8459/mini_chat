from src.api.v1.message import message_api
from src.api.v1.account import account_api
from src.api.v1.chat import chat_api
from fastapi import APIRouter

v1: APIRouter = APIRouter(prefix="/v1")

v1.include_router(account_api)
v1.include_router(chat_api)
v1.include_router(message_api)
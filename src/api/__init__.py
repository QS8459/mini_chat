from fastapi import APIRouter
from src.api.v1 import v1
from src.api.wbs import websocket_api

api: APIRouter = APIRouter(prefix='/api')

api.include_router(v1)
api.include_router(websocket_api)

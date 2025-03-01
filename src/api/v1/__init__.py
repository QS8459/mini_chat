from src.api.v1.account import account_api
from fastapi import APIRouter

v1: APIRouter = APIRouter(prefix="/v1")

v1.include_router(account_api)
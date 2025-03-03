from fastapi import FastAPI
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

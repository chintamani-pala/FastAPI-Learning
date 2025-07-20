from fastapi import FastAPI
from sqlmodel import SQLModel
from db.database import engine
from auth.routes import router as auth_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
# app = FastAPI()

app.include_router(auth_router)

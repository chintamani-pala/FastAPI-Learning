# type: ignore
from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_sapn(app: FastAPI):
    print("server is starting...")
    await init_db()
    yield
    print("server has been stopped")


version = "v1"
app = FastAPI(
    title="Bookly",
    description="A Rest API for a book review web service",
    version=version,
    lifespan=life_sapn,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])

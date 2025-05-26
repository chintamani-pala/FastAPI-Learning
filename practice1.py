# type: ignore
from fastapi import FastAPI, Header
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/greet/{name}")  # path parameter
async def greet_path_name(name: str) -> dict:
    return {"message": f"Hello {name}"}


@app.get("/greet")
async def greet_query_name(name: str) -> dict:  # query parameter
    return {"message": f"Hello {name}"}


@app.get("/greet/age/{name}")  # both query and path parameter
async def greet_path_query_name(name: str, age: int):
    return {"message": f"Hello {name}", "age": age}


# optional query parameters
@app.get("/greet/optional/query")
async def greet(name: str = "User", age: int = 0):
    return {"message": f"Hello {name}", "age": age}


# Request body validation


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {"title": book_data.title, "author": book_data.author}


# Request header
@app.get("/get_headers", status_code=200)
async def get_headers(
    accept: str = Header(None),
    user_agent: str = Header(None),
    content_type: str = Header(None),
    host: str = Header(None),
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["User-Agent"] = user_agent
    request_headers["Content-Type"] = content_type
    request_headers["Host"] = host
    return request_headers

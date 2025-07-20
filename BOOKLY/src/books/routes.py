# type: ignore
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException

# from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.main import get_session
from .service import BookService

book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
):
    new_book = await book_service.create_book(book_data, session)

    return new_book


@book_router.get("/{book_uid}", response_model=Book)
async def get_book_by_id(
    book_uid: str, session: AsyncSession = Depends(get_session)
) -> dict:
    book = await book_service.get_book_by_uid(book_uid, session)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if update_book:
        return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_uid}", status_code=status.HTTP_200_OK)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    # print(book_to_delete)
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book_to_delete

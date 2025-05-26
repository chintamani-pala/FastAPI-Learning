from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book
# from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book_by_uid(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        if book is None:
            return None
        return book

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book_by_uid(book_uid, session)

        if book_to_update is None:  # type: ignore
            return None
        updated_data_dict = update_data.model_dump()

        for k, v in updated_data_dict.items():
            setattr(book_to_update, k, v)

        await session.commit()

        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book_by_uid(book_uid, session)
        print(book_to_delete)
        if book_to_delete is None:  # type: ignore
            return None
        await session.delete(book_to_delete)
        await session.commit()
        return book_to_delete

from bd.base import async_session
from fastapi import HTTPException
from bd.models import Reader
from bd.models import Books
from sqlalchemy.orm import joinedload
from sqlalchemy import update, select


class AsyncRequests:
    @staticmethod
    async def add_book(user_id: int, book_id: int) -> dict:
        async with async_session() as session:

            stmt = select(Books).where(Books.id == book_id)
            result = await session.execute(stmt)
            book = result.scalar_one_or_none()
            if not book:
                raise HTTPException(status_code=400, detail="Book not found")
            if book.in_store <= 0:
                raise HTTPException(status_code=400, detail="No books available in store")

            stmt = select(Reader).where(Reader.id == user_id).options(joinedload(Reader.books))
            result = await session.execute(stmt)
            reader = result.scalar_one_or_none()
            if not reader:
                raise HTTPException(status_code=400, detail="Reader not found")
            
            if len(reader.books) >= 5:
                raise HTTPException(status_code=400, detail="Too many books assigned to this reader")
                
            book.in_store -= 1
            reader.books.append(book)
            await session.commit()
            return {
                'id': reader.id,
                'username': reader.username,
                'books': [{'id': b.id, 'title': b.title} for b in reader.books],  # Преобразуем книги в словари
                'is_admin': reader.is_admin,
            }
        

    @staticmethod
    async def return_book(user_id: int, book_id: int) -> dict:
        async with async_session() as session:

            stmt = select(Books).where(Books.id == book_id)
            result = await session.execute(stmt)
            book = result.scalar_one_or_none()
            if not book:
                raise HTTPException(status_code=400, detail="Book not found")

            stmt = select(Reader).where(Reader.id == user_id).options(joinedload(Reader.books))
            result = await session.execute(stmt)
            reader = result.scalar_one_or_none()
            if not reader:
                raise HTTPException(status_code=400, detail="Reader not found")

            if book not in reader.books:
                raise HTTPException(status_code=400, detail="Book is not assigned to this reader")
            reader.books.remove(book)
            book.in_store += 1

            await session.commit()
            return {
                'id': reader.id,
                'username': reader.username,
                'books': [b.id for b in reader.books],
                'is_admin': reader.is_admin
            }

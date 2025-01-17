from bd.base import async_session
from fastapi import HTTPException
from bd.reader_models import Reader
from sqlalchemy import update, select


class AsyncRequests:
    @staticmethod
    async def add_book(user_id: int, book_id: int):
        async with async_session() as session:
            stmt = select(Reader).where(Reader.id == user_id)
            reader = await session.execute(stmt)
            if not reader:
                raise HTTPException(status_code = 400, detail = 'reader was not found')

            reader = reader.scalars().all() 
            if len(reader.books) > 5:
                raise HTTPException(status_code=400, detail = "too many books have been prescribed")
                
            reader['books'].append(book_id)
            
            await session.commit()

            return {
                'id': reader.id,
                'username': reader.username,
                'books': reader.books,
                'is_admin': reader.is_admin
            }
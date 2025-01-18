from bd.base import async_session
from fastapi import HTTPException
from bd.models import Reader
from bd.models import Books
from sqlalchemy.orm import joinedload, selectinload, aliased
from sqlalchemy import update, select, insert, delete
import datetime
from bd.models import book_to_reader


class AsyncRequests:
    @staticmethod
    async def add_book(user_id: int, book_id: int, expected_return: datetime.date = None):
        async with async_session() as session:

            # stmt = select(Reader).where(Reader.id == user_id).options(joinedload(Reader.books))
            stmt = select(Books).where(Books.id == book_id)
            try:
                book_obj = await session.execute(stmt)
                book_obj = book_obj.scalar()
            except:
                raise HTTPException(status_code=400, detail = 'no such book')

            if not book_obj or not book_obj.in_store > 0:
                raise HTTPException(status_code = 400)
            else:
                book_obj.in_store -= 1

            stmt = insert(book_to_reader).values(
                reader_id = user_id,
                book_id = book_id,
                borrowed_book = datetime.date.today(),
                expected_return_date = expected_return
            )
            try:
                await session.execute(stmt)
            except:
                await session.rollback()
                raise HTTPException(status_code = 400, detail = 'incorrect values were passed')
            
            await session.commit()

            return 'success'


    @staticmethod
    async def return_book(user_id: int, book_id: int):
        async with async_session() as session:
            stmt = select(Books).where(Books.id == book_id)
            for_removal = await session.execute(stmt)
            for_removal = for_removal.scalar()

            stmt = (delete(book_to_reader)
                    .where(book_to_reader.c.reader_id == user_id,
                           book_to_reader.c.book_id == book_id)
                )
            
            try:
                removed = await session.execute(stmt)
                print(removed.rowcount)
                if not removed.rowcount > 0:
                    await session.rollback()
                    raise HTTPException(400, detail = 'nothing to remove')
            except:
                await session.rollback()
                raise HTTPException(status_code = 400, detail = 'something went wrong')

            for_removal.in_store += 1
            await session.commit()
            
            return 'removed successfully!'



            






# class AsyncRequests:
#     @staticmethod
#     async def add_book(user_id: int, book_id: int) -> dict:
#         async with async_session() as session:

#             stmt = select(Books).where(Books.id == book_id)
#             result = await session.execute(stmt)
#             book = result.scalar_one_or_none()
#             if not book:
#                 raise HTTPException(status_code=400, detail="Book not found")
#             if book.in_store <= 0:
#                 raise HTTPException(status_code=400, detail="No books available in store")

#             stmt = select(Reader).where(Reader.id == user_id).options(joinedload(Reader.books))
#             result = await session.execute(stmt)
#             reader = result.scalar_one_or_none()
#             if not reader:
#                 raise HTTPException(status_code=400, detail="Reader not found")
            
#             if len(reader.books) >= 5:
#                 raise HTTPException(status_code=400, detail="Too many books assigned to this reader")
                
#             book.in_store -= 1
#             reader.books.append(book)
#             await session.commit()
#             return {
#                 'id': reader.id,
#                 'username': reader.username,
#                 'books': [{'id': b.id, 'title': b.title} for b in reader.books],  # Преобразуем книги в словари
#                 'is_admin': reader.is_admin,
#             }
        

#     @staticmethod
#     async def return_book(user_id: int, book_id: int) -> dict:
#         async with async_session() as session:

#             stmt = select(Books).where(Books.id == book_id)
#             result = await session.execute(stmt)
#             book = result.scalar_one_or_none()
#             if not book:
#                 raise HTTPException(status_code=400, detail="Book not found")

#             stmt = select(Reader).where(Reader.id == user_id).options(joinedload(Reader.books))
#             result = await session.execute(stmt)
#             reader = result.scalar_one_or_none()
#             if not reader:
#                 raise HTTPException(status_code=400, detail="Reader not found")

#             if book not in reader.books:
#                 raise HTTPException(status_code=400, detail="Book is not assigned to this reader")
#             reader.books.remove(book)
#             book.in_store += 1

#             await session.commit()
#             return {
#                 'id': reader.id,
#                 'username': reader.username,
#                 'books': [b.id for b in reader.books],
#                 'is_admin': reader.is_admin
#             }



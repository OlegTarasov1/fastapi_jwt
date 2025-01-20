from bd.base import async_session
from fastapi import HTTPException
from bd.models import Reader
from bd.models import Books
from sqlalchemy import select, insert, delete
import datetime
from bd.models import book_to_reader


class AsyncRequests:
    @staticmethod
    async def add_book(user_id: int, book_id: int, expected_return: datetime.date = None):
        async with async_session() as session:

            stmt = (select(book_to_reader)
                .where(book_to_reader.c.reader_id == user_id)
            )
            try:
                reader_data = await session.execute(stmt)
                print(len(reader_data))
                if len(reader_data) > 5:
                    raise HTTPException(status_code = 400, detail = 'the user has too manu books prescribed')
            except:
                pass

            stmt = select(Books).where(Books.id == book_id)
            try:
                book_obj = await session.execute(stmt)
                book_obj = book_obj.scalar()
            except:
                raise HTTPException(status_code=400, detail = 'no such book')


            if not book_obj or not book_obj.in_store > 0:
                raise HTTPException(status_code = 400, detail= 'books are not in store')
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
                raise HTTPException(status_code = 400)
   
            await session.commit()

            stmt = (
                select(book_to_reader, Books, Reader)
                .join(Books, book_to_reader.c.book_id == Books.id)
                .join(Reader, book_to_reader.c.reader_id == Reader.id)
                .where(
                    book_to_reader.c.reader_id == user_id,
                    book_to_reader.c.book_id == book_id
                )
            )
            
            resp = await session.execute(stmt)
            resp = resp.mappings().all()
            del resp[0]['Reader'].password
            return resp


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
                raise HTTPException(status_code = 400, detail = 'there\'s nothing to remove')

            for_removal.in_store += 1
            await session.commit()

            stmt = (
                select(book_to_reader, Books, Reader)
                .join(Books, book_to_reader.c.book_id == Books.id)
                .join(Reader, book_to_reader.c.reader_id == Reader.id)
                .where(book_to_reader.c.reader_id == user_id)
            )
            
            resp = await session.execute(stmt)
            resp = resp.mappings().all()
            if resp:
                del resp[0]['Reader'].password
            return resp


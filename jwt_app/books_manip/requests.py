from sqlalchemy import select, delete, update, insert
from sqlalchemy.orm import selectinload, joinedload
from bd.models import Books, Authors, auth_books_table
from bd.base import async_session

class AsyncRequests:

    # overthink to shorten

    @staticmethod
    async def add_book(book: dict) -> dict | None:
        async with async_session() as session:
            stmt = select(Authors).where(Authors.id.in_(book['authors']))
            authors = await session.execute(stmt)
            authors = authors.scalars().all()
            book['authors'] = authors

            new_book = Books(**book)
            session.add(new_book)
            stmt = select(Books).where(
                Books.title == book['title'],
                Books.description == book['description'],
                Books.genres == book['genres'],
                Books.date == book['date'],
                Books.in_store == book['in_store']
            ).options(selectinload(Books.authors))
            
            obj = await session.execute(stmt)
            obj = obj.scalars().all()[-1]

            try:
                obj = {
                    'id': obj.id,
                    **book,
                    'authors': obj.authors
                }
                await session.commit()
                return obj
            except:
                pass

            await session.commit()
            return 'not all data has been passed'
    
    @staticmethod
    async def get_book(id: int) -> dict:
        async with async_session() as session:
            stmt = select(Books).where(Books.id == id).options(selectinload(Books.authors))
            answer = await session.execute(stmt)
            answer = answer.scalars().first()
            try:
                obj = {
                    'id': answer.id,
                    'title': answer.title,
                    'description': answer.description,
                    'date': answer.date,
                    'in_store': answer.in_store,
                    'authors': [
                            {
                                'id': i.id,
                                'name': i.name,
                                'bio': i.bio
                            } for i in answer.authors
                        ]
                }
                return obj
            except:
                return None

    
    @staticmethod
    async def delete_book(id: int) -> bool:
        async with async_session() as session:
            stmt = delete(Books).where(Books.id == id)
            res = await session.execute(stmt)
            await session.commit()
            if res.rowcount > 0:
                return True
            else:
                return False

    @staticmethod
    async def patch_book(id: int, book: dict):
        async with async_session() as session:
            if book['authors'] and book['authors'] != [0]:
                stmt = delete(auth_books_table).where(auth_books_table.c.book_id == id)
                await session.execute(stmt)
                auths = book.pop('authors')

                try:
                    stmt = insert(auth_books_table).values([{"book_id": id, 'author_id': i} for i in auths])
                    await session.execute(stmt)
                except:
                    await session.rollback()

            elif book['authors'] == [0]:
                stmt = delete(auth_books_table).where(auth_books_table.c.book_id == id)
                await session.execute(stmt)
                auths = book.pop('authors')

            stmt = update(Books).where(Books.id == id).values(**book)
            await session.execute(stmt)

            await session.commit()

            resp = select(Authors).where(Authors.id.in_(auths))
            resp = await session.execute(resp)
            resp = resp.scalars().all()
            try:
                resp = {
                    'id': id,
                    **book,
                    'authors': resp
                }
                return resp
            except:
                return None

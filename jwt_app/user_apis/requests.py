from bd.base import async_session
from fastapi import HTTPException
from bd.models import Reader, book_to_reader, Books
from sqlalchemy import select, delete, update, asc, func, label
import bcrypt


class AsyncRequests:
    
    @staticmethod
    async def add_user(user):
        async with async_session() as session:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user['password'].encode(), salt)
            new_reader = Reader(username = user['username'], password = hashed_password, is_admin = False)
            session.add(new_reader)
            await session.commit()
            
            stmt = select(Reader).where(Reader.username == user['username'])
            resp = await session.execute(stmt)
            resp = resp.scalars().all()[-1]
            obj = {
                'id': resp.id,
                'username': resp.username,
                'is_admin': resp.is_admin
            }
            return obj


    @staticmethod
    async def get_user_data(id: int):
        async with async_session() as session:
            stmt = (
                select(
                    book_to_reader,
                    Books,
                    Reader.id,
                    Reader.username,
                    Reader.is_admin                    
                )
                .join(Reader, book_to_reader.c.reader_id == Reader.id)
                .join(Books, book_to_reader.c.book_id == Books.id)
                .where(
                    book_to_reader.c.reader_id == id
                )
            )
        
            try:
                run = await session.execute(stmt)
            except:
                raise HTTPException(status_code=400, detail = 'no such user')
                
            run = run.mappings().all()
            return run
        

    @staticmethod
    async def del_user(id: int) -> bool:
        async with async_session() as session:
            stmt = delete(Reader).where(Reader.id == id)
            reader_deleted = await session.execute(stmt)
            await session.commit()
            if reader_deleted.rowcount > 0:
                return True
            else:
                return False
            

    @staticmethod
    async def is_allowed(user) -> bool:
        async with async_session() as session:
            stmt = select(Reader).where(Reader.username == user.username)
            to_auth = await session.execute(stmt) 
            to_auth = to_auth.scalars().first()
            if to_auth:
                if bcrypt.checkpw(user.password.encode(), to_auth.password):
                    return to_auth
                else:
                    return False
            else:
                return False
            
    
    @staticmethod
    async def patch_user(id: int, new_user: dict):
        async with async_session() as session:
            stmt = update(Reader).where(Reader.id == id).values(**new_user)
            await session.execute(stmt)
            await session.commit()
            return {
                'id': id,
                **new_user,
                'is_admin': False
            }
        

    @staticmethod
    async def get_list(limit: int, offset: int):
        async with async_session() as session:
            
            stmt = (
                select(
                    Reader.id,
                    Reader.username,
                    Reader.is_admin,
                    func.count(book_to_reader.c.reader_id)
                        .label('books_prescribed')
                )
                .join(
                    book_to_reader,
                    book_to_reader.c.reader_id == Reader.id,
                    isouter = True
                )
                .order_by(asc(Reader.id))
                .group_by(
                    Reader.id,
                    Reader.username,
                    Reader.is_admin
                )
                .limit(limit)
                .offset(offset * limit)
            )

            result = await session.execute(stmt)
            resp = result.mappings().all()

            return resp
        
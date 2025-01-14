from bd.base import async_session
from bd.reader_models import Reader
from sqlalchemy import select, delete
import bcrypt


class AsyncRequests:
    
    @staticmethod
    async def add_user(user):
        async with async_session() as session:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user.password.encode(), salt)
            new_reader = Reader(username = user.username, password = hashed_password, is_admin = False)
            session.add(new_reader)
            await session.commit()


    @staticmethod
    async def get_user_data(id: int) -> object:
        async with async_session() as session:
            stmt = select(Reader).where(Reader.id == id)
            run = await session.execute(stmt)
            return run.scalars().first()
        
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
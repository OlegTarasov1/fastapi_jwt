from bd.base import async_session
from bd.reader_models import Reader
from sqlalchemy import select, delete, update
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
            
    
    @staticmethod
    async def patch_user(id: int, new_user: dict):
        async with async_session() as session:
            stmt = update(Reader).where(Reader.id == id).values(**new_user)
            await session.execute(stmt)
            await session.commit()
            return {
                'id': id,
                **new_user
            }
from bd.base import async_session
from bd.models import Books, Authors
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete, update


class AsyncRequests:

    @staticmethod
    async def add_author(author: object) -> None:
        async with async_session() as session:
            new_auth = Authors(**author)
            session.add(new_auth)
            stmt = select(Authors).where(Authors.name == author['name'], Authors.bio == author['bio'], Authors.birth_date == author['birth_date'])
            resp = await session.execute(stmt)
            try:
                resp = resp.scalars().all()[-1]
                obj = {
                    'id': resp.id,
                    'name': resp.name,
                    'bio': resp.bio
                }
            except:
                return None
            await session.commit()
            return obj

    @staticmethod
    async def get_author(id: int) -> dict | None:
        async with async_session() as session:
            stmt = select(Authors).where(Authors.id == id).options(selectinload(Authors.books))
            res = await session.execute(stmt)
            obj = res.scalars().first()
            
            try:
                resp = {
                    'id': obj.id,
                    'name': obj.name,
                    'bio': obj.bio,
                    'birth_date': obj.birth_date,
                    'books': obj.books
                }
            except:
                return None
            return resp
        
        
    @staticmethod
    async def del_author(id: int) -> bool:
        async with async_session() as session:
            stmt = delete(Authors).where(Authors.id == id)
            res = await session.execute(stmt)
            await session.commit()
            if res.rowcount > 0:
                return True
            else:
                return False
            
    @staticmethod
    async def patch_author(author: dict, id: int) -> bool:
        async with async_session() as session:
            stmt = update(Authors).where(Authors.id == id).values(**author)
            res = await session.execute(stmt)
            await session.commit()
            if res.rowcount > 0:
                return True
            else:
                return False
           


from fastapi import APIRouter, HTTPException
from authors_manip.requests import AsyncRequests
from pydantic import BaseModel
from datetime import date

authors_router = APIRouter()


class AuthorToAdd(BaseModel):
    name: str
    bio: str
    birth_date: date | None


@authors_router.post('/api/v1/add_author/', tags = ['auhtors'])
async def add_auhtor(author: AuthorToAdd):
    res = await AsyncRequests.add_author(author.dict(exclude_none = True))
    if res:
        return res
    else:
        raise HTTPException(status_code=400)


@authors_router.get('/api/v1/get_author/{id}/', tags = ['auhtors'])
async def get_author(id: int):
    author = await AsyncRequests.get_author(id)
    if author:
        return author
    else:
        raise HTTPException(status_code=400)


@authors_router.delete('/api/v1/del_auhtor/{id}', tags=['auhtors'])
async def del_author(id: int):
    res = await AsyncRequests.del_author(id)
    if res:
        return 'Author has been deleted successfully!'
    else:
        raise HTTPException(status_code = 400, detail = 'no author with such id was found')
    

class AuthorToPatch(BaseModel):
    name: str | None
    bio: str | None
    birth_date: date | None


@authors_router.patch('/api/v1/patch_author/{id}', tags = ['auhtors'])
async def update_author(author: AuthorToPatch, id: int):
    print('works')
    res = await AsyncRequests.patch_author(author.dict(exclude_none = True), id)
    print(res)
    if res:
        return 'data has been updated'
    else:
        raise HTTPException(status_code = 401)


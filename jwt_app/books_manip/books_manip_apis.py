from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .requests import AsyncRequests
from user_apis.jwt import decoding_jwt
import datetime

books_manip = APIRouter()

class BookToAdd(BaseModel):
    title: str
    description: str
    date: datetime.date
    genres: list[str]
    authors: list[int]
    in_store: int


@books_manip.post('/api/v1/add_book/', tags = ['books'])
async def add_book(book: BookToAdd, token: dict = Depends(decoding_jwt)):
    resp = await AsyncRequests.add_book(book.dict())
    if type(resp) == dict:
        return resp
    else:
        raise HTTPException(status_code = 400, detail = resp)

@books_manip.get('/api/v1/get_book/{id}/', tags = ['books'])
async def get_book(id: int):
    book = await AsyncRequests.get_book(id)
    if book:
        return book
    else:
        raise HTTPException(status_code = 400)
    
@books_manip.delete('/api/v1/delete_book/{id}/', tags = ['books'])
async def delete_book(id: int, token: dict = Depends(decoding_jwt)):
    del_rows = await AsyncRequests.delete_book(id)
    if del_rows:
        return {
            "status": "success",
            "id": id
        }
    else:
        raise HTTPException(status_code=400)


class BookToPatch(BaseModel):
    title: str | None
    description: str | None
    date: datetime.date | None
    authors: list[int] | None
    in_store: int | None

@books_manip.patch('/api/v1/patch_book/{id}/', tags = ['books'])
async def patch_book(id: int, book: BookToPatch, token: dict = Depends(decoding_jwt)):
    resp = await AsyncRequests.patch_book(id, book.dict(exclude_none = True))
    if resp:
        return resp
    else:
        raise HTTPException(status_code = 400)


from fastapi import APIRouter, Depends, Query
from user_apis.jwt import is_creator_or_admin
import datetime
from user_book_manip.user_book_requests import AsyncRequests

user_book_router = APIRouter()

@user_book_router.post('/api/v1/assign_book/{id}/{book_id}/', tags = ['user_book'])
async def add_book_to_user(id: int, book_id: int, expected_return: datetime.date = Query(None)):
    resp = await AsyncRequests.add_book(id, book_id, expected_return) 
    return resp
# , token: dict = Depends(is_creator_or_admin)

@user_book_router.delete('/api/v1/return_book/{id}/{book_id}/', tags = ['user_book'])
async def return_book(id: int, book_id: int):
    resp = await AsyncRequests.return_book(id, book_id)
    return resp

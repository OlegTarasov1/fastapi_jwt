from fastapi import APIRouter, Depends
from user_apis.jwt import is_creator_or_admin
from user_book_manip.user_book_requests import AsyncRequests

user_book_router = APIRouter()

@user_book_router.post('/api/v1/assign_book/{id}/{book_id}', tags = ['user_book'])
async def add_book_to_user(id: int, book_id: int, token: dict = Depends(is_creator_or_admin)):
    resp = await AsyncRequests.add_book(id, book_id) 
    return resp



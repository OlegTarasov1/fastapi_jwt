from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .requests import AsyncRequests

user_api_router = APIRouter()

class User(BaseModel):
    username: str
    password: str


@user_api_router.post('/api/v1/add_user', tags=['users'])
async def add_user(user: User):
    try:
        await AsyncRequests.add_user(user)
        return "user has been successfully registerd!"
    except:
        raise HTTPException(status_code=400)
    

@user_api_router.get('/api/v1/get_user/{id}', tags=['users'])
async def get_user(id: int):
    user_data = await AsyncRequests.get_user_data(id) 
    if user_data:
        return {'username': user_data.username, 'is_admin': user_data.is_admin}
    else:
        raise HTTPException(status_code = 400, detail = 'no such user was found')


@user_api_router.delete('/api/v1/del_user/{id}', tags=['users'])
async def del_user(id: int):
    is_deleted = await AsyncRequests.del_user(id)
    print(is_deleted)
    if is_deleted:
        return {'status': 'success'}
    else:
        raise HTTPException(status_code = 400)
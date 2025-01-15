from fastapi import APIRouter, HTTPException, Depends, Header
from user_apis.jwt import create_access_token, decoding_jwt, is_creator
from pydantic import BaseModel
from .requests import AsyncRequests
from dotenv import load_dotenv
import datetime
import os

user_api_router = APIRouter()

load_dotenv()


class User(BaseModel):
    username: str
    password: str


@user_api_router.post('/api/v1/add_user/', tags=['users'])
async def add_user(reader: User):
    try:
        resp = await AsyncRequests.add_user(reader.dict())
        return resp
    except:
        raise HTTPException(status_code=400)
    

@user_api_router.get('/api/v1/get_user/{id}/', tags=['users'])
async def get_user(id: int):
    user_data = await AsyncRequests.get_user_data(id) 
    if user_data:
        return {'id': id, 'username': user_data.username, 'is_admin': user_data.is_admin}
    else:
        raise HTTPException(status_code = 400, detail = 'no such user was found')


@user_api_router.delete('/api/v1/del_user/{id}/', tags=['users'])
async def del_user(id: int, token: dict = Depends(is_creator)):
    is_deleted = await AsyncRequests.del_user(id)
    print(is_deleted)
    if is_deleted:
        return {'status': 'success'}
    else:
        raise HTTPException(status_code = 400)
    

@user_api_router.post('/api/v1/login/', tags = ['users'])
async def login(user: User):
    resp = await AsyncRequests.is_allowed(user)
    if resp:
        token = await create_access_token(resp.username, resp.is_admin, resp.id, datetime.timedelta(minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))))
        return {'access_token': token, 'type': 'bearer'}
    else:
        raise HTTPException(status_code=401, detail = 'incorrect data')


class UserPatch(BaseModel):
    username: str

@user_api_router.patch('/api/v1/patch_user/{id}/', tags = ['users'])
async def patch_user(id: int, new_user: UserPatch, token: dict = Depends(is_creator)):
    # try:
    obj = await AsyncRequests.patch_user(id, new_user.dict())
    return obj
    # except:
    #     raise HTTPException(status_code=400)
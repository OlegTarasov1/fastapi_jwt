from fastapi import APIRouter, HTTPException, Depends, status, Query
from user_apis.jwt import create_access_token, is_creator_or_admin, is_admin
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


@user_api_router.post('/api/v1/add_user/', tags=['users'], status_code=status.HTTP_201_CREATED)
async def add_user(reader: User):
    try:
        resp = await AsyncRequests.add_user(reader.dict())
        return resp
    except:
        raise HTTPException(status_code=422)
    

@user_api_router.get('/api/v1/get_user/{id}/', tags=['users'])
async def get_user(id: int):
    user_data = await AsyncRequests.get_user_data(id) 
    return user_data


@user_api_router.delete('/api/v1/del_user/{id}/', tags=['users'])
async def del_user(id: int, token: dict = Depends(is_creator_or_admin)):
    is_deleted = await AsyncRequests.del_user(id)
    print(is_deleted)
    if is_deleted:
        return {'status': 'success'}
    else:
        raise HTTPException(status_code = 403)
    

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
async def patch_user(id: int, new_user: UserPatch, token: dict = Depends(is_creator_or_admin)):
    try:
        obj = await AsyncRequests.patch_user(id, new_user.dict())
        return obj
    except:
        raise HTTPException(status_code=403)
    

@user_api_router.get('/api/v1/list_readers/', tags = ['users'])
async def list_readers(limit: int = Query(10), offset: int = Query(0), token: int = Depends(is_admin)):
    resp = await AsyncRequests.get_list(limit, offset)
    return resp

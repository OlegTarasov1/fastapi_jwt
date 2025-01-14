from jose import jwt, JWTError
import datetime
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Header

load_dotenv()

async def create_access_token(username: str, is_admin: bool, id: int, expire_delta: datetime.timedelta):
    encode = {'username': username, 'id': id, 'role': is_admin}
    expires = datetime.datetime.utcnow() + expire_delta
    encode.update({'exp': expires})
    return jwt.encode(
        encode,
        os.getenv('SECRET_KEY'),
        os.getenv('ALGORITHM')
    )


async def decoding_jwt(token):
    try:
        payload = jwt.decode(
            token,
            os.getenv('SECRET_KEY'),
            os.getenv('ALGORITHM')
        )
        username: str = payload.get('username')
        user_role: bool = payload.get('role')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail='invalid user')
        return {'username': username, 'id': user_id, 'role': user_role}
        
    except JWTError:
        raise HTTPException(status_code=401, detail = 'invalid user')


async def get_token(authorization: str = Header(...)):
    print(authorization)
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization format")
    return authorization[6:] 
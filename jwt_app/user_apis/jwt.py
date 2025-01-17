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


# checks weather the jwt token is valid
async def decoding_jwt(token: str = Header('authorization')):
    try:
        payload = jwt.decode(
            token[7:],
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



async def is_creator_or_admin(id: int, token: str = Header('authorization')):
    token_dict = await decoding_jwt(token)
    if id == token_dict.get('id') or token_dict.get('role'):
        return token_dict
    else:
        raise HTTPException(status_code=401)


async def is_admin(token: str = Header('authorization')):
    token_dict = await decoding_jwt(token)
    if token_dict['role']:
        return 1
    else:
        raise HTTPException(status_code=403)
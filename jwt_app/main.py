from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
from dotenv import load_dotenv
from user_apis.apis import user_api_router
from authors_manip.authors_manip_apis import authors_router
from books_manip.books_manip_apis import books_manip
import uvicorn
import os

app = FastAPI()

load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

app.include_router(user_api_router)
app.include_router(authors_router)
app.include_router(books_manip)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
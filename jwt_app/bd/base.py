from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(url = os.getenv('POSTGRES_URL'))
async_session = async_sessionmaker(engine)

metadata_obj = MetaData()


class Base(DeclarativeBase):
    pass

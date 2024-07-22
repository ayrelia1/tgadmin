# database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

#DATABASE_URL = f"postgresql+asyncpg://{os.environ.get('DB_LOG')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"

DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ.get('DB_LOG')}:"
    f"{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}:"
    f"{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
)

#DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(engine)



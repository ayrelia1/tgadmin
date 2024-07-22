from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, DeclarativeBase
from db.db import engine
from sqlalchemy.ext.asyncio import AsyncAttrs




class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users_site'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users_site.id'))
    session_token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)

    user = relationship("User", back_populates="sessions")
    

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
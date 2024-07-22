from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from db.models import User, Session
from schemas import UserCreate, UserInDB
import secrets
from sqlalchemy import delete
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_user(db_session: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password, full_name=user.full_name)
    db_session.add(new_user)
    await db_session.commit()
    return new_user

async def get_user_by_username(db_session: AsyncSession, username: str) -> UserInDB:
    result = await db_session.execute(select(User).filter_by(username=username))
    user = result.scalars().first()
    return user

async def create_session(db_session: AsyncSession, user_id: int, expiration_time: int) -> Session:
    session_token = secrets.token_urlsafe(16)
    expires_at = datetime.utcnow() + timedelta(seconds=expiration_time)
    session = Session(user_id=user_id, session_token=session_token, expires_at=expires_at)
    db_session.add(session)
    await db_session.commit()
    await db_session.refresh(session)
    return session

async def get_session_by_token(db_session: AsyncSession, session_token: str) -> Session:
    result = await db_session.execute(
        select(Session).options(joinedload(Session.user)).filter_by(session_token=session_token)
    )
    
    session = result.scalars().first()
    if session and session.expires_at < datetime.utcnow():
        await db_session.delete(session)
        await db_session.commit()
        return None
    return session

async def delete_session(db_session: AsyncSession, session_token: str):
    result = await db_session.execute(select(Session).filter_by(session_token=session_token))
    session_to_delete = result.scalars().first()
    if session_to_delete:
        await db_session.execute(delete(Session).where(Session.id == session_to_delete.id))
        await db_session.commit()
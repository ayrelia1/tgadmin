from typing import Optional
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from db.models import User, Session
from exc import UpdateQuestionException
from schemas import UserCreate, UserInDB
import secrets
from sqlalchemy import delete
from passlib.context import CryptContext
from models import CreateUpdateOtdel
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from bot.db.models import Otdels, Questions



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

async def delete_session(db_session: AsyncSession, session_token: str) -> None:
    result = await db_session.execute(select(Session).filter_by(session_token=session_token))
    session_to_delete = result.scalars().first()
    if session_to_delete:
        await db_session.execute(delete(Session).where(Session.id == session_to_delete.id))
        await db_session.commit()
        
        
async def create_otdel(db_session: AsyncSession, otdel: CreateUpdateOtdel) -> Otdels:
    new_otdel = Otdels(name=otdel.name)
    db_session.add(new_otdel)
    await db_session.commit()
    return new_otdel

async def delete_otdel(db_session: AsyncSession, otdel_id: int):
    async with db_session.begin():  # Начало транзакции
        try:
            query = select(Otdels).where(Otdels.id == otdel_id)
            result = await db_session.execute(query)
            otdel = result.scalar_one_or_none()
            
            if not otdel:
                return JSONResponse(
                    content={"status": "error", "message": "Otdel not found"},
                    status_code=404
                )

            await db_session.delete(otdel)  # Удаление объекта
            # Не требуется явного commit, так как begin автоматически обрабатывает commit или rollback
        except Exception as e:
            await db_session.rollback()
            return JSONResponse(
                content={"status": "error", "message": f"Database error: {str(e)}"},
                status_code=500
            )

    return JSONResponse(
        content={"status": "success", "otdel_id": otdel_id},
        status_code=200
    )
    
    
async def update_otdel(db_session: AsyncSession, otdel_id: int, otdel: CreateUpdateOtdel) -> None:
    # Создаем запрос для получения объекта отдела по ID
    query = select(Otdels).filter(Otdels.id == otdel_id)
    
    try:
        # Выполняем запрос для поиска отдела
        result = await db_session.execute(query)
        existing_otdel = result.scalars().one()
        
        # Обновляем атрибуты отдела
        existing_otdel.name = otdel.name

        # Фиксируем изменения
        await db_session.commit()
    
        return JSONResponse(
            content={"status": "success", "otdel_id": otdel_id},
            status_code=200
        )
    
    except Exception as ex:
        # В случае других ошибок откатываем изменения
        await db_session.rollback()
        return JSONResponse(
                content={"status": "error", "message": f"Database error: {str(ex)}"},
                status_code=500
            )
        
        
        
        
async def create_question(
    db_session: AsyncSession,
    title: str,
    text: Optional[str],
    file_data: Optional[str],
    otdel_id: int,
):
    new_question = Questions(
        name=title,
        answer=text,
        file=file_data,
        otdel_id=otdel_id,
    )
    
    db_session.add(new_question)
    await db_session.commit()
    return new_question



async def update_question(
    db_session: AsyncSession,
    question_id: int,
    title: Optional[str] = None,
    text: Optional[str] = None,
    file_data: Optional[str] = None,
):
    try:
        # Получаем существующий вопрос по его ID
        result = await db_session.execute(select(Questions).where(Questions.id == question_id))
        question = result.scalar_one()

        # Обновляем поля, даже если они None
        question.name = title
        question.answer = text
        question.file = file_data

        # Сохраняем изменения в базе данных
        await db_session.commit()
        return question

    except Exception as ex:
        # Если вопрос с данным ID не найден, можно вернуть None или выбросить исключение
        raise UpdateQuestionException(f'ERROR - {ex}')


async def delete_question(db_session: AsyncSession, question_id: int):
    async with db_session.begin():  # Начало транзакции
        try:
            query = select(Questions).where(Questions.id == question_id)
            result = await db_session.execute(query)
            question = result.scalar_one_or_none()
            
            if not question:
                return JSONResponse(
                    content={"status": "error", "message": "Question not found"},
                    status_code=404
                )

            await db_session.delete(question)  # Удаление объекта
            # Не требуется явного commit, так как begin автоматически обрабатывает commit или rollback
        except Exception as e:
            await db_session.rollback()
            return JSONResponse(
                content={"status": "error", "message": f"Database error: {str(e)}"},
                status_code=500
            )

    return JSONResponse(
        content={"status": "success", "question_id": question_id},
        status_code=200
    )
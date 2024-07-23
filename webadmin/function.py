
from fastapi import FastAPI, HTTPException, Request, Cookie
from cryptography.fernet import Fernet
from sqlalchemy import select
from db.db import async_session
from db import crud
from db.models import User
from exc import NotAuthenticatedException, NewsletterException
import logging
import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from bot.db.models import UserTg
from bot.config import bot


key = os.getenv('SECRET_KEY_AUTH')
cipher_suite = Fernet(key)


def encrypt_token(token: str) -> str:
    return cipher_suite.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    return cipher_suite.decrypt(encrypted_token.encode()).decode()

async def get_current_user(request: Request, session_token: str = Cookie(None)):
    
    if not session_token:
        return None
    try:
        decrypted_token = decrypt_token(session_token)
    except Exception as ex:
        logging.error(ex)
        return None
    async with async_session() as db_session:
        session = await crud.get_session_by_token(db_session, decrypted_token)
        if not session:
            return None
        user = await db_session.get(User, session.user_id)
        return user

async def get_authenticated_user(request: Request, session_token: str = Cookie(None)) -> User:
    user = await get_current_user(request, session_token)
    if user is None:
        raise NotAuthenticatedException(status_code=401, detail="Not authenticated")
    return user



async def send_newsletter(message: str, db_session: AsyncSession) -> dict:
    try:
        # Создание запроса для получения всех пользователей
        query = select(UserTg)  # Запрос на выбор всех записей из UserTg
        
        # Выполнение запроса и получение всех пользователей
        result = await db_session.execute(query)
        users = result.scalars().all()  # Получаем все записи
        
        
        for user in users:
            try:
                await bot.send_message(chat_id=user.user_id, text=message)
                await asyncio.sleep(2.5)
            except Exception as ex:
                pass
    except Exception as ex:
        logging.error(ex)
        raise NewsletterException(status_code=502, detail=f"Ошибка, рассылка не была начата - {ex}")

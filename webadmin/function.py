
from fastapi import FastAPI, HTTPException, Request, Cookie
from cryptography.fernet import Fernet
from db.db import async_session
from db import crud
from db.models import User
from exc import NotAuthenticatedException
import logging
import os

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
        print(f'error - {ex}')
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

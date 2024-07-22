from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from db import crud
from db.db import async_session
from function import decrypt_token, get_authenticated_user
from config import templates
from db.models import User
from sqlalchemy.future import select
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from bot.db.models import UserTg

user_router = APIRouter()

@user_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user: User = Depends(get_authenticated_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@user_router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user: User = Depends(get_authenticated_user)):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_hour = datetime.now().hour
    if current_hour < 12:
        time_of_day = "morning"
    elif 12 <= current_hour < 18:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "time_of_day": time_of_day, "current_time": current_time})




@user_router.get("/users", response_class=HTMLResponse)
async def profile(request: Request, user: User = Depends(get_authenticated_user)):
    async with async_session() as db_session:
        # Создаем запрос для выборки всех пользователей
        stmt = select(UserTg)
        result = await db_session.execute(stmt)
        # Получаем все строки
        users = result.scalars().all()
        

    return templates.TemplateResponse("users.html", {"request": request, "user": user, "users": users})




@user_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request, session_token: str = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        decrypted_token = decrypt_token(session_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session token")

    async with async_session() as db_session:
        await crud.delete_session(db_session, decrypted_token)
    
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session_token")
    return response
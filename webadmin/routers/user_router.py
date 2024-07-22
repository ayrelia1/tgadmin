import math
from fastapi import APIRouter, Query, Request, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy import func
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
async def profile(
    request: Request, 
    user: User = Depends(get_authenticated_user), 
    page: int = Query(1, alias='page', ge=1)
):
    ITEMS_PER_PAGE = 12
    PAGINATION_BUTTONS = 10
    
    async with async_session() as db_session:
        # Подсчитываем общее количество пользователей
        total_users = await db_session.execute(select(func.count(UserTg.id)))
        total_users = total_users.scalar_one()
        total_pages = (total_users + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        # Вычисляем смещение и лимит
        offset = (page - 1) * ITEMS_PER_PAGE

        # Создаем запрос с сортировкой по id
        stmt = select(UserTg).order_by(UserTg.id).offset(offset).limit(ITEMS_PER_PAGE)
        result = await db_session.execute(stmt)
        users = result.scalars().all()

    # Определяем страницы для отображения пагинации
    start_page = max(1, page - PAGINATION_BUTTONS // 2)
    end_page = min(total_pages, start_page + PAGINATION_BUTTONS - 1)
    start_page = max(1, end_page - PAGINATION_BUTTONS + 1)

    return templates.TemplateResponse(
        "users.html", 
        {
            "request": request, 
            "user": user, 
            "users": users, 
            "current_page": page, 
            "total_pages": total_pages,
            "start_page": start_page,
            "end_page": end_page
        }
    )



@user_router.post("/update_status/{user_id}", response_class=HTMLResponse)
async def update_status(
    request: Request, 
    user_id: int,
    user: User = Depends(get_authenticated_user)
):
    async with async_session() as db_session:
        # Выполняем запрос для поиска пользователя по user_id
        result = await db_session.execute(select(UserTg).filter(UserTg.id == user_id))
        user_record = result.scalars().first()

        if not user_record:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Изменяем поле has_access
        if user_record.has_access == True:
            user_record.has_access = False
        else: 
            user_record.has_access = True
            
        # Сохраняем изменения
        db_session.add(user_record)
        await db_session.commit()
        return JSONResponse(content={"status": "success"})
        

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
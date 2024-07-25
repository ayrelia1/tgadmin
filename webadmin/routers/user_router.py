import math
from fastapi import APIRouter, Body, Form, Query, Request, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from db import crud
from db.db import async_session
from function import decrypt_token, get_authenticated_user, send_newsletter, get_user_with_access, send_msg
from config import templates
from db.models import User
from sqlalchemy.future import select
import asyncio
import logging
from models import NewsletterRequest


from bot.db.models import UserTg, Otdels, Questions


user_router = APIRouter()

@user_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user: User = Depends(get_authenticated_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@user_router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user: User = Depends(get_authenticated_user)):


    return templates.TemplateResponse("profile.html", {"request": request, "user": user})




@user_router.get("/users", response_class=HTMLResponse)
async def users(
    request: Request, 
    user: User = Depends(get_user_with_access), 
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
    user: User = Depends(get_user_with_access)
):
    logging.info(f"Received request to update status for user_id: {user_id}")
    async with async_session() as db_session:
        result = await db_session.execute(select(UserTg).filter(UserTg.id == user_id))
        user_record = result.scalars().first()

        if not user_record:
            raise HTTPException(status_code=404, detail="User not found")
        
        
        if user_record.has_access == True:
            user_record.has_access = False
        else:
            user_record.has_access = True
            await send_msg(user_id)
        
        db_session.add(user_record)
        await db_session.commit()
        
        logging.info(f"Successfully updated status for user_id: {user_id}")
        return JSONResponse(content={"status": "success"})
        
        
        

@user_router.post("/send-newsletter", response_class=JSONResponse)
async def newsletter(
    request: NewsletterRequest,  # Используем Pydantic модель
    user: User = Depends(get_user_with_access)
):
    async with async_session() as db_session:
        try:
            asyncio.create_task(send_newsletter(str(request.message), db_session))
        except Exception as ex:
            logging.error(ex)
            return JSONResponse(content={"status": f"error", "message": f"error - {ex}"}, status_code=501)
        
    return JSONResponse(content={"status": "success"}, status_code=200)
    
        
        

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
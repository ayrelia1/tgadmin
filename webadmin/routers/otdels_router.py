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
from models import CreateUpdateOtdel
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from bot.db.models import Otdels, Questions


otdels_router = APIRouter()



@otdels_router.get("/otdels", response_class=HTMLResponse)
async def users(
    request: Request, 
    user: User = Depends(get_authenticated_user), 
    page: int = Query(1, alias='page', ge=1)
):
    ITEMS_PER_PAGE = 9
    PAGINATION_BUTTONS = 10
    
    async with async_session() as db_session:
        # Подсчитываем общее количество пользователей
        total_users = await db_session.execute(select(func.count(Otdels.id)))
        total_users = total_users.scalar_one()
        total_pages = (total_users + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        # Вычисляем смещение и лимит
        offset = (page - 1) * ITEMS_PER_PAGE

        # Создаем запрос с сортировкой по id
        stmt = select(Otdels).order_by(Otdels.id).offset(offset).limit(ITEMS_PER_PAGE)
        result = await db_session.execute(stmt)
        otdels = result.scalars().all()
        
    # Определяем страницы для отображения пагинации
    start_page = max(1, page - PAGINATION_BUTTONS // 2)
    end_page = min(total_pages, start_page + PAGINATION_BUTTONS - 1)
    start_page = max(1, end_page - PAGINATION_BUTTONS + 1)

    return templates.TemplateResponse(
        "otdels.html", 
        {
            "request": request, 
            "user": user, 
            "otdels": otdels, 
            "current_page": page, 
            "total_pages": total_pages,
            "start_page": start_page,
            "end_page": end_page
        }
    )
    
    
@otdels_router.post("/create-otdel", response_class=JSONResponse)
async def create_otdel(
    request: CreateUpdateOtdel, 
    user: User = Depends(get_authenticated_user), 
):
    
    try:
        async with async_session() as db_session:
            new_otdel = await crud.create_otdel(db_session, request)
            await db_session.refresh(new_otdel)  # Обновить объект перед возвратом
    except Exception as ex:
        await db_session.rollback()
        logging.error(ex)
        return JSONResponse(content={"status": "error", "message": f"error - {ex}"}, status_code=501)
        
    return JSONResponse(content={"status": "success", "otdel": {"id": new_otdel.id, "name": new_otdel.name}}, status_code=200)
    
    
    
@otdels_router.delete("/delete-otdel/{otdel_id}", response_class=JSONResponse)
async def delete_otdel_endpoint(
    request: Request,
    otdel_id: int,
    user: User = Depends(get_authenticated_user)
):
    async with async_session() as db_session:
        result = await crud.delete_otdel(db_session, otdel_id)
        return result



@otdels_router.put("/edit-otdel/{otdel_id}", response_class=JSONResponse)
async def edit_otdel_endpoint(
    request: CreateUpdateOtdel,
    otdel_id: int,
    user: User = Depends(get_authenticated_user)
):
    async with async_session() as db_session:
        otdel = CreateUpdateOtdel(name=request.name)
        result = await crud.update_otdel(db_session, otdel_id, otdel)
        return result



    
    
@otdels_router.get("/questions", response_class=HTMLResponse)
async def users(
    request: Request, 
    user: User = Depends(get_authenticated_user), 
    page: int = Query(1, alias='page', ge=1)
):
    ITEMS_PER_PAGE = 9
    PAGINATION_BUTTONS = 10
    
    async with async_session() as db_session:
        # Подсчитываем общее количество пользователей
        total_users = await db_session.execute(select(func.count(Questions.id)))
        total_users = total_users.scalar_one()
        total_pages = (total_users + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        # Вычисляем смещение и лимит
        offset = (page - 1) * ITEMS_PER_PAGE

        # Создаем запрос с сортировкой по id
        stmt = select(Questions).order_by(Questions.id).offset(offset).limit(ITEMS_PER_PAGE)
        result = await db_session.execute(stmt)
        questions = result.scalars().all()
        
    # Определяем страницы для отображения пагинации
    start_page = max(1, page - PAGINATION_BUTTONS // 2)
    end_page = min(total_pages, start_page + PAGINATION_BUTTONS - 1)
    start_page = max(1, end_page - PAGINATION_BUTTONS + 1)

    return templates.TemplateResponse(
        "questions.html", 
        {
            "request": request, 
            "user": user, 
            "questions": questions, 
            "current_page": page, 
            "total_pages": total_pages,
            "start_page": start_page,
            "end_page": end_page
        }
    )
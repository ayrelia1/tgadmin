import base64
import math
from typing import Optional
import uuid
from fastapi import APIRouter, Body, File, Form, Query, Request, Depends, Cookie, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from db import crud
from db.db import async_session
from function import decrypt_token, get_authenticated_user, get_user_with_access
from config import templates
from db.models import User
from sqlalchemy.future import select
import os
from models import CreateUpdateOtdel
import logging
from pathlib import Path



from bot.db.models import Otdels, Questions

from config import current_directory
UPLOAD_DIRECTORY = current_directory + "/uploads"

otdels_router = APIRouter()


def generate_unique_filename(original_filename: str) -> str:
    """Генерирует уникальное имя файла, если файл с таким именем уже существует."""
    file_extension = Path(original_filename).suffix
    base_filename = Path(original_filename).stem

    while True:
        unique_filename = f"{base_filename}_{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
        if not os.path.exists(file_path):
            return unique_filename


@otdels_router.get("/otdels", response_class=HTMLResponse)
async def users(
    request: Request, 
    user: User = Depends(get_user_with_access), 
    page: int = Query(1, alias='page', ge=1),
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
    request: CreateUpdateOtdel = Body(), 
    user: User = Depends(get_user_with_access), 
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
    user: User = Depends(get_user_with_access)
):
    async with async_session() as db_session:
        result = await crud.delete_otdel(db_session, otdel_id)
        return result



@otdels_router.put("/edit-otdel/{otdel_id}", response_class=JSONResponse)
async def edit_otdel_endpoint(
    request: CreateUpdateOtdel,
    otdel_id: int,
    user: User = Depends(get_user_with_access)
):
    async with async_session() as db_session:
        otdel = CreateUpdateOtdel(name=request.name)
        result = await crud.update_otdel(db_session, otdel_id, otdel)
        return result



    
    
@otdels_router.get("/questions", response_class=HTMLResponse)
async def questions_page(
    request: Request,
    user: User = Depends(get_user_with_access),
    page: int = Query(1, alias='page', ge=1),
    otdel_id: Optional[int] = Query(None, alias='otdel', ge=1),
    
    
):
    ITEMS_PER_PAGE = 9
    async with async_session() as db_session:
        # Получаем список отделов
        stmt_otdels = select(Otdels).order_by(Otdels.id)
        result_otdels = await db_session.execute(stmt_otdels)
        otdels = result_otdels.scalars().all()

        # Получаем количество вопросов и сами вопросы для выбранного отдела
        if otdel_id:
            total_questions_stmt = select(func.count(Questions.id)).where(Questions.otdel_id == otdel_id)
            total_questions_result = await db_session.execute(total_questions_stmt)
            total_questions = total_questions_result.scalar_one()
            total_pages = (total_questions + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

            offset = (page - 1) * ITEMS_PER_PAGE

            stmt_questions = (
                select(Questions)
                .where(Questions.otdel_id == otdel_id)
                .order_by(Questions.id)
                .offset(offset)
                .limit(ITEMS_PER_PAGE)
            )
            result_questions = await db_session.execute(stmt_questions)
            questions = result_questions.scalars().all()

        else:
            questions = []
            total_questions = 0
            total_pages = 0

        # Определяем страницы для отображения пагинации
        start_page = max(1, page - 5)
        end_page = min(total_pages, start_page + 10 - 1)
        start_page = max(1, end_page - 10 + 1)

    return templates.TemplateResponse(
        "questions.html",
        {
            "request": request,
            "user": user,
            "otdels": otdels,
            "questions": questions,
            "current_page": page,
            "total_pages": total_pages,
            "start_page": start_page,
            "end_page": end_page,
            "selected_otdel_id": otdel_id
        }
    )
    
    
    

    
@otdels_router.post("/create-question", response_class=JSONResponse)
async def create_question(
    title: str = Form(...),
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    otdel_id: int = Form(...),
    user: User = Depends(get_user_with_access),
):
    
    try:
        # Пример сохранения файла (если файл передан)
        file_name = None
        
        if file:
            print(file.filename)
            print(current_directory)
            # Генерация уникального имени файла
            file_name = generate_unique_filename(file.filename)
            file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
            
            # Сохранение файла на сервере
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            
        async with async_session() as db_session:
            # Вызов CRUD функции для создания вопроса
            new_question = await crud.create_question(
                db_session=db_session,
                title=title,
                text=text,
                file_data=file_name,
                otdel_id=otdel_id
            )
        
            await db_session.refresh(new_question)  # Обновить объект перед возвратом

    except Exception as ex:
        logging.error(ex)
        return JSONResponse(content={"status": "error", "message": f"error - {ex}"}, status_code=501)
        
    return JSONResponse(content={"status": "success", "question": {"id": new_question.id, "title": new_question.name}}, status_code=200)






@otdels_router.put("/edit-question", response_class=JSONResponse)
async def update_questions(
    title: str = Form(...),
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    id: int = Form(...),
    user: User = Depends(get_user_with_access),
):
    
    try:
        # Пример сохранения файла (если файл передан)
        file_name = None
        if file:
            print(file.filename)
            print(current_directory)
            # Генерация уникального имени файла
            file_name = generate_unique_filename(file.filename)
            file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
            
            # Сохранение файла на сервере
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            
        async with async_session() as db_session:
            # Вызов CRUD функции для создания вопроса
            new_question = await crud.update_question(
                db_session=db_session,
                question_id=id,
                title=title,
                text=text,
                file_data=file_name,
            )
        
            await db_session.refresh(new_question)  # Обновить объект перед возвратом

    except Exception as ex:
        logging.error(ex)
        return JSONResponse(content={"status": "error", "message": f"error - {ex}"}, status_code=501)
        
    return JSONResponse(content={"status": "success", "question": {"id": new_question.id, "title": new_question.name}}, status_code=200)








@otdels_router.delete("/delete-question/{question_id}", response_class=JSONResponse)
async def delete_otdel_endpoint(
    request: Request,
    question_id: int,
    user: User = Depends(get_user_with_access)
):
    async with async_session() as db_session:
        result = await crud.delete_question(db_session, question_id)
        return result
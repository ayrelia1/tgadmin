from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db import crud
from db.db import async_session
from schemas import UserCreate
from config import settings
from function import encrypt_token, get_current_user
from config import templates
from db.models import User
from schemas import UserLogin

auth_router = APIRouter()

@auth_router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request, user: User = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/profile", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    async with async_session() as db_session:
        user = await crud.get_user_by_username(db_session, username)
        if user is None or not crud.verify_password(password, user.password):
            return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})

        session = await crud.create_session(db_session, user.id, settings.SESSION_EXPIRATION_TIME)

    response = RedirectResponse(url="/profile", status_code=303)
    encrypted_token = encrypt_token(session.session_token)
    response.set_cookie(
        key="session_token",
        value=encrypted_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=settings.SESSION_EXPIRATION_TIME
    )
    return response

@auth_router.get("/register", response_class=HTMLResponse)
async def get_register(request: Request, user: User = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/profile", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request})

@auth_router.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...), full_name: str = Form(...)):
    if not username or not password or not full_name:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Заполните все поля!"})

    async with async_session() as db_session:
        existing_user = await crud.get_user_by_username(db_session, username)
        if existing_user:
            return templates.TemplateResponse("register.html", {"request": request, "error": "Такой логин уже есть!"})

        user = UserCreate(username=username, password=password, full_name=full_name)
        await crud.create_user(db_session, user)

    return RedirectResponse(url="/login", status_code=303)
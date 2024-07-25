import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi import FastAPI, HTTPException, Request, Cookie, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from exc import NotAuthenticatedException, NotAccessException
from routers import routers
from config import app
from db.models import create_tables
from db.db import engine
from starlette.middleware.cors import CORSMiddleware

# Настройка CORS
orig_origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8004",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=orig_origins,  # список разрешенных доменов
    allow_credentials=True,
    allow_methods=["POST", "PUT", "GET", "DELETE"],  # Разрешить все методы HTTP (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)



@app.exception_handler(NotAuthenticatedException)
async def not_authenticated_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url="/login", status_code=303)


@app.exception_handler(NotAccessException)
async def not_authenticated_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url="/", status_code=303)


for router in routers:
    app.include_router(router)



if __name__ == "__main__":
    
    
    # log_dir = '/app/logs'
    # os.makedirs(log_dir, exist_ok=True)  # Создать директорию, если не существует
    # log_file = os.path.join(log_dir, 'app_webadmin.log')
    
    # # Создать форматтер
    # formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - '
    #                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    
    # logging.getLogger("requests").setLevel(logging.WARNING)
    # logging.getLogger("apscheduler").setLevel(logging.WARNING)
    # # Настроить основной логгер
    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    
    # # Создать обработчик для ротации логов
    # file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    # file_handler.setLevel(logging.INFO)
    # file_handler.setFormatter(formatter)
    
    #     # Создать консольный обработчик
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(formatter)
    
    # # Добавить обработчики к логгеру
    # logger.addHandler(file_handler)
    # logger.addHandler(console_handler)
    
    
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
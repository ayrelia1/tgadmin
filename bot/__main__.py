from logging.handlers import RotatingFileHandler
import os
from config import dp, logging, bot, Bot, current_directory, root_path
from aiogram.types import BotCommand, BotCommandScopeDefault

from middlewares import setup
from handlers import routers
import asyncio
from db.models import create_tables
from db.db import engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import sys


schedulers = AsyncIOScheduler()




@dp.startup()
async def start_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='🔄 Главное меню'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    
    #schedulers.add_job() 123
    schedulers.start()
    
    task1 = asyncio.create_task(create_tables()) # создаем базу юзеров если нет

    
@dp.shutdown()
async def dispose(bot: Bot):
    schedulers.shutdown()
    engine.dispose()

            
                

async def main() -> None:     # функция запуска бота
    log_dir = '/app/logs'
    os.makedirs(log_dir, exist_ok=True)  # Создать директорию, если не существует
    log_file = os.path.join(log_dir, 'app_bot.log')
    
    # Создать форматтер
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - '
                                  '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    # Настроить основной логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Создать обработчик для ротации логов
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
        # Создать консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Добавить обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    


    
    for router in routers:
        dp.include_router(router) # импорт роутеров
        
        
    setup(dp)  # мидлвари    
    try:
        await dp.start_polling(bot) # запуск поллинга
    except Exception as ex:
        print(ex)

        
    
if __name__ == "__main__":
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # устанавливаем политику для лупа если wind
            
    
    asyncio.run(main()) 
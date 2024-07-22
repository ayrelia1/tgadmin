from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile
from aiogram.types import FSInputFile
from aiogram.types import (
    KeyboardButton,
    Message,
    Update,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram import types
from aiogram.filters import Filter
import logging
import datetime
import json
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

load_dotenv()

    
current_directory = os.path.abspath(os.path.dirname(__file__))
root_path = Path(__file__).parent.parent


class Settings(BaseSettings): # создаем settings class
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    
        
settings = Settings()

     
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))







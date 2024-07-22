from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, FSInputFile, settings
from markups.markup import *
from filters import filtersbot
from sql_function import databasework
from states.states import RequestState
from datetime import timedelta
import datetime
from aiogram.types import Chat
from db.models import User


router = Router()



   


# меню
@router.callback_query(F.data == 'main_menu', F.chat.type == 'private')
async def go_main(callback: types.CallbackQuery, state: FSMContext):
    
    
    await state.clear()
    markup = start_markup()
    await bot.edit_message_text(message_id=callback.message.message_id, chat_id=callback.message.chat.id, text='⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)



@router.message(F.text == '/start', F.chat.type == 'private')
async def start(message: types.Message, state: FSMContext, bot_user: User):
    
    await state.clear()
    markup = start_markup()
    await message.answer(f'⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)


user = router
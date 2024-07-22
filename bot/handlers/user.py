from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, FSInputFile, settings
from markups.markup import *
from filters import filtersbot
from sql_function import databasework
from states.states import RequestState
from datetime import timedelta
import datetime
from aiogram.types import Chat
from db.models import UserTg


router = Router()


router.message.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру
router.callback_query.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру
   

@router.callback_query(filtersbot.PageCallback.filter(F.action == 'otdels'))
async def orders_page_handler(callback: types.CallbackQuery, callback_data: filtersbot.PageCallback) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=await otdels_markup(callback_data.filter_type, callback.from_user.id, callback_data.page),
    )
    await callback.answer()


# меню
@router.callback_query(F.data == 'main_menu')
async def go_main(callback: types.CallbackQuery, state: FSMContext):
    
    
    await state.clear()
    markup = start_markup()
    await bot.edit_message_text(message_id=callback.message.message_id, chat_id=callback.message.chat.id, text='⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)



@router.message(F.text == '/start', F.chat.type == 'private')
async def start(message: types.Message, state: FSMContext, bot_user: UserTg):
    
    await state.clear()
    markup = start_markup()
    await message.answer(f'⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)
    


# ============ Отделы ========== # 
@router.callback_query(F.data.in_(['pizza', 'ebi']))
async def otdels(callback: types.CallbackQuery, state: FSMContext):
    markup = await otdels_markup()
    await bot.edit_message_text(text=f'⭐️ Выберите нужный вам отдел', chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)

# ============ Вопросы ========== # 
@router.callback_query(filtersbot.OtdelsMarkup.filter(F.action == 'open'))
async def questions(callback: types.CallbackQuery, callback_data: filtersbot.OtdelsMarkup) -> None:
    markup = await questions_markup(callback_data.id_otdel)
    await bot.edit_message_text(text=f'⭐️ Выберите нужный вам вопрос', chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)


# ============ Ответ на вопрос ========== # 
@router.callback_query(filtersbot.QuestionsMarkup.filter(F.action == 'open'))
async def question(callback: types.CallbackQuery, callback_data: filtersbot.QuestionsMarkup) -> None:
    pass







user = router
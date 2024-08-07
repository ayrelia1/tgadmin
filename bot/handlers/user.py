import base64
from io import BytesIO
from pathlib import Path

from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, FSInputFile, settings
from markups.markup import *
from filters import filtersbot
from sql_function import databasework
from states.states import RequestState
from datetime import timedelta
import datetime
from aiogram.types import Chat
from db.models import UserTg

from config import current_directory

# Создайте объект Path из текущего пути
current_path = Path(current_directory)

# Перейдите на одну папку назад
parent_directory = current_path.parent

# Добавьте 'uploads' к родительскому пути
UPLOAD_DIRECTORY = parent_directory / "webadmin/uploads"




router = Router()


router.message.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру
router.callback_query.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру
   
   
   
   
# ========= Старт ======== #
@router.message(F.text == '/start', F.chat.type == 'private')
async def start(message: types.Message, state: FSMContext, bot_user: UserTg):
    
    await state.clear()
    markup = start_markup()
    await message.answer(f'⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)
   
   
# ======= Возвраты назад ===== #
@router.callback_query(filtersbot.BackToQuestions.filter(F.action == 'back'))
async def questions_page_handler(callback: types.CallbackQuery, callback_data: filtersbot.BackToQuestions) -> None:
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    texts, markup = await questions_markup(callback_data.id_otdel)
    

    text_ = '\n'.join(texts)
    
    await bot.send_message(text=f'⭐️ Выберите нужный вам вопрос\n\n{text_}', chat_id=callback.message.chat.id, reply_markup=markup)

@router.callback_query(F.data == 'back_to_otdels')
async def back_to_otdels(callback: types.CallbackQuery, state: FSMContext):
    
    
    await state.clear()
    markup = await otdels_markup()
    await bot.edit_message_text(message_id=callback.message.message_id, chat_id=callback.message.chat.id, text='⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)



# ========= Пагинация ======== #

@router.callback_query(filtersbot.PageCallback.filter(F.action == 'otdel'))
async def otdels_page_handler(callback: types.CallbackQuery, callback_data: filtersbot.PageCallback) -> None:
    await callback.message.edit_reply_markup(
        reply_markup=await otdels_markup(callback_data.page),
    )
    await callback.answer()


@router.callback_query(filtersbot.PageCallbackQuestions.filter(F.action == 'question'))
async def questions_page_handler(callback: types.CallbackQuery, callback_data: filtersbot.PageCallbackQuestions) -> None:
    texts, markup = await questions_markup(callback_data.otdel_id, callback_data.page)
    
    text_ = '\n'.join(texts)
    
    await callback.message.edit_text(
        text=f'⭐️ Выберите нужный вам вопрос\n\n{text_}',
        reply_markup=markup,
    )
    await callback.answer()



# ========= Меню ======== #
@router.callback_query(F.data == 'main_menu')
async def go_main(callback: types.CallbackQuery, state: FSMContext):
    
    
    await state.clear()
    markup = start_markup()
    await bot.edit_message_text(message_id=callback.message.message_id, chat_id=callback.message.chat.id, text='⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)


    


# ============ Отделы ========== # 
@router.callback_query(F.data.in_(['pizza', 'ebi']))
async def otdels(callback: types.CallbackQuery, state: FSMContext):
    markup = await otdels_markup()
    await bot.edit_message_text(text=f'⭐️ Выберите нужный вам отдел', chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)

# ============ Вопросы ========== # 
@router.callback_query(filtersbot.OtdelsMarkup.filter(F.action == 'open'))
async def questions(callback: types.CallbackQuery, callback_data: filtersbot.OtdelsMarkup) -> None:
    texts, markup = await questions_markup(callback_data.id_otdel)
    
    text_ = '\n'.join(texts)
    
    await bot.edit_message_text(text=f'⭐️ Выберите нужный вам вопрос\n\n{text_}', chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)


# ============ Ответ на вопрос ========== # 
MAX_MESSAGE_LENGTH = 4095

def split_text(text, max_length):
    # Split the text into parts not exceeding max_length
    parts = []
    while len(text) > max_length:
        # Find the last space character within the max_length limit to avoid splitting words
        split_pos = text.rfind(' ', 0, max_length)
        if split_pos == -1:
            split_pos = max_length  # In case there's no space, split at max_length
        parts.append(text[:split_pos])
        text = text[split_pos:].strip()
    parts.append(text)
    return parts

@router.callback_query(filtersbot.QuestionsMarkup.filter(F.action == 'open_ques'))
async def question(callback: types.CallbackQuery, callback_data: filtersbot.QuestionsMarkup) -> None:
    id_question = callback_data.id_question
    question = await databasework.get_question(id_question)
    answer = question[2]
    filename = question[4]
    markup = back_to_questions(callback_data.id_otdel)
    
    if filename:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        file = FSInputFile(path=f"{UPLOAD_DIRECTORY}/{filename}")
        answer_bot = None
        if answer:
            answer_bot = answer[:MAX_MESSAGE_LENGTH]
            remaining_text = answer[MAX_MESSAGE_LENGTH:]
        if filename.split('.')[-1] in ['jpg', 'png']:
            await bot.send_photo(caption=answer_bot, chat_id=callback.message.chat.id, photo=file, reply_markup=markup)
            
        elif filename.split('.')[-1] == 'mp4':
            await bot.send_video(caption=answer_bot, chat_id=callback.message.chat.id, video=file, reply_markup=markup)
            
        else:
            await bot.send_document(caption=answer_bot, chat_id=callback.message.chat.id, document=file, reply_markup=markup)
            
        
        # Send remaining text if any
        if remaining_text:
            parts = split_text(remaining_text, MAX_MESSAGE_LENGTH)
            for part in parts:
                await bot.send_message(chat_id=callback.message.chat.id, text=part, reply_markup=markup)
    else:
        parts = split_text(answer, MAX_MESSAGE_LENGTH)
        await bot.edit_message_text(text=parts[0], chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)
        for part in parts[1:]:
            await bot.send_message(chat_id=callback.message.chat.id, text=part, reply_markup=markup)


user = router
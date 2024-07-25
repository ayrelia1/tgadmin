from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types

from filters import filtersbot
from sql_function import databasework
import math

def start_markup(): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='Тич-Пицца', callback_data='pizza') # 
        .button(text='Ебидоеби', callback_data='ebi')
        .adjust(1, repeat=True)
        .as_markup()
    )
    
    return markup


async def otdels_markup(current_page: int = 0):
    locations = await databasework.get_all_otdels()
    markup = InlineKeyboardBuilder()
    
    page_width = 10 # настройка пагинации
    page_offset = current_page * page_width

    last_page = max(0, math.ceil(len(locations) / page_width) - 1)
    prev_page = max(0, current_page - 1)
    next_page = min(last_page, current_page + 1)
    
    for i in locations[page_offset : page_offset + page_width]:
        name = i[1]
        markup.add(
            types.InlineKeyboardButton(
                text=name, 
                callback_data=filtersbot.OtdelsMarkup(action='open', id_otdel=i[0]).pack()
            )
        )
    
    markup.adjust(1)
    
    # Создаем кнопки для пагинации
    pagination_buttons = []
    
    if prev_page != current_page: # кнопка "Назад"
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="◀️",
                callback_data=filtersbot.PageCallback(page=prev_page, action='otdel').pack()
            )
        )

    # Кнопка для текущей страницы
    pagination_buttons.append(
        types.InlineKeyboardButton(
            text=f"{current_page + 1}/{last_page + 1}",
            callback_data='no_action'  # Эта кнопка не будет выполнять действие
        )
    )
    
    if last_page != current_page: # кнопка "Вперед"
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="▶️",
                callback_data=filtersbot.PageCallback(page=next_page, action='otdel').pack()
            )
        )

    markup.row(*pagination_buttons)

    # Кнопка "В главное меню"
    markup.row(
        types.InlineKeyboardButton(
            text='🔙 В главное меню', 
            callback_data='main_menu'
        )
    )
    
    return markup.as_markup()



async def questions_markup(otdel_id: int, current_page: int = 0):
    locations = await databasework.get_all_questions_where_otdel_id(otdel_id)
    markup = InlineKeyboardBuilder()
    
    page_width = 20  # настройка пагинации
    page_offset = current_page * page_width

    last_page = max(0, math.ceil(len(locations) / page_width) - 1)
    prev_page = max(0, current_page - 1)
    next_page = min(last_page, current_page + 1)

    # Создаем список для хранения текста кнопок с учетом пагинации
    texts = []

    # Номер первого вопроса на текущей странице
    start_index = page_offset + 1

    # Добавляем кнопки с вопросами
    for index, i in enumerate(locations[page_offset: page_offset + page_width], start=start_index):
        name = i[1]
        text = f"{index}. {name}"  # Форматируем текст с номером вопроса
        texts.append(text)  # Сохраняем текст кнопки
        markup.add(
            types.InlineKeyboardButton(
                text=text, 
                callback_data=filtersbot.QuestionsMarkup(action='open_ques', id_question=i[0], id_otdel=otdel_id).pack()
            )
        )
    
    # Выбираем количество кнопок в строке (2 или 3)
    markup.adjust(2, 3)
    
    # Создаем кнопки для пагинации
    pagination_buttons = []
    
    if prev_page != current_page:  # кнопка "Назад"
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="◀️",
                callback_data=filtersbot.PageCallbackQuestions(otdel_id=otdel_id, page=prev_page, action='question').pack()
            )
        )

    # Кнопка для текущей страницы
    pagination_buttons.append(
        types.InlineKeyboardButton(
            text=f"{current_page + 1}/{last_page + 1}",
            callback_data='no_action'  # Эта кнопка не будет выполнять действие
        )
    )
    
    if last_page != current_page:  # кнопка "Вперед"
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="▶️",
                callback_data=filtersbot.PageCallbackQuestions(otdel_id=otdel_id, page=next_page, action='question').pack()
            )
        )
        
    if last_page == current_page:
        markup.row(
            types.InlineKeyboardButton(
                text="Спроси HR",
                url="https://docs.google.com/forms/d/1jyqXjKX_MrcboWJiUOJsUIzuq_gwb_iEzwQKWqUoUPQ/edit"
            )
        )

    markup.row(*pagination_buttons)
    
    # Кнопка "Назад"
    markup.row(
        types.InlineKeyboardButton(
            text='🔙 Назад', 
            callback_data='back_to_otdels'
        )
    )
    
    return (texts, markup.as_markup())






def back_to_questions(id_otdel: int): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='🔙 Назад', callback_data=filtersbot.BackToQuestions(id_otdel=id_otdel, action='back').pack())
        .adjust(1, repeat=True)
        .as_markup()
    )
    
    return markup
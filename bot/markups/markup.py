from config import types, InlineKeyboardBuilder
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
    

    
    page_width = 20 # настройка пагинации
    page_offset = current_page * page_width

    last_page = max(0, math.ceil((len(locations) / page_width) - 1))
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
        
    markup.adjust(2)
    buttons = []

    if prev_page != current_page: # кнопки для управления пагинацией
        buttons.append(
            types.InlineKeyboardButton(
                text="◀️",
                callback_data=filtersbot.PageCallback(page=prev_page, action='otdel').pack(),
            ),
        )

    if last_page != current_page:
        buttons.append(
            types.InlineKeyboardButton(
                text="▶️",
                callback_data=filtersbot.PageCallback(page=next_page, action='otdel').pack(),
            ),
        )

    markup.row(*buttons)
    
    markup.row(types.InlineKeyboardButton(text='🔙 В главное меню', callback_data='main_menu'))
    return markup.as_markup()



async def questions_markup(otdel_id: int, current_page: int = 0):
    locations = await databasework.get_all_questions_where_otdel_id(otdel_id)
    markup = InlineKeyboardBuilder()
    

    
    page_width = 20 # настройка пагинации
    page_offset = current_page * page_width

    last_page = max(0, math.ceil((len(locations) / page_width) - 1))
    prev_page = max(0, current_page - 1)
    next_page = min(last_page, current_page + 1)
    
    for i in locations[page_offset : page_offset + page_width]:
        name = i[1]

        
        markup.add(
            types.InlineKeyboardButton(
                text=name, 
                callback_data=filtersbot.QuestionsMarkup(action='open', id_question=i[0]).pack()
                )
            )
        
    markup.adjust(2)
    buttons = []

    if prev_page != current_page: # кнопки для управления пагинацией
        buttons.append(
            types.InlineKeyboardButton(
                text="◀️",
                callback_data=filtersbot.PageCallback(page=prev_page, action='otdel').pack(),
            ),
        )

    if last_page != current_page:
        buttons.append(
            types.InlineKeyboardButton(
                text="▶️",
                callback_data=filtersbot.PageCallback(page=next_page, action='otdel').pack(),
            ),
        )
        
    if last_page == current_page:
        buttons.append(
            types.InlineKeyboardButton(
                text="Спроси HR",
                url="https://docs.google.com/forms/d/1jyqXjKX_MrcboWJiUOJsUIzuq_gwb_iEzwQKWqUoUPQ/edit"
            ),
        )

    markup.row(*buttons)
    
    markup.row(types.InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_otdels'))
    return markup.as_markup()


def back_to_questions(): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='🔙 Назад', callback_data='back_to_questions')
        .adjust(1, repeat=True)
        .as_markup()
    )
    
    return markup
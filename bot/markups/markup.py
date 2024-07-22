from config import types, InlineKeyboardBuilder
from filters import filtersbot
from sql_function import databasework


def start_markup(): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='✔️ Заявка', callback_data='application') # 
        .button(text='📋 Портфолио', url='https://google.com')
        .adjust(2, repeat=True)
        .as_markup()
    )
    
    return markup







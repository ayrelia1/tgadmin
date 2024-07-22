from config import CallbackData, Filter
from sql_function import databasework

class AdminCheck(Filter): # фильтр проверка на админа
    async def __call__(self, message) -> bool:
        return await databasework.check_admin(message.from_user.id)




class PageCallback(CallbackData, prefix="page"):
    action: str
    page: int
    
class OtdelsMarkup(CallbackData, prefix="page"):
    action: str
    id_otdel: int
    
class QuestionsMarkup(CallbackData, prefix="page"):
    action: str
    id_question: int
    



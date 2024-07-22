from config import CallbackData, Filter
from sql_function import databasework

class AdminCheck(Filter): # фильтр проверка на админа
    async def __call__(self, message) -> bool:
        return await databasework.check_admin(message)




    
    
    
    
    



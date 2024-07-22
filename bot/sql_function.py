from config import types
from db.db import async_session, engine
import sys, asyncio
from sqlalchemy import text
from sqlalchemy.future import select
from db.models import UserTg, UserData

class databasework:
    
    
    
    

    
    
    async def create_user(user_id: str, username: str):
        async with async_session() as session:
            async with session.begin():
                sql = """
                INSERT INTO users (user_id, username)
                VALUES (:user_id, :username)
                """
                await session.execute(text(sql), {"user_id": str(user_id), "username": username})
            await session.commit()  # Подтверждение транзакции
    
    async def update_username_user(username: str, user_id: str):
        async with async_session() as session:
            async with session.begin():
                sql = "UPDATE users SET username = :username WHERE user_id = :user_id"
                await session.execute(text(sql), {"username": username, "user_id": str(user_id)})
            await session.commit()
    
        
    async def check_user(user_id: str):
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM users WHERE user_id = :user_id"
                result = await session.execute(text(sql), {"user_id": str(user_id)})
                return result.one_or_none() # Возвращает один результат или None
            
            
    async def check_user_o(user_id: str):
        async with async_session() as session:
            async with session.begin():
                stmt = select(UserTg).where(UserTg.user_id == str(user_id))  # Используем ORM-запрос
                result = await session.execute(stmt)  # Выполнение запроса
                user = result.scalar_one_or_none()  # Получение первого ORM-объекта
                
                user_data = UserData(
                    id=user.id,
                    user_id=user.user_id,
                    username=user.username,
                    status=user.status,
                    has_access=user.has_access,
                    reg_date=user.reg_date,
                    ban=user.ban,
                )
                
                
                return user_data  # Возвращает экземпляр `dataclass`
                
  
                
    async def check_ban(user_id: str):
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM users WHERE user_id = :user_id"
                result = await session.execute(text(sql), {"user_id": str(user_id)})
                ban_status = result.one_or_none()  # Получение значения
                return ban_status and ban_status[7] == 'yes'
        
        
       

    async def check_admin(user_id: str):
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM users WHERE user_id = :user_id"
                result = await session.execute(text(sql), {"user_id": str(user_id)})
                status = result.one_or_none()  # Получение статуса пользователя 
                if status:
                    return status[4] == True
                return 
    
    
    
    async def get_all_users():
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM users"
                result = await session.execute(text(sql))  # Выполнение запроса
                return result.all()  # Возвращает все строки
    
    
    
    async def get_all_otdels():
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM otdels"
                result = await session.execute(text(sql))  # Выполнение запроса
                return result.all()  # Возвращает все строки
            
            
    async def get_all_questions_where_otdel_id(otdel_id: int):
        async with async_session() as session:
            async with session.begin():
                sql = """
                        SELECT q.id AS question_id, q.name AS question_name, q.answer, q.type_answer, q.file, o.name AS otdel_name
                        FROM questions q
                        JOIN otdels o ON q.otdel_id = o.id
                        WHERE o.id = :otdel_id
                    """
                result = await session.execute(text(sql), {"otdel_id": otdel_id})  # Выполнение запроса
                return result.all()  # Возвращает все строки
    

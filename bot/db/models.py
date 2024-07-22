from dataclasses import dataclass
from db.db import engine, async_session

from sqlalchemy import BigInteger, text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Integer, String, CheckConstraint, UniqueConstraint, Boolean





class Base(AsyncAttrs, DeclarativeBase):
    pass

# Модель для таблицы `users`
class UserTg(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(String(100), unique=True, index=True)
    username = mapped_column(String(100), default=None)  # На уровне Python
    
    status = mapped_column(
        String(25),
        CheckConstraint("status IN ('user', 'oper', 'admin')"),  # Позиционный аргумент перед именованными
        default='user',  # На уровне Python
        server_default='user',  # На уровне базы данных
    )
    
    has_access = mapped_column(
        Boolean,
        default='False',  # На уровне Python
        server_default='False',  # На уровне базы данных,
        nullable=False
    )
    
    reg_date = mapped_column(
        String(50),
        server_default=text("CURRENT_TIMESTAMP"),  # На уровне базы данных
    )
    
    ban = mapped_column(
        String(25),
        CheckConstraint("ban IN ('yes', 'no')"),
        default='no',  # На уровне Python__annotat__annotations__())ons__())
        server_default='no',  # На уровне базы данных
    )




class Otdels(Base):
    __tablename__ = 'otdels'

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String)
    questions = relationship("Questions", back_populates="otdel")

class Questions(Base):
    __tablename__ = 'questions'

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String)
    answer = mapped_column(String)
    type_answer = mapped_column(String)
    file = mapped_column(String)
    otdel_id = mapped_column(Integer, ForeignKey('otdels.id'))

    otdel = relationship("Otdels", back_populates="questions")




async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

from dataclasses import dataclass

@dataclass
class UserData:
    id: int
    user_id: str
    username: str
    status: str
    has_access: str
    reg_date: str
    ban: str
from pydantic import BaseModel
from pydantic import BaseModel, field_validator

class UserBase(BaseModel):
    username: str
    full_name: str



class UserCreate(UserBase):
    password: str

    @field_validator('username')
    def username_length(cls, v):
        if len(v) < 4:
            raise ValueError('Имя пользователя должно содержать не менее 4 символов')
        return v

    @field_validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль должен состоять минимум из 6 символов')
        return v

class UserLogin(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True
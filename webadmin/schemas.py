from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True
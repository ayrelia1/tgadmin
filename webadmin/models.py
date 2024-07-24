
from pydantic import BaseModel, field_validator
import re



class NewsletterRequest(BaseModel):
    message: str
    
class CreateUpdateOtdel(BaseModel):
    name: str    


class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def username_validation(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]{4,}$", v):
            raise ValueError('Username must be at least 4 characters long and contain only English letters, digits, hyphens, or underscores')
        return v

    @field_validator('password')
    def password_validation(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
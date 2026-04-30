from pydantic import BaseModel, EmailStr, ConfigDict
from core.enum import Role
from datetime import datetime




class UserLogin(BaseModel):
    password: str
    email: EmailStr

class RegisterUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    
class ResponseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    email: EmailStr
    role: Role
    is_active: bool
    created_at: datetime



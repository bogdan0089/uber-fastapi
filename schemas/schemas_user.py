from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from core.enum import Role
from datetime import datetime


class UserLogin(BaseModel):
    password: str
    email: EmailStr

class RegisterUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Role = Role.PASSENGER

    @field_validator("password")
    @classmethod
    def validate_password(cla, p: str) -> str:
        if len(p) < 8:
            raise ValueError("Password must be longest")
        return p
    
class ResponseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: Role
    is_active: bool
    created_at: datetime

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None



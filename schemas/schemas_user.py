from pydantic import BaseModel, EmailStr, ConfigDict
from core.enum import Role



class RegisterUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    

    
class ResponseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: Role



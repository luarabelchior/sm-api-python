from pydantic import BaseModel, EmailStr
from datetime import datetime 
from typing import Optional 

class UserBase(BaseModel):
    full_name: Optional[str] = None 
    role: str = "member" 

class UserCreate(BaseModel):
    email: EmailStr
    password: str 
    full_name: Optional[str] = None 
    role: str = "member" 

class UserUpdate(BaseModel): 
    full_name: Optional[str] = None  
    role: Optional[str] = None 

class User(UserBase): 
    id: str 
    email: EmailStr 
    updated_at: Optional[datetime] = None 

    class Config: 
        from_attributes = True
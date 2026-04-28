from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr


class UserCreate(UserBase):
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

    


class UserResponse(UserBase):
    id:int
    role:str
    created_at:datetime

    class config:from_attributes=True
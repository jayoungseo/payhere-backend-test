from pydantic import BaseModel, EmailStr
from typing import List, Any, Optional, Union, Dict


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str
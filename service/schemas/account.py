from pydantic import BaseModel, EmailStr
from typing import List, Any, Optional, Union, Dict
from datetime import date, datetime

class AccountPostDTO(BaseModel):
    amount: int
    memo: str


class AccountUpdateDTO(BaseModel):
    amount: Optional[int]
    memo: Optional[str]


class AccountReturnData(BaseModel):
    use_date: date
    amount: int
    memo: str

    class Config:
        orm_mode = True


class AccountDataInDB(AccountReturnData):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

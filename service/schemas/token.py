from pydantic import BaseModel, EmailStr
from typing import List, Any, Optional, Union, Dict

class RefreshToken(BaseModel):
    refresh_token: str
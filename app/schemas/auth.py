from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    is_superuser: Optional[bool] = False
    user_type: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str 
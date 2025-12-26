from pydantic import BaseModel
from typing import List, Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    buttons: List[str]
    roles: List[str]
    userId: int
    username: str
    email: str
    avatar: Optional[str] = None
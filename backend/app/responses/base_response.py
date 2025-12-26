from typing import Any, Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    succ: bool
    msg: str
    data: Optional[Any] = None
    code: int
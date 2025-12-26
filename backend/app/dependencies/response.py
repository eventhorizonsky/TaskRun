from typing import Any, Optional
from app.responses import BaseResponse


def success_response(msg: str = "操作成功", data: Optional[Any] = None, code: int = 200) -> BaseResponse:
    return BaseResponse(succ=True, msg=msg, data=data, code=code)


def error_response(msg: str = "操作失败", data: Optional[Any] = None, code: int = 400) -> BaseResponse:
    return BaseResponse(succ=False, msg=msg, data=data, code=code)
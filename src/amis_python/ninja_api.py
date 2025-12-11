
from typing import List, Optional, Callable, Any, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status: int = 0
    msg: str = "操作成功"
    data: Optional[T] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    count: int
    page: int
    pages: int

def success_response(data: Any = None, msg: str = "操作成功") -> dict:
    return ApiResponse(status=0, msg=msg, data=data).model_dump()

def error_response(msg: str = "操作失败", data: Any = None) -> dict:
    return ApiResponse(status=1, msg=msg, data=data).model_dump()
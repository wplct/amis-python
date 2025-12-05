from typing import Literal, Optional, Dict, Any, Callable

from pydantic import BaseModel, Field

from .base import BaseBuilder


class AmisApiObject(BaseBuilder):
    """
    AMIS 中结构化的 API 配置对象。
    参考：https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/api
    """
    type: Literal["api_config"] = "api_config"

    url: str = Field(..., description="接口地址")
    method: Literal["get", "post", "put", "delete", "patch"] = Field(
        "get", description="HTTP 请求方法"
    )
    data: Optional[Dict[str, Any]] = Field(
        None, description="请求体数据（通常用于 POST/PUT）"
    )
    headers: Optional[Dict[str, str]] = Field(
        None, description="自定义请求头"
    )
    request_adaptor: Optional[str] = Field(
        None,
        description="请求发送前的适配器函数（前端 JS 函数名或代码字符串）"
    )
    adaptor: Optional[str] = Field(
        None,
        description="响应数据适配器（用于转换返回结果）"
    )
    timeout: Optional[int] = Field(
        None, description="请求超时时间（毫秒）"
    )

    class Config:
        populate_by_name = True  # 允许通过 snake_case 赋值，自动转为 camelCase

class LazyAmisApiObject(BaseBuilder):
    """
    AMIS 中结构化的 API 配置对象，用于懒加载。
    """
    type: Literal["lazy_api_config"] = "lazy_api_config"
    api_view: Optional[Callable] = None

    def __init__(self, api_view,**kwargs):
        super().__init__(**kwargs)
        self.api_view = api_view

    def to_schema(
            self,
            *,
            by_alias: bool = True,
            exclude_none: bool = True,
            **dump_kwargs: Any,
    ) -> Dict[str, Any]:
        print(self.api_view)
        print(dir(self.api_view))
        return {}


def api(api_view):
    return LazyAmisApiObject(api_view=api_view)
from typing import Literal, Optional, Dict, Any, Callable

from django.urls import reverse

from .base import BaseBuilder


class AmisApiObject(BaseBuilder):
    """
    AMIS 中结构化的 API 配置对象。
    参考：https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/api
    """
    type: Literal["api_config"] = "api_config"

    # 基础属性
    url: str  # 接口地址
    method: Literal["get", "post", "put", "delete", "patch"] = "get"  # HTTP 请求方法
    data: Optional[Dict[str, Any]] = None  # 请求体数据（通常用于 POST/PUT）
    headers: Optional[Dict[str, str]] = None  # 自定义请求头
    request_adaptor: Optional[str] = None  # 请求发送前的适配器函数（前端 JS 函数名或代码字符串）
    adaptor: Optional[str] = None  # 响应数据适配器（用于转换返回结果）
    timeout: Optional[int] = None  # 请求超时时间（毫秒）

    def __init__(self, url: str, **kwargs):
        # 设置必填字段
        self.url = url
        
        # 设置可选字段
        self.method = kwargs.pop("method", "get")
        self.data = kwargs.pop("data", None)
        self.headers = kwargs.pop("headers", None)
        self.request_adaptor = kwargs.pop("request_adaptor", None)
        self.adaptor = kwargs.pop("adaptor", None)
        self.timeout = kwargs.pop("timeout", None)
        
        # 设置额外字段
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        super().__init__(**kwargs)

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
        print(reverse("api:save_form"))
        return {}


def api(api_view):
    return LazyAmisApiObject(api_view=api_view)
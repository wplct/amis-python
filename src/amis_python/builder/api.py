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


class LazyAmisApiObject(BaseBuilder):
    """
    AMIS 中结构化的 API 配置对象，用于懒加载。
    """
    type: Literal["lazy_api_config"] = "lazy_api_config"
    _api_view: Optional[Callable] = None
    _api_obj: Optional[AmisApiObject] = None
    _kwargs: Optional[Dict[str, Any]] = None

    def __init__(self, api_view,data=None,headers=None,request_adaptor=None,adaptor=None,timeout=None ,**kwargs):
        super().__init__(**kwargs)
        self.api_view = api_view
        self._kwargs = {
            "data": data,
            "headers": headers,
            "request_adaptor": request_adaptor,
            "adaptor": adaptor,
            "timeout": timeout,
        }

    def to_schema(self, by_alias=True, exclude_none=True) -> Dict[str, Any]:
        print(reverse("api:save_form"))
        if self._api_obj is None:
            self._api_obj = AmisApiObject(
                url=reverse("api:save_form"),
                method="post",
                **self._kwargs
            )
        return self._api_obj.to_schema(by_alias, exclude_none)


def api(api_view) -> LazyAmisApiObject:
    return LazyAmisApiObject(api_view=api_view)

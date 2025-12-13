import re
from typing import Literal, Optional, Dict, Any, Callable

from django.urls import reverse, reverse_lazy

from .base import BaseModel, Field


class AmisApiObject(BaseModel):
    """
    AMIS 中结构化的 API 配置对象。
    参考：https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/api
    """
    type: Literal["api_config"] = Field("api_config", description="组件类型")

    # 基础属性
    url: Optional[str] = Field(None, description="接口地址")
    method: Optional[Literal["get", "post", "put", "delete", "patch"]] = Field(None, description="HTTP 请求方法")
    data: Optional[Dict[str, Any]] = Field(None, description="请求体数据（通常用于 POST/PUT）")
    headers: Optional[Dict[str, str]] = Field(None, description="自定义请求头")
    request_adaptor: Optional[str] = Field(None, description="请求发送前的适配器函数（前端 JS 函数名或代码字符串）")
    adaptor: Optional[str] = Field(None, description="响应数据适配器（用于转换返回结果）")
    timeout: Optional[int] = Field(None, description="请求超时时间（毫秒）")


class LazyAmisApiObject(BaseModel):
    """
    AMIS 中结构化的 API 配置对象，用于懒加载。
    """
    type: Literal["lazy_api_config"] = Field("lazy_api_config", description="组件类型")

    def __init__(self, api_view, data=None, headers=None, request_adaptor=None, adaptor=None, timeout=None, **kwargs):
        super().__init__(**kwargs)
        # 使用普通实例变量，而不是 Pydantic 字段，因为 Pydantic 不允许字段名以下划线开头
        self._api_view = api_view
        self._api_obj = None
        self._kwargs = {
            "data": data,
            "headers": headers,
            "request_adaptor": request_adaptor,
            "adaptor": adaptor,
            "timeout": timeout,
        }

    def model_dump(self, by_alias=True, exclude_none=True, **kwargs) -> Dict[str, Any]:
        if self._api_obj is None:
            operation = self._api_view._ninja_operation
            methods = operation.methods
            base_url = '/'.join(reverse("api-1.0.0:base_url").split('/')[:-1])
            method = ''
            if 'GET' in methods:
                method = 'get'
            elif 'POST' in methods:
                method = 'post'
            elif 'PUT' in methods:
                method = 'put'
            elif 'DELETE' in methods:
                method = 'delete'
            elif 'PATCH' in methods:
                method = 'patch'
            url = convert_ninja_path_to_amis_template(f"{base_url}{operation.path}")
            self._api_obj = AmisApiObject(
                url=url,
                method=method,
                **self._kwargs
            )
        return self._api_obj.model_dump(by_alias, exclude_none, **kwargs)


def to_api(api_view) -> LazyAmisApiObject:
    return LazyAmisApiObject(api_view=api_view)

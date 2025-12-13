import re
from typing import Literal, Optional, Dict, Any, Callable

from django.urls import reverse, reverse_lazy

from .base import BaseModel, Field


def convert_ninja_path_to_amis_template(path: str) -> str:
    """
    将 Django-Ninja 风格的路径 /xxx/{param}/yyy
    转换为 AMIS 模板风格的路径 /xxx/${param}/yyy
    """
    return re.sub(r'\{([^}]+)\}', r'${\1}', path)


class Api(BaseModel):
    """
    AMIS 中结构化的 API 配置对象。
    参考：https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/api
    """


    # === 基础属性 ===
    url: Optional[str] = Field(None, description="请求地址，支持模板字符串")
    method: Optional[Literal["get", "post", "put", "delete", "patch"]] = Field(None, description="请求方式，支持：get、post、put、delete、patch")
    data: Optional[Dict[str, Any]] = Field(None, description="请求数据，支持数据映射")
    headers: Optional[Dict[str, Any]] = Field(None, description="自定义请求头")
    
    # === 数据格式 ===
    data_type: Optional[Literal["json", "form", "form-data"]] = Field(None, description="数据体格式，默认为 json，可以配置成 form 或者 form-data")
    qs_options: Optional[Dict[str, Any]] = Field(None, description="当 dataType 为 form 或者 form-data 时有用")
    convert_key_to_path: Optional[bool] = Field(None, description="是否处理 key 中的路径，默认 true")
    
    # === 请求控制 ===
    send_on: Optional[str] = Field(None, description="请求条件，通过表达式配置")
    cache: Optional[int] = Field(None, description="接口缓存时间，单位毫秒")
    auto_refresh: Optional[bool] = Field(None, description="是否自动刷新接口")
    track_expression: Optional[str] = Field(None, description="跟踪变量表达式")
    
    # === 响应处理 ===
    adaptor: Optional[str] = Field(None, description="接收适配器，用于处理不符合要求的响应结构")
    request_adaptor: Optional[str] = Field(None, description="发送适配器，用于自定义请求处理")
    replace_data: Optional[bool] = Field(None, description="返回的数据是否替换掉当前的数据，默认为 false（即追加）")
    response_type: Optional[Literal["json", "blob"]] = Field(None, description="返回类型，如果是下载需要设置为 'blob'")
    response_data: Optional[Dict[str, Any]] = Field(None, description="对返回结果做映射")
    
    # === 提示信息 ===
    messages: Optional[Dict[str, Any]] = Field(None, description="配置接口请求的提示信息，messages.success 表示请求成功提示信息、messages.failed 表示请求失败提示信息")
    
    # === GraphQL ===
    graphql: Optional[str] = Field(None, description="GraphQL 查询")


class LazyAmisApiObject(BaseModel):
    """
    AMIS 中结构化的 API 配置对象，用于懒加载。
    """
    model_config = {
        "arbitrary_types_allowed": True
    }

    def __init__(self, api_view, data=None, headers=None, request_adaptor=None, adaptor=None, **kwargs):
        super().__init__(**kwargs)
        # 使用普通实例变量，而不是 Pydantic 字段，因为 Pydantic 不允许字段名以下划线开头
        self._api_view = api_view
        self._api_obj = None
        self._kwargs = {
            "data": data,
            "headers": headers,
            "request_adaptor": request_adaptor,
            "adaptor": adaptor,
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
            self._api_obj = Api(
                url=url,
                method=method,
                **self._kwargs
            )
        return self._api_obj.model_dump(by_alias, exclude_none, **kwargs)


def to_api(api_view) -> LazyAmisApiObject:
    return LazyAmisApiObject(api_view=api_view)

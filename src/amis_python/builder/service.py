from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import Field
from .base import BaseModel


class Service(BaseModel):
    """Service 组件，用于定义页面或组件的数据源服务
    
    详细文档: https://aisuda.bce.baidu.com/amis/zh-CN/components/service
    """
    type: Literal['service'] = Field('service', description="组件类型")
    api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="API 配置")
    init_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="初始数据 API 配置")
    data: Optional[Dict[str, Any]] = Field(None, description="静态数据")
    request_method: Optional[Literal['get', 'post', 'put', 'delete', 'patch']] = Field(None, description="请求方法")
    request_data: Optional[Dict[str, Any]] = Field(None, description="请求数据")
    request_headers: Optional[Dict[str, Any]] = Field(None, description="请求头")
    auto_request: Optional[bool] = Field(True, description="是否自动请求")
    silent_request: Optional[bool] = Field(False, description="是否静默请求")
    debounce: Optional[int] = Field(0, description="防抖时间")
    throttle: Optional[int] = Field(0, description="节流时间")
    cache: Optional[bool] = Field(False, description="是否缓存")
    cache_life: Optional[int] = Field(300, description="缓存时间")
    fetch_on: Optional[Dict[str, Any]] = Field(None, description="触发请求的事件配置")
    messages: Optional[Dict[str, Any]] = Field(None, description="消息配置")
    body: Optional[Union[Dict[str, Any], List[Dict[str, Any]],Any]] = Field(None, description="请求体")
    data_type: Optional[Literal['json', 'form']] = Field(None, description="数据类型")
    timeout: Optional[int] = Field(30000, description="超时时间")
    retries: Optional[int] = Field(0, description="重试次数")
    retry_interval: Optional[int] = Field(1000, description="重试间隔")
    transform: Optional[Dict[str, Any]] = Field(None, description="数据转换配置")
    response_data: Optional[Dict[str, Any]] = Field(None, description="响应数据处理")


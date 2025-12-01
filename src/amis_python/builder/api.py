from typing import Literal, Optional, Dict, Any

from pydantic import BaseModel, Field


class AmisApiObject(BaseModel):
    """
    AMIS 中结构化的 API 配置对象。
    参考：https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/api
    """
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
        alias="requestAdaptor",
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
from typing import Optional, Literal, Dict, Any, Union
from pydantic import Field

from amis_python.builder import BaseModel


class Wrapper(BaseModel):
    """
    amis Wrapper 包裹容器组件
    对应组件类型: wrapper
    文档地址: docs/zh-CN/components/wrapper.md
    """

    # ==================== 基本属性 ====================
    type: Literal["wrapper"] = Field("wrapper", description="指定为 Wrapper 渲染器")

    # ==================== 内容属性 ====================
    body: Optional[Union[Any, Dict[str, Any], str, list]] = Field(None, description="内容容器")

    # ==================== 样式属性 ====================
    class_name: Optional[str] = Field(None, description="外层 Dom 的类名")
    size: Optional[Literal["xs", "sm", "md", "lg", "none"]] = Field(None, description="支持: xs、sm、md、lg、none，用于调整内边距")
    style: Optional[Union[Dict[str, Any], str]] = Field(None, description="自定义样式，可以是对象或字符串")

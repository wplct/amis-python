from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder import BaseModel


class Container(BaseModel):
    """
    amis Container 容器组件
    对应组件类型: container
    文档地址: docs/zh-CN/components/container.md
    """

    # ==================== 基本属性 ====================
    type: Literal["container"] = Field("container", description="指定为 container 渲染器")
    
    # ==================== 容器属性 ====================
    class_name: Optional[str] = Field(None, description="外层 Dom 的类名")
    body_class_name: Optional[str] = Field(None, description="容器内容区的类名")
    wrapper_component: Optional[str] = Field("div", description="容器标签名")
    style: Optional[Dict[str, Any]] = Field(None, description="自定义样式")
    body: Optional[Union[str, List[Any], Dict[str, Any]]] = Field(None, description="容器内容")

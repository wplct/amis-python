from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder import BaseModel


class Flex(BaseModel):
    """
    amis Flex 布局组件
    对应组件类型: flex
    文档地址: docs/zh-CN/components/flex.md
    """

    # ==================== 基本属性 ====================
    type: Literal["flex"] = Field("flex", description="指定为 Flex 渲染器")
    
    # ==================== 布局属性 ====================
    class_name: Optional[str] = Field(None, description="css 类名")
    justify: Optional[Literal["start", "flex-start", "center", "end", "flex-end", "space-around", "space-between", "space-evenly"]] = Field(None, description="水平分布方式")
    align_items: Optional[Literal["stretch", "start", "flex-start", "flex-end", "end", "center", "baseline"]] = Field(None, description="垂直方向位置")
    style: Optional[Dict[str, Any]] = Field(None, description="自定义样式")
    items: Optional[Union[List[Any], Dict[str, Any]]] = Field(None, description="子组件列表")
    direction: Optional[Literal["row", "column"]] = Field(None, description="布局方向")
    mobile: Optional[Dict[str, Any]] = Field(None, description="移动端配置")

from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from .base import BaseModel
from .action import Action


class ButtonGroup(BaseModel):
    """
    amis ButtonGroup 按钮组组件
    对应组件类型: button-group
    文档地址: docs/zh-CN/components/button-group.md
    
    用于将多个按钮组合在一起，形成按钮组。
    """

    # ==================== 基本属性 ====================
    type: Literal["button-group"] = Field("button-group", description="指定为按钮组组件")
    buttons: List[Any] = Field(..., description="按钮组中的按钮列表")
    className: Optional[str] = Field(None, description="CSS 类名")
    direction: Optional[Literal["horizontal", "vertical"]] = Field(None, description="按钮组方向")
    justify: Optional[Literal["start", "center", "end", "space-between"]] = Field(None, description="按钮对齐方式")
    size: Optional[Literal["xs", "sm", "md", "lg"]] = Field(None, description="按钮组大小")
    disabled: Optional[bool] = Field(None, description="是否禁用整个按钮组")
    visible: Optional[bool] = Field(None, description="是否显示")
    hidden: Optional[bool] = Field(None, description="是否隐藏")

from __future__ import annotations
from typing import List, Optional, Union, Literal
from pydantic import Field

from .base import BaseBuilder
from .button import ButtonBuilder


class DropdownButtonBuilder(BaseBuilder):
    """
    构建 AMIS 下拉按钮配置对象，对应 <DropdownButton> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/button#dropdown-button-%E4%B8%8B%E6%8B%89%E6%8C%89%E9%92%AE
    
    示例：
        dropdown_button = DropdownButtonBuilder(
            label="下拉按钮",
            buttons=[
                ButtonBuilder(label="按钮1"),
                ButtonBuilder(label="按钮2")
            ]
        )
    """
    type: Literal["dropdown-button"] = "dropdown-button"
    
    # 按钮显示文本
    label: str = Field(..., description="按钮显示文本")
    
    # 下拉按钮列表
    buttons: List[Union[ButtonBuilder, dict]] = Field(..., description="下拉按钮列表")
    
    # 其他属性
    class_name: Optional[str] = Field(None, description="指定添加 dropdown-button 类名")
    size: Optional[Literal["xs", "sm", "md", "lg"]] = Field(None, description="设置按钮大小")
    level: Optional[Literal["link", "primary", "enhance", "secondary", "info", "success", "warning", "danger", "light", "dark", "default"]] = Field("default", description="设置按钮样式")
    placement: Optional[Literal["top", "bottom", "left", "right"]] = Field("bottom", description="下拉菜单位置")

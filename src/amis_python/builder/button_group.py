from __future__ import annotations
from typing import List, Optional, Union, Literal

from .base import BaseBuilder
from .button import ButtonBuilder


class ButtonGroupBuilder(BaseBuilder):
    """
    构建 AMIS 按钮组配置对象，对应 <ButtonGroup> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/button#button-group-%E6%8C%89%E9%92%AE%E7%BB%84
    
    示例：
        button_group = ButtonGroupBuilder(
            buttons=[
                ButtonBuilder(label="按钮1"),
                ButtonBuilder(label="按钮2")
            ]
        )
    """
    type: Literal["button-group"] = "button-group"
    
    # 按钮列表
    buttons: List[Union[ButtonBuilder, dict]]  # 按钮列表
    
    # 其他属性
    class_name: Optional[str] = None  # 指定添加 button-group 类名
    size: Optional[Literal["xs", "sm", "md", "lg"]] = None  # 设置按钮组大小

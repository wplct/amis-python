from __future__ import annotations
from typing import List, Optional, Union
from pydantic import Field

from .base import BaseBuilder
from .button import ButtonBuilder


class ButtonToolbarBuilder(BaseBuilder):
    """
    构建 AMIS 按钮工具栏配置对象，对应 <ButtonToolbar> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/button#button-toolbar-%E6%8C%89%E9%92%AE%E5%B7%A5%E5%85%B7%E6%9D%A1
    
    示例：
        button_toolbar = ButtonToolbarBuilder(
            buttons=[
                ButtonBuilder(label="按钮1"),
                ButtonBuilder(label="按钮2")
            ]
        )
    """
    type: str = "button-toolbar"
    
    # 按钮列表
    buttons: List[Union[ButtonBuilder, dict]] = Field(..., description="按钮列表")
    
    # 其他属性
    class_name: Optional[str] = Field(None, description="指定添加 button-toolbar 类名")
    align: Optional[str] = Field(None, description="按钮对齐方式")

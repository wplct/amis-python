from __future__ import annotations
from typing import Optional, Literal

from .base import BaseBuilder


class ColorBuilder(BaseBuilder):
    """
    构建 AMIS 颜色选择器配置对象，对应 <Color> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/form/color
    
    示例：
        color = ColorBuilder(
            value="#108cee"
        )
    """
    type: Literal["color"] = "color"
    
    # 颜色值
    value: Optional[str] = None  # 颜色值
    
    # 其他属性
    name: Optional[str] = None  # 字段名称
    label: Optional[str] = None  # 字段标签
    disabled: Optional[bool] = False  # 是否禁用
    required: Optional[bool] = False  # 是否必填
    class_name: Optional[str] = None  # 指定添加 color 类名

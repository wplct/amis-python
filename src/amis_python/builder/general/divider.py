from __future__ import annotations
from typing import Optional, Literal, Any

from ..base import BaseBuilder


class DividerBuilder(BaseBuilder):
    """
    构建 AMIS 分割线配置对象，对应 <Divider> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/divider
    
    示例：
        divider = DividerBuilder(
            line_style="dashed",
            color="#e8e8e8",
            title="分割线标题",
            title_position="center"
        )
    """
    type: Literal["divider"] = "divider"
    
    # 外层 Dom 的类名
    class_name: Optional[str] = None
    
    # 分割线的样式，支持dashed和solid
    line_style: Optional[Literal["dashed", "solid"]] = "solid"
    
    # 分割线的方向，支持horizontal和vertical
    direction: Optional[Literal["horizontal", "vertical"]] = "horizontal"
    
    # 分割线的颜色
    color: Optional[str] = None
    
    # 分割线的旋转角度
    rotate: Optional[float] = None
    
    # 分割线的标题
    title: Optional[Any] = None
    
    # 分割线的标题类名
    title_class_name: Optional[str] = None
    
    # 分割线的标题位置，支持left、center和right
    title_position: Optional[Literal["left", "center", "right"]] = "center"

__all__ = [
    "DividerBuilder"
]
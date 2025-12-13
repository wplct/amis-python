from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder.action import Action


class Button(Action):
    """
    amis Button 按钮组件
    对应组件类型: button
    文档地址: docs/zh-CN/components/button.md
    
    Button 实际上是 Action 的别名，更多用法见 Action 组件
    """

    # ==================== 基本属性 ====================
    type: Literal["button"] = Field("button", description="指定为按钮组件")
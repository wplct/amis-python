from __future__ import annotations
from typing import List, Optional, Union

from .base import BaseBuilder


class ActionContainerBuilder(BaseBuilder):
    """
    构建 AMIS 动作容器配置对象，对应 <Action> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action
    
    示例：
        action_container = ActionContainerBuilder(
            body=[
                {"type": "color", "value": "#108cee"}
            ]
        )
    """
    type: str = "action"
    
    # 容器内容
    body: List[Union[BaseBuilder, dict]]  # 容器内容
    
    # 其他属性
    class_name: Optional[str] = None  # 指定添加 action 类名
    disabled: Optional[bool] = False  # 是否禁用

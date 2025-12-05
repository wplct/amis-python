from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, Literal

from amis_python.builder.base import BaseBuilder
from amis_python.builder.utils import camelize


class ActionBuilder(BaseBuilder):
    """
    构建 AMIS 动作配置对象的基类
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/docs/concepts/event-action
    """
    # 动作类型，由用户指定，不使用固定Literal，以支持所有AMIS动作类型
    type: Optional[str] = None
    
    # 基础属性
    action_type: str  # 动作类型，如dialog、ajax、link等
    label: Optional[str] = None  # 动作显示文本
    
    # 其他通用属性
    confirm_text: Optional[str] = None  # 确认提示文本
    close: Optional[bool] = None  # 是否关闭当前组件
    reload: Optional[Union[bool, str]] = None  # 是否刷新指定组件


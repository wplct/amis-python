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
    
    def __init__(self, action_type: str, **kwargs):
        # 处理 actionType 和 type 的兼容
        if "type" in kwargs and "action_type" not in kwargs:
            kwargs["action_type"] = kwargs["type"]
        
        # 设置必填字段
        self.action_type = action_type
        
        # 设置可选字段
        self.label = kwargs.pop("label", None)
        self.confirm_text = kwargs.pop("confirm_text", None)
        self.close = kwargs.pop("close", None)
        self.reload = kwargs.pop("reload", None)
        
        # 设置额外字段
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        super().__init__(**kwargs)

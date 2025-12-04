from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field

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
    action_type: str = Field(..., description="动作类型，如dialog、ajax、link等", alias="actionType")
    label: Optional[str] = Field(None, description="动作显示文本")
    
    # 其他通用属性
    confirm_text: Optional[str] = Field(None, description="确认提示文本", alias="confirmText")
    close: Optional[bool] = Field(None, description="是否关闭当前组件")
    reload: Optional[Union[bool, str]] = Field(None, description="是否刷新指定组件")
    
    # 支持动态添加其他属性
    model_config = {
        "extra": "allow",  # 允许添加额外属性
        "validate_default": True,
        "populate_by_name": True,
        "alias_generator": camelize,
    }

    def __init__(self, **data):
        # 处理 actionType 和 type 的兼容
        if "type" in data and "action_type" not in data:
            data["action_type"] = data["type"]
        super().__init__(**data)

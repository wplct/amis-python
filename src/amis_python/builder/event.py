from __future__ import annotations
from typing import Any, Dict, List
from pydantic import BaseModel, Field

# 导入现有工具和配置
from .utils import camelize


class EventAction(BaseModel):
    """
    事件动作配置
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/docs/concepts/event-action
    """
    actions: List[Dict[str, Any]] = Field(..., description="事件对应的响应动作集合")
    
    model_config = {
        "validate_default": True,
        "populate_by_name": True,
        "alias_generator": camelize,
    }

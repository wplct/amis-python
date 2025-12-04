from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

# 导入现有工具和配置
from .utils import camelize


class AmisEvent(str, Enum):
    """
    AMIS 事件名称枚举
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/docs/concepts/event-action
    """
    click = "click"
    change = "change"
    submit = "submit"
    reset = "reset"
    focus = "focus"
    blur = "blur"
    load = "load"
    ready = "ready"
    validate = "validate"
    itemClick = "itemClick"
    itemChange = "itemChange"
    success = "success"
    error = "error"
    beforeSubmit = "beforeSubmit"
    afterSubmit = "afterSubmit"
    beforeReset = "beforeReset"
    afterReset = "afterReset"
    mouseenter = "mouseenter"
    mouseleave = "mouseleave"


class EventAction(BaseModel):
    """
    事件动作配置
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/docs/concepts/event-action
    """
    actions: List[Any] = Field(..., description="事件对应的响应动作集合")
    
    model_config = {
        "validate_default": True,
        "populate_by_name": True,
        "alias_generator": camelize,
    }

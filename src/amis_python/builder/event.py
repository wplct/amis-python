from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Literal

# 导入现有工具和配置
from .utils import camelize
from .. import BaseBuilder


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


class EventAction(BaseBuilder):
    """
    事件动作配置
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/docs/concepts/event-action
    """
    type:Literal["event"] = "event"

    actions: List[Any]  # 事件对应的响应动作集合

    def __init__(self, actions: List[Any], **kwargs):
        self.actions = actions
        super().__init__(**kwargs)

# base.py
"""
Pydantic 基础构造器模块，为所有 amis 节点提供统一的序列化能力。

核心功能：
- 所有 amis 组件继承自 BaseBuilder；
- 自动递归将嵌套的组件转换为符合 amis 规范的 JSON 字典；
- 强制每个组件必须声明 type 字段（由子类以 Literal 形式提供）。

注意：type 字段不再通过抽象属性强制，而是作为 Pydantic 模型字段，
      由子类使用 Literal 显式定义，确保序列化能正确进行。
"""

from abc import ABC
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict

from .utils import camelize


class BaseBuilder(BaseModel, ABC):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_default=True,
        populate_by_name=True,
        alias_generator=camelize,
    )

    # type 由子类以 Literal 字段形式提供，确保是 Pydantic 字段
    type: str
    
    # 事件动作配置
    on_event: Optional[Dict[str, Any]] = Field(None, description="事件动作配置")
    
    def add_action(
        self, 
        event_name: Union[str, 'AmisEvent'],
        *actions: 'ActionBuilder'
    ) -> 'BaseBuilder':
        """
        动态添加事件动作
        
        Args:
            event_name: 事件名称，如 "click"、"change" 等，或 AmisEvent 枚举
            actions: 动作列表，每个动作可以是字典或 ActionBuilder 实例
            
        Returns:
            self: 支持链式调用
        """
        from .event import AmisEvent
        from .action.action import ActionBuilder
        
        # 初始化 on_event 字典（如果不存在）
        if self.on_event is None:
            self.on_event = {}
        
        # 处理事件名称为枚举的情况
        if isinstance(event_name, AmisEvent):
            event_name_str = event_name.value
        else:
            event_name_str = event_name
        
        # 处理动作列表，将 ActionBuilder 实例转换为字典
        processed_actions = []
        for action in actions:
            if isinstance(action, ActionBuilder):
                processed_actions.append(action.to_schema())
            else:
                processed_actions.append(action)
        
        # 创建 EventAction 对象
        from .event import EventAction
        event_action = EventAction(actions=processed_actions)
        
        # 添加到 on_event 字典
        if event_name_str in self.on_event:
            self.on_event[event_name_str].actions.extend(event_action.actions)
        else:
            self.on_event[event_name_str] = event_action
        
        # 返回 self 支持链式调用
        return self

    def to_schema(
            self,
            *,
            by_alias: bool = True,
            exclude_none: bool = True,
            **dump_kwargs: Any,
    ) -> Dict[str, Any]:
        result = {}
        for field_name, field_info in self.model_fields.items():
            # 获取实际属性值（可能是 BaseBuilder 实例）
            value = getattr(self, field_name)

            # 处理别名
            key = camelize(field_name) if by_alias else field_name

            # 排除 None
            if exclude_none and value is None:
                continue

            # 如果是 BaseBuilder 且要求序列化，则调用 to_schema
            if  isinstance(value, BaseBuilder):
                value = value.to_schema(
                    by_alias=by_alias,
                    exclude_none=exclude_none,
                )


            # 处理list
            if isinstance(value, list):
                value = [
                    v.to_schema(
                        by_alias=by_alias,
                        exclude_none=exclude_none,
                    )
                    if isinstance(v, BaseBuilder)
                    else v
                    for v in value
                ]
            # 处理dict
            elif isinstance(value, dict):
                value = {
                    k: v.to_schema(
                        by_alias=by_alias,
                        exclude_none=exclude_none,
                    )
                    if isinstance(v, BaseBuilder)
                    else v
                    for k, v in value.items()
                }
            result[key] = value
        return result


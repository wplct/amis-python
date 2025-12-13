# base.py
"""
Pydantic 基础构造器模块，为所有 amis 节点提供统一的序列化能力。

核心功能：
- 所有 amis 组件继承自 BaseModel；
- 自动递归将嵌套的组件转换为符合 amis 规范的 JSON 字典；
- 强制每个组件必须声明 type 字段（由子类以 Literal 形式提供）。

注意：type 字段不再通过抽象属性强制，而是作为 Pydantic 模型字段，
      由子类使用 Literal 显式定义，确保序列化能正确进行。
"""
from typing import Any, Dict, List, Optional, Union, get_origin, get_args, Literal


from .utils import camelize




from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field


def camelize(snake_str: str) -> str:
    """将 snake_case 转换为 camelCase，例如 label_width → labelWidth"""
    components = snake_str.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])

class BaseModel(PydanticBaseModel):
    """amis 组件通用基类，统一处理序列化行为"""
    model_config = ConfigDict(
        alias_generator=camelize,
        populate_by_name=True,
        extra='allow'
    )
    
    # ==================== 事件配置 ====================
    on_event: Optional[Dict[str, Any]] = Field(None, description="事件动作配置")
    
    def model_dump(self,exclude_none=True,by_alias=True,**kwargs):
        return super().model_dump(exclude_none=exclude_none,by_alias=by_alias,**kwargs)
    
    def model_dump_json(self,*,exclude_none=True,by_alias=True,**kwargs) -> str:
        return super().model_dump_json(exclude_none=exclude_none,by_alias=by_alias,**kwargs)
    
    def add_action(self, event_name: str, action: 'BaseModel') -> 'BaseModel':
        """
        添加事件动作
        
        Args:
            event_name: 事件名称，如 'click'、'change' 等
            action: Action 对象，包含动作类型和参数
        
        Returns:
            self，支持链式调用
        """
        # 确保 onEvent 属性存在
        if not self.on_event:
            self.on_event = {}
        
        # 确保事件存在并初始化 actions 列表
        if event_name not in self.on_event:
            self.on_event[event_name] = {'actions': []}
        
        # 直接添加 action 对象到 actions 列表中
        self.on_event[event_name]['actions'].append(action)
        
        return self
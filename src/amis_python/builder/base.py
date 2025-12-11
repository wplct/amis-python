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
import types
from abc import ABC
from typing import Any, Dict, List, Optional, Union, get_origin, get_args
from .utils import camelize


class BaseBuilder:
    type: str  # 类变量 or 实例变量
    on_event: Optional[Dict[str, Any]] = None  # 事件动作配置

    def __init__(self, **kwargs):
        # 使用传入的 kwargs 更新属性
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_schema(self, by_alias=True, exclude_none=True):
        result = {}
        # 遍历所有注解的字段（包括类属性）

        for key in [k for k in dir(self) if not callable(getattr(self, k))]:
            if key.startswith('_'):
                continue
            if not hasattr(self, key):
                continue
            value = getattr(self, key)
            if exclude_none and value is None:
                continue
            k = camelize(key) if by_alias else key
            result[k] = self._serialize_value(value, by_alias, exclude_none)
        return result

    def _serialize_value(self, value, by_alias, exclude_none):
        if isinstance(value, BaseBuilder):
            return value.to_schema(by_alias, exclude_none)
        elif isinstance(value, list):
            return [self._serialize_value(v, by_alias, exclude_none) for v in value]
        elif isinstance(value, dict):
            return {k: self._serialize_value(v, by_alias, exclude_none) for k, v in value.items()}
        else:
            return value

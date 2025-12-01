# base.py
"""
Pydantic-v2 基础构造器模块，为所有 amis 节点提供统一的序列化能力。

核心功能：
- 所有 amis 组件继承自 BaseBuilder；
- 自动递归将嵌套的组件转换为符合 amis 规范的 JSON 字典；
- 支持通过 extra_schema() 钩子追加动态字段；
- 强制每个组件必须声明 type 字段（由子类以 Literal 形式提供）。

注意：type 字段不再通过抽象属性强制，而是作为 Pydantic 模型字段，
      由子类使用 Literal 显式定义，确保 model_dump() 能正确序列化。
"""

from abc import ABC
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict
from typing_extensions import Literal  # 兼容 Python <3.8


class BaseBuilder(BaseModel, ABC):
    # 启用 validate_default 确保 default_factory 创建的对象也被正确验证和序列化
    model_config = ConfigDict(validate_default=True)

    # type 由子类以 Literal 字段形式提供，确保是 Pydantic 字段
    type: str

    def to_schema(
            self,
            *,
            by_alias: bool = True,
            exclude_none: bool = True,
            **dump_kwargs: Any,
    ) -> Dict[str, Any]:
        # 1. 使用 model_dump(exclude_none=False) 获取所有字段，
        #    并让它进行默认的字典序列化（如您遇到的问题）。
        #    如果必须避免自动序列化，我们绕过 model_dump。

        # 绕过 model_dump()，直接从实例中获取字段值
        raw = {}
        for name, field_info in self.__class__.model_fields.items():
            # 检查字段是否已设置（如果使用 Field(default_factory) 则应存在）
            if name in self.__dict__:
                value = self.__dict__[name]  # 获取原始值，可能是一个 BaseBuilder 实例

                # 排除 None 值（如果用户在 to_schema 中设置了 exclude_none=True）
                if exclude_none and value is None:
                    continue

                # 处理别名
                key = field_info.alias if by_alias and field_info.alias else name
                raw[key] = value

        # 2. 合并额外字段
        extra = self.extra_schema()
        if extra:
            raw.update(extra)

        # 3. 递归展开所有嵌套的 BaseBuilder（此时 raw 中包含 BaseBuilder 实例）
        return self._walk_children(raw, exclude_none=exclude_none)  # 假设 _walk_children 已修改以处理 exclude_none

    def extra_schema(self) -> Optional[Dict[str, Any]]:
        return None

    def _walk_children(self, obj: Any, exclude_none: bool = True) -> Any:

        # 1. 处理 BaseBuilder 实例
        if isinstance(obj, BaseBuilder):
            # 递归调用 to_schema，并传递 exclude_none 标志
            result = obj.to_schema(exclude_none=exclude_none)
            # 如果 to_schema 返回的是 None (理论上不应发生，但作为 BaseBuilder 的返回值，保留检查)
            if exclude_none and result is None:
                return None
            return result

        # 2. 处理字典
        elif isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                # 递归处理子值
                child = self._walk_children(v, exclude_none=exclude_none)

                # 如果 exclude_none 为 True 且子值是 None，则跳过此键值对
                if exclude_none and child is None:
                    continue

                result[k] = child
            return result

        # 3. 处理列表/元组
        elif isinstance(obj, (list, tuple)):
            result = []
            for item in obj:
                # 递归处理列表项
                child = self._walk_children(item, exclude_none=exclude_none)

                # 如果 exclude_none 为 True 且列表项是 None，则跳过此项
                if exclude_none and child is None:
                    continue

                result.append(child)
            return result

        # 4. 处理 None 值 (只在最深层出现 None 时处理)
        if exclude_none and obj is None:
            return None

        # 5. 返回其他基本类型的值
        return obj
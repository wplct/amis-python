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
from pydantic import BaseModel
from typing_extensions import Literal  # 兼容 Python <3.8


# 动态检测 Pydantic 版本，选择合适的配置方式
try:
    # 检查是否是 Pydantic v2
    from pydantic import ConfigDict
    IS_PYDANTIC_V2 = True
except ImportError:
    # Pydantic v1
    IS_PYDANTIC_V2 = False
def camelize(name: str) -> str:
    """snake_case -> camelCase"""
    parts = name.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

class BaseBuilder(BaseModel, ABC):
    if IS_PYDANTIC_V2:                       # ----------- Pydantic V2 -----------
        model_config = {
            "validate_default": True,
            "populate_by_name": True,        # 允许用原始字段名反序列化
            "alias_generator": camelize,     # 👈 关键：自动生成驼峰别名
        }
    else:                                    # ----------- Pydantic V1 -----------
        class Config:
            validate_default = True
            allow_population_by_field_name = True
            alias_generator = camelize       # 👈 关键：自动生成驼峰别名

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
        if IS_PYDANTIC_V2:
            raw = self.model_dump(exclude_none=exclude_none,by_alias=by_alias,**dump_kwargs)
        else:
            raw = self.dict(exclude_none=exclude_none,by_alias=by_alias,**dump_kwargs)
        # 3. 递归展开所有嵌套的 BaseBuilder（此时 raw 中包含 BaseBuilder 实例）
        return self._walk_children(raw, exclude_none=exclude_none)  # 假设 _walk_children 已修改以处理 exclude_none

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
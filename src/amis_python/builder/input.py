from __future__ import annotations
from typing import Optional, Literal

from .base import BaseBuilder


class InputTextBuilder(BaseBuilder):
    """
    构建 AMIS 文本输入框配置对象，对应 <InputText> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/form/input-text
    
    示例：
        input_text = InputTextBuilder(
            name="name",
            label="名称"
        )
    """
    type: Literal["input-text"] = "input-text"
    
    # 字段名称
    name: str  # 字段名称
    
    # 字段标签
    label: str  # 字段标签
    
    # 其他属性
    value: Optional[str] = None  # 默认值
    placeholder: Optional[str] = None  # 占位提示文本
    disabled: Optional[bool] = False  # 是否禁用
    read_only: Optional[bool] = False  # 是否只读
    required: Optional[bool] = False  # 是否必填
    class_name: Optional[str] = None  # 指定添加 input-text 类名


class InputEmailBuilder(BaseBuilder):
    """
    构建 AMIS 邮箱输入框配置对象，对应 <InputEmail> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/form/input-email
    
    示例：
        input_email = InputEmailBuilder(
            name="email",
            label="邮箱"
        )
    """
    type: Literal["input-email"] = "input-email"
    
    # 字段名称
    name: str  # 字段名称
    
    # 字段标签
    label: str  # 字段标签
    
    # 其他属性
    value: Optional[str] = None  # 默认值
    placeholder: Optional[str] = None  # 占位提示文本
    disabled: Optional[bool] = False  # 是否禁用
    read_only: Optional[bool] = False  # 是否只读
    required: Optional[bool] = False  # 是否必填
    class_name: Optional[str] = None  # 指定添加 input-email 类名

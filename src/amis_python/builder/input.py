from __future__ import annotations
from typing import Optional, Literal
from pydantic import Field

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
    name: str = Field(..., description="字段名称")
    
    # 字段标签
    label: str = Field(..., description="字段标签")
    
    # 其他属性
    value: Optional[str] = Field(None, description="默认值")
    placeholder: Optional[str] = Field(None, description="占位提示文本")
    disabled: Optional[bool] = Field(False, description="是否禁用")
    read_only: Optional[bool] = Field(False, description="是否只读", alias="readOnly")
    required: Optional[bool] = Field(False, description="是否必填")
    class_name: Optional[str] = Field(None, description="指定添加 input-text 类名")

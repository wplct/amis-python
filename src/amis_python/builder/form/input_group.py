from typing import Optional, Literal, Dict, Any, List, Union
from pydantic import Field

from amis_python.builder.form.form_item import FormItem


class InputGroup(FormItem):
    """
    amis InputGroup 输入框组合组件
    对应组件类型: input-group
    文档地址: docs/zh-CN/components/form/input-group.md
    """

    # ==================== 基本属性 ====================
    type: Literal["input-group"] = Field("input-group", description="指定为输入框组合组件")
    
    # ==================== 核心属性 ====================
    body: Optional[List[Dict[str, Any]]] = Field(None, description="表单项集合")
    
    # ==================== 校验相关属性 ====================
    validation_config: Optional[Dict[str, Any]] = Field(None, description="校验相关配置")
    
    # ==================== 样式属性 ====================
    class_name: Optional[str] = Field(None, description="CSS 类名")

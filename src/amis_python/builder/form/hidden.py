from typing import Optional, Literal, Any
from pydantic import Field

from amis_python.builder.form.form_item import FormItem


class Hidden(FormItem):
    """
    amis Hidden 隐藏字段组件
    对应组件类型: hidden
    文档地址: docs/zh-CN/components/form/hidden.md
    """

    # ==================== 基本属性 ====================
    type: Literal["hidden"] = Field("hidden", description="指定为隐藏字段组件")

    # ==================== 值属性 ====================
    value: Optional[Any] = Field(None, description="隐藏字段的值")

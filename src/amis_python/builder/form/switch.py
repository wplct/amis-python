from typing import Optional, Literal, Dict, Any, Union
from pydantic import Field

from amis_python.builder.form.form_item import FormItem


class Switch(FormItem):
    """
    amis Switch 开关组件
    对应组件类型: switch
    文档地址: docs/zh-CN/components/form/switch.md
    """

    # ==================== 基本属性 ====================
    type: Literal["switch"] = Field("switch", description="指定为开关组件")

    # ==================== 状态相关属性 ====================
    checked_value: Optional[Any] = Field(None, description="选中时的值，默认值为 True")
    un_checked_value: Optional[Any] = Field(None, description="未选中时的值，默认值为 False")
    checked: Optional[Any] = Field(None, description="是否默认选中")
    disabled: Optional[Any] = Field(None, description="是否禁用")

    # ==================== 样式相关属性 ====================
    size: Optional[Literal["sm", "md", "lg"]] = Field(None, description="开关大小，默认值为 'md'")
    on_text: Optional[str] = Field(None, description="选中时显示的文本，默认值为 '开启'")
    off_text: Optional[str] = Field(None, description="未选中时显示的文本，默认值为 '关闭'")
    on_border_color: Optional[str] = Field(None, description="选中时边框颜色")
    off_border_color: Optional[str] = Field(None, description="未选中时边框颜色")
    on_background_color: Optional[str] = Field(None, description="选中时背景颜色")
    off_background_color: Optional[str] = Field(None, description="未选中时背景颜色")

    # ==================== 事件相关属性 ====================
    change_event: Optional[Dict[str, Any]] = Field(None, description="开关状态变化事件")

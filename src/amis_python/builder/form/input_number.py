from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder.form.form_item import FormItem


class InputNumber(FormItem):
    """
    amis InputNumber 数字输入框组件
    对应组件类型: input-number
    文档地址: docs/zh-CN/components/form/input-number.md
    """

    # ==================== 基本属性 ====================
    type: Literal["input-number"] = Field("input-number", description="指定为数字输入框组件")

    # ==================== 数值范围属性 ====================
    min: Optional[Union[int, float, str, Dict[str, Any]]] = Field(None, description="最小值")
    max: Optional[Union[int, float, str, Dict[str, Any]]] = Field(None, description="最大值")
    step: Optional[float] = Field(None, description="步长")
    precision: Optional[int] = Field(None, description="精度，即小数点后几位，支持 0 和正整数")

    # ==================== 显示属性 ====================
    show_steps: Optional[bool] = Field(None, description="是否显示上下点击按钮，默认值为 true")
    read_only: Optional[bool] = Field(None, description="只读")
    prefix: Optional[str] = Field(None, description="前缀")
    suffix: Optional[str] = Field(None, description="后缀")
    kilobit_separator: Optional[bool] = Field(None, description="千分分隔，默认值为 false")

    # ==================== 单位属性 ====================
    unit_options: Optional[List[str]] = Field(None, description="单位选项")

    # ==================== 高级属性 ====================
    keyboard: Optional[bool] = Field(None, description="键盘事件（方向上下），默认值为 true")
    big: Optional[bool] = Field(None, description="是否使用大数，默认值为 false")
    display_mode: Optional[Literal["base", "enhance"]] = Field(None, description="样式类型，默认值为 'base'")
    border_mode: Optional[Literal["full", "half", "none"]] = Field(None, description="边框模式，全边框，还是半边框，或者没边框，默认值为 'full'")

    # ==================== 重置属性 ====================
    reset_value: Optional[Union[int, float, str]] = Field(None, description="清空输入内容时，组件值将设置为 resetValue，默认值为 ''")
    clear_value_on_empty: Optional[bool] = Field(None, description="内容为空时从数据域中删除该表单项对应的值，默认值为 false")
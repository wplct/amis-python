from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder.form.form_item import FormItem


class InputText(FormItem):
    """
    amis InputText 输入框组件
    对应组件类型: input-text
    文档地址: docs/zh-CN/components/form/input-text.md
    """

    # ==================== 基本属性 ====================
    type: Literal["input-text"] = Field("input-text", description="指定为输入框组件")

    # ==================== 选项相关属性 ====================
    options: Optional[Union[List[Dict[str, Any]], List[str]]] = Field(None, description="选项组")
    source: Optional[Union[str, Dict[str, Any]]] = Field(None, description="动态选项组")
    auto_complete: Optional[Union[str, Dict[str, Any]]] = Field(None, description="自动补全")
    multiple: Optional[bool] = Field(None, description="是否多选")
    delimiter: Optional[str] = Field(None, description="拼接符，默认值为 ','")
    label_field: Optional[str] = Field(None, description="选项标签字段，默认值为 'label'")
    value_field: Optional[str] = Field(None, description="选项值字段，默认值为 'value'")
    join_values: Optional[bool] = Field(None, description="拼接值，默认值为 True")
    extract_value: Optional[bool] = Field(None, description="提取多选值，默认值为 False")

    # ==================== 附加组件属性 ====================
    add_on: Optional[Dict[str, Any]] = Field(None, description="输入框附加组件")

    # ==================== 文本处理属性 ====================
    trim_contents: Optional[bool] = Field(None, description="是否去除首尾空白文本")
    clear_value_on_empty: Optional[bool] = Field(None, description="文本内容为空时去掉这个值")
    creatable: Optional[bool] = Field(None, description="是否可以创建，默认为可以，除非设置为 false 即只能选择选项中的值")
    clearable: Optional[bool] = Field(None, description="是否可清除")
    reset_value: Optional[str] = Field(None, description="清除后设置此配置项给定的值，默认值为 ''")
    prefix: Optional[str] = Field(None, description="前缀，默认值为 ''")
    suffix: Optional[str] = Field(None, description="后缀，默认值为 ''")
    show_counter: Optional[bool] = Field(None, description="是否显示计数器")
    min_length: Optional[int] = Field(None, description="限制最小字数")
    max_length: Optional[int] = Field(None, description="限制最大字数")

    # ==================== 转换属性 ====================
    transform: Optional[Dict[str, Any]] = Field(None, description="自动转换值，可选 transform: { lowerCase: true, upperCase: true }")

    # ==================== 样式属性 ====================
    border_mode: Optional[Literal["full", "half", "none"]] = Field(None, description="输入框边框模式，全边框，还是半边框，或者没边框，默认值为 'full'")
    input_control_class_name: Optional[str] = Field(None, description="control 节点的 CSS 类名")
    native_input_class_name: Optional[str] = Field(None, description="原生 input 标签的 CSS 类名")
    native_auto_complete: Optional[str] = Field(None, description="原生 input 标签的 autoComplete 属性，默认值为 'off'")

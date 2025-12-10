from __future__ import annotations
from typing import Optional, Literal, Any, Dict

from ..base import BaseBuilder


class FormItemBuilder(BaseBuilder):
    """
    构建 AMIS 表单项配置对象，对应 <FormItem> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/form/formitem
    
    示例：
        form_item = FormItemBuilder(
            name="name",
            label="名称"
        )
    """
    # 基本属性
    name: str  # 字段名，标识表单数据域中，当前表单项值的key
    label: Optional[str] = None  # 表单项标签
    type: Optional[str] = None  # 表单项类型
    
    # 展示属性
    class_name: Optional[str] = None  # 表单最外层类名
    input_class_name: Optional[str] = None  # 表单控制器类名
    label_class_name: Optional[str] = None  # label 的类名
    mode: Optional[Literal["horizontal", "vertical", "inline"]] = None  # 表单项模式
    size: Optional[Literal["xs", "sm", "md", "lg", "full"]] = None  # 表单项尺寸
    
    # 状态属性
    disabled: Optional[bool] = None  # 是否禁用，默认：False
    disabled_on: Optional[str] = None  # 禁用条件表达式
    visible: Optional[bool] = None  # 是否可见，默认：True
    visible_on: Optional[str] = None  # 可见条件表达式
    required: Optional[bool] = None  # 是否必填，默认：False
    required_on: Optional[str] = None  # 必填条件表达式
    
    # 静态展示属性
    static: Optional[bool] = None  # 是否静态展示，默认：False
    static_on: Optional[str] = None  # 静态展示条件表达式
    static_schema: Optional[Any] = None  # 自定义静态展示方式
    static_class_name: Optional[str] = None  # 静态展示时的类名
    static_label_class_name: Optional[str] = None  # 静态展示时的 Label 类名
    static_input_class_name: Optional[str] = None  # 静态展示时的 value 的类名
    
    # 校验属性
    validations: Optional[Any] = None  # 表单项值格式验证
    validation_errors: Optional[Dict[str, str]] = None  # 自定义校验信息
    validate_api: Optional[Any] = None  # 表单校验接口
    validate_on_change: Optional[bool] = None  # 值变化时是否校验，默认：False
    
    # 自动填充属性
    auto_fill: Optional[Any] = None  # 自动填充配置
    
    # 其他属性
    strict_mode: Optional[bool] = None  # 是否严格模式，通过配置 false 可以及时获取所有表单里面的数据，默认：True
    submit_on_change: Optional[bool] = None  # 是否值变化时提交表单，默认：False
    clear_value_on_hidden: Optional[bool] = None  # 隐藏时是否删除值，默认：False
    placeholder: Optional[str] = None  # 占位提示文本
    description: Optional[str] = None  # 表单项描述
    value: Optional[Any] = None  # 默认值

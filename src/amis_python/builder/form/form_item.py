from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder import BaseModel


class FormItem(BaseModel):
    """
    amis FormItem 普通表单项
    对应组件类型: 派生自 FormItem 的各种表单项类型
    文档地址: https://aisuda.bce.baidu.com/amis/zh-CN/components/form/formitem
    """

    # ==================== 基本属性 ====================
    type: Optional[str] = Field(None, description="表单项类型")
    name: Optional[str] = Field(None, description="表单项名称，标识表单数据域中当前表单项值的key")
    label: Optional[Union[str, bool]] = Field(None, description="表单项标签，设置为false时不显示标签且清除空间")
    label_remark: Optional[Union[str, Dict[str, Any]]] = Field(None, description="标签提示，支持字符串或对象配置")
    mode: Optional[str] = Field(None, description="表单项模式，如 'inline' 表示内联模式")
    size: Optional[Literal['xs', 'sm', 'md', 'lg', 'full']] = Field(None, description="表单项尺寸")
    description: Optional[str] = Field(None, description="表单项描述")

    # ==================== 状态属性 ====================
    disabled: Optional[bool] = Field(None, description="是否禁用表单项")
    disabled_on: Optional[str] = Field(None, description="禁用条件表达式")
    hidden: Optional[bool] = Field(None, description="是否隐藏表单项")
    hidden_on: Optional[str] = Field(None, description="隐藏条件表达式")
    static: Optional[bool] = Field(None, description="是否静态展示")
    static_on: Optional[str] = Field(None, description="静态展示条件表达式")
    static_schema: Optional[Union[Dict[str, Any], List[Union[str, Dict[str, Any]]]]] = Field(None, description="静态展示配置")

    # ==================== 值属性 ====================
    value: Optional[Any] = Field(None, description="表单项默认值")
    clear_value_on_hidden: Optional[bool] = Field(None, description="隐藏时是否清除值")

    # ==================== 校验属性 ====================
    required: Optional[bool] = Field(None, description="是否必填")
    required_on: Optional[str] = Field(None, description="必填条件表达式")
    validations: Optional[Union[str, Dict[str, Any]]] = Field(None, description="校验规则")
    validation_errors: Optional[Dict[str, str]] = Field(None, description="自定义校验错误信息")
    validate_on_change: Optional[bool] = Field(None, description="值变化时是否校验")
    validate_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="服务端校验接口")

    # ==================== 自动填充属性 ====================
    auto_fill: Optional[Dict[str, Any]] = Field(None, description="自动填充配置")

    # ==================== 其他属性 ====================
    id: Optional[str] = Field(None, description="组件ID")
    class_name: Optional[str] = Field(None, description="CSS类名")
    style: Optional[Dict[str, Any]] = Field(None, description="自定义样式")
    visible: Optional[bool] = Field(None, description="是否可见")
    visible_on: Optional[str] = Field(None, description="可见条件表达式")

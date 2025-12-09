from __future__ import annotations
from typing import Optional, Literal

from ..base import BaseBuilder


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


class InputPasswordBuilder(BaseBuilder):
    """
    构建 AMIS 密码输入框配置对象，对应 <InputPassword> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/form/input-password
    
    示例：
        input_password = InputPasswordBuilder(
            name="password",
            label="密码"
        )
    """
    type: Literal["input-password"] = "input-password"
    
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
    class_name: Optional[str] = None  # 指定添加 input-password 类名
    reveal_password: Optional[bool] = True  # 是否展示密码显/隐按钮，默认为true


class InputDatetimeBuilder(BaseBuilder):
    """
    构建 AMIS 日期时间输入框配置对象，对应 <InputDatetime> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/form/input-datetime
    
    示例：
        input_datetime = InputDatetimeBuilder(
            name="datetime",
            label="日期时间"
        )
    """
    type: Literal["input-datetime"] = "input-datetime"
    
    # 字段名称
    name: str  # 字段名称
    
    # 字段标签
    label: str  # 字段标签
    
    # 其他属性
    value: Optional[str] = None  # 默认值，支持相对值如"+1hours"
    inputFormat: Optional[str] = None  # 显示格式，如"YYYY-MM-DD HH:mm:ss"
    format: Optional[str] = None  # 值格式，默认是时间戳
    placeholder: Optional[str] = None  # 占位提示文本
    shortcuts: Optional[list] = None  # 快捷选择日期，如["yesterday", "today", "tomorrow"]
    minDate: Optional[str] = None  # 限制最小日期时间
    maxDate: Optional[str] = None  # 限制最大日期时间
    utc: Optional[bool] = False  # 是否保存UTC值
    clearable: Optional[bool] = True  # 是否可清除
    embed: Optional[bool] = False  # 是否内联
    timeConstraints: Optional[dict] = None  # 控制时间输入范围
    isEndDate: Optional[bool] = False  # 如果为true，会自动默认为23:59:59秒
    disabledDate: Optional[str] = None  # 用字符函数来控制哪些天不可以被点选
    popOverContainerSelector: Optional[str] = None  # 弹层挂载位置选择器
    disabled: Optional[bool] = False  # 是否禁用
    read_only: Optional[bool] = False  # 是否只读
    required: Optional[bool] = False  # 是否必填
    class_name: Optional[str] = None  # 指定添加 input-datetime 类名

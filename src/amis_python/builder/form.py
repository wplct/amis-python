from __future__ import annotations
import inspect
from typing import List, Optional, Union, Any, Literal, Callable, get_type_hints

from .base import BaseBuilder
from .button import ButtonBuilder
from .input import InputTextBuilder, InputEmailBuilder
from .api import to_api


class FormBuilder(BaseBuilder):
    """
    构建 AMIS 表单配置对象，对应 <Form> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/form
    
    示例：
        form = FormBuilder(
            api="/amis/api/mock2/form/saveForm",
            body=[
                InputTextBuilder(name="name", label="名称")
            ],
            actions=[
                ButtonBuilder(label="Submit", action_type="submit"),
                ButtonBuilder(label="Reset", action_type="reset")
            ]
        )
    """
    type: Literal["form"] = "form"
    
    # 表单提交API
    api: Optional[Any] = None  # 表单提交API
    
    # 表单内容
    body: List[Any] = None  # 表单内容
    
    # 表单按钮
    actions: Optional[List[Union[ButtonBuilder, dict]]] = None  # 表单按钮
    
    # 其他属性
    debug: Optional[bool] = False  # 是否开启调试模式
    class_name: Optional[str] = None  # 指定添加 form 类名
    title: Optional[str] = None  # 表单标题
    mode: Optional[str] = None  # 表单模式
    
    # 布局属性
    horizontal: Optional[bool] = None  # 是否水平布局
    label_align: Optional[str] = None  # 标签对齐方式
    label_width: Optional[Union[str, int]] = None  # 标签宽度


def api_to_form(api_view: Callable) -> FormBuilder:
    """
    根据 API 函数自动生成 FormBuilder 对象
    
    :param api_view: Django-Ninja API 函数
    :return: 自动生成的 FormBuilder 对象
    """
    # 从函数注解中获取 Body 参数的 ModelSchema 类型
    body_model = None
    
    # 获取函数的签名和参数
    sig = inspect.signature(api_view)
    params = list(sig.parameters.values())
    print(params)
    # 获取类型提示
    type_hints = get_type_hints(api_view)
    
    # 遍历参数，查找 Body 参数
    for param in params:
        param_name = param.name
        param_annotation = param.annotation
        
        # 检查参数是否有 Body 注解
        if param_annotation != inspect.Parameter.empty:
            # 检查参数是否是 Body 类型
            annotation_str = str(param_annotation)
            if 'Body' in annotation_str:
                # 从类型提示中获取实际的 ModelSchema 类型
                if param_name in type_hints:
                    # 获取类型提示中的实际类型
                    hint_type = type_hints[param_name]
                    
                    # 处理泛型类型，获取内部类型
                    if hasattr(hint_type, '__origin__'):
                        # 对于泛型类型，获取第一个类型参数
                        origin = hint_type.__origin__
                        if origin is not None and hasattr(hint_type, '__args__'):
                            args = hint_type.__args__
                            if args:
                                body_model = args[0]
                    else:
                        # 直接使用类型
                        body_model = hint_type
                    break
    print(body_model)
    if not body_model:
        # 如果没有找到 Body 参数，检查所有参数类型
        for param_name, param_type in type_hints.items():
            # 检查类型是否是 ModelSchema 子类
            if hasattr(param_type, '__mro__'):
                for base in param_type.__mro__:
                    if base.__name__ == 'ModelSchema':
                        body_model = param_type
                        break
                if body_model:
                    break
    
    if not body_model:
        # 如果没有 Body 参数，返回空表单
        return FormBuilder(
            api=to_api(api_view),
            body=[]
        )
    
    # 生成表单字段
    form_fields = []
    for field_name, field in body_model.model_fields.items():
        # 生成字段标签（首字母大写，下划线转空格）
        label = field_name.replace('_', ' ').capitalize()
        
        # 根据字段类型生成对应的表单字段
        # 这里可以扩展更多字段类型的映射
        if field_name.endswith('_email') or field_name == 'email':
            form_fields.append(InputEmailBuilder(name=field_name, label=label))
        else:
            # 默认使用文本输入框
            form_fields.append(InputTextBuilder(name=field_name, label=label))
    
    # 创建并返回 FormBuilder 对象
    return FormBuilder(
        api=to_api(api_view),
        body=form_fields
    )

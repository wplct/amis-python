from __future__ import annotations
import inspect
from datetime import datetime
from typing import List, Optional, Union, Any, Literal, Callable, get_type_hints, Type

from ninja import ModelSchema
from pydantic import BaseModel

from .action import ToastActionBuilder, ReloadActionBuilder
from .base import BaseBuilder
from .button import ButtonBuilder
from .input import InputTextBuilder, InputEmailBuilder, InputDatetimeBuilder
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

    wrap_with_panel: Optional[bool] = None

def schema_to_form(schema: Type[BaseModel],**kwargs) -> FormBuilder:
    """
    根据 ModelSchema 生成 FormBuilder 对象
    """
    form_fields = []
    for field_name, field in schema.model_fields.items():

        py_type = field.annotation

        if py_type is datetime:
            form_fields.append(
                InputDatetimeBuilder(  # 换成你自己的日期组件
                    label=field.title or field_name,
                    name=field_name,
                    required=field.is_required()
                )
            )
            continue
        form_fields.append(
            InputTextBuilder(
                label=field.title,
                name=field_name,
                required=field.is_required()
            )
        )
    return FormBuilder(
        body=form_fields,
        **kwargs,
    )


def api_to_form(api_view: Callable) -> FormBuilder:
    """
    根据 API 函数自动生成 FormBuilder 对象
    
    :param api_view: Django-Ninja API 函数
    :return: 自动生成的 FormBuilder 对象
    """
    # 从函数注解中获取 Body 参数的 ModelSchema 类型
    body_model = None
    
    # 获取函数的签名和参数
    # sig = inspect.signature(api_view)
    # params = list(sig.parameters.values())
    # 获取类型提示
    type_hints = get_type_hints(api_view)
    if 'data' in type_hints:
        body_model = type_hints['data']
        if not issubclass(body_model, BaseModel):
            raise ValueError("data 必须是 ModelSchema 子类")
    if not body_model:
        # 如果没有 Body 参数，返回空表单
        return FormBuilder(
            api=to_api(api_view),
            body=[]
        )
    
    # 生成表单字段
    form = schema_to_form(body_model)
    form.api = to_api(api_view)
    form.add_action('submitSucc',ReloadActionBuilder(component_id="curd"))
    # 返回 FormBuilder 对象
    return form

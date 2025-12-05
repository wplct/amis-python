from __future__ import annotations
from typing import List, Optional, Union, Any, Literal

from .base import BaseBuilder
from .button import ButtonBuilder


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

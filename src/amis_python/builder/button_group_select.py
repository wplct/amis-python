from __future__ import annotations
from typing import List, Optional, Union, Literal
from pydantic import Field

from .base import BaseBuilder


class ButtonGroupSelectBuilder(BaseBuilder):
    """
    构建 AMIS 按钮点选配置对象，对应 <ButtonGroupSelect> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/button#button-group-select-%E6%8C%89%E9%92%AE%E7%82%B9%E9%80%89
    
    示例：
        button_group_select = ButtonGroupSelectBuilder(
            name="a",
            options=[
                {"label": "选项1", "value": "a"},
                {"label": "选项2", "value": "b"}
            ]
        )
    """
    type: Literal["button-group-select"] = "button-group-select"
    
    # 组件名称，用于表单提交时的标识
    name: str = Field(..., description="组件名称，用于表单提交时的标识")
    
    # 选项列表
    options: List[dict] = Field(..., description="选项列表")
    
    # 其他属性
    value: Optional[Union[str, int]] = Field(None, description="默认选中值")
    class_name: Optional[str] = Field(None, description="指定添加 button-group-select 类名")
    size: Optional[Literal["xs", "sm", "md", "lg"]] = Field(None, description="设置按钮大小")
    multiple: Optional[bool] = Field(False, description="是否支持多选")

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field

from .base import BaseBuilder


class ButtonBuilder(BaseBuilder):
    """
    构建 AMIS 按钮的配置对象，对应 <Button> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/button
    
    示例：
        button = ButtonBuilder(
            action_type="submit",
            level="primary",
            label="提交",
            size="md"
        )
    """
    type: Literal["button"] = "button"
    
    # === 基本信息 ===
    label: str = Field(..., description="按钮显示文本")
    class_name: Optional[str] = Field(None, description="指定添加 button 类名")
    url: Optional[str] = Field(None, description="点击跳转的地址，指定此属性 button 的行为和 a 链接一致")
    
    # === 外观配置 ===
    size: Optional[Literal["xs", "sm", "md", "lg"]] = Field(None, description="设置按钮大小")
    level: Optional[Literal["link", "primary", "enhance", "secondary", "info", "success", "warning", "danger", "light", "dark", "default"]] = Field("default", description="设置按钮样式")
    block: Optional[bool] = Field(False, description="将按钮宽度调整为其父宽度的选项")
    
    # === 状态配置 ===
    disabled: Optional[bool] = Field(False, description="按钮失效状态")
    loading: Optional[bool] = Field(False, description="显示按钮 loading 效果")
    loading_on: Optional[str] = Field(None, description="显示按钮 loading 表达式")
    
    # === 提示配置 ===
    tooltip: Optional[Union[str, Dict[str, Any]]] = Field(None, description="气泡提示内容")
    tooltip_placement: Optional[Literal["top", "right", "bottom", "left"]] = Field("top", description="气泡框位置器")
    tooltip_trigger: Optional[Literal["hover", "focus"]] = Field(None, description="触发 tooltip")
    disabled_tip: Optional[Union[str, Dict[str, Any]]] = Field(None, description="按钮失效状态下的提示")
    
    # === 功能配置 ===
    action_type: Optional[str] = Field(None, description="动作类型，如submit、reset等", alias="actionType")
    name: Optional[str] = Field(None, description="组件名称，用于表单提交时的标识")
    value: Optional[Any] = Field(None, description="组件值，用于表单提交时的值")


from __future__ import annotations
from typing import Optional
from pydantic import Field

from amis_python.builder.action.action import ActionBuilder


class UrlActionBuilder(ActionBuilder):
    """
    构建 AMIS URL 动作配置对象（直接跳转）
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 url
    action_type: str = Field("url", description="动作类型", alias="actionType")
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = Field(None, description="动作显示文本")
    
    # Url 相关属性
    url: str = Field(..., description="跳转地址，会直接跳转指定页面")
    blank: Optional[bool] = Field(None, description="是否在新 tab 页面打开")
    
    # 其他通用属性
    confirm_text: Optional[str] = Field(None, description="确认提示文本", alias="confirmText")
    close: Optional[bool] = Field(None, description="是否关闭当前组件")
    reload: Optional[Any] = Field(None, description="是否刷新指定组件")

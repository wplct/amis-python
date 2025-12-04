from __future__ import annotations
from typing import Optional, Any
from pydantic import Field

from amis_python.builder.action.action import ActionBuilder


class LinkActionBuilder(ActionBuilder):
    """
    构建 AMIS 链接动作配置对象（单页跳转）
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 link
    action_type: str = Field("link", description="动作类型", alias="actionType")
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = Field(None, description="动作显示文本")
    
    # Link 相关属性
    link: str = Field(..., description="跳转地址，单页跳转方式，不会刷新浏览器")
    target: Optional[str] = Field(None, description="跳转目标")
    
    # 其他通用属性
    confirm_text: Optional[str] = Field(None, description="确认提示文本", alias="confirmText")
    close: Optional[bool] = Field(None, description="是否关闭当前组件")
    reload: Optional[Any] = Field(None, description="是否刷新指定组件")

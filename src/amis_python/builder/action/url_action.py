from __future__ import annotations
from typing import Optional, Any

from amis_python.builder.action.action import ActionBuilder


class UrlActionBuilder(ActionBuilder):
    """
    构建 AMIS URL 动作配置对象（直接跳转）
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 url
    action_type: str = "url"  # 动作类型
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = None  # 动作显示文本
    
    # Url 相关属性
    url: str  # 跳转地址，会直接跳转指定页面
    blank: Optional[bool] = None  # 是否在新 tab 页面打开
    
    # 其他通用属性
    confirm_text: Optional[str] = None  # 确认提示文本
    close: Optional[bool] = None  # 是否关闭当前组件
    reload: Optional[Any] = None  # 是否刷新指定组件
    redirect_type: Optional[str] = None  # 重定向类型，设置为'none'时不会将表单结果作为参数附加到URL

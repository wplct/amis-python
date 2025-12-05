from __future__ import annotations
from typing import Optional, Any

from amis_python.builder.action.action import ActionBuilder


class LinkActionBuilder(ActionBuilder):
    """
    构建 AMIS 链接动作配置对象（单页跳转）
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 link
    action_type: str = "link"  # 动作类型
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = None  # 动作显示文本
    
    # Link 相关属性
    link: str  # 跳转地址，单页跳转方式，不会刷新浏览器
    target: Optional[str] = None  # 跳转目标
    
    # 其他通用属性
    confirm_text: Optional[str] = None  # 确认提示文本
    close: Optional[bool] = None  # 是否关闭当前组件
    reload: Optional[Any] = None  # 是否刷新指定组件

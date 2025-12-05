from __future__ import annotations
from typing import Any, Dict, Optional

from amis_python.builder.action.action import ActionBuilder


class DialogActionBuilder(ActionBuilder):
    """
    构建 AMIS 对话框动作配置对象
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 dialog
    action_type: str = "dialog"  # 动作类型
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = None  # 动作显示文本
    
    # Dialog 相关属性
    dialog: Dict[str, Any]  # 对话框配置
    
    # 其他通用属性
    confirm_text: Optional[str] = None  # 确认提示文本
    close: Optional[bool] = None  # 是否关闭当前组件
    reload: Optional[Any] = None  # 是否刷新指定组件

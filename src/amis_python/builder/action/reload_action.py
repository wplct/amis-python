from __future__ import annotations
from typing import Optional, Any, Dict, Literal

from amis_python.builder.action.action import ActionBuilder


class ReloadActionBuilder(ActionBuilder):
    """
    构建 AMIS 刷新动作配置对象
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/docs/concepts/event-action
    """
    # 动作类型固定为 reload
    action_type: str = "reload"  # 动作类型
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = None  # 动作显示文本
    
    # Reload动作特有属性
    component_id: Optional[str] = None  # 要刷新的组件ID
    ignore_error: Optional[bool] = None  # 是否忽略错误
    data_merge_mode: Optional[Literal["merge", "override"]] = None  # 数据合并模式
    data: Optional[Dict[str, Any]] = None  # 要传递的数据
    args: Optional[Dict[str, Any]] = None  # 额外参数，如 resetPage 等
    
    # 其他通用属性
    confirm_text: Optional[str] = None  # 确认提示文本
    close: Optional[bool] = None  # 是否关闭当前组件
    reload: Optional[Any] = None  # 是否刷新指定组件

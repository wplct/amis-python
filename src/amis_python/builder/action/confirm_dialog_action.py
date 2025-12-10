from __future__ import annotations
from typing import Any, Dict, Optional, Union

from amis_python.builder.action.action import ActionBuilder


class ConfirmDialogActionBuilder(ActionBuilder):
    """
    构建 AMIS Ajax 动作配置对象
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 ajax
    action_type: str = "confirmDialog"  # 动作类型
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = None  # 动作显示文本

    # dialog
    dialog: Optional[Dict[str, Any]] = None

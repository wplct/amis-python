from __future__ import annotations
from typing import Any, Dict, Optional, Union
from pydantic import Field

from amis_python.builder.action.action import ActionBuilder


class SaveToLocalActionBuilder(ActionBuilder):
    """
    构建 AMIS 保存到本地动作配置对象
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 saveToLocal
    action_type: str = Field("saveToLocal", description="动作类型", alias="actionType")
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = Field(None, description="动作显示文本")
    
    # SaveToLocal 相关属性
    api: Union[str, Dict[str, Any]] = Field(..., description="数据请求地址")
    
    # 其他通用属性
    confirm_text: Optional[str] = Field(None, description="确认提示文本", alias="confirmText")
    close: Optional[bool] = Field(None, description="是否关闭当前组件")
    reload: Optional[Any] = Field(None, description="是否刷新指定组件")

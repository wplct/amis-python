from __future__ import annotations
from typing import Optional, Literal
from pydantic import Field

from .action import ActionBuilder


class ToastActionBuilder(ActionBuilder):
    """
    构建 AMIS Toast 动作配置对象
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/docs/concepts/event-action#toast-%E6%9F%A5%E7%9C%8B%E6%8F%90%E7%A4%BA
    
    示例：
        toast = ToastActionBuilder(
            msg_type="success",
            msg="操作成功"
        )
    """
    action_type: Literal["toast"] = "toast"
    
    # 提示消息内容
    msg: str = Field(..., description="提示消息内容")
    
    # 提示类型
    msg_type: Optional[Literal["info", "success", "warning", "error"]] = Field("info", description="提示类型", alias="msgType")
    
    # 持续时间
    duration: Optional[int] = Field(3000, description="提示持续时间，单位毫秒")
    
    # 是否自动关闭
    close: Optional[bool] = Field(True, description="是否自动关闭")

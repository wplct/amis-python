from __future__ import annotations
from typing import Optional, Literal

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
    args: Optional[dict] = None
    
    def __init__(self, **data):
        # 将所有参数包装到args字段中
        args = {}
        
        # 提取msg和msg_type参数
        if "msg" in data:
            args["msg"] = data.pop("msg")
        
        if "msg_type" in data:
            args["msgType"] = data.pop("msg_type")
        
        if "duration" in data:
            args["duration"] = data.pop("duration")
        
        if "close" in data:
            args["close"] = data.pop("close")
        
        # 将args添加到data中
        data["args"] = args
        
        super().__init__(**data)

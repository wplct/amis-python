from __future__ import annotations
from typing import Optional, Any

from amis_python.builder.action.action import ActionBuilder


class EmailActionBuilder(ActionBuilder):
    """
    构建 AMIS 邮件动作配置对象
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 email
    action_type: str = "email"  # 动作类型
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = None  # 动作显示文本
    
    # Email 相关属性
    to: Optional[str] = None  # 收件人邮箱
    cc: Optional[str] = None  # 抄送邮箱
    bcc: Optional[str] = None  # 匿名抄送邮箱
    subject: Optional[str] = None  # 邮件主题
    body: Optional[str] = None  # 邮件正文
    
    # 其他通用属性
    confirm_text: Optional[str] = None  # 确认提示文本
    close: Optional[bool] = None  # 是否关闭当前组件
    reload: Optional[Any] = None  # 是否刷新指定组件

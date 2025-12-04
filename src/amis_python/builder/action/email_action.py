from __future__ import annotations
from typing import Optional, Any
from pydantic import Field

from amis_python.builder.action.action import ActionBuilder


class EmailActionBuilder(ActionBuilder):
    """
    构建 AMIS 邮件动作配置对象
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 email
    action_type: str = Field("email", description="动作类型", alias="actionType")
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = Field(None, description="动作显示文本")
    
    # Email 相关属性
    to: Optional[str] = Field(None, description="收件人邮箱")
    cc: Optional[str] = Field(None, description="抄送邮箱")
    bcc: Optional[str] = Field(None, description="匿名抄送邮箱")
    subject: Optional[str] = Field(None, description="邮件主题")
    body: Optional[str] = Field(None, description="邮件正文")
    
    # 其他通用属性
    confirm_text: Optional[str] = Field(None, description="确认提示文本", alias="confirmText")
    close: Optional[bool] = Field(None, description="是否关闭当前组件")
    reload: Optional[Any] = Field(None, description="是否刷新指定组件")

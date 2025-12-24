from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder.base import BaseModel


class Dialog(BaseModel):
    """
    amis Dialog 对话框组件
    对应组件类型: dialog
    文档地址: docs/zh-CN/components/dialog.md
    
    Dialog 弹框主要由 Action 触发，展示一个对话框以供用户操作。
    """

    # ==================== 基本属性 ====================
    type: Literal["dialog"] = Field("dialog", description="指定为对话框组件")
    title: Optional[Any] = Field(None, description="弹出层标题")
    body: Optional[Any] = Field(None, description="往 Dialog 内容区加内容")
    size: Optional[Literal["xs", "sm", "md", "lg", "xl", "full", "custom"]] = Field(None, description="指定 dialog 大小，支持: xs、sm、md、lg、xl、full、custom")
    width: Optional[Union[float, int, str]] = Field(None, description="Dialog 宽度, size 为 custom 时生效")
    height: Optional[Union[float, int, str]] = Field(None, description="Dialog 高度, size 为 custom 时生效")
    body_class_name: Optional[str] = Field(None, description="Dialog body 区域的样式类名")
    close_on_esc: Optional[bool] = Field(True, description="是否支持按 Esc 关闭 Dialog")
    close_on_outside: Optional[bool] = Field(True, description="是否允许点击外部区域关闭 Dialog")
    show_close_button: Optional[bool] = Field(None, description="是否显示右上角的关闭按钮")
    show_error_msg: Optional[bool] = Field(None, description="是否在弹框左下角显示报错信息")
    show_loading: Optional[bool] = Field(None, description="是否在弹框左下角显示 loading 动画")
    disabled: Optional[bool] = Field(None, description="如果设置此属性，则该 Dialog 只读没有提交操作")
    draggable: Optional[bool] = Field(None, description="是否支持拖拽 Dialog")
    actions: Optional[List[Any]] = Field(None, description="底部按钮配置，默认显示【确认】和【取消】")
    data: Optional[Dict[str, Any]] = Field(None, description="支持数据映射，如果不设定将默认继承触发按钮的上下文数据")

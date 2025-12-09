from __future__ import annotations
from typing import Literal, Union, Optional, List, Dict, Any

from ..base import BaseBuilder
from ..button import ButtonBuilder
from ..action import ActionBuilder


class DialogBuilder(BaseBuilder):
    """
    构建 AMIS 对话框配置对象，对应 <Dialog> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/dialog?page=1
    
    示例：
        dialog = DialogBuilder(
            title="示例对话框",
            body="这是对话框内容",
            size="md",
            close_on_esc=True,
            show_close_button=True
        )
    """
    type: Literal["dialog"] = "dialog"
    
    # 基础属性
    title: Optional[Union[str, Dict[str, Any]]] = None  # 弹出层标题
    body: Optional[Union[str, Dict[str, Any]]] = None  # 往 Dialog 内容区加内容
    
    # 尺寸配置
    size: Optional[Literal["xs", "sm", "md", "lg", "xl", "full", "custom"]] = None  # 指定 dialog 大小
    width: Optional[Union[int, float, str]] = None  # Dialog 宽度, size 为 custom 时生效
    height: Optional[Union[int, float, str]] = None  # Dialog 高度, size 为 custom 时生效
    
    # 样式配置
    body_class_name: Optional[str] = None  # Dialog body 区域的样式类名
    
    # 行为配置
    close_on_esc: Optional[bool] = None  # 是否支持按 Esc 关闭 Dialog
    show_close_button: Optional[bool] = None  # 是否显示右上角的关闭按钮
    show_error_msg: Optional[bool] = None  # 是否在弹框左下角显示报错信息
    show_loading: Optional[bool] = None  # 是否在弹框左下角显示 loading 动画
    disabled: Optional[bool] = None  # 如果设置此属性，则该 Dialog 只读没有提交操作
    draggable: Optional[bool] = None  # 是否支持拖
    
    # 按钮配置
    actions: Optional[List[Union[ButtonBuilder, ActionBuilder, Dict[str, Any]]]] = None  # 对话框按钮配置
    
    # 数据映射
    data: Optional[Dict[str, Any]] = None  # 数据映射配置
    
    # 其他属性
    name: Optional[str] = None  # 对话框名称，用于关闭指定对话框
    close_on_outside: Optional[bool] = None  # 是否支持点击外部关闭 Dialog
    position: Optional[Literal["top", "center", "bottom"]] = None  # 对话框位置
    footer: Optional[Union[bool, Dict[str, Any]]] = None  # 对话框底部配置
    header: Optional[Union[bool, Dict[str, Any]]] = None  # 对话框头部配置
    overlay: Optional[bool] = None  # 是否显示遮罩
    overlay_class_name: Optional[str] = None  # 遮罩样式类名
    
    # 动画配置
    animation: Optional[str] = None  # 对话框动画
    transition_name: Optional[str] = None  # 自定义动画类名
    
    # 反馈配置
    feedback: Optional[Dict[str, Any]] = None  # 反馈弹框配置

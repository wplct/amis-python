from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder.base import BaseModel
from amis_python.builder.api import AmisApiObject


class Action(BaseModel):
    """
    amis Action 行为按钮组件
    对应组件类型: action
    文档地址: docs/zh-CN/components/action.md
    """

    # ==================== 基本属性 ====================
    type: Literal["action"] = Field("action", description="指定为行为按钮组件")
    action_type: Optional[Literal["ajax", "link", "url", "drawer", "dialog", "confirm", "cancel", "prev", "next", "copy", "close", "button", "reset", "submit", "clear", "download", "saveAs", "email", "reload"]] = Field(None, description="行为类型")
    label: Optional[str] = Field(None, description="按钮文本")
    level: Optional[Literal["link", "primary", "enhance", "secondary", "info", "success", "warning", "danger", "light", "dark", "default"]] = Field(None, description="按钮样式")
    size: Optional[Literal["xs", "sm", "md", "lg"]] = Field(None, description="按钮大小")
    icon: Optional[str] = Field(None, description="按钮图标")
    icon_class_name: Optional[str] = Field(None, description="图标类名")
    right_icon: Optional[str] = Field(None, description="右侧图标")
    right_icon_class_name: Optional[str] = Field(None, description="右侧图标类名")
    active: Optional[bool] = Field(None, description="是否高亮")
    active_level: Optional[Literal["link", "primary", "enhance", "secondary", "info", "success", "warning", "danger", "light", "dark", "default"]] = Field(None, description="高亮时的样式")
    active_class_name: Optional[str] = Field(None, description="高亮类名")
    block: Optional[bool] = Field(None, description="是否块状显示")
    disabled: Optional[bool] = Field(None, description="是否禁用")
    loading: Optional[bool] = Field(None, description="是否加载中")
    loading_on: Optional[str] = Field(None, description="加载状态表达式")
    class_name: Optional[str] = Field(None, description="按钮类名")
    confirm_text: Optional[str] = Field(None, description="确认文本")
    confirm_title: Optional[str] = Field(None, description="确认标题")
    reload: Optional[str] = Field(None, description="需要刷新的组件")
    target: Optional[str] = Field(None, description="需要刷新的目标组件名字")
    tooltip: Optional[Union[str, Dict[str, Any]]] = Field(None, description="提示信息")
    disabled_tip: Optional[Union[str, Dict[str, Any]]] = Field(None, description="禁用提示")
    tooltip_placement: Optional[Literal["top", "right", "bottom", "left"]] = Field(None, description="提示位置")
    tooltip_trigger: Optional[Literal["hover", "focus"]] = Field(None, description="提示触发方式")
    hot_key: Optional[str] = Field(None, description="快捷键")
    onClick: Optional[str] = Field(None, description="自定义点击事件")
    required: Optional[List[str]] = Field(None, description="需要验证的字段")
    close: Optional[Union[bool, str]] = Field(None, description="是否关闭当前弹窗")

    # ==================== AJAX 相关属性 ====================
    api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="请求接口")
    redirect: Optional[str] = Field(None, description="请求结束后跳转的路径")
    feedback: Optional[Dict[str, Any]] = Field(None, description="请求成功后显示的反馈弹框")
    messages: Optional[Dict[str, str]] = Field(None, description="请求成功/失败提示信息")
    download_file_name: Optional[str] = Field(None, description="下载文件名")

    # ==================== 链接相关属性 ====================
    url: Optional[str] = Field(None, description="跳转地址")
    blank: Optional[bool] = Field(None, description="是否在新窗口打开")
    link: Optional[str] = Field(None, description="单页跳转地址")

    # ==================== 弹框相关属性 ====================
    dialog: Optional[Dict[str, Any]] = Field(None, description="弹框配置")
    drawer: Optional[Dict[str, Any]] = Field(None, description="抽屉配置")
    next_condition: Optional[bool] = Field(None, description="下一条数据的条件")

    # ==================== 复制相关属性 ====================
    content: Optional[str] = Field(None, description="复制内容")
    copy_format: Optional[str] = Field(None, description="复制格式")

    # ==================== 倒计时相关属性 ====================
    count_down: Optional[int] = Field(None, description="倒计时秒数")
    count_down_tpl: Optional[str] = Field(None, description="倒计时模板")

    # ==================== 容器相关属性 ====================
    body: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = Field(None, description="容器内容")

    # ==================== 邮件相关属性 ====================
    to: Optional[str] = Field(None, description="收件人")
    cc: Optional[str] = Field(None, description="抄送")
    bcc: Optional[str] = Field(None, description="密送")
    subject: Optional[str] = Field(None, description="邮件主题")
    body_email: Optional[str] = Field(None, description="邮件正文", alias="body")
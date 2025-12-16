from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder.base import BaseModel


class EventAction(BaseModel):
    """
    amis 事件动作组件
    对应概念: 事件动作
    文档地址: docs/zh-CN/concepts/event-action.md
    
    用于配置组件的事件响应动作
    """

    # ==================== 基本属性 ====================
    action_type: Literal["ajax", "link", "url", "drawer", "dialog", "confirm", "cancel", "prev", "next", "copy", "close", "button", "reset", "submit", "clear", "download", "saveAs", "email", "reload", "toast", "goBack", "goPage", "refresh", "closeDialog", "closeDrawer", "confirmDialog", "alert", "print","search"] = Field(..., description="动作类型")
    
    # ==================== AJAX 相关属性 ====================
    api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="请求接口")
    options: Optional[Dict[str, Any]] = Field(None, description="其他配置")
    messages: Optional[Dict[str, str]] = Field(None, description="请求成功/失败后的提示信息")
    output_var: Optional[str] = Field(None, description="输出数据变量名")
    silent: Optional[bool] = Field(None, description="是否静默模式")
    
    # ==================== 弹框相关属性 ====================
    dialog: Optional[Union[str, Dict[str, Any], Any]] = Field(None, description="弹框配置")
    drawer: Optional[Dict[str, Any]] = Field(None, description="抽屉配置")
    wait_for_action: Optional[bool] = Field(None, description="是否等待弹窗响应")

    # ==================== 提示相关属性 ====================
    args: Optional[Dict[str, Any]] = Field(None, description="动作参数")
    
    # ==================== 页面跳转相关属性 ====================
    url: Optional[str] = Field(None, description="跳转地址")
    blank: Optional[bool] = Field(None, description="是否在新窗口打开")
    params: Optional[Dict[str, Any]] = Field(None, description="页面参数")
    link: Optional[str] = Field(None, description="单页跳转地址")
    target_type: Optional[Literal["page", "blank", "self"]] = Field(None, description="打开方式")
    
    # ==================== 浏览器相关属性 ====================
    delta: Optional[int] = Field(None, description="前进/后退的步数")
    
    # ==================== 复制相关属性 ====================
    content: Optional[str] = Field(None, description="复制内容")
    copy_format: Optional[str] = Field(None, description="复制格式")
    
    # ==================== 打印相关属性 ====================
    id: Optional[str] = Field(None, description="要打印的组件ID")
    ids: Optional[List[str]] = Field(None, description="要打印的组件ID列表")
    
    # ==================== 通用属性 ====================
    component_id: Optional[str] = Field(None, description="目标组件ID")
    expression: Optional[str] = Field(None, description="条件表达式")
    
    # ==================== 表单相关属性 ====================
    data: Optional[Dict[str, Any]] = Field(None, description="表单数据")
    
    # ==================== 广播相关属性 ====================
    event_name: Optional[str] = Field(None, description="广播事件名称")
    broadcast_type: Optional[str] = Field(None, description="广播类型")
    
    # ==================== JS 脚本相关属性 ====================
    script: Optional[str] = Field(None, description="JS 脚本")
    
    # ==================== 逻辑编排相关属性 ====================
    cases: Optional[List[Dict[str, Any]]] = Field(None, description="条件分支")
    items: Optional[List[Dict[str, Any]]] = Field(None, description="循环项")
    actions: Optional[List[Dict[str, Any]]] = Field(None, description="动作列表")
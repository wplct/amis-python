from __future__ import annotations
from typing import Any, Dict, Optional, Union

from amis_python.builder.action.action import ActionBuilder


class AjaxActionBuilder(ActionBuilder):
    """
    构建 AMIS Ajax 动作配置对象
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/action?page=1
    """
    # 动作类型固定为 ajax
    action_type: str = "ajax"  # 动作类型
    
    # 基础属性
    type: Optional[str] = None
    label: Optional[str] = None  # 动作显示文本
    
    # Ajax 相关属性
    api: Union[str, Dict[str, Any]]  # 请求地址，参考 api 格式说明
    data: Optional[Dict[str, Any]] = None  # 请求数据
    redirect: Optional[str] = None  # 请求结束后跳转的路径
    feedback: Optional[Dict[str, Any]] = None  # 请求成功后弹出的 dialog 配置
    messages: Optional[Dict[str, str]] = None  # 自定义接口返回toast信息
    
    # 其他通用属性
    confirm_text: Optional[str] = None  # 确认提示文本
    close: Optional[bool] = None  # 是否关闭当前组件
    reload: Optional[Any] = None  # 是否刷新指定组件

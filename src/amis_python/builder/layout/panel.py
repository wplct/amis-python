from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder import BaseModel


class Panel(BaseModel):
    """
    amis Panel 面板组件
    对应组件类型: panel
    文档地址: docs/zh-CN/components/panel.md
    """

    # ==================== 基本属性 ====================
    type: Literal["panel"] = Field("panel", description="指定为 Panel 渲染器")
    
    # ==================== 样式属性 ====================
    class_name: Optional[str] = Field("panel-default", description="外层 Dom 的类名")
    header_class_name: Optional[str] = Field("panel-heading", description="header 区域的类名")
    footer_class_name: Optional[str] = Field("panel-footer bg-light lter wrapper", description="footer 区域的类名")
    actions_class_name: Optional[str] = Field("panel-footer", description="actions 区域的类名")
    body_class_name: Optional[str] = Field("panel-body", description="body 区域的类名")
    
    # ==================== 内容属性 ====================
    title: Optional[Union[str, Dict[str, Any]]] = Field(None, description="标题")
    header: Optional[Union[str, Dict[str, Any]]] = Field(None, description="头部容器")
    body: Optional[Union[str, List[Any], Dict[str, Any]]] = Field(None, description="内容容器")
    footer: Optional[Union[str, Dict[str, Any]]] = Field(None, description="底部容器")
    
    # ==================== 功能属性 ====================
    affix_footer: Optional[bool] = Field(None, description="是否固定底部容器")
    actions: Optional[List[Any]] = Field(None, description="按钮区域")

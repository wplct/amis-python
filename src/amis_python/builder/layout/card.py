from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder import BaseModel


class Card(BaseModel):
    """
    amis Card 卡片组件
    对应组件类型: card
    文档地址: docs/zh-CN/components/card.md
    """

    # ==================== 基本属性 ====================
    type: Literal["card"] = Field("card", description="指定为 card 组件")
    
    # ==================== 内容属性 ====================
    title: Optional[Union[str, Dict[str, Any]]] = Field(None, description="卡片标题")
    sub_title: Optional[Union[str, Dict[str, Any]]] = Field(None, description="卡片副标题")
    description: Optional[Union[str, Dict[str, Any]]] = Field(None, description="卡片描述")
    avatar: Optional[Union[str, Dict[str, Any]]] = Field(None, description="卡片头像")
    body: Optional[Union[str, List[Any], Dict[str, Any]]] = Field(None, description="卡片内容")
    header: Optional[Union[str, Dict[str, Any]]] = Field(None, description="卡片头部")
    footer: Optional[Union[str, Dict[str, Any]]] = Field(None, description="卡片底部")
    
    # ==================== 样式属性 ====================
    class_name: Optional[str] = Field(None, description="卡片外层类名")
    header_class_name: Optional[str] = Field(None, description="卡片头部类名")
    body_class_name: Optional[str] = Field(None, description="卡片内容类名")
    footer_class_name: Optional[str] = Field(None, description="卡片底部类名")
    avatar_class_name: Optional[str] = Field(None, description="卡片头像类名")
    highlight: Optional[bool] = Field(None, description="是否高亮卡片")
    
    # ==================== 功能属性 ====================
    actions: Optional[List[Any]] = Field(None, description="卡片操作按钮")
    link: Optional[Union[str, Dict[str, Any]]] = Field(None, description="卡片链接")
    target: Optional[str] = Field(None, description="链接打开方式")
    
    # ==================== 高级属性 ====================
    id: Optional[str] = Field(None, description="卡片 ID")
    name: Optional[str] = Field(None, description="卡片名称")
    visible: Optional[bool] = Field(None, description="是否显示卡片")
    hidden: Optional[bool] = Field(None, description="是否隐藏卡片")
    disabled: Optional[bool] = Field(None, description="是否禁用卡片")
    read_only: Optional[bool] = Field(None, description="是否只读卡片")
    required: Optional[bool] = Field(None, description="是否必填卡片")
    tooltip: Optional[Union[str, Dict[str, Any]]] = Field(None, description="卡片提示")
    description: Optional[str] = Field(None, description="卡片描述")

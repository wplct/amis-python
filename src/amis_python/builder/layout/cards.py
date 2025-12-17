from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field


from amis_python.builder import BaseModel


class Cards(BaseModel):
    """
    amis Cards 卡片列表组件
    对应组件类型: cards
    文档地址: docs/zh-CN/components/cards.md
    """

    # ==================== 基本属性 ====================
    type: Literal["cards"] = Field("cards", description="指定为 cards 组件")
    
    # ==================== 数据源配置 ====================
    api: Optional[Union[str, Dict[str, Any], Any]] = Field(None, description="数据接口配置")
    source: Optional[str] = Field(None, description="静态数据源，支持变量表达式")
    
    # ==================== 布局配置 ====================
    columns_count: Optional[int] = Field(None, description="卡片列数")
    row_gap: Optional[Union[int, str]] = Field(None, description="行间距")
    col_gap: Optional[Union[int, str]] = Field(None, description="列间距")
    
    # ==================== 卡片配置 ====================
    card: Optional[Dict[str, Any]] = Field(None, description="卡片配置")
    
    # ==================== 分页配置 ====================
    pagination: Optional[Union[bool, Dict[str, Any]]] = Field(None, description="分页配置")
    load_more: Optional[Union[bool, Dict[str, Any]]] = Field(None, description="加载更多配置")
    per_page: Optional[int] = Field(None, description="每页数量")
    
    # ==================== 样式属性 ====================
    class_name: Optional[str] = Field(None, description="外层类名")
    card_class_name: Optional[str] = Field(None, description="卡片类名")
    
    # ==================== 功能属性 ====================
    placeholder: Optional[Union[str, Dict[str, Any]]] = Field(None, description="空数据提示")
    empty_data: Optional[Union[str, Dict[str, Any]]] = Field(None, description="空数据配置")
    auto_fill_height: Optional[bool] = Field(None, description="是否自动填充高度")
    
    # ==================== 高级属性 ====================
    id: Optional[str] = Field(None, description="组件 ID")
    name: Optional[str] = Field(None, description="组件名称")
    visible: Optional[bool] = Field(None, description="是否显示组件")
    hidden: Optional[bool] = Field(None, description="是否隐藏组件")
    disabled: Optional[bool] = Field(None, description="是否禁用组件")
    read_only: Optional[bool] = Field(None, description="是否只读组件")
    required: Optional[bool] = Field(None, description="是否必填组件")
    tooltip: Optional[Union[str, Dict[str, Any]]] = Field(None, description="组件提示")
    description: Optional[str] = Field(None, description="组件描述")
    on_event: Optional[Dict[str, Any]] = Field(None, description="事件配置")

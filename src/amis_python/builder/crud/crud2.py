from typing import Optional, Literal, List, Dict, Union, Any
from enum import Enum

from pydantic import Field

from amis_python import Api
from amis_python.builder import BaseModel


# ====================== 枚举类型 ======================

class CRUD2Mode(str, Enum):
    TABLE2 = "table2"      # 表格模式
    CARDS = "cards"        # 卡片模式
    LIST = "list"          # 列表模式

class LoadType(str, Enum):
    NONE = ""              # 无
    PAGINATION = "pagination"  # 分页模式
    MORE = "more"          # 加载更多模式


# ====================== 主模型 ======================

class CRUD2(BaseModel):
    """
    amis CRUD2 组件完整 Pydantic 模型
    对应组件类型: type: "crud2"
    文档地址: docs/amis-crud2-documentation.md
    """

    type: Literal["crud2"] = Field("crud2", description="指定为 crud2 组件")

    # ==================== 基础配置 ====================
    mode: Optional[CRUD2Mode] = Field(None, description="展示模式：'table2'（默认）、'cards'、'list'")
    api: Optional[Union[str, Dict[str, Any], Api]] = Field(None, description="数据接口配置")
    source: Optional[str] = Field(None, description="静态数据源，支持变量表达式")
    primary_field: Optional[str] = Field(None, description="主键字段名，默认为 'id'")

    # ==================== 数据加载配置 ====================
    load_type: Optional[LoadType] = Field(None, description="数据加载模式：''、'pagination'（默认）、'more'")
    per_page: Optional[int] = Field(None, description="每页显示条数（加载更多模式）")
    load_data_once: Optional[bool] = Field(None, description="是否前端分页模式，默认为 false")
    sync_location: Optional[bool] = Field(None, description="是否同步查询条件到地址栏，默认为 true")
    page_field: Optional[str] = Field(None, description="页码字段名，默认为 'page'")
    per_page_field: Optional[str] = Field(None, description="每页条数字段名，默认为 'perPage'")

    # ==================== 选择配置 ====================
    selectable: Optional[bool] = Field(None, description="是否可选择行，默认为 false")
    multiple: Optional[bool] = Field(None, description="是否支持多选，默认为 false")
    show_selection: Optional[bool] = Field(None, description="是否显示已选数据区域，默认为 true")
    keep_item_selection_on_page_change: Optional[bool] = Field(None, description="翻页时是否保留选择，默认为 false")

    # ==================== 接口配置 ====================
    quick_save_api: Optional[Union[str, Dict[str, Any], Api]] = Field(None, description="快速编辑批量保存接口")
    quick_save_item_api: Optional[Union[str, Dict[str, Any], Api]] = Field(None, description="单行快速编辑保存接口")
    save_order_api: Optional[Union[str, Dict[str, Any], Api]] = Field(None, description="拖拽排序保存接口")

    # ==================== 样式配置 ====================
    auto_fill_height: Optional[bool] = Field(None, description="是否自动填充高度，默认为 false")
    header_toolbar: Optional[List[Any]] = Field(None, description="头部工具栏配置")
    footer_toolbar: Optional[List[Any]] = Field(None, description="底部工具栏配置")
    header_toolbar_class_name: Optional[str] = Field(None, description="头部工具栏 CSS 类名")
    footer_toolbar_class_name: Optional[str] = Field(None, description="底部工具栏 CSS 类名")

    # ==================== 高级配置 ====================
    interval: Optional[int] = Field(None, description="自动刷新间隔（毫秒）")
    silent_polling: Optional[bool] = Field(None, description="是否静默拉取数据，默认为 false")
    stop_auto_refresh_when: Optional[str] = Field(None, description="停止自动刷新的条件表达式")
    pull_refresh: Optional[Dict[str, Any]] = Field(None, description="下拉刷新配置（移动端）")
    auto_jump_to_top_on_pager_change: Optional[bool] = Field(None, description="翻页时是否自动回到顶部，默认为 true")

    # ==================== 其他配置 ====================
    columns: Optional[List[Any]] = Field(None, description="列配置，仅在 table2 模式下有效")
    filter: Optional[Any] = Field(None, description="筛选条件配置")
    card: Optional[Any] = Field(None, description="卡片配置，仅在 cards 模式下有效")
    list_item: Optional[Any] = Field(None, description="列表项配置，仅在 list 模式下有效")
    ds_type: Optional[str] = Field(None, description="数据源类型")
    row_selection: Optional[Dict[str, Any]] = Field(None, description="行选择配置")
    bordered: Optional[bool] = Field(None, description="是否显示边框")
    sticky: Optional[bool] = Field(None, description="是否粘性定位")
    debug: Optional[bool] = Field(None, description="是否开启调试模式")

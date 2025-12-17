from typing import Optional, Literal, List, Dict, Union, Any
from enum import Enum

from pydantic import Field

from amis_python import Api
from amis_python.builder import BaseModel


# ====================== 枚举类型 ======================

class CRUDMode(str, Enum):
    TABLE = "table"      # 表格模式（默认）
    CARDS = "cards"        # 卡片模式
    LIST = "list"          # 列表模式

class OrderDir(str, Enum):
    ASC = "asc"            # 升序
    DESC = "desc"          # 降序


# ====================== 主模型 ======================

class CRUD(BaseModel):
    """
    amis CRUD 组件完整 Pydantic 模型
    对应组件类型: type: "crud"
    文档地址: docs/zh-CN/components/crud.md
    """

    type: Literal["crud"] = Field("crud", description="指定为 crud 组件")

    # ==================== 基本配置 ====================
    api: Optional[Union[str, Dict[str, Any], Api]] = Field(None, description="数据接口配置")
    sync_location: Optional[bool] = Field(None, description="是否同步查询条件到地址栏")
    columns: Optional[List[Any]] = Field(None, description="列配置")
    name: Optional[str] = Field(None, description="组件名称，用于数据域通信")
    default_params: Optional[Dict[str, Any]] = Field(None, description="配置拉取接口时的默认参数")
    interval: Optional[int] = Field(None, description="自动刷新间隔（毫秒），最低为 1000")
    stop_auto_refresh_when: Optional[str] = Field(None, description="停止自动刷新的条件表达式")
    per_page: Optional[int] = Field(None, description="每页数量")
    switch_per_page: Optional[bool] = Field(None, description="是否显示切换每页数量的下拉框")
    columns_togglable: Optional[bool] = Field(None, description="是否允许切换列显示")
    affix_header: Optional[bool] = Field(None, description="是否固定表头")
    title: Optional[str] = Field(None, description="组件标题")
    placeholder: Optional[str] = Field(None, description="空数据时的提示")
    mode: Optional[CRUDMode] = Field(None, description="展示模式：table（默认）、list、cards")

    # ==================== 数据源配置 ====================
    source: Optional[str] = Field(None, description="静态数据源，支持变量表达式")
    load_data_once: Optional[bool] = Field(None, description="是否前端分页模式")
    defer_api: Optional[Union[str, Dict[str, Any], Api]] = Field(None, description="嵌套懒加载接口")
    page_field: Optional[str] = Field(None, description="分页字段名")
    per_page_field: Optional[str] = Field(None, description="每页数量字段名")

    # ==================== 展示配置 ====================
    columns_count: Optional[int] = Field(None, description="卡片模式下的列数")
    header_toolbar: Optional[List[Any]] = Field(None, description="头部工具栏配置")
    footer_toolbar: Optional[List[Any]] = Field(None, description="底部工具栏配置")
    card: Optional[Dict[str, Any]] = Field(None, description="卡片配置，仅在 cards 模式下有效")
    list_item: Optional[Dict[str, Any]] = Field(None, description="列表项配置，仅在 list 模式下有效")
    bordered: Optional[bool] = Field(None, description="是否显示边框")
    sticky: Optional[bool] = Field(None, description="是否粘性定位")
    debug: Optional[bool] = Field(None, description="是否开启调试模式")

    # ==================== 操作配置 ====================
    filter: Optional[Any] = Field(None, description="筛选条件配置")
    auto_generate_filter: Optional[Union[bool, Dict[str, Any]]] = Field(None, description="是否自动生成查询区域")
    quick_edit: Optional[bool] = Field(None, description="是否支持快速编辑")
    quick_save_api: Optional[Union[str, Dict[str, Any], Api]] = Field(None, description="快速编辑保存接口")

    # ==================== 高级配置 ====================
    parse_primitive_query: Optional[Union[bool, Dict[str, Any]]] = Field(None, description="解析 Query 原始类型配置")
    can_access_super_data: Optional[bool] = Field(None, description="是否允许访问父级数据域")
    target: Optional[str] = Field(None, description="表单提交目标")
    ds_type: Optional[str] = Field(None, description="数据源类型")
    row_selection: Optional[Dict[str, Any]] = Field(None, description="行选择配置")
    show_header: Optional[bool] = Field(None, description="是否显示头部")
    show_footer: Optional[bool] = Field(None, description="是否显示底部")
    header_class_name: Optional[str] = Field(None, description="头部 CSS 类名")
    body_class_name: Optional[str] = Field(None, description="主体 CSS 类名")
    footer_class_name: Optional[str] = Field(None, description="底部 CSS 类名")
    table_layout: Optional[str] = Field(None, description="表格布局")
    row_class_name: Optional[str] = Field(None, description="行 CSS 类名")
    row_merge: Optional[Dict[str, Any]] = Field(None, description="行合并配置")
    column_merge: Optional[Dict[str, Any]] = Field(None, description="列合并配置")
    scroll_x: Optional[Union[int, str]] = Field(None, description="横向滚动宽度")
    scroll_y: Optional[Union[int, str]] = Field(None, description="纵向滚动高度")
    auto_fill_height: Optional[bool] = Field(None, description="是否自动填充高度")
    auto_jump_to_top_on_pager_change: Optional[bool] = Field(None, description="翻页时是否自动回到顶部")
    silent_polling: Optional[bool] = Field(None, description="是否静默拉取数据")
    pull_refresh: Optional[Dict[str, Any]] = Field(None, description="下拉刷新配置（移动端）")
    check_on_init: Optional[bool] = Field(None, description="初始化时是否检查数据")
    check_on_init_delay: Optional[int] = Field(None, description="初始化检查延迟时间")
    check_on_init_api: Optional[Union[str, Dict[str, Any], Api]] = Field(None, description="初始化检查接口")
    init_data: Optional[Dict[str, Any]] = Field(None, description="初始化数据")
    init_fetch: Optional[bool] = Field(None, description="是否初始拉取数据")
    reload: Optional[str] = Field(None, description="刷新策略")
    replace_data: Optional[bool] = Field(None, description="是否替换数据")
    prepend_data: Optional[bool] = Field(None, description="是否前置数据")
    append_data: Optional[bool] = Field(None, description="是否追加数据")
    clear_data: Optional[bool] = Field(None, description="是否清空数据")
    reset_page: Optional[bool] = Field(None, description="是否重置页码")
    reset_filters: Optional[bool] = Field(None, description="是否重置筛选条件")
    reset_sorters: Optional[bool] = Field(None, description="是否重置排序条件")
    reset_params: Optional[bool] = Field(None, description="是否重置参数")
    cache: Optional[bool] = Field(None, description="是否缓存数据")
    cache_key: Optional[str] = Field(None, description="缓存键")
    cache_duration: Optional[int] = Field(None, description="缓存 duration")
    defer: Optional[bool] = Field(None, description="是否延迟加载")
    defer_params: Optional[Dict[str, Any]] = Field(None, description="延迟加载参数")
    batch_actions: Optional[List[Any]] = Field(None, description="批量操作配置")
    item_actions: Optional[List[Any]] = Field(None, description="行操作配置")
    selection_config: Optional[Dict[str, Any]] = Field(None, description="选择配置")
    tree_config: Optional[Dict[str, Any]] = Field(None, description="树形配置")
    expand_config: Optional[Dict[str, Any]] = Field(None, description="展开配置")
    collapse_config: Optional[Dict[str, Any]] = Field(None, description="折叠配置")
    edit_config: Optional[Dict[str, Any]] = Field(None, description="编辑配置")
    view_config: Optional[Dict[str, Any]] = Field(None, description="查看配置")
    delete_config: Optional[Dict[str, Any]] = Field(None, description="删除配置")
    export_config: Optional[Dict[str, Any]] = Field(None, description="导出配置")
    import_config: Optional[Dict[str, Any]] = Field(None, description="导入配置")
    copy_config: Optional[Dict[str, Any]] = Field(None, description="复制配置")
    move_config: Optional[Dict[str, Any]] = Field(None, description="移动配置")
    bulk_config: Optional[Dict[str, Any]] = Field(None, description="批量配置")
    statistics_config: Optional[Dict[str, Any]] = Field(None, description="统计配置")
    summary: Optional[Any] = Field(None, description="汇总配置")
    operation_column: Optional[Dict[str, Any]] = Field(None, description="操作列配置")
    operation_column_label: Optional[str] = Field(None, description="操作列标题")
    operation_column_width: Optional[Union[int, str]] = Field(None, description="操作列宽度")
    operation_column_fixed: Optional[Union[bool, str]] = Field(None, description="操作列是否固定")
    operation_column_min_width: Optional[Union[int, str]] = Field(None, description="操作列最小宽度")
    operation_column_max_width: Optional[Union[int, str]] = Field(None, description="操作列最大宽度")
    operation_column_class_name: Optional[str] = Field(None, description="操作列 CSS 类名")
    operation_column_header_class_name: Optional[str] = Field(None, description="操作列表头 CSS 类名")
    operation_column_body_class_name: Optional[str] = Field(None, description="操作列体 CSS 类名")
    operation_column_footer_class_name: Optional[str] = Field(None, description="操作列尾 CSS 类名")
    operation_column_align: Optional[str] = Field(None, description="操作列对齐方式")
    operation_column_valign: Optional[str] = Field(None, description="操作列垂直对齐方式")
    operation_column_wrap: Optional[bool] = Field(None, description="操作列是否换行")
    operation_column_ellipsis: Optional[bool] = Field(None, description="操作列是否省略")
    operation_column_tooltip: Optional[Union[bool, Dict[str, Any]]] = Field(None, description="操作列提示配置")
    operation_column_hidden: Optional[bool] = Field(None, description="操作列是否隐藏")
    operation_column_disabled: Optional[bool] = Field(None, description="操作列是否禁用")
    operation_column_read_only: Optional[bool] = Field(None, description="操作列是否只读")
    operation_column_visible: Optional[bool] = Field(None, description="操作列是否可见")
    operation_column_required: Optional[bool] = Field(None, description="操作列是否必填")
    operation_column_unique: Optional[bool] = Field(None, description="操作列是否唯一")
    operation_column_validations: Optional[List[Dict[str, Any]]] = Field(None, description="操作列验证规则")
    operation_column_validation_errors: Optional[List[str]] = Field(None, description="操作列验证错误")
    operation_column_validation_status: Optional[str] = Field(None, description="操作列验证状态")
    operation_column_messages: Optional[Dict[str, Any]] = Field(None, description="操作列消息配置")
    operation_column_description: Optional[str] = Field(None, description="操作列描述")
    operation_column_documentation: Optional[str] = Field(None, description="操作列文档")
    operation_column_examples: Optional[List[Dict[str, Any]]] = Field(None, description="操作列示例")
    operation_column_schema: Optional[Dict[str, Any]] = Field(None, description="操作列 Schema")
    operation_column_json_schema: Optional[Dict[str, Any]] = Field(None, description="操作列 JSON Schema")
    operation_column_ui_schema: Optional[Dict[str, Any]] = Field(None, description="操作列 UI Schema")
    operation_column_meta: Optional[Dict[str, Any]] = Field(None, description="操作列元数据")
    operation_column_custom_context: Optional[Dict[str, Any]] = Field(None, description="操作列自定义上下文")
    operation_column_custom_settings: Optional[Dict[str, Any]] = Field(None, description="操作列自定义设置")

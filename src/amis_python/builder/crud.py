from typing import Literal, Union, Optional, List, Dict, Any

from amis_python import BaseBuilder, AmisApiObject


class CRUDBuilder(BaseBuilder):
    """
    CRUD 组件的配置对象，对应 <CRUD> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/crud
    """
    type: Literal["crud"] = "crud"
    mode: Literal["table", "cards", "list"] = "table"
    # API地址或API对象，用于获取数据
    api: Optional[Union[AmisApiObject, str, Dict[str, Any]]] = None
    # 数据源接口地址，可以通过变量实现动态拼接
    source: Optional[str] = None
    # 分页，从1开始
    page: Optional[int] = None
    # 每页数量
    per_page: Optional[int] = None
    # 排序字段，目前CRUD只支持一个
    order_by: Optional[str] = None
    # 排序方式，可选值：asc、desc
    order_dir: Optional[Literal["asc", "desc"]] = None
    # 搜索关键字
    keywords: Optional[str] = None
    # 是否同步地址栏参数
    sync_location: Optional[bool] = None
    # 解析Query原始类型配置，支持将字符串类型转换为布尔值或数字
    parse_primitive_query: Optional[Union[bool, Dict[str, Any]]] = None
    # 没有数据时的文字提示
    placeholder: Optional[str] = None
    # 外层CSS类名
    class_name: Optional[str] = None
    # 顶部外层CSS类名
    header_class_name: Optional[str] = None
    # 底部外层CSS类名
    footer_class_name: Optional[str] = None
    # 是否只加载一次数据，开启后不会自动刷新
    load_data_once: Optional[bool] = None
    # 默认查询参数，每次请求都会带上
    default_params: Optional[Dict[str, Any]] = None
    # 快速保存API，用于行内快速编辑保存
    quick_save_api: Optional[Union[AmisApiObject, str, Dict[str, Any]]] = None
    # 批量操作配置，用于配置批量操作按钮
    bulk_actions: Optional[List[Any]] = None
    # 主键字段，默认使用id
    primary_key: Optional[str] = None
    # 顶部工具栏配置
    header_toolbar: Optional[List[Any]] = None
    # 底部工具栏配置
    footer_toolbar: Optional[List[Any]] = None
    # 筛选条件配置
    filter: Optional[Any] = None
    # 默认是否显示筛选条件
    filter_default_visible: Optional[bool] = None
    # 列配置，表格模式下的列定义
    columns: Optional[List[Dict[str, Any]]] = None
    # 操作列配置，用于配置行操作按钮
    operations: Optional[List[Any]] = None
    # 自动填充高度，支持布尔值或具体高度值
    auto_fill_height: Optional[Union[bool, int]] = None
    # 自动刷新间隔，单位：秒
    interval: Optional[int] = None
    # 弹窗打开时是否停止自动刷新
    stop_auto_refresh_when_modal_open: Optional[bool] = None
    # 全选模式，可选值：page（仅当前页）、all（所有数据）
    select_all_mode: Optional[Literal["page", "all"]] = None
    # 列状态保存配置，用于保存列的显示状态
    columns_state: Optional[Dict[str, Any]] = None
    # 行是否可删除，支持表达式
    row_deletable: Optional[Union[bool, str]] = None
    # 行是否禁用，支持表达式
    row_disabled: Optional[Union[bool, str]] = None
    # 行CSS类名，支持表达式
    row_class_name: Optional[Union[str, Dict[str, Any]]] = None
    # 行选择配置，用于配置行选择相关功能
    row_selection: Optional[Dict[str, Any]] = None
    # 是否显示勾选框
    checkable: Optional[bool] = None
    # 勾选框列宽
    check_column_width: Optional[Union[str, int]] = None


class CRUDTableBuilder(CRUDBuilder):
    """
    CRUD 表格模式配置对象，对应 <CRUD mode="table"> 组件。
    参考文档：
    - https://aisuda.bce.baidu.com/amis/zh-CN/components/crud
    - https://aisuda.bce.baidu.com/amis/zh-CN/components/table#%E5%88%97%E9%85%8D%E7%BD%AE%E5%B1%9E%E8%A1%A8
    """
    mode: Literal["table"] = "table"
    # 列配置
    columns: Optional[List[Dict[str, Any]]] = None
    # 表格布局方式
    table_layout: Optional[Literal["auto", "fixed"]] = None
    # 是否显示序号
    show_index: Optional[bool] = None
    # 序号列宽度
    index_column_width: Optional[Union[str, int]] = None
    # 是否显示选择框
    selectable: Optional[bool] = None
    # 是否为多选
    multiple: Optional[bool] = None
    # 点击行是否选中
    check_on_item_click: Optional[bool] = None
    # 是否显示列切换按钮
    columns_togglable: Optional[Union[bool, Literal["auto"]]] = None
    # 默认折叠列
    columns_default_fold: Optional[List[str]] = None
    # 列是否可折叠
    columns_foldable: Optional[bool] = None
    # 是否显示行头
    row_header: Optional[bool] = None
    # 是否隐藏表头
    hide_header: Optional[bool] = None
    # 是否显示边框
    bordered: Optional[bool] = None
    # 是否显示斑马纹
    striped: Optional[bool] = None
    # 是否高亮当前行
    highlight_row: Optional[bool] = None
    # 行是否可悬停
    row_hoverable: Optional[bool] = None
    # 合并单元格配置
    combine_num: Optional[int] = None
    # 合并单元格起始索引
    combine_from_index: Optional[int] = None
    # 是否启用 footable
    footable: Optional[Union[bool, Dict[str, Any]]] = None
    # 是否显示汇总行
    show_summary: Optional[bool] = None
    # 汇总数据
    summary_data: Optional[List[Any]] = None
    # 展开行配置
    expand_config: Optional[Dict[str, Any]] = None
    # 树形结构配置
    tree_config: Optional[Dict[str, Any]] = None
    # 是否固定表头
    fixed_header: Optional[bool] = None
    # 虚拟列表配置
    virtual_list: Optional[Union[bool, Dict[str, Any]]] = None
    # 表格行点击事件
    on_item_click: Optional[Dict[str, Any]] = None
    # 表格行双击事件
    on_row_double_click: Optional[Dict[str, Any]] = None
    # 列排序事件
    on_column_sort: Optional[Dict[str, Any]] = None
    # 列宽调整事件
    on_column_resize: Optional[Dict[str, Any]] = None
    # 列显示隐藏事件
    on_column_visible_change: Optional[Dict[str, Any]] = None
    # 勾选事件
    on_check: Optional[Dict[str, Any]] = None
    # 全选事件
    on_check_all: Optional[Dict[str, Any]] = None


class CRUDCardsBuilder(CRUDBuilder):
    """
    CRUD 卡片模式配置对象，对应 <CRUD mode="cards"> 组件。
    参考文档：
    - https://aisuda.bce.baidu.com/amis/zh-CN/components/crud
    - https://aisuda.bce.baidu.com/amis/zh-CN/components/cards?page=1
    """
    mode: Literal["cards"] = "cards"
    # 卡片 CSS 类名
    item_class_name: Optional[str] = None
    # 卡片配置
    card: Optional[Dict[str, Any]] = None
    # 卡片组是否可选
    selectable: Optional[bool] = None
    # 卡片组是否为多选
    multiple: Optional[bool] = None
    # 点选卡片内容是否选中卡片
    check_on_item_click: Optional[bool] = None
    # 是否开启瀑布流布局模式
    masonry_layout: Optional[bool] = None
    # 固定列数
    columns_count: Optional[int] = None
    # 卡片头部配置
    card_header: Optional[Any] = None
    # 卡片内容配置
    card_body: Optional[Any] = None
    # 卡片底部配置
    card_footer: Optional[Any] = None
    # 卡片间距
    card_gap: Optional[Union[str, int]] = None
    # 卡片宽度
    card_width: Optional[Union[str, int]] = None
    # 卡片高度
    card_height: Optional[Union[str, int]] = None
    # 卡片选择样式
    card_selected_class_name: Optional[str] = None
    # 卡片悬停样式
    card_hover_class_name: Optional[str] = None
    # 卡片加载状态
    loading_state: Optional[Dict[str, Any]] = None
    # 卡片空状态
    empty_state: Optional[Dict[str, Any]] = None
    # 卡片列表样式
    list_class_name: Optional[str] = None
    # 卡片容器样式
    container_class_name: Optional[str] = None




class CRUDListBuilder(CRUDBuilder):
    """
    CRUD 列表模式配置对象，对应 <CRUD mode="list"> 组件。
    参考文档：
    - https://aisuda.bce.baidu.com/amis/zh-CN/components/crud
    - https://aisuda.bce.baidu.com/amis/zh-CN/components/list
    """
    mode: Literal["list"] = "list"
    # 列表项配置
    list_item: Optional[List[Dict[str, Any]]] = None
    # 列表是否可选
    selectable: Optional[bool] = None
    # 列表是否为多选
    multiple: Optional[bool] = None
    # 点击行操作配置
    item_action: Optional[Dict[str, Any]] = None
    # 是否显示右侧字母索引条
    show_index_bar: Optional[bool] = None
    # 索引依据字段，默认使用 title 字段或列表项标题
    index_field: Optional[str] = None
    # 索引条偏移量，用于设置点击索引条跳转时的滚动位置偏移
    index_bar_offset: Optional[int] = None
    # 外层 CSS 类名
    inner_class_name: Optional[str] = None
    # 列表项 CSS 类名
    item_class_name: Optional[str] = None
    # 列表容器 CSS 类名
    list_class_name: Optional[str] = None
    # 列表项模板
    item_template: Optional[Any] = None
    # 列表项点击事件
    on_item_click: Optional[Dict[str, Any]] = None
    # 列表项双击事件
    on_item_double_click: Optional[Dict[str, Any]] = None
    # 列表滚动到底部事件
    on_scroll_to_bottom: Optional[Dict[str, Any]] = None
    # 滚动容器配置
    scroll_container: Optional[Union[str, Dict[str, Any]]] = None
    # 列表高度
    list_height: Optional[Union[str, int]] = None
    # 是否显示分割线
    split: Optional[bool] = None
    # 是否紧凑模式
    compact: Optional[bool] = None
    # 列表项对齐方式
    align: Optional[Literal["left", "center", "right"]] = None
    # 列表项垂直对齐方式
    vertical_align: Optional[Literal["top", "middle", "bottom"]] = None
    # 索引条样式
    index_bar_class_name: Optional[str] = None
    # 索引条激活样式
    index_bar_active_class_name: Optional[str] = None
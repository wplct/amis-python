from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder.form.form_item import FormItem


class Select(FormItem):
    """
    amis Select 选择器组件
    对应组件类型: select
    文档地址: https://aisuda.bce.baidu.com/amis/zh-CN/components/form/select
    """

    # ==================== 基本属性 ====================
    type: Literal["select"] = Field("select", description="指定为选择器组件")

    # ==================== 选项相关属性 ====================
    options: Optional[Union[List[Dict[str, Any]], List[str]]] = Field(None, description="选项组")
    source: Optional[Union[str, Dict[str, Any]]] = Field(None, description="动态选项组")
    auto_complete: Optional[Union[str, Dict[str, Any]]] = Field(None, description="自动提示补全")

    # ==================== 选项处理属性 ====================
    delimiter: Optional[str] = Field(None, description="拼接符")
    label_field: Optional[str] = Field(None, description="选项标签字段，默认值为 'label'")
    value_field: Optional[str] = Field(None, description="选项值字段，默认值为 'value'")
    join_values: Optional[bool] = Field(None, description="拼接值，默认值为 True")
    extract_value: Optional[bool] = Field(None, description="提取多选值，默认值为 False")
    multiple: Optional[bool] = Field(None, description="是否多选，默认值为 false")

    # ==================== 全选属性 ====================
    check_all: Optional[bool] = Field(None, description="是否支持全选，默认值为 false")
    check_all_label: Optional[str] = Field(None, description="全选的文字，默认值为 '全选'")
    check_all_by_search: Optional[bool] = Field(None, description="有检索时只全选检索命中的项，默认值为 true")
    default_check_all: Optional[bool] = Field(None, description="默认是否全选，默认值为 false")

    # ==================== 可创建选项属性 ====================
    creatable: Optional[bool] = Field(None, description="是否支持新增选项")
    create_btn_label: Optional[str] = Field(None, description="新增选项按钮文字，默认值为 '新增选项'")
    add_controls: Optional[List[Dict[str, Any]]] = Field(None, description="自定义新增表单项")
    add_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="配置新增选项接口")

    # ==================== 可编辑选项属性 ====================
    editable: Optional[bool] = Field(None, description="是否支持编辑选项")
    edit_controls: Optional[List[Dict[str, Any]]] = Field(None, description="自定义编辑表单项")
    edit_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="配置编辑选项接口")

    # ==================== 可删除选项属性 ====================
    removable: Optional[bool] = Field(None, description="是否支持删除选项")
    delete_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="配置删除选项接口")

    # ==================== 显示模式属性 ====================
    select_mode: Optional[Literal["group", "table", "tree", "chained", "associated"]] = Field(None, description="选择模式，可选：list、group、table、tree、chained、associated")
    search_result_mode: Optional[Literal["group", "table", "tree", "chained", "associated"]] = Field(None, description="搜索结果展示模式，参考 selectMode")
    columns: Optional[List[Dict[str, Any]]] = Field(None, description="当展示形式为 table 时，配置展示的列")
    left_options: Optional[List[Dict[str, Any]]] = Field(None, description="当展示形式为 associated 时，配置左边的选项集")
    left_mode: Optional[Literal["list", "tree"]] = Field(None, description="当展示形式为 associated 时，配置左边的选择形式")
    right_mode: Optional[Literal["list", "table", "tree", "chained"]] = Field(None, description="当展示形式为 associated 时，配置右边的选择形式")

    # ==================== 标签处理属性 ====================
    max_tag_count: Optional[int] = Field(None, description="标签的最大展示数量，超出数量后以收纳浮层的方式展示")
    overflow_tag_popover: Optional[Dict[str, Any]] = Field(None, description="收纳浮层的配置属性，参考 Tooltip")

    # ==================== 其他属性 ====================
    menu_tpl: Optional[str] = Field(None, description="自定义菜单模板")
    clearable: Optional[bool] = Field(None, description="单选模式下是否支持清空")
    hide_selected: Optional[bool] = Field(None, description="隐藏已选选项")
    mobile_class_name: Optional[str] = Field(None, description="移动端浮层类名")
    overlay: Optional[Dict[str, Any]] = Field(None, description="自定义下拉区域宽度与对齐方式")
    defer: Optional[bool] = Field(None, description="是否延时加载选项")
    defer_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="延时加载选项的接口")
    search_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="搜索接口")
    filter_option: Optional[Union[str, Dict[str, Any]]] = Field(None, description="自定义搜索过滤函数")
    sortable: Optional[bool] = Field(None, description="是否支持排序")
    auto_fill: Optional[Dict[str, Any]] = Field(None, description="自动填充配置")
    searchable: Optional[bool] = Field(None, description="是否支持检索")
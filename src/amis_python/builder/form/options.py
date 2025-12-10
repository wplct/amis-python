from __future__ import annotations
from typing import Optional, Literal, Any, Dict, List

from .form_item import FormItemBuilder


class OptionsBuilder(FormItemBuilder):
    """
    构建 AMIS 选择器表单项配置对象，对应具有选择器特性的表单项。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/form/formitem#%E9%80%89%E6%8B%A9%E5%99%A8%E8%A1%A8%E5%8D%95%E9%A1%B9
    
    示例：
        options = OptionsBuilder(
            name="select_field",
            label="选择字段",
            options=[
                {"label": "选项1", "value": "value1"},
                {"label": "选项2", "value": "value2"}
            ],
            multiple=True
        )
    """
    # 选项相关属性
    options: Optional[List[Dict[str, Any]]] = None  # 静态选项组
    source: Optional[Any] = None  # 动态选项组源，可通过数据映射获取当前数据域变量、或者配置 API 对象
    
    # 选择模式属性
    multiple: Optional[bool] = None  # 是否支持多选，默认：False
    check_all: Optional[bool] = None  # 是否支持全选，默认：False
    
    # 数据格式属性
    delimiter: Optional[str] = None  # 多选值拼接符，默认："," 
    join_values: Optional[bool] = None  # 是否拼接value值，默认：True
    extract_value: Optional[bool] = None  # 是否将value值抽取出来组成新的数组，只有在join_values是false时生效，默认：False
    
    # 搜索与补全属性
    searchable: Optional[bool] = None  # 是否支持搜索，默认：False
    auto_complete: Optional[Any] = None  # 自动补全配置
    
    # 选项字段配置
    label_field: Optional[str] = None  # 选项标签字段，默认："label"
    value_field: Optional[str] = None  # 选项值字段，默认："value"
    defer_field: Optional[str] = None  # 选项延迟加载字段，默认："defer"
    
    # 新增选项属性
    creatable: Optional[bool] = None  # 是否支持前端新增选项，默认：False
    create_btn_label: Optional[str] = None  # 新增选项按钮文本
    option_label: Optional[str] = None  # 选项名称，用于自定义新增/编辑弹框标题
    add_controls: Optional[List[Any]] = None  # 自定义新增表单项
    add_dialog: Optional[Dict[str, Any]] = None  # 自定义新增弹框配置
    
    # 编辑选项属性
    editable: Optional[bool] = None  # 是否支持前端编辑选项，默认：False
    edit_controls: Optional[List[Any]] = None  # 自定义编辑表单项
    edit_dialog: Optional[Dict[str, Any]] = None  # 自定义编辑弹框配置
    
    # 删除选项属性
    removable: Optional[bool] = None  # 是否支持删除选项，默认：False
    
    # 选项操作接口
    add_api: Optional[Any] = None  # 新增选项接口
    edit_api: Optional[Any] = None  # 编辑选项接口
    delete_api: Optional[Any] = None  # 删除选项接口
    
    # 自动填充属性
    auto_fill: Optional[Any] = None  # 自动填充配置
    init_auto_fill: Optional[Literal[True, False, "fillIfNotSet"]] = None  # 初始化时是否自动填充，默认："fillIfNotSet"
    
    # 虚拟渲染属性
    item_height: Optional[int] = None  # 每个选项的高度，用于虚拟渲染，默认：32
    virtual_threshold: Optional[int] = None  # 开启虚拟渲染的阈值，默认：100
    
    # 其他属性
    values_no_wrap: Optional[bool] = None  # 多选值是否不折行，默认：False
    clear_value_on_source_change: Optional[bool] = None  # 数据源变化时是否清空值
    select_first: Optional[bool] = None  # 是否默认选择第一个选项，默认：False

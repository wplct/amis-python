from typing import Optional, Literal, Union, List, Dict, Any
from pydantic import Field

from amis_python.builder import BaseModel


class Pagination(BaseModel):
    """
    amis Pagination 分页组件
    对应组件类型: pagination
    文档地址: docs/zh-CN/components/pagination.md
    """

    # ==================== 基本属性 ====================
    type: Literal["pagination"] = Field("pagination", description="指定为 Pagination 渲染器")
    
    # ==================== 分页属性 ====================
    mode: Optional[Literal["normal", "simple"]] = Field(None, description="迷你版本/简易版本 只显示左右箭头，配合 hasNext 使用")
    layout: Optional[Union[str, List[str]]] = Field(None, description="通过控制 layout 属性的顺序，调整分页结构布局")
    max_buttons: Optional[Union[int, str]] = Field(None, description="最多显示多少个分页按钮，最小为 5")
    total: Optional[Union[int, str]] = Field(None, description="总条数")
    active_page: Optional[Union[int, str]] = Field(None, description="当前页数")
    per_page: Optional[Union[int, str]] = Field(None, description="每页显示多条数据")
    show_per_page: Optional[bool] = Field(None, description="是否展示 perPage 切换器 layout 和 showPerPage 都可以控制")
    size: Optional[Literal["sm", "md"]] = Field(None, description="组件尺寸，支持md、sm设置")
    ellipsis_page_gap: Optional[Union[int, str]] = Field(None, description="多页跳转页数，页数较多出现...时点击省略号时每次前进/后退的页数，默认为5")
    per_page_available: Optional[List[int]] = Field(None, description="指定每页可以显示多少条")
    show_page_input: Optional[bool] = Field(None, description="是否显示快速跳转输入框 layout 和 showPageInput 都可以控制")
    disabled: Optional[bool] = Field(None, description="是否禁用")
    has_next: Optional[bool] = Field(None, description="是否有下一页，配合 simple 模式使用")
    last_page: Optional[Union[int, str]] = Field(None, description="最后一页")
    on_event: Optional[Dict[str, Any]] = Field(None, description="事件配置")
    on_page_change: Optional[Any] = Field(None, description="page、perPage 改变时会触发")

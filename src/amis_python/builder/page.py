from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field

from .base import BaseBuilder
from .api import AmisApiObject


class PageBuilder(BaseBuilder):
    """
    构建 AMIS 页面的配置对象，对应 <Page> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/page
    
    示例：
        page = PageBuilder(
            title="首页",
            body=[
                # 页面内容组件
            ]
        )
    """
    type: Literal["page"] = "page"
    
    # === 基本信息 ===
    title: Optional[str] = Field(None, description="页面标题")
    sub_title: Optional[Any] = Field(None, description="页面副标题")
    remark: Optional[Any] = Field(None, description="标题附近的提示图标，鼠标放上去会提示该内容")
    
    # === 区域配置 ===
    body: Union[str, List[Any]] = Field(default_factory=list, description="页面内容区域")
    aside: Optional[Union[str, List[Any]]] = Field(None, description="侧边栏区域")
    toolbar: Optional[Union[str, List[Any]]] = Field(None, description="工具栏区域")
    
    # === API 配置 ===
    init_api: Optional[Union[str, "AmisApiObject"]] = Field(None, description="页面初始化请求的接口")
    init_fetch: bool = Field(True, description="是否起始拉取 initApi")
    init_fetch_on: Optional[str] = Field(None, description="是否起始拉取 initApi, 通过表达式配置")
    
    # === 轮询配置 ===
    interval: Optional[int] = Field(None, description="刷新时间(最小 1000 毫秒)")
    silent_polling: bool = Field(False, description="配置刷新时是否显示加载动画")
    stop_auto_refresh_when: Optional[str] = Field(None, description="通过表达式来配置停止刷新的条件")
    
    # === 下拉刷新 ===
    pull_refresh: Optional[Dict[str, Any]] = Field(None, description="下拉刷新配置（仅用于移动端）")
    
    # === 样式配置 ===
    class_name: Optional[str] = Field(None, description="外层 dom 类名")
    css_vars: Optional[Dict[str, str]] = Field(None, description="自定义 CSS 变量，用于主题定制")
    toolbar_class_name: Optional[str] = Field(None, description="Toolbar dom 类名")
    body_class_name: Optional[str] = Field(None, description="Body dom 类名")
    aside_class_name: Optional[str] = Field(None, description="Aside dom 类名")
    header_class_name: Optional[str] = Field(None, description="Header 区域 dom 类名")
    
    # === 侧边栏配置 ===
    aside_resizor: Optional[bool] = Field(None, description="页面的边栏区域宽度是否可调整")
    aside_min_width: Optional[int] = Field(None, description="页面边栏区域的最小宽度")
    aside_max_width: Optional[int] = Field(None, description="页面边栏区域的最大宽度")
    aside_position: Literal["left", "right"] = Field("left", description="页面边栏区域的位置")
    aside_sticky: bool = Field(True, description="用来控制边栏固定与否")
    
    # === 自定义 CSS ===
    custom_style: Optional[str] = Field(None, description="自定义 CSS 样式")


PageBuilder.model_rebuild()

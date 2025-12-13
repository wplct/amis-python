from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, Literal

from ..base import BaseModel, Field
from ..api import AmisApiObject


class PageBuilder(BaseModel):
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
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    type: Literal["page"] = Field("page", description="指定为 Page 组件")
    
    # === 基本信息 ===
    title: Optional[Any] = Field(None, description="页面标题")
    sub_title: Optional[Any] = Field(None, description="页面副标题")
    remark: Optional[Any] = Field(None, description="标题附近的提示图标，鼠标放上去会提示该内容")
    
    # === 区域配置 ===
    body: Optional[Union[str, List[Any]]] = Field(None, description="往页面的内容区域加内容")
    aside: Optional[Union[str, List[Any]]] = Field(None, description="往页面的边栏区域加内容")
    toolbar: Optional[Union[str, List[Any]]] = Field(None, description="往页面的右上角加内容，需要注意的是，当有 title 时，该区域在右上角，没有时该区域在顶部")
    
    # === API 配置 ===
    init_api: Optional[Union[str, "AmisApiObject"]] = Field(None, description="Page 用来获取初始数据的 api。返回的数据可以整个 page 级别使用")
    init_fetch: Optional[bool] = Field(None, description="是否起始拉取 initApi，默认 true")
    init_fetch_on: Optional[str] = Field(None, description="是否起始拉取 initApi, 通过表达式配置")
    
    # === 轮询配置 ===
    interval: Optional[int] = Field(None, description="刷新时间(最小 1000)，默认 3000")
    silent_polling: Optional[bool] = Field(None, description="配置刷新时是否显示加载动画，默认 false")
    stop_auto_refresh_when: Optional[str] = Field(None, description="通过表达式来配置停止刷新的条件，默认空字符串")
    
    # === 下拉刷新 ===
    pull_refresh: Optional[Dict[str, Any]] = Field(None, description="下拉刷新配置（仅用于移动端），默认 {disabled: true}")
    
    # === 样式配置 ===
    class_name: Optional[str] = Field(None, description="外层 dom 类名")
    css_vars: Optional[Dict[str, str]] = Field(None, description="自定义 CSS 变量")
    toolbar_class_name: Optional[str] = Field(None, description="Toolbar dom 类名，默认 v-middle wrapper text-right bg-light b-b")
    
    # === 样式配置（续） ===
    body_class_name: Optional[str] = Field(None, description="Body dom 类名，默认 wrapper")
    aside_class_name: Optional[str] = Field(None, description="Aside dom 类名，默认 w page-aside-region bg-auto")
    header_class_name: Optional[str] = Field(None, description="Header 区域 dom 类名，默认 bg-light b-b wrapper")
    
    # === 侧边栏配置 ===
    aside_resizor: Optional[bool] = Field(None, description="页面的边栏区域宽度是否可调整")
    aside_min_width: Optional[int] = Field(None, description="页面边栏区域的最小宽度")
    aside_max_width: Optional[int] = Field(None, description="页面边栏区域的最大宽度")
    aside_position: Optional[Literal["left", "right"]] = Field(None, description="页面边栏区域的位置，默认 left")
    aside_sticky: Optional[bool] = Field(None, description="用来控制边栏固定与否，默认 true")
    
    # === 自定义 CSS ===
    css: Optional[Dict[str, Any]] = Field(None, description="自定义 CSS")
    custom_style: Optional[str] = Field(None, description="自定义 CSS 样式")



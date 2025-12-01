from __future__ import annotations
from typing import Any, Dict, List, Union, Optional, Literal
from pydantic import BaseModel, Field

from .api import AmisApiObject
from .base import BaseBuilder
from .page import PageBuilder


class AppPageBuilder(BaseBuilder):
    """
    表示一个应用中的独立页面（可出现在导航菜单中）。
    对应 AMIS pages 配置中的单个页面项（非分组）。
    """
    type: Literal["app-page"] = "app-page"
    label: Optional[str] = Field(None, description="页面在导航菜单中显示的名称")
    children: List[Union["AppPageBuilder", PageBuilder]] = Field(
        default_factory=list,
        description="子页面列表，用于实现嵌套路由或子菜单"
    )


class AppPageGroupBuilder(BaseBuilder):
    """
    表示一个页面分组，用于在侧边栏中对多个页面进行逻辑归类。
    对应 AMIS pages 中 type='group' 的配置项。
    """
    type: Literal["app-group"] = "app-group"
    label: Optional[str] = Field(None, description="分组在导航菜单中显示的标题")
    children: List[Union[AppPageBuilder, AppPageGroupBuilder]] = Field(
        default_factory=list,
        description="分组内包含的页面或嵌套分组"
    )


class AppBuilder(BaseBuilder):
    """
    构建整个 AMIS 应用的根配置对象，对应 <App> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/app

    示例：
        app = AppBuilder(
            brand_name="我的系统",
            pages=[
                AppPageBuilder(label="首页", children=[...]),
                AppPageGroupBuilder(label="用户管理", children=[...])
            ]
        )
    """
    type: Literal["app"] = "app"

    # === 基础信息 ===
    api: Optional[Union[str, AmisApiObject]] = Field(
        None,
        description="动态拉取应用配置的接口。可以是 URL 字符串，或结构化 API 对象（支持 method/data/headers 等）"
    )
    brand_name: str = Field(
        "amis-python",
        alias="brandName",
        description="应用左上角的品牌名称"
    )
    logo: Optional[str] = Field(
        None,
        description="品牌 Logo 图片 URL，显示在品牌名左侧"
    )

    # === 布局控制 ===
    affix_header: bool = Field(
        True,
        alias="affixHeader",
        description="是否固定顶部栏（默认 true）"
    )
    aside_fixed: bool = Field(
        True,
        alias="asideFixed",
        description="是否固定侧边栏（默认 true）"
    )
    aside_folded: bool = Field(
        False,
        alias="asideFolded",
        description="侧边栏是否默认折叠（默认 false）"
    )

    # === 自定义区域 ===
    header: Optional[str] = Field(
        None,
        description="顶部区域内容（支持 HTML 或 amis schema 字符串）"
    )
    toolbar: Optional[str] = Field(
        None,
        description="顶部右侧工具栏内容（常用于放置通知、用户头像等）"
    )
    aside_before: Optional[str] = Field(
        None,
        alias="asideBefore",
        description="侧边栏上方自定义内容"
    )
    aside_after: Optional[str] = Field(
        None,
        alias="asideAfter",
        description="侧边栏下方自定义内容"
    )
    footer: Optional[str] = Field(
        None,
        description="底部区域内容"
    )

    # === 主题与国际化 ===
    css_vars: Optional[Dict[str, str]] = Field(
        None,
        alias="cssVars",
        description="自定义 CSS 变量，用于主题定制（如 {'--primary': '#1890ff'}）"
    )
    locale: Optional[str] = Field(
        None,
        description="语言区域设置，如 'zh-CN'、'en-US'（需配合 localeProvider 使用）"
    )

    # === 页面结构 ===
    pages: List[Union[AppPageBuilder, AppPageGroupBuilder]] = Field(
        default_factory=list,
        description="应用的页面结构，支持顶层直接放置页面或分组（混合列表）"
    )
# from __future__ import annotations
from typing import Any, Dict, List, Union, Optional, Literal

from ..api import AmisApiObject
from ..base import BaseModel, Field
from ..layout.page import PageBuilder
from .group import AppPageGroupBuilder
from .page import AppPageBuilder


class AppBuilder(BaseModel):
    """
    构建整个 AMIS 应用的根配置对象，对应 <App> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/app

    示例：
        app = AppBuilder(
            brand_name="我的系统",
            pages=[
                AppPageGroupBuilder(label="首页", children=[...]),
                AppPageGroupBuilder(label="用户管理", children=[...])
            ]
        )
    """
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    type: Literal["app"] = Field("app", description="组件类型")

    # === 基础信息 ===
    api: Optional[Union[str, AmisApiObject]] = Field(None, description="动态拉取应用配置的接口。可以是 URL 字符串，或结构化 API 对象（支持 method/data/headers 等）")
    brand_name: Optional[str] = Field(None, description="应用左上角的品牌名称")
    logo: Optional[str] = Field(None, description="品牌 Logo 图片 URL，显示在品牌名左侧")
    class_name: Optional[str] = Field(None, description="CSS 类名")

    # === 布局控制 ===
    affix_header: Optional[bool] = Field(None, description="是否固定顶部栏")
    aside_fixed: Optional[bool] = Field(None, description="是否固定侧边栏")
    aside_folded: Optional[bool] = Field(None, description="侧边栏是否默认折叠")

    # === 自定义区域 ===
    header: Optional[Union[str, dict, list]] = Field(None, description="顶部区域内容（支持 HTML 或 amis schema）")
    toolbar: Optional[Union[str, dict]] = Field(None, description="顶部右侧工具栏内容（常用于放置通知、用户头像等）")
    aside_before: Optional[Union[str, dict]] = Field(None, description="页面菜单上前面区域")
    aside_after: Optional[Union[str, dict]] = Field(None, description="页面菜单下前面区域")
    footer: Optional[Union[str, dict]] = Field(None, description="底部区域内容")

    # === 主题与国际化 ===
    css_vars: Optional[Dict[str, str]] = Field(None, description="自定义 CSS 变量，用于主题定制（如 {'--primary': '#1890ff'}）")
    locale: Optional[str] = Field(None, description="语言区域设置，如 'zh-CN'、'en-US'（需配合 localeProvider 使用）")

    # === 页面结构 ===
    pages: Optional[List[AppPageGroupBuilder]] = Field(None, description="应用的页面结构，顶层只允许放置分组")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 添加默认没有名字的分组
        if self.pages is None:
            self.pages = []
        self.pages.append(AppPageGroupBuilder(label="", children=[]))

    def register_page(
            self,
            label: str,
            path: str,
            page: Optional[PageBuilder] = None,
            group_label: Optional[str] = ''
    ) -> AppPageBuilder:
        """
        注册页面，需要指定分组
        
        Args:
            path: 页面路径，如 "/home" 或 "/users/list"
            page: 页面实例
            label: 页面在导航菜单中显示的名称
            group_label: 分组标题，如果未指定，则使用空组
        Returns:
            注册的 AppPageBuilder 实例
        """

        # 将页面添加到指定分组
        group = self.get_group(group_label)
        app_page = group.register_page(label, path)
        if page:
            app_page.set_page_schema(page)
            app_page.schema_api = f"/amis/page{path}"
        return app_page

    def register_page_group(
            self,
            label: str,
            icon: Optional[str] = None,
            class_name: Optional[str] = None
    ) -> AppPageGroupBuilder:
        """
        注册页面分组
        :param label:
        :param icon:
        :param class_name:
        Returns:
            注册的 AppPageGroupBuilder 实例
        """
        # 检查分组标题是否已存在
        for group in self.pages:
            if group.label == label:
                raise ValueError(f"Group '{label}' already exists.")
        # 创建分组实例
        new_group = AppPageGroupBuilder(label=label, icon=icon, class_name=class_name, children=[])
        self.pages.append(new_group)
        return new_group

    def get_group(self, label: str="") -> Optional[AppPageGroupBuilder]:
        """
        根据分组标题获取已注册的分组
        """
        for group in self.pages:
            if group.label == label:
                return group
        raise ValueError(f"Group '{label}' does not exist.")

    def get_page(self, path: str) -> PageBuilder:
        """
        根据路径获取已注册的页面
        """
        # 暂时只支持默认分组
        group = self.get_group()
        return group.get_page(path)

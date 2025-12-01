# from __future__ import annotations
from typing import Any, Dict, List, Union, Optional, Literal
from pydantic import BaseModel, Field

from .api import AmisApiObject
from .base import BaseBuilder
from .page import PageBuilder


# 路径处理工具函数
def parse_path(path: str) -> List[str]:
    """
    解析路径字符串为路径段列表
    
    Args:
        path: 路径字符串，如 "/home" 或 "/users/list"
        
    Returns:
        路径段列表，如 ["home"] 或 ["users", "list"]
    """
    # 移除首尾的斜杠，然后按斜杠分割
    segments = path.strip("/").split("/")
    # 过滤掉空字符串
    return [seg for seg in segments if seg]


def generate_path(segments: List[str]) -> str:
    """
    根据路径段列表生成路径字符串
    
    Args:
        segments: 路径段列表，如 ["home"] 或 ["users", "list"]
        
    Returns:
        路径字符串，如 "/home" 或 "/users/list"
    """
    return f"/{'/'.join(segments)}"


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
    
    def register_page(
        self,
        path: str,
        page: PageBuilder,
        label: Optional[str] = None
    ) -> "AppPageBuilder":
        """
        在当前页面下注册子页面
        
        Args:
            path: 页面路径，如 "/list" 或 "/detail/{id}"
            page: 页面实例
            label: 页面在导航菜单中显示的名称
            
        Returns:
            当前 AppPageBuilder 实例，支持链式调用
        """
        segments = parse_path(path)
        
        if not segments:
            # 路径为空，直接添加到当前页面的 children 中
            if isinstance(page, PageBuilder):
                self.children.append(page)
            return self
        
        # 处理嵌套路径
        child_path = generate_path(segments[1:]) if len(segments) > 1 else ""
        
        # 检查是否已存在同名子页面
        for child in self.children:
            if isinstance(child, AppPageBuilder) and child.label == segments[0]:
                # 已存在，递归注册
                child.register_page(child_path, page, label)
                return self
        
        # 不存在，创建新的 AppPageBuilder
        new_page = AppPageBuilder(label=segments[0], children=[])
        new_page.register_page(child_path, page, label)
        self.children.append(new_page)
        
        return self
    
    def get_page(self, path: str) -> Optional[PageBuilder]:
        """
        根据路径获取已注册的页面
        
        Args:
            path: 页面路径，如 "/list" 或 "/detail/{id}"
            
        Returns:
            找到的 PageBuilder 实例，未找到则返回 None
        """
        segments = parse_path(path)
        
        if not segments:
            # 路径为空，返回当前页面的第一个 PageBuilder 子节点
            for child in self.children:
                if isinstance(child, PageBuilder):
                    return child
            return None
        
        # 遍历子节点
        for child in self.children:
            if isinstance(child, AppPageBuilder) and child.label == segments[0]:
                # 递归查找
                child_path = generate_path(segments[1:])
                return child.get_page(child_path)
            elif isinstance(child, PageBuilder) and segments[0] == child.label:
                # 找到页面
                return child
        
        return None


class AppPageGroupBuilder(BaseBuilder):
    """
    表示一个页面分组，用于在侧边栏中对多个页面进行逻辑归类。
    对应 AMIS pages 中 type='group' 的配置项。
    """
    type: Literal["app-group"] = "app-group"
    label: Optional[str] = Field(None, description="分组在导航菜单中显示的标题")
    children: List[Union[AppPageBuilder, "AppPageGroupBuilder"]] = Field(
        default_factory=list,
        description="分组内包含的页面或嵌套分组"
    )
    
    def register_page(
        self,
        path: str,
        page: PageBuilder,
        label: Optional[str] = None
    ) -> "AppPageBuilder":
        """
        在当前分组下注册页面
        
        Args:
            path: 页面路径，如 "/list" 或 "/detail/{id}"
            page: 页面实例
            label: 页面在导航菜单中显示的名称
            
        Returns:
            注册的 AppPageBuilder 实例
        """
        segments = parse_path(path)
        
        if not segments:
            # 路径为空，直接创建 AppPageBuilder
            new_page = AppPageBuilder(label=label, children=[page])
            self.children.append(new_page)
            return new_page
        
        # 处理嵌套路径
        child_path = generate_path(segments[1:]) if len(segments) > 1 else ""
        
        # 检查是否已存在同名子页面或分组
        for child in self.children:
            if isinstance(child, AppPageBuilder) and child.label == segments[0]:
                # 已存在 AppPageBuilder，递归注册
                child.register_page(child_path, page, label)
                return child
            elif isinstance(child, AppPageGroupBuilder) and child.label == segments[0]:
                # 已存在分组，递归注册
                return child.register_page(child_path, page, label)
        
        # 不存在，创建新的 AppPageBuilder
        new_page = AppPageBuilder(label=segments[0], children=[])
        new_page.register_page(child_path, page, label)
        self.children.append(new_page)
        
        return new_page
    
    def register_subgroup(
        self,
        path: str,
        label: Optional[str] = None
    ) -> "AppPageGroupBuilder":
        """
        在当前分组下注册子分组
        
        Args:
            path: 分组路径，如 "/users" 或 "/admin/system"
            label: 分组在导航菜单中显示的标题
            
        Returns:
            注册的 AppPageGroupBuilder 实例
        """
        segments = parse_path(path)
        
        if not segments:
            # 路径为空，直接创建分组
            new_group = AppPageGroupBuilder(label=label, children=[])
            self.children.append(new_group)
            return new_group
        
        # 处理嵌套路径
        child_path = generate_path(segments[1:]) if len(segments) > 1 else ""
        
        # 检查是否已存在同名子分组
        for child in self.children:
            if isinstance(child, AppPageGroupBuilder) and child.label == segments[0]:
                # 已存在，递归注册
                return child.register_subgroup(child_path, label)
            elif isinstance(child, AppPageBuilder) and child.label == segments[0]:
                # 已存在页面，无法在页面下创建分组
                raise ValueError(f"Cannot create subgroup under page: {segments[0]}")
        
        # 不存在，创建新的分组
        new_group = AppPageGroupBuilder(label=segments[0], children=[])
        result = new_group.register_subgroup(child_path, label)
        self.children.append(new_group)
        
        return result
    
    def get_page(self, path: str) -> Optional[PageBuilder]:
        """
        根据路径获取已注册的页面
        
        Args:
            path: 页面路径，如 "/list" 或 "/detail/{id}"
            
        Returns:
            找到的 PageBuilder 实例，未找到则返回 None
        """
        segments = parse_path(path)
        
        if not segments:
            return None
        
        # 遍历子节点
        for child in self.children:
            if isinstance(child, AppPageBuilder) and child.label == segments[0]:
                if len(segments) == 1:
                    # 找到页面，返回其第一个子页面（假设每个 AppPageBuilder 只有一个 PageBuilder 子节点）
                    for grandchild in child.children:
                        if isinstance(grandchild, PageBuilder):
                            return grandchild
                    return None
                else:
                    # 递归查找
                    child_path = generate_path(segments[1:])
                    return child.get_page(child_path)
            elif isinstance(child, AppPageGroupBuilder) and child.label == segments[0]:
                # 递归查找分组
                child_path = generate_path(segments[1:])
                return child.get_page(child_path)
        
        return None


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
    
    def register_page(
        self,
        path: str,
        page: PageBuilder,
        label: Optional[str] = None
    ) -> AppPageBuilder:
        """
        直接在根目录注册页面
        
        Args:
            path: 页面路径，如 "/home" 或 "/users/list"
            page: 页面实例
            label: 页面在导航菜单中显示的名称
            
        Returns:
            注册的 AppPageBuilder 实例
        """
        segments = parse_path(path)
        
        if not segments:
            # 路径为空，直接创建 AppPageBuilder
            new_page = AppPageBuilder(label=label, children=[page])
            self.pages.append(new_page)
            return new_page
        
        # 处理嵌套路径
        child_path = generate_path(segments[1:]) if len(segments) > 1 else ""
        
        # 检查是否已存在同名页面或分组
        for child in self.pages:
            if isinstance(child, AppPageBuilder) and child.label == segments[0]:
                # 已存在 AppPageBuilder，递归注册
                child.register_page(child_path, page, label)
                return child
            elif isinstance(child, AppPageGroupBuilder) and child.label == segments[0]:
                # 已存在分组，递归注册
                return child.register_page(child_path, page, label)
        
        # 不存在，创建新的 AppPageBuilder
        new_page = AppPageBuilder(label=segments[0], children=[])
        new_page.register_page(child_path, page, label)
        self.pages.append(new_page)
        
        return new_page
    
    def register_page_group(
        self,
        path: str,
        label: Optional[str] = None
    ) -> AppPageGroupBuilder:
        """
        注册页面分组
        
        Args:
            path: 分组路径，如 "/users" 或 "/admin/system"
            label: 分组在导航菜单中显示的标题
            
        Returns:
            注册的 AppPageGroupBuilder 实例
        """
        segments = parse_path(path)
        
        if not segments:
            # 路径为空，直接创建分组
            new_group = AppPageGroupBuilder(label=label, children=[])
            self.pages.append(new_group)
            return new_group
        
        # 处理嵌套路径
        child_path = generate_path(segments[1:]) if len(segments) > 1 else ""
        
        # 检查是否已存在同名分组或页面
        for child in self.pages:
            if isinstance(child, AppPageGroupBuilder) and child.label == segments[0]:
                # 已存在分组，递归注册
                return child.register_subgroup(child_path, label)
            elif isinstance(child, AppPageBuilder) and child.label == segments[0]:
                # 已存在页面，无法在页面下创建分组
                raise ValueError(f"Cannot create group under page: {segments[0]}")
        
        # 不存在，创建新的分组
        new_group = AppPageGroupBuilder(label=segments[0], children=[])
        result = new_group.register_subgroup(child_path, label)
        self.pages.append(new_group)
        
        return result
    
    def get_page(self, path: str) -> Optional[PageBuilder]:
        """
        根据路径获取已注册的页面
        
        Args:
            path: 页面路径，如 "/home" 或 "/users/list"
            
        Returns:
            找到的 PageBuilder 实例，未找到则返回 None
        """
        segments = parse_path(path)
        
        if not segments:
            return None
        
        # 遍历顶层页面和分组
        for child in self.pages:
            if isinstance(child, AppPageBuilder) and child.label == segments[0]:
                if len(segments) == 1:
                    # 找到页面，返回其第一个子页面（假设每个 AppPageBuilder 只有一个 PageBuilder 子节点）
                    for grandchild in child.children:
                        if isinstance(grandchild, PageBuilder):
                            return grandchild
                    return None
                else:
                    # 递归查找
                    child_path = generate_path(segments[1:])
                    return child.get_page(child_path)
            elif isinstance(child, AppPageGroupBuilder) and child.label == segments[0]:
                # 递归查找分组
                child_path = generate_path(segments[1:])
                return child.get_page(child_path)
        
        return None
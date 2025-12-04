# from __future__ import annotations
from typing import Any, Dict, List, Union, Optional, Literal
from pydantic import BaseModel, Field

from ..base import BaseBuilder
from ..page import PageBuilder
from .page import AppPageBuilder


class AppPageGroupBuilder(BaseBuilder):
    """
    表示一个页面分组，用于在侧边栏中对多个页面进行逻辑归类。
    对应 AMIS pages 中 type='group' 的配置项。
    """
    type: Literal["group"] = "group"
    label: Optional[str] = Field(None, description="分组在导航菜单中显示的标题")
    children: List[Union[AppPageBuilder, "AppPageGroupBuilder"]] = Field(
        default_factory=list,
        description="分组内包含的页面或嵌套分组"
    )
    icon: Optional[str] = Field(None, description="菜单图标，比如：fa fa-file")
    class_name: Optional[str] = Field(None, description="菜单类名")

    def register_page(
            self,
            label: str,
            path: str,
    ) -> "AppPageBuilder":
        """
        在当前分组下注册页面
        """

        paths = [p for p in path.split('/') if p]
        if len(paths) == 1:
            page = AppPageBuilder(label=label, path=path)
            self.children.append(page)
            return page

        for child in self.children:
            if path.startswith(child.path):
                return child.register_page(label,path)

        child = AppPageBuilder(path='/' + paths[0], children=[])
        self.children.append(child)
        return child.register_page(label,path)

    def get_page(self, path: str) -> Optional[PageBuilder]:
        """
        根据路径获取已注册的页面
        
        Args:
            path: 页面路径，如 "/list"
            
        Returns:
            找到的 PageBuilder 实例，未找到则返回 None
        """
        # 遍历子节点
        for child in self.children:
            if isinstance(child, AppPageBuilder):
                if child.url == path:
                    return child.schema
            elif isinstance(child, AppPageGroupBuilder):
                # 递归查找子分组
                page = child.get_page(path)
                if page:
                    return page

        return None

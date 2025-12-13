# from __future__ import annotations
from typing import Any, Dict, List, Union, Optional, Literal

from ..base import BaseModel, Field
from ..layout.page import PageBuilder
from .page import AppPageBuilder


class AppPageGroupBuilder(BaseModel):
    """
    表示一个页面分组，用于在侧边栏中对多个页面进行逻辑归类。
    对应 AMIS pages 中 type='group' 的配置项。
    """
    type: Literal["group"] = Field("group", description="组件类型")
    label: Optional[str] = Field(None, description="分组在导航菜单中显示的标题")
    children: Optional[List[Union[AppPageBuilder]]] = Field(None, description="分组内包含的页面或嵌套分组")
    icon: Optional[str] = Field(None, description="菜单图标，比如：fa fa-file")
    class_name: Optional[str] = Field(None, description="菜单类名")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化列表
        if self.children is None:
            self.children = []
        
        # 处理 children 参数
        if "children" in kwargs:
            self.children.extend(kwargs.pop("children"))

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
            page = AppPageBuilder(label=label, path=path, url=path)
            self.children.append(page)
            return page

        for child in self.children:
            if path.startswith(child.path):
                return child.register_page(label,path)

        raise ValueError(f"未找到页面：{path}")

    def get_page(self, path: str) -> Optional[PageBuilder]:
        """
        根据路径获取已注册的页面
        """
        # 遍历子节点
        for child in self.children:
            if path.startswith(child.path):
                return child.get_page(path)
        raise ValueError(f"未找到页面：{path}")

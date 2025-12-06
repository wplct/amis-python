# from __future__ import annotations
from typing import Any, Dict, List, Union, Optional, Literal

from ..base import BaseBuilder
from ..page import PageBuilder
from ..api import AmisApiObject


class AppPageBuilder(BaseBuilder):
    """
    表示一个应用中的独立页面（可出现在导航菜单中）。
    对应 AMIS pages 配置中的单个页面项（非分组）。
    """
    type: Literal["appPage"] = "appPage"
    label: Optional[str] = None  # 页面在导航菜单中显示的名称
    url: Optional[str] = None  # 页面路由路径
    schema: Optional[PageBuilder] = None  # 页面配置
    icon: Optional[str] = None  # 菜单图标，比如：fa fa-file
    schema_api: Optional[Union[str, dict]] = None  # 如果想通过接口拉取，请配置。返回路径为 json>data
    link: Optional[str] = None  # 如果想配置个外部链接菜单，只需要配置 link 即可
    redirect: Optional[str] = None  # 跳转，当命中当前页面时，跳转到目标页面
    rewrite: Optional[str] = None  # 改成渲染其他路径的页面，这个方式页面地址不会发生修改
    is_default_page: Optional[bool] = None  # 当你需要自定义 404 页面的时候有用
    visible: Optional[bool] = None  # 有些页面可能不想出现在菜单中，可以配置成 false
    class_name: Optional[str] = None  # 菜单类名
    children: Optional[List["AppPageBuilder"]] = None  # 分组内包含的页面或嵌套分组
    # ---- 辅助字段 ----
    path: Optional[str] = None  # 页面路径,对于Amis没用
    _lazy_schema: Optional[PageBuilder] = None  # 懒加载页面

    def get_page(self, path: str) -> Optional[PageBuilder]:
        """
        根据路径获取已注册的页面
        """
        if self.path == path:
            return self._lazy_schema
        elif self.children:
            for child in self.children:
                if path.startswith(child.path):
                    return child.get_page(path)
        raise ValueError(f"页面不存在 {path}")

    def register_page(
            self,
            label: str,
            path: str,
    ) -> "AppPageBuilder":
        if self.children is None:
            self.children = []
        if not path.startswith(self.path):
            raise ValueError(f"Path '{path}' is not under '{self.path}'.")

        paths = [p for p in path.split('/') if p]
        self_paths = [p for p in self.path.split('/') if p]
        if len(paths) == len(self_paths):
            raise ValueError(f"path 注册错误 {path} {self.path}")
        if len(paths) - len(self_paths) == 1:
            app_page = AppPageBuilder(label=label, path=path, url=path)
            self.children.append(app_page)
            return app_page
        elif len(paths) - len(self_paths) > 1:
            for child in self.children:
                if path.startswith(child.path):
                    return child.register_page(label, path)
            raise ValueError(f"上级页面不存在 {path}")
        else:
            raise ValueError(f"path 注册错误 {path} {self.path}")

    def set_page_schema(self, schema: PageBuilder):
        self._lazy_schema = schema


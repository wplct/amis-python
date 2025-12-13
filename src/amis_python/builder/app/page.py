# from __future__ import annotations
from typing import Any, Dict, List, Union, Optional, Literal

from ..base import BaseModel, Field
from ..layout.page import Page
from ..api import Api


class AppPageBuilder(BaseModel):
    """
    表示一个应用中的独立页面（可出现在导航菜单中）。
    对应 AMIS pages 配置中的单个页面项（非分组）。
    """
    type: Literal["appPage"] = Field("appPage", description="组件类型")
    label: Optional[str] = Field(None, description="页面在导航菜单中显示的名称")
    url: Optional[str] = Field(None, description="页面路由路径")
    page_schema: Optional[Page] = Field(None, alias="schema", description="页面配置")
    icon: Optional[str] = Field(None, description="菜单图标，比如：fa fa-file")
    schema_api: Optional[Union[str, dict]] = Field(None, description="如果想通过接口拉取，请配置。返回路径为 json>data")
    link: Optional[str] = Field(None, description="如果想配置个外部链接菜单，只需要配置 link 即可")
    redirect: Optional[str] = Field(None, description="跳转，当命中当前页面时，跳转到目标页面")
    rewrite: Optional[str] = Field(None, description="改成渲染其他路径的页面，这个方式页面地址不会发生修改")
    is_default_page: Optional[bool] = Field(None, description="当你需要自定义 404 页面的时候有用")
    visible: Optional[bool] = Field(None, description="有些页面可能不想出现在菜单中，可以配置成 false")
    class_name: Optional[str] = Field(None, description="菜单类名")
    children: Optional[List["AppPageBuilder"]] = Field(None, description="分组内包含的页面或嵌套分组")
    # ---- 辅助字段 ----
    path: Optional[str] = Field(None, description="页面路径")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 使用普通实例变量，而不是 Pydantic 字段，因为 Pydantic 不允许字段名以下划线开头
        self._lazy_schema = None

    def get_page(self, path: str) -> Optional[Page]:
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

    def set_page_schema(self, schema: Page):
        self._lazy_schema = schema


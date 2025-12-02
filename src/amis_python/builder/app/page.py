# from __future__ import annotations
from typing import Any, Dict, List, Union, Optional, Literal
from pydantic import BaseModel, Field

from ..base import BaseBuilder
from ..page import PageBuilder


class AppPageBuilder(BaseBuilder):
    """
    表示一个应用中的独立页面（可出现在导航菜单中）。
    对应 AMIS pages 配置中的单个页面项（非分组）。
    """
    type: Literal["page"] = "page"
    label: Optional[str] = Field(None, description="页面在导航菜单中显示的名称")
    url: str = Field(..., description="页面路由路径")
    schema: Optional[PageBuilder] = Field(None, description="页面配置")
    icon: Optional[str] = Field(None, description="菜单图标，比如：fa fa-file")
    schema_api: Optional[Union[str, dict]] = Field(None, description="如果想通过接口拉取，请配置。返回路径为 json>data")
    link: Optional[str] = Field(None, description="如果想配置个外部链接菜单，只需要配置 link 即可")
    redirect: Optional[str] = Field(None, description="跳转，当命中当前页面时，跳转到目标页面")
    rewrite: Optional[str] = Field(None, description="改成渲染其他路径的页面，这个方式页面地址不会发生修改")
    is_default_page: Optional[bool] = Field(None, description="当你需要自定义 404 页面的时候有用")
    visible: Optional[bool] = Field(None, description="有些页面可能不想出现在菜单中，可以配置成 false")
    class_name: Optional[str] = Field(None, description="菜单类名")
    
    def get_page(self, path: str) -> Optional[PageBuilder]:
        """
        根据路径获取已注册的页面
        
        Args:
            path: 页面路径，如 "/list" 或 "/detail/{id}"
            
        Returns:
            找到的 PageBuilder 实例，未找到则返回 None
        """
        if self.url == path:
            return self.schema
        return None
    
    def to_schema(
            self,
            *, 
            by_alias: bool = True,
            exclude_none: bool = True,
            **dump_kwargs: Any,
    ) -> Dict[str, Any]:
        # 获取基本字段
        result = super().to_schema(by_alias=by_alias, exclude_none=exclude_none, **dump_kwargs)
        
        # 移除 schema 字段，因为它不应该出现在最终的 JSON 中
        if "schema" in result:
            del result["schema"]
        
        return result

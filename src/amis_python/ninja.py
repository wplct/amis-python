from typing import Any, Dict, List, Optional
from django.urls import path
from ninja import NinjaAPI
from amis_python.builder.app import AppBuilder
from amis_python.builder.page import PageBuilder


class AmisNinja:
    """
    amis-python 与 django-ninja 的集成入口类
    
    提供 register_amis_app 方法，用于在 django-ninja 中注册 amis 应用，
    自动生成路由和视图函数。
    """
    
    def __init__(self, api: NinjaAPI):
        """
        初始化 AmisNinja 实例
        
        Args:
            api: django-ninja API 实例
        """
        self.api = api
        self.amis_apps: Dict[str, AppBuilder] = {}
    
    def register_amis_app(
        self,
        amis_app: AppBuilder,
        prefix: str = "/amis",
        name: Optional[str] = None
    ) -> None:
        """
        在 django-ninja 中注册 amis 应用
        
        Args:
            amis_app: amis 应用实例
            prefix: 路由前缀，默认为 "/amis"
            name: 应用名称，默认为 None
        """
        # 保存应用实例
        app_name = name or f"amis_app_{len(self.amis_apps) + 1}"
        self.amis_apps[app_name] = amis_app
        
        # 生成应用级路由
        self._generate_app_routes(amis_app, prefix)
        
        # 生成页面级路由
        self._generate_page_routes(amis_app, prefix)
    
    def _generate_app_routes(self, amis_app: AppBuilder, prefix: str) -> None:
        """
        生成应用级路由
        
        Args:
            amis_app: amis 应用实例
            prefix: 路由前缀
        """
        # 应用配置路由
        @self.api.get(f"{prefix}/config")
        def get_amis_app_config(request) -> Dict[str, Any]:
            return amis_app.to_schema()
    
    def _generate_page_routes(self, amis_app: AppBuilder, prefix: str) -> None:
        """
        生成页面级路由
        
        Args:
            amis_app: amis 应用实例
            prefix: 路由前缀
        """
        # 遍历所有页面，生成路由
        self._traverse_pages(amis_app.pages, prefix)
    
    def _traverse_pages(self, pages: List[Any], prefix: str) -> None:
        """
        遍历页面列表，生成路由
        
        Args:
            pages: 页面列表
            prefix: 路由前缀
        """
        from amis_python.builder.app import AppPageBuilder, AppPageGroupBuilder
        
        for page in pages:
            if isinstance(page, AppPageBuilder):
                # 生成页面路由
                self._generate_single_page_routes(page, prefix)
                # 递归处理子页面
                self._traverse_pages(page.children, f"{prefix}/{page.label}")
            elif isinstance(page, AppPageGroupBuilder):
                # 递归处理分组内的页面
                self._traverse_pages(page.children, f"{prefix}/{page.label}")
    
    def _generate_single_page_routes(self, page_builder: Any, prefix: str) -> None:
        """
        生成单个页面的路由
        
        Args:
            page_builder: 页面构建器实例
            prefix: 路由前缀
        """
        from amis_python.builder.page import PageBuilder
        
        # 遍历页面的 children，找到 PageBuilder 实例
        for child in page_builder.children:
            if isinstance(child, PageBuilder):
                # 生成页面配置路由
                @self.api.get(f"{prefix}/{page_builder.label}")
                def get_page_config(request) -> Dict[str, Any]:
                    return child.to_schema()
                break
    
    def get_amis_app(self, name: str) -> Optional[AppBuilder]:
        """
        根据名称获取已注册的 amis 应用
        
        Args:
            name: 应用名称
            
        Returns:
            找到的 amis 应用实例，未找到则返回 None
        """
        return self.amis_apps.get(name)
    
    def list_amis_apps(self) -> List[str]:
        """
        列出所有已注册的 amis 应用名称
        
        Returns:
            已注册的 amis 应用名称列表
        """
        return list(self.amis_apps.keys())
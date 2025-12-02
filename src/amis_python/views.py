from typing import Any, Optional
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import os
from .builder.app import AppBuilder

# 默认 amis 应用实例初始化为 None，允许用户手动注册
_default_amis_app: Optional[AppBuilder] = None

def register_default_app(app: AppBuilder) -> None:
    """
    注册默认的 amis 应用实例
    
    Args:
        app: 要注册的 amis 应用实例
        
    Raises:
        ValueError: 如果默认应用已经注册
    """
    global _default_amis_app
    if _default_amis_app is not None:
        raise ValueError("Default amis app already registered.")
    _default_amis_app = app

def get_amis_app(name: str = "default") -> AppBuilder:
    """
    获取默认的 amis 应用实例
    
    Args:
        name: 应用名称（兼容旧代码，实际只返回默认应用）
        
    Returns:
        默认的 amis 应用实例
        
    Raises:
        ValueError: 如果默认应用未注册
    """
    if _default_amis_app is None:
        raise ValueError("Default amis app not registered. Please call register_default_app() first.")
    return _default_amis_app

def get_amis_app_config(request) -> JsonResponse:
    """
    获取 amis 应用配置
    
    Args:
        request: Django 请求对象
        
    Returns:
        JsonResponse，包含 amis 应用配置
    """
    if _default_amis_app is None:
        return JsonResponse({"error": "Default amis app not registered"}, status=500)
    return JsonResponse(_default_amis_app.to_schema())

def get_page_config(request, page_path: str) -> JsonResponse:
    """
    获取页面配置
    
    Args:
        request: Django 请求对象
        page_path: 页面路径
        
    Returns:
        JsonResponse，包含页面配置
    """
    if _default_amis_app is None:
        return JsonResponse({"error": "Default amis app not registered"}, status=500)
    
    # 构建完整路径
    full_path = f"/{page_path}"
    page = _default_amis_app.get_page(full_path)
    
    if not page:
        return JsonResponse({"error": f"Page '{full_path}' not found"}, status=404)
    
    return JsonResponse(page.to_schema())

def amis_index(request) -> HttpResponse:
    """
    提供 AMIS 应用的首页
    
    Args:
        request: Django 请求对象
        
    Returns:
        HttpResponse，包含 AMIS 应用的首页 HTML
    """
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 index.html 文件的路径
    index_path = os.path.join(current_dir, 'static', 'amis_python', 'index.html')
    
    # 如果文件存在，直接返回文件内容
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    
    # 否则返回 404
    return HttpResponse(f"Index.html not found at {index_path}", status=404)

# 提供全局访问点
def get_default_app() -> Optional[AppBuilder]:
    """
    获取默认的 amis 应用实例
    
    Returns:
        默认的 amis 应用实例，未注册则返回 None
    """
    return _default_amis_app

from typing import Dict, Any, Optional
from django.http import JsonResponse
from .builder.app import AppBuilder

# 全局 amis 应用实例，用于存储和管理所有注册的 amis 应用
_global_amis_apps: Dict[str, AppBuilder] = {}
_default_amis_app: Optional[AppBuilder] = None

def register_amis_app(amis_app: AppBuilder, name: str = "default") -> None:
    """
    注册 amis 应用实例
    
    Args:
        amis_app: amis 应用实例
        name: 应用名称，默认为 "default"
    """
    global _default_amis_app
    _global_amis_apps[name] = amis_app
    if name == "default" or _default_amis_app is None:
        _default_amis_app = amis_app

def get_amis_app(name: str = "default") -> Optional[AppBuilder]:
    """
    获取已注册的 amis 应用实例
    
    Args:
        name: 应用名称，默认为 "default"
        
    Returns:
        找到的 amis 应用实例，未找到则返回 None
    """
    return _global_amis_apps.get(name)

def get_amis_app_config(request) -> JsonResponse:
    """
    获取 amis 应用配置
    
    Args:
        request: Django 请求对象
        
    Returns:
        JsonResponse，包含 amis 应用配置
    """
    app_name = request.GET.get("app", "default")
    amis_app = get_amis_app(app_name)
    
    if not amis_app:
        return JsonResponse({"error": f"Amis app '{app_name}' not found"}, status=404)
    
    return JsonResponse(amis_app.to_schema())

def get_page_config(request, page_path: str) -> JsonResponse:
    """
    获取页面配置
    
    Args:
        request: Django 请求对象
        page_path: 页面路径
        
    Returns:
        JsonResponse，包含页面配置
    """
    app_name = request.GET.get("app", "default")
    amis_app = get_amis_app(app_name)
    
    if not amis_app:
        return JsonResponse({"error": f"Amis app '{app_name}' not found"}, status=404)
    
    # 构建完整路径
    full_path = f"/{page_path}"
    page = amis_app.get_page(full_path)
    
    if not page:
        return JsonResponse({"error": f"Page '{full_path}' not found"}, status=404)
    
    return JsonResponse(page.to_schema())
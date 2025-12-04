from django.http import JsonResponse, HttpResponse
import os
from .registry import get_default_app, get_page


def get_amis_app_config(request) -> JsonResponse:
    """
    获取 amis 应用配置
    
    Args:
        request: Django 请求对象
        
    Returns:
        JsonResponse，包含 amis 应用配置
    """
    if get_default_app() is None:
        return JsonResponse({"error": "Default amis app not registered"}, status=500)
    return JsonResponse(get_default_app().to_schema())

def get_page_config(request, page_path: str) -> JsonResponse:
    """
    获取页面配置
    """
    page_path = '/' + page_path
    page = get_page(page_path)
    return JsonResponse(page.to_schema())

def amis_index(request) -> HttpResponse:
    """
    提供 AMIS 应用的首页
    """
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 index.html 文件的路径
    index_path = os.path.join(current_dir, 'static', 'amis', 'index.html')
    
    # 如果文件存在，直接返回文件内容
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    
    # 否则返回 404
    return HttpResponse(f"Index.html not found at {index_path}", status=404)

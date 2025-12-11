from django.http import JsonResponse, HttpResponse
import os
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_exempt
import json
from .registry import get_default_app, get_page
from .login_config import get_login_page


def get_amis_app_config(request) -> JsonResponse:
    """
    获取 amis 应用配置
    
    Args:
        request: Django 请求对象
        
    Returns:
        JsonResponse，包含 amis 应用配置
    """
    # 检查用户是否已登录
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)
    
    if get_default_app() is None:
        return JsonResponse({"error": "Default amis app not registered"}, status=500)
    return JsonResponse(get_default_app().to_schema())


def get_page_config(request, page_path: str) -> JsonResponse:
    """
    获取页面配置
    """
    # 检查用户是否已登录
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)
    
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


def get_login_config(request) -> JsonResponse:
    """
    获取登录页面配置
    """
    login_page = get_login_page()
    return JsonResponse(login_page.to_schema())


@csrf_exempt
def login(request) -> JsonResponse:
    """
    用户登录API
    """
    if request.method == 'POST':
        try:
            # 解析请求体
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # 验证用户名和密码
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # 登录成功，设置session
                django_login(request, user)
                return JsonResponse({"username": user.username})
            else:
                # 登录失败
                return JsonResponse({"status": 1, "msg": "用户名或密码错误"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": 1, "msg": "无效的请求体"}, status=400)
        except Exception as e:
            return JsonResponse({"status": 1, "msg": str(e)}, status=400)
    return JsonResponse({"status": 1, "msg": "仅支持POST请求"}, status=405)


@csrf_exempt
def logout(request) -> JsonResponse:
    """
    用户登出API
    """
    if request.method == 'POST':
        django_logout(request)
        return JsonResponse({"status": 0, "msg": "登出成功"})
    return JsonResponse({"status": 1, "msg": "仅支持POST请求"}, status=405)


@csrf_exempt
def current_user(request) -> JsonResponse:
    """
    获取当前登录用户信息API
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse({"status": 0, "msg": "", "data": {"username": request.user.username}})
        else:
            return JsonResponse({"status": 1, "msg": "未登录"})
    return JsonResponse({"status": 1, "msg": "仅支持GET请求"}, status=405)

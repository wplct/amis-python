import hashlib
import uuid

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
import os
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

from . import Page
from .builder.layout import Container, Panel

from .registry import get_default_app, get_page
from .builder.form.form import Form
from .builder.form.input_text import InputText
from .builder.form.input_password import InputPassword
from .builder.button import Button
from .builder.api import Api


def get_login_page() -> dict:
    """
    创建登录页面配置
    """
    # 创建登录表单
    login_form = Form(
        title="用户登录",
        api=Api(
            url="/amis/api/login",  # 表单提交到登录API
            method="post"
        ),
        mode="normal",  # 垂直布局
        body=[
            InputText(
                name="username",
                label="用户名",
                required=True,
                placeholder="请输入用户名"
            ),
            InputPassword(
                name="password",
                label="密码",
                required=True,
                placeholder="请输入密码"
            )
        ],
        actions=[
            Button(
                label="登录",
                action_type="submit",
                primary=True
            ),
            Button(
                label="重置",
                action_type="reset"
            )
        ],
        on_event={
            "submitSucc": {
                "actions": [
                    {
                        "actionType": "refresh"
                    }
                ]
            }
        }
    )

    # 将对象转换为字典
    login_form = login_form.model_dump()

    # 创建登录页面
    login_page = Page(
        title="登录",
        body=[
            Container(
                class_name="login-container",
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "height": "100%",
                    "backgroundColor": "#f5f5f5"
                },
                body=[
                    Panel(
                        class_name="login-panel",
                        style={
                            "width": "400px",
                            "padding": "20px",
                            "backgroundColor": "#fff",
                            "borderRadius": "8px",
                            "boxShadow": "0 2px 12px 0 rgba(0, 0, 0, 0.1)"
                        },
                        body=login_form
                    )
                ]
            )
        ]
    )

    # 将对象转换为字典
    return login_page.model_dump()


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
    return JsonResponse(get_default_app().model_dump())


def get_page_config(request, page_path: str=None) -> JsonResponse:
    """
    获取页面配置
    """
    # 检查用户是否已登录
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)
    if page_path is None:
        page = get_page('/')
        return JsonResponse(page)
    page_path = '/' + page_path
    page = get_page(page_path)
    if callable(page):
        page = page(request)
    if isinstance(page, Page):
        return JsonResponse(page.model_dump())
    return JsonResponse(page)


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
    return JsonResponse(login_page)


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


@method_decorator(login_required, name='dispatch')
class UploadView(View):
    http_method_names = ['post']

    def post(self, request):
        from amis_python.models import File

        uploaded = request.FILES.get('file')
        if not uploaded:
            return JsonResponse({'error': 'missing file'}, status=400)

        # 先建实例
        obj = File(
            key=str(uuid.uuid4()),
            name=uploaded.name,
            size=uploaded.size,
            type=uploaded.content_type or 'application/octet-stream',
            uploader=request.user
        )
        # 把文件挂上去；upload_to 会拿到 obj.uuid 去拼文件名
        obj.file = uploaded
        obj.save()

        return JsonResponse({
            'status': 0,
            'msg': '上传成功',
            'data': {
                'value': obj.id,
                'url': obj.file.url,
                'name': obj.file.name,
            }
        })

@method_decorator(login_required, name='dispatch')
class UploadImageView(View):
    http_method_names = ['post']

    def post(self, request):
        from amis_python.models import File

        uploaded = request.FILES.get('file')
        if not uploaded:
            return JsonResponse({'error': 'missing file'}, status=400)

        # 先建实例
        obj = File(
            key=str(uuid.uuid4()),
            name=uploaded.name,
            size=uploaded.size,
            type=uploaded.content_type or 'application/octet-stream',
            uploader=request.user
        )
        # 把文件挂上去；upload_to 会拿到 obj.uuid 去拼文件名
        obj.file = uploaded
        obj.save()

        return JsonResponse({
            'status': 0,
            'msg': '上传成功',
            'data': {
                'value': obj.file.url,
                'id': obj.id,
            }
        })
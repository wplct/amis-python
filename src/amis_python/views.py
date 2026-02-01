import uuid

from django.http import HttpResponse
import os
from django.contrib.auth import  login as django_login, logout as django_logout
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from . import Page
from .builder.layout import Container, Panel

from .registry import get_default_app, get_page, get_app
from .builder.form.form import Form
from .builder.form.input_text import InputText
from .builder.form.input_password import InputPassword
from .builder.button import Button
from .builder.api import Api
from .drf import AmisResponse
from .serializers import FileSerializer, LoginSerializer

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


class GetAmisAppConfig(APIView):
    """
    获取 amis 应用配置
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if get_default_app() is None:
            return AmisResponse(code=500, msg="Default amis app not registered", data={})
        # 尝试从session中获取应用配置
        if request.session.get("app_config"):
            app = get_app(request.session.get("app_config"))
            if app is None:
                django_logout(request)
                # 跳转到首页
                return HttpResponse(status=302, headers={"Location": "/"})
            return AmisResponse(data=app.model_dump())
        return AmisResponse(data=get_default_app().model_dump())


class GetPageConfig(APIView):
    """
    获取页面配置
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, page_path: str=None):
        if page_path is None:
            page = get_page(request,'/')
            return AmisResponse(data=page)
        page_path = '/' + page_path
        page = get_page(request,page_path)
        if callable(page):
            page = page(request)
        if isinstance(page, Page):
            return AmisResponse(data=page.model_dump())
        return AmisResponse(data=page)

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


class GetLoginConfig(APIView):
    """
    获取登录页面配置
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        login_page = get_login_page()
        return AmisResponse(data=login_page)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    """
    用户登录API
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            django_login(request, user)
            return AmisResponse(data={"username": user.username})
        return AmisResponse(code=400, msg=serializer.errors, data={})


class LogoutView(APIView):
    """
    用户登出API
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        django_logout(request)
        return AmisResponse(data={"status": 0, "msg": "登出成功"})


class CurrentUserView(APIView):
    """
    获取当前登录用户信息API
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return AmisResponse(data={"status": 0, "msg": "", "data": {"username": request.user.username}})


class UnauthorizedUserView(APIView):
    """
    未登录用户访问时的处理
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        return AmisResponse(code=1, msg="未登录", data={})


class UploadView(APIView):
    """
    文件上传API
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        from amis_python.models import File

        uploaded = request.FILES.get('file')
        if not uploaded:
            return AmisResponse(code=400, msg='missing file', data={})

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

        return AmisResponse(data={
                'value': obj.id,
                'url': obj.file.url,
                'name': obj.file.name,
            },msg='上传成功')


class UploadImageView(APIView):
    """
    图片上传API
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        from amis_python.models import File

        uploaded = request.FILES.get('file')
        if not uploaded:
            return AmisResponse(code=400, msg='missing file', data={})

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

        return AmisResponse(data={
                'value': obj.file.url,
                'id': obj.id,
            },msg='上传成功')
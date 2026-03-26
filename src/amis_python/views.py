import os
import uuid

from django.contrib.auth import login as django_login, logout as django_logout
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from . import Page
from .builder.api import Api
from .builder.button import Button
from .builder.form.form import Form
from .builder.form.input_password import InputPassword
from .builder.form.input_text import InputText
from .builder.layout import Container, Panel
from .drf import AmisResponse
from .registry import get_app, get_default_app, get_page
from .serializers import LoginSerializer


def _store_uploaded_file(uploaded):
    ext = os.path.splitext(uploaded.name)[1] or ".bin"
    storage_path = default_storage.save(f"files/{uuid.uuid4().hex}{ext}", uploaded)
    return {
        "name": uploaded.name,
        "path": storage_path,
        "url": default_storage.url(storage_path),
    }


def get_login_page() -> dict:
    """
    创建登录页面配置
    """
    login_form = Form(
        title="用户登录",
        api=Api(url="/amis/api/login", method="post"),
        mode="normal",
        body=[
            InputText(name="username", label="用户名", required=True, placeholder="请输入用户名"),
            InputPassword(name="password", label="密码", required=True, placeholder="请输入密码"),
        ],
        actions=[
            Button(label="登录", action_type="submit", primary=True),
            Button(label="重置", action_type="reset"),
        ],
        on_event={"submitSucc": {"actions": [{"actionType": "refresh"}]}},
    ).model_dump()

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
                    "backgroundColor": "#f5f5f5",
                },
                body=[
                    Panel(
                        class_name="login-panel",
                        style={
                            "width": "400px",
                            "padding": "20px",
                            "backgroundColor": "#fff",
                            "borderRadius": "8px",
                            "boxShadow": "0 2px 12px 0 rgba(0, 0, 0, 0.1)",
                        },
                        body=login_form,
                    )
                ],
            )
        ],
    )
    return login_page.model_dump()


class GetAmisAppConfig(APIView):
    """
    获取 amis 应用配置
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.session.get("app_config"):
            app = get_app(request.session.get("app_config"))
            if app is None:
                django_logout(request)
                return HttpResponse(status=302, headers={"Location": "/"})
            return AmisResponse(data=app.model_dump())
        return AmisResponse(data=get_default_app().model_dump())


class GetPageConfig(APIView):
    """
    获取页面配置
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, page_path: str = None):
        if page_path is None:
            page = get_page(request, "/")
            return AmisResponse(data=page)
        page_path = "/" + page_path
        page = get_page(request, page_path)
        if callable(page):
            page = page(request)
        if isinstance(page, Page):
            return AmisResponse(data=page.model_dump())
        return AmisResponse(data=page)


def amis_index(request) -> HttpResponse:
    """
    提供 AMIS 应用的首页
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(current_dir, "static", "amis", "index.html")

    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HttpResponse(f.read(), content_type="text/html")
    return HttpResponse(f"Index.html not found at {index_path}", status=404)


class GetLoginConfig(APIView):
    """
    获取登录页面配置
    """

    permission_classes = [AllowAny]

    def get(self, request):
        return AmisResponse(data=get_login_page())


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginView(APIView):
    """
    用户登录 API
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            django_login(request, user)
            return AmisResponse(data={"username": user.username})
        return AmisResponse(code=400, msg=serializer.errors, data={})


class LogoutView(APIView):
    """
    用户登出 API
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)
        return AmisResponse(data={"status": 0, "msg": "登出成功"})


class CurrentUserView(APIView):
    """
    获取当前登录用户信息 API
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
    文件上传 API
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        uploaded = request.FILES.get("file")
        if not uploaded:
            return AmisResponse(code=400, msg="missing file", data={})

        stored = _store_uploaded_file(uploaded)
        return AmisResponse(
            data={
                "value": stored["path"],
                "url": stored["url"],
                "name": stored["name"],
            },
            msg="上传成功",
        )


class UploadImageView(APIView):
    """
    图片上传 API
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        uploaded = request.FILES.get("file")
        if not uploaded:
            return AmisResponse(code=400, msg="missing file", data={})

        stored = _store_uploaded_file(uploaded)
        return AmisResponse(
            data={
                "value": stored["url"],
                "id": stored["path"],
                "name": stored["name"],
                "url": stored["url"],
            },
            msg="上传成功",
        )

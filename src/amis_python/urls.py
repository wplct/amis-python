from django.urls import path, re_path
from django.views.static import serve
from django.views.generic import RedirectView
import os

from .views import amis_index, GetAmisAppConfig, GetPageConfig, GetLoginConfig, LoginView, LogoutView, CurrentUserView, \
    UploadView, UploadImageView

UploadView, UploadImageView

# 获取当前应用的静态目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
amis_static_dir = os.path.join(current_dir, 'static', 'amis')
amis_edit_static_dir = os.path.join(current_dir, 'static', 'amis_edit')

# from django.apps import apps
# from django.utils.module_loading import module_has_submodule
# from importlib import import_module

# def load_all_amis_configs():
#     for app_config in apps.get_app_configs():
#         if not module_has_submodule(app_config.module, "amis"):
#             continue
#
#         amis_module = import_module(f"{app_config.name}.amis")
#         print(f"正在加载 {app_config.name} 的 amis 配置...")
#
#         # 1. 调用register函数（如果存在）
#         if hasattr(amis_module, "register"):
#             amis_module.register()
#
#         # 2. 递归导入所有子模块
#         amis_module_path = getattr(amis_module, "__file__", None)
#         if amis_module_path:
#             amis_module_dir = os.path.dirname(amis_module_path)
#             # 如果是目录（即amis是一个包），则递归导入所有子模块
#             if os.path.isdir(amis_module_dir):
#                 # 遍历amis目录下的所有文件和子目录
#                 for root, dirs, files in os.walk(amis_module_dir):
#                     for file in files:
#                         # 只处理Python文件，跳过__init__.py
#                         if file.endswith('.py') and file != '__init__.py':
#                             # 构建模块路径
#                             relative_path = os.path.relpath(root, amis_module_dir)
#                             if relative_path == '.':
#                                 module_name = file[:-3]
#                             else:
#                                 module_name = f"{relative_path.replace(os.sep, '.')}.{file[:-3]}"
#                             full_module_name = f"{app_config.name}.amis.{module_name}"
#                             try:
#                                 import_module(full_module_name)
#                                 print(f"  已导入 {full_module_name}")
#                             except Exception as e:
#                                 print(f"  导入 {full_module_name} 失败: {e}")
#
# load_all_amis_configs()

urlpatterns = [
    # 应用首页
    path('', amis_index, name='amis_index'),
    # 登录页面配置路由
    path('login/config/', GetLoginConfig.as_view(), name='get_login_config'),
    # 应用配置路由
    path('config/', GetAmisAppConfig.as_view(), name='get_amis_app_config'),
    path('page/', GetPageConfig.as_view(), name='get_page_config'),
    # 页面配置路由（动态路由，匹配任意页面路径）
    path('page/<path:page_path>', GetPageConfig.as_view(), name='get_page_config'),
    # API路由，必须在静态文件路由之前
    path('api/login', LoginView.as_view(), name='login'),
    path('api/logout', LogoutView.as_view(), name='logout'),
    path('api/current_user', CurrentUserView.as_view(), name='current_user'),
    path('upload', UploadView.as_view(), name='upload'),
    path('upload_img', UploadImageView.as_view(), name='upload_img'),
    # edit路径重定向到edit/index.html
    path('edit', RedirectView.as_view(url='edit/index.html', permanent=False)),
    # 静态文件路由，处理 /edit/ 开头的静态文件请求
    re_path(r'^edit/(?P<path>.*)$', serve, {
        'document_root': amis_edit_static_dir,
    }),
    # 静态文件路由，处理其他静态文件请求
    re_path(r'^(?P<path>.*)$', serve, {
        'document_root': amis_static_dir,
    }),

]

from django.urls import path, re_path
from django.views.static import serve
import os
from .ninja_api import amis_api
from .views import get_amis_app_config, get_page_config, amis_index

# 获取当前应用的静态目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
amis_static_dir = os.path.join(current_dir, 'static', 'amis')



from django.apps import apps
from django.utils.module_loading import module_has_submodule
from importlib import import_module

def load_all_amis_configs():
    for app_config in apps.get_app_configs():
        if not module_has_submodule(app_config.module, "amis"):
            continue
        amis_module = import_module(f"{app_config.name}.amis")
        print(f"正在加载 {app_config.name} 的 amis 配置...")
        if hasattr(amis_module, "register"):
            amis_module.register()
load_all_amis_configs()
urlpatterns = [
    # 应用首页
    path('', amis_index, name='amis_index'),
    # 应用配置路由
    path('config/', get_amis_app_config, name='get_amis_app_config'),
    # 页面配置路由（动态路由，匹配任意页面路径）
    path('page/<path:page_path>', get_page_config, name='get_page_config'),
    # 静态文件路由，处理静态文件请求
    re_path(r'^(?P<path>.*)$', serve, {
        'document_root': amis_static_dir,
    }),
    path('api/', amis_api.urls),
]

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
        
        # 1. 调用register函数（如果存在）
        if hasattr(amis_module, "register"):
            amis_module.register()
        
        # 2. 递归导入所有子模块
        amis_module_path = getattr(amis_module, "__file__", None)
        if amis_module_path:
            amis_module_dir = os.path.dirname(amis_module_path)
            # 如果是目录（即amis是一个包），则递归导入所有子模块
            if os.path.isdir(amis_module_dir):
                # 遍历amis目录下的所有文件和子目录
                for root, dirs, files in os.walk(amis_module_dir):
                    for file in files:
                        # 只处理Python文件，跳过__init__.py
                        if file.endswith('.py') and file != '__init__.py':
                            # 构建模块路径
                            relative_path = os.path.relpath(root, amis_module_dir)
                            if relative_path == '.':
                                module_name = file[:-3]
                            else:
                                module_name = f"{relative_path.replace(os.sep, '.')}.{file[:-3]}"
                            full_module_name = f"{app_config.name}.amis.{module_name}"
                            try:
                                import_module(full_module_name)
                                print(f"  已导入 {full_module_name}")
                            except Exception as e:
                                print(f"  导入 {full_module_name} 失败: {e}")
load_all_amis_configs()
urlpatterns = [
    # 应用首页
    path('', amis_index, name='amis_index'),
    # 应用配置路由
    path('config/', get_amis_app_config, name='get_amis_app_config'),
    # 页面配置路由（动态路由，匹配任意页面路径）
    path('page/<path:page_path>', get_page_config, name='get_page_config'),
    # API路由，必须在静态文件路由之前
    path('api/', amis_api.urls),
    # 静态文件路由，处理静态文件请求
    re_path(r'^(?P<path>.*)$', serve, {
        'document_root': amis_static_dir,
    }),
]

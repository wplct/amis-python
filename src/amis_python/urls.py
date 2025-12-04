from django.urls import path, re_path
from django.views.static import serve
import os
from .views import get_amis_app_config, get_page_config, amis_index

# 获取当前应用的静态目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
amis_static_dir = os.path.join(current_dir, 'static', 'amis')

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
]


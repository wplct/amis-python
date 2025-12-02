from django.urls import path
from .views import get_amis_app_config, get_page_config, amis_index

urlpatterns = [
    # 应用首页
    path('', amis_index, name='amis_index'),
    # 应用配置路由
    path('config/', get_amis_app_config, name='get_amis_app_config'),
    # 页面配置路由（动态路由，匹配任意页面路径）
    path('page/<path:page_path>/', get_page_config, name='get_page_config'),
]
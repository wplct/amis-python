# 导出核心功能
from .builder.api import Api, to_api
from .builder.layout import PageBuilder
from .builder.app import AppBuilder, AppPageGroupBuilder, AppPageBuilder
from .registry import get_default_app, get_page, register_default_app, register_group, register_page
from .views import get_amis_app_config, get_page_config, amis_index, get_login_config, login, logout, current_user

# 延迟导入 ninja_api，避免在不需要时加载 Django 设置
try:
    from .ninja_api import amis_api, ApiResponse, success_response, error_response
except Exception:
    # 如果导入失败，可能是因为 Django 没有配置或其他原因，此时不导入
    pass

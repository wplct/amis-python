# 导出核心功能
from .builder import *
from .views import *
from .views import get_default_app
from .registry import *

# 延迟导入 ninja_api，避免在不需要时加载 Django 设置
try:
    from .ninja_api import amis_api, ApiResponse, success_response, error_response
except Exception:
    # 如果导入失败，可能是因为 Django 没有配置或其他原因，此时不导入
    pass

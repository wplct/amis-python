from typing import Optional

from django.apps import AppConfig
from django.conf import settings

from . import AppBuilder, register_default_app
# 默认 amis 应用实例初始化为 None，允许用户手动注册
_default_amis_app: Optional[AppBuilder] = None

class AmisPythonConfig(AppConfig):
    """
    amis-python Django 应用配置
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'amis_python'
    verbose_name = 'Amis Python'
    
    def ready(self):
        """
        应用就绪时执行的初始化代码
        """
        app_config = getattr(settings, 'AMIS_APP_CONFIG', {})
        register_default_app(AppBuilder(
            **app_config
        ))
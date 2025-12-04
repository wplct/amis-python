from typing import Optional

from django.apps import AppConfig
from django.conf import settings

from . import AppBuilder, register_default_app
# 默认 amis 应用实例初始化为 None，允许用户手动注册
_default_amis_app: Optional[AppBuilder] = None
from django.utils.module_loading import module_has_submodule
from importlib import import_module

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

        # 新增：自动扫描其他app中的amis配置
        self._discover_amis_configs()

    def _discover_amis_configs(self):
        """扫描并加载其他Django应用中的amis配置"""
        from django.apps import apps

        for app_config in apps.get_app_configs():
            try:
                # 检查app是否有amis模块
                if module_has_submodule(app_config.module, 'amis'):
                    amis_module = import_module(f'{app_config.name}.amis')
                    # 如果amis模块有register函数，则调用它
                    if hasattr(amis_module, 'register'):
                        amis_module.register()
            except ImportError:
                pass  # 忽略无法导入的模块
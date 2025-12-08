from typing import Optional

from django.apps import AppConfig
from django.conf import settings

from . import AppBuilder, register_default_app
from .builder.action import AjaxActionBuilder
from .builder.button import ButtonBuilder

# 默认 amis 应用实例初始化为 None，允许用户手动注册
_default_amis_app: Optional[AppBuilder] = None
from django.utils.module_loading import module_has_submodule
from importlib import import_module
from django.apps import apps

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
            header=[ButtonBuilder(label="退出登录").add_action(
                'click',
                AjaxActionBuilder(label="注销", api="/amis/api/logout")
            )],
            **app_config
        ))
    #
    #     # 新增：自动扫描其他app中的amis配置
    #     self._discover_amis_configs()
    #
    # def _discover_amis_configs(self):
    #     """扫描并加载其他 Django 应用中的 amis 配置（支持单文件和目录包）"""
    #     for app_config in apps.get_app_configs():
    #         # 1. 先快速判断有没有 amis 这个“子模块”
    #         if not module_has_submodule(app_config.module, "amis"):
    #             continue
    #
    #         # 2. 真正 import 它（文件或目录都会成功）
    #         amis_module = import_module(f"{app_config.name}.amis")
    #         print(f"正在加载 {app_config.name} 的 amis 配置...")
    #
    #         # 3. 如果包里提供了 register 函数，就调用它
    #         if hasattr(amis_module, "register"):
    #             amis_module.register()
    #             print(f"{app_config.name} 的 amis 配置已加载。")

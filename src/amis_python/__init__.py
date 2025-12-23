# 导出核心功能
from .builder.api import Api, to_api
from .builder.layout import Page
from .builder.app import AppBuilder, AppPageGroupBuilder, AppPageBuilder
from .registry import get_default_app, get_page, register_default_app, register_group, register_page



default_app_config = 'amis_python.apps.AmisPythonConfig'
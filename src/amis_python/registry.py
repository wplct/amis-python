import threading
from typing import Optional, Union, Callable, Dict

from django.contrib.auth import logout

from amis_python import AppBuilder
from . import Page
from .builder.app import AppBuilder, AppPageGroupBuilder, AppPageBuilder

# 模块级变量：显式初始化为 None，并带类型注解
_default_amis_app: Optional[AppBuilder] = None

amis_app_map: Dict[str,AppBuilder] = {}
# 用于保护注册过程的线程锁
_register_lock = threading.Lock()


def register_default_app(app: AppBuilder,name: str=None) -> None:
    """
    注册默认的 amis 应用实例（仅允许注册一次）
    """
    global _default_amis_app
    if not isinstance(app, AppBuilder):
        raise TypeError("app must be an instance of AppBuilder")

    with _register_lock:
        if name is not None:
            amis_app_map[name] = app
        else:
            if _default_amis_app is not None:
                raise ValueError("Default amis app has already been registered.")
            _default_amis_app = app


def register_group(group: AppPageGroupBuilder) -> None:
    """
    注册默认 amis 应用实例的分组
    """
    get_default_app().register_group(group)


def register_page(label: str, path: str, page=None,app_name: str=None) -> AppPageBuilder:
    """
    注册默认 amis 应用实例的页面
    """
    if app_name:
        app = get_app(app_name)
        return app.register_page(label, path, page=page)
    return get_default_app().register_page(label, path, page=page)


def get_default_app() -> AppBuilder:
    """
    获取已注册的默认 amis 应用实例
    """
    if _default_amis_app is None:
        raise RuntimeError(
            "Default amis app is not registered. "
            "Call `register_default_app(app)` first."
        )
    return _default_amis_app

def get_app(name: str) -> Optional[AppBuilder]:
    """
    根据名称获取已注册的 amis 应用实例
    """
    if name not in amis_app_map:
        return None
    return amis_app_map[name]

def get_page(request,path: str) -> Union[Page,Callable]:
    """
    根据路径获取已注册的页面
    """
    if request.session.get("app_config"):
        app = get_app(request.session.get("app_config"))
        if app is None:
            print("app_config not found")
            logout(request)
            raise RuntimeError("app_config not found")
        return app.get_page(path)
    return get_default_app().get_page(path)
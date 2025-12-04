import threading
from typing import Optional
from amis_python import AppBuilder, AppPageGroupBuilder, PageBuilder, AppPageBuilder

# 模块级变量：显式初始化为 None，并带类型注解
_default_amis_app: Optional[AppBuilder] = None
# 用于保护注册过程的线程锁
_register_lock = threading.Lock()


def register_default_app(app: AppBuilder) -> None:
    """
    注册默认的 amis 应用实例（仅允许注册一次）
    """
    global _default_amis_app
    if not isinstance(app, AppBuilder):
        raise TypeError("app must be an instance of AppBuilder")

    with _register_lock:
        if _default_amis_app is not None:
            raise ValueError("Default amis app has already been registered.")
        _default_amis_app = app


def register_group(group: AppPageGroupBuilder) -> None:
    """
    注册默认 amis 应用实例的分组
    """
    get_default_app().register_group(group)


def register_page(label: str, path: str, page: PageBuilder=None) -> AppPageBuilder:
    """
    注册默认 amis 应用实例的页面
    """
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


def get_page(path: str) -> PageBuilder:
    """
    根据路径获取已注册的页面
    """
    return get_default_app().get_page(path)
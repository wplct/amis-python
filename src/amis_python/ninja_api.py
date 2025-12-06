from typing import List, Optional, Callable

from ninja import NinjaAPI, Router
from ninja.types import TCallable

# 用于记录所有已注册的 URL name，确保全局唯一性
url_name_set = set()

def _get_unique_url_name(url_name: str) -> str:
    """
    生成一个唯一的 URL name。

    如果传入的 url_name 尚未被使用，则直接返回；
    如果已被使用，则在其后追加下划线和递增数字（如 _1, _2, ...），
    直到生成一个未被使用的名称为止。

    Args:
        url_name (str): 原始的 URL name（通常来自视图函数名）。

    Returns:
        str: 唯一的 URL name。
    """
    # 检查原始名称是否尚未使用
    if url_name not in url_name_set:
        # 未使用：加入集合并直接返回
        url_name_set.add(url_name)
        return url_name

    # 若原始名称已存在，则尝试添加后缀生成新名称
    counter = 1
    while True:
        # 构造带序号的新名称，例如 "list_users_1"
        new_name = f"{url_name}_{counter}"
        # 如果新名称未被使用，则注册并返回
        if new_name not in url_name_set:
            url_name_set.add(new_name)
            return new_name
        # 否则继续尝试下一个序号
        counter += 1


class AmisRouter(Router):
    def api_operation(
            self,
            methods: List[str],
            path: str,
            *,
            url_name: Optional[str] = None,
            **kwargs
    ) -> Callable[[TCallable], TCallable]:
        def decorator(view_func: TCallable) -> TCallable:
            # 如果 url_name 为 None，则使用 view_func 的函数名
            effective_url_name = _get_unique_url_name(url_name) if url_name is not None else _get_unique_url_name(view_func.__name__)
            # 调用 add_api_operation，传入 effective_url_name 和其他参数
            self.add_api_operation(
                path,
                methods,
                view_func,
                url_name=effective_url_name,
                **kwargs
            )
            return view_func

        return decorator


class AmisAPI(NinjaAPI):


    def __init__(self, *args, **kwargs):
        super().__init__(default_router=AmisRouter(), *args, **kwargs)



    def get_operation_url_name(self, operation, router):
        """
        为给定的操作（operation）生成唯一的 URL name。

        默认使用视图函数的 __name__ 作为基础名称，
        并通过 _get_unique_url_name 确保其唯一性。
        """
        return _get_unique_url_name(operation.view_func.__name__)


amis_api = AmisAPI()
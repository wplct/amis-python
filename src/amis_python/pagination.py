from functools import wraps
from typing import Callable, TypeVar, Type

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja.pagination import PaginationBase
from .ninja_api import PaginatedResponse

class AmisPagination(PaginationBase):
    def __init__(self, page_size: int = 20):
        self.page_size = page_size

    def paginate_queryset(self, queryset, request, **params):
        try:
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            page = 1

        paginator = Paginator(queryset, self.page_size)
        total_pages = paginator.num_pages
        current_page = max(1, min(page, total_pages)) if total_pages > 0 else 1

        page_obj = paginator.page(current_page)

        # 返回 PaginatedResponse 的数据字典（会被 Ninja 自动序列化）
        return {
            "items": list(page_obj.object_list),  # QuerySet -> list of models/dicts
            "count": paginator.count,
            "page": current_page,
            "pages": total_pages,
        }


T = TypeVar("T")
ViewFunc = Callable[..., QuerySet]


def amis_paginate(schema: Type[T], page_size: int = 20):
    """
    分页装饰器，用于 Django Ninja 视图。

    要求：
      - 视图函数返回 QuerySet
      - 接口声明 response=ApiResponse[PaginatedResponse[schema]]
    """

    def decorator(view_func: ViewFunc) -> Callable[..., PaginatedResponse[T]]:
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> PaginatedResponse[T]:
            queryset = view_func(request, *args, **kwargs)
            if not isinstance(queryset, QuerySet):
                raise ValueError(f"View {view_func.__name__} must return a QuerySet")
            # 获取page_size 参数
            per_page = request.GET.get("perPage", page_size)
            # 使用你已有的 AmisPagination
            paginator = AmisPagination(page_size=per_page)
            raw_data = paginator.paginate_queryset(queryset, request)

            # 构造强类型的 PaginatedResponse
            return PaginatedResponse[schema](
                items=raw_data["items"],
                count=raw_data["count"],
                page=raw_data["page"],
                pages=raw_data["pages"]
            )

        return wrapper

    return decorator
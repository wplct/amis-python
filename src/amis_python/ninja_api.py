from functools import wraps
from typing import List, Optional, Callable, Any, TypeVar, Generic, Dict

from django.core.paginator import Paginator
from django.db.models import QuerySet, Q
from django.http import HttpRequest
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status: int = 0
    msg: str = "操作成功"
    data: Optional[T] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    count: int
    page: int
    pages: int

def success_response(data: Any = None, msg: str = "操作成功") -> ApiResponse:
    return ApiResponse(status=0, msg=msg, data=data)

def error_response(msg: str = "操作失败", data: Any = None) -> ApiResponse:
    return ApiResponse(status=1, msg=msg, data=data)


def amis_wrap():
    """
    响应包装装饰器，将视图返回值包装为标准 ApiResponse 格式
    """

    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> ApiResponse:
            print(request.method)
            result = view_func(request, *args, **kwargs)
            return success_response(data=result)

        return wrapper

    return decorator


def amis_paginate(page_size: int = 10):
    """
    分页装饰器，处理查询集的分页逻辑
    """

    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> Dict[str, Any]:
            result = view_func(request, *args, **kwargs)

            if not isinstance(result, QuerySet):
                raise ValueError(f"View {view_func.__name__} must return a QuerySet")

            # 处理分页参数
            try:
                page = int(request.GET.get("page", 1))
            except (TypeError, ValueError):
                page = 1

            try:
                per_page = int(request.GET.get("perPage", page_size))
            except (TypeError, ValueError):
                per_page = page_size

            paginator = Paginator(result, per_page)
            total_pages = paginator.num_pages
            current_page = max(1, min(page, total_pages)) if total_pages > 0 else 1

            page_obj = paginator.page(current_page)

            return {
                "items": list(page_obj.object_list),
                "count": paginator.count,
                "page": current_page,
                "pages": total_pages,
            }

        return wrapper

    return decorator


def amis_filter():
    """
    筛选装饰器，自动解析请求参数作为筛选条件
    默认支持所有模型字段的精确筛选
    """

    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> QuerySet:
            result = view_func(request, *args, **kwargs)
            if not isinstance(result, QuerySet):
                raise ValueError(f"View {view_func.__name__} must return a QuerySet")

            model = result.model
            filter_conditions = Q()
            # 获取所有请求参数作为筛选条件
            for param_name, param_value in request.GET.items():
                # 跳过分页和搜索相关参数
                if param_name not in ["page", "perPage", "search"] and param_value:
                    # 检查字段是否存在于模型中
                    if param_name in [f.name for f in model._meta.fields]:
                        filter_conditions &= Q(**{param_name: param_value})

            if filter_conditions:
                result = result.filter(filter_conditions)

            return result

        return wrapper

    return decorator


def amis_search(*search_fields):
    """
    搜索装饰器，支持多字段搜索
    仅在指定search_fields时启用，通过search参数触发
    """

    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> QuerySet:
            result = view_func(request, *args, **kwargs)

            if not isinstance(result, QuerySet):
                raise ValueError(f"View {view_func.__name__} must return a QuerySet")

            search_term = request.GET.get("search")
            if search_term:
                search_query = Q()
                for field in search_fields:
                    search_query |= Q(**{f"{field}__icontains": search_term})
                result = result.filter(search_query)

            return result

        return wrapper

    return decorator


def amis_crud(page_size: int = 20, search_fields: Optional[List[str]] = None):
    """
    组合装饰器，整合分页、筛选、搜索和响应包装功能

    参数：
      - page_size: 默认每页条数
      - search_fields: 允许搜索的字段列表，不提供则不启用搜索功能
    """

    def decorator(view_func: Callable) -> Callable:
        # 应用装饰器链
        wrapped_func = view_func

        # 1. 应用筛选装饰器
        wrapped_func = amis_filter()(wrapped_func)

        # 2. 应用搜索装饰器（仅当指定search_fields时）
        if search_fields:
            wrapped_func = amis_search(search_fields)(wrapped_func)

        # 3. 应用分页装饰器
        wrapped_func = amis_paginate(page_size)(wrapped_func)

        # 4. 应用响应包装装饰器
        wrapped_func = amis_wrap()(wrapped_func)

        return wrapped_func

    return decorator
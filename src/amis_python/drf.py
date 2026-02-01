import logging
import traceback
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exc_handler
from rest_framework import exceptions as drf_exceptions
from django.conf import settings

logger = logging.getLogger(__name__)


# ---------- 分页 ----------
class AmisPagination(PageNumberPagination):
    page_size_query_param = "perPage"

# ---------- 统一响应体 ----------
class AmisResponse(Response):
    """
    统一包装成 { code: 0, msg: 'ok', data: ... }
    """
    def __init__(self, data=None, code=0, msg='ok', status=None,
                 template_name=None, headers=None, exception=False, content_type=None, **kwargs):

        super().__init__(
            data={'status': code, 'msg': msg, 'data': data, **kwargs},
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )

class AmisErrorResponse(Response):
    """
    统一包装成 { code: 1, msg: 'error', error: ... }
    """
    def __init__(self, exc, code=1, msg='error', status=None,
                 template_name=None, headers=None, content_type=None):
        super().__init__(
            data={'status': code, 'msg': msg, 'error': exc},
            status=status,
            template_name=template_name,
            headers=headers,
            content_type=content_type
        )
# ---------- 异常处理 ----------
def std_exception_handler(exc, context):
    """
    全局异常处理器 - 返回原始数据结构，不创建Response对象
    实际响应包装在AmisViewSet.finalize_response中完成
    """
    # 1. 先让DRF原生处理器处理
    response = drf_exc_handler(exc, context)

    # 2. 获取请求对象（用于判断是否显示详细错误）
    request = context.get('request')
    # 3. 处理验证错误
    if isinstance(exc, drf_exceptions.ValidationError):
        logger.info('[%s] %s', type(exc).__name__, exc)
        exc_str = ""
        if isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                # 处理嵌套错误
                if isinstance(value, list):
                    exc_str += f'{key}: {"; ".join(str(v) for v in value)}\n'
                else:
                    exc_str += f'{key}: {str(value)}\n'
        elif isinstance(exc.detail, list):
            exc_str = "; ".join(str(v) for v in exc.detail)

        return {
            'status': 400,
            'msg': exc_str.strip() or '数据验证失败',
            'data': response.data if response else exc.detail
        }

    # 4. 处理API异常
    if isinstance(exc, drf_exceptions.APIException):
        logger.info('[%s %s] %s', type(exc).__name__, exc.status_code, exc)
        return {
            'status': exc.status_code,
            'msg': str(exc.detail),
            'data': response.data if response else {'detail': str(exc.detail)}
        }

    # 5. 处理未捕获的程序级异常
    logger.exception('Unhandled exception: %s', exc)
    error_detail = str(exc)

    # 仅对管理员/开发环境显示详细错误
    if settings.DEBUG or (request and hasattr(request, 'user') and request.user.is_superuser):
        error_detail += f"\n{traceback.format_exc()}"

    return {
        'status': 500,
        'msg': '服务器内部错误' if not settings.DEBUG else error_detail,
        'data': None
    }


# ---------- 通用 ViewSet ----------
class AmisViewSet(viewsets.ModelViewSet):
    pagination_class = AmisPagination

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        # 把带 btn 标记的方法反向绑定 viewset
        for name, attr in cls.__dict__.items():
            if getattr(attr, 'btn', False):
                attr.viewset = cls

    def finalize_response(self, request, response, *args, **kwargs):
        """
        关键修复：在DRF渲染流程最后阶段统一包装
        此时 .accepted_renderer 已正确设置，避免AssertionError
        """
        # 1. 先执行DRF标准流程（设置渲染器/处理异常等）
        response = super().finalize_response(request, response, *args, **kwargs)

        # 2. 检查是否已处理（防止重复包装）
        if hasattr(response, '_amis_processed'):
            return response

        # 3. 仅处理有data属性的响应（排除StreamingHttpResponse等）
        if hasattr(response, 'data'):
            # 处理204 No Content（保持HTTP语义正确性）
            if response.status_code == 204:
                response.data = {
                    'status': 0,
                    'msg': '操作成功',
                    'data': None
                }
                response.status_code = 200

            # 处理成功响应 (2xx)
            elif 200 <= response.status_code < 300:
                # 避免重复包装
                if not isinstance(response.data, dict) or 'status' not in response.data:
                    response.data = {
                        'status': 0,
                        'msg': 'success',
                        'data': response.data
                    }

            # 处理错误响应 (4xx/5xx)
            elif response.status_code >= 400:
                # 如果异常处理器返回了字典格式，直接使用
                if isinstance(response.data, dict) and 'status' in response.data:
                    pass  # 已是标准格式
                else:
                    # 从异常处理器获取错误数据
                    exc_data = getattr(request, '_error_data', None)
                    if exc_data and isinstance(exc_data, dict):
                        response.data = exc_data
                        response.status_code = exc_data.get('status', response.status_code)
                    else:
                        # 默认错误格式
                        response.data = {
                            'status': response.status_code,
                            'msg': '请求失败',
                            **response.data
                        }

        # 4. 标记已处理
        response._amis_processed = True
        return response

    def success(self, data=None):
        """快捷成功响应方法"""
        return Response({
            'status': 0,
            'msg': 'success',
            'data': data
        })
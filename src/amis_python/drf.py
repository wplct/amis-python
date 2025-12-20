import json
import logging
import traceback
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exc_handler
from rest_framework import exceptions as drf_exceptions

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
                 template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(
            data={'code': code, 'msg': msg, 'data': data},
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )

# ---------- 异常处理 ----------
def std_exception_handler(exc, context):
    response = drf_exc_handler(exc, context)          # 先让 DRF 处理

    if isinstance(exc, drf_exceptions.APIException):  # 已知业务异常
        logger.info('[%s] %s', type(exc).__name__, exc)
        return AmisResponse(
            data=response.data if response else {},
            code=response.status_code if response else 400,
            msg=response.status_text if response else 'error',
            status=200,
            headers=response.headers if response else {}
        )

    # 程序级异常
    logger.exception('Unhandled exception: %s', exc)  # 自动带 traceback
    return AmisResponse(
        data=traceback.format_exc(),
        code=500,
        msg='服务器内部错误',
        status=200
    )

# ---------- 通用 ViewSet ----------
class AmisViewSet(viewsets.ModelViewSet):
    pagination_class = AmisPagination

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        # 把带 btn 标记的方法反向绑定 viewset
        for name, attr in cls.__dict__.items():
            if getattr(attr, 'btn', False):
                attr.viewset = cls

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
            if isinstance(response, dict):
                return AmisResponse(data=response)
            if isinstance(response, AmisResponse):
                return response
            if isinstance(response, Response):
                # 把非 200 的 HTTP 状态码也包成 200 返回
                response.status_code = 200
                response.data.update({'code': 0, 'msg': 'success'})
                return response
            return response
        except Exception as exc:
            # 统一走上面的异常处理
            return std_exception_handler(exc, self.get_exception_handler_context())
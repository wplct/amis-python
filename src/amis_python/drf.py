from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exc_handler


class AmisPagination(PageNumberPagination):
    page_size_query_param = "perPage"


class AmisResponse(Response):
    """
    统一包装成 { status: 0, msg: 'ok', data: ... }
    """

    def __init__(self, data=None, code=0, msg='ok',
                 status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        super().__init__(
            data={'status': code, 'msg': msg, 'data': data},
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )


def std_exception_handler(exc, context):
    # 先让 DRF 把原始错误对象转成 dict
    response = drf_exc_handler(exc, context)
    if response is not None:
        # 业务逻辑正常，只是 DRF 抛了 4xx/5xx
        return AmisResponse(
            data=response.data,
            code=response.status_code,
            msg=response.status_text,
            status=response.status_code,
            headers=response.headers
        )
    # DRF 没接住，是更低层的异常（如 500）
    return AmisResponse(
        data=str(exc),
        code=500,
        msg='服务器内部错误',
        status=500
    )

class AmisViewSet(viewsets.ModelViewSet):
    """
    统一处理分页、错误返回
    """
    pagination_class = AmisPagination

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        # 类已经生成，可以扫描自己
        for name, attr in cls.__dict__.items():
            if getattr(attr, 'btn', False):
                attr.viewset = cls


    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
            response.data = {
                'code': 0,
                'msg': 'success',
                'data': response.data
            }
            return response
        except Exception as exc:
            # 这里可以写异常日志
            raise
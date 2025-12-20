# from django.urls import reverse
from contextlib import contextmanager

from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from amis_python import Api
from amis_python.build_amis.form import ViewSetForm
from amis_python.builder import Button, EventAction, Dialog, Flex, Container, Pagination, ButtonGroup, Card, BaseModel
from amis_python.builder.crud import CRUD2, CRUD2Mode, LoadType
from amis_python.builder.form import Form, InputText


def _action_allowed(viewset_cls, request, action: str, method: str, kwargs=None) -> bool:
    """
    任意 Django/DRF request 都能用，内部会转成 DRF Request 再走权限链路。
    """
    kwargs = kwargs or {}

    # 1. 先造一个 DRF 版本的 request（带上 authenticators 等全套属性）
    drf_request = APIView().initialize_request(request)

    # 2. 临时改 method
    origin = drf_request.method
    drf_request.method = method.upper()
    try:
        # 3. 实例化 ViewSet 并跑权限
        viewset = viewset_cls(kwargs=kwargs)
        viewset.action = action
        viewset.request = drf_request
        viewset.check_permissions(drf_request)
        return True
    except PermissionDenied:
        return False
    finally:
        drf_request.method = origin      # 恢复 method


# 下面四个语义化函数，随便调
def can_list   (viewset_cls, request) -> bool:
    return _action_allowed(viewset_cls, request, 'list',   'GET')

def can_create (viewset_cls, request) -> bool:
    return _action_allowed(viewset_cls, request, 'create', 'POST')

def can_update (viewset_cls, request, pk) -> bool:
    return _action_allowed(viewset_cls, request, 'partial_update', 'PATCH', {'pk': pk})

def can_delete (viewset_cls, request, pk) -> bool:
    return _action_allowed(viewset_cls, request, 'destroy', 'DELETE', {'pk': pk})


class ViewSetCRUD:
    def __init__(self, view_set: GenericAPIView, request, basename=None):
        self.request = request
        self.view_set = view_set
        self.serializer = view_set.get_serializer_class()()
        self.view_form = ViewSetForm(view_set, basename)
        if not basename:
            self.basename = view_set.queryset.model._meta.model_name
        else:
            self.basename = basename

        self.component_id = f"{self.basename}-crud"

    def get_api(self):
        return Api(
            method="get",
            url=reverse(f"{self.basename}-list"),
        )

    def get_delete_api(self):
        return Api(
            method="delete",
            url=reverse(f"{self.basename}-detail", kwargs={"pk": "0"}).replace("0", "${id}"),
        )

    def get_list_action_button(self):
        buttons = []
        return buttons

    def get_detail_action_button(self):
        buttons = []
        return buttons

    def get_create_button(self):
        if not can_create(self.view_set.__class__, self.request):
            return []
        return [Button(
            label="新建",
            level="primary",
            class_name='m-r-xs'
        ).add_action('click', EventAction(
            action_type="dialog",
            dialog=Dialog(
                title="新建",
                body=self.view_form.to_create_form(),
                size="md",
            )
        ))]

    def get_header_toolbar(self):

        return self.get_create_button() + self.get_list_action_button()

    def get_footer_toolbar(self):
        return [
            Pagination(
                per_page=10,
                layout=[
                    "total",
                    "perPage",
                    "pager"
                ],
                mode="normal",
                per_page_available=[
                    5,
                    10,
                    20,
                    50,
                    100
                ]
            ),
        ]

    def get_update_button(self):
        if not can_update(self.view_set.__class__, self.request,""):
            return []
        return [Button(label="修改", level="primary",
                       action_type="dialog",
                       dialog=Dialog(
                           title="修改",
                           body=self.view_form.to_update_form(),
                           size="md"
                       ))]

    def get_delete_button(self):
        if not can_delete(self.view_set.__class__, self.request,""):
            return []
        return [(Button(label="删除", level="danger",
                        confirm_text="确定要删除吗？")
                 .add_action(
            'click',
            EventAction(
                action_type="ajax",
                api=self.get_delete_api(),
            )
        ).add_action('click', EventAction(action_type='search', component_id=self.component_id)))]

    def get_list_button(self, group=True):
        buttons = [
            *self.get_detail_action_button(),
            *self.get_update_button(),
            *self.get_delete_button()
        ]
        if group:
            return [
                ButtonGroup(
                    label="操作",
                    buttons=buttons
                )
            ]
        return buttons

    def get_columns(self):
        return self.view_form.get_list_items(static=True)

    def get_filter(self):
        if not self.view_set.filter_backends:
            return None
        filter_items = []
        if SearchFilter in self.view_set.filter_backends:
            filter_items.append(
                InputText(
                    name="search",
                    label="搜索",
                )
            )
        if hasattr(self.view_set, 'filterset_fields'):
            if isinstance(self.view_set.filterset_fields, list):
                for field in self.view_set.filterset_fields:
                    filter_items.append(
                        self.view_form.field_to_input(field, no_required=True)
                    )

        return Form(
            title="筛选",
            body=filter_items,
            mode="inline",
            actions=[
                Button(label="清空", action_type="clear"),
                BaseModel(label="查询", level="primary", type="submit")
            ]
        )

    def to_crud(self, **kwargs):
        return CRUD2(
            id=f"{self.basename}-crud",
            mode=CRUD2Mode.TABLE2,
            filter=self.get_filter(),
            api=self.get_api(),
            columns=self.get_columns() + self.get_list_button(),
            header_toolbar=self.get_header_toolbar(),
            footer_toolbar=self.get_footer_toolbar(),
            sync_location=True,
            primary_field="id",
            load_type=LoadType.PAGINATION,
            **kwargs
        )


class ViewSetCRUDCard(ViewSetCRUD):
    def to_crud(self, **kwargs):
        return CRUD2(
            id=f"{self.basename}-crud",
            mode=CRUD2Mode.CARDS,
            api=self.get_api(),
            card=Card(
                body=self.get_columns(),
                actions=self.get_list_button(group=False)
            ),
            columns=self.get_columns(),
            header_toolbar=self.get_header_toolbar(),
            footer_toolbar=self.get_footer_toolbar(),
            sync_location=True,
            primary_field="id",
            load_type=LoadType.PAGINATION,
            **kwargs
        )

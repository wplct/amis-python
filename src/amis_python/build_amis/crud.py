# from django.urls import reverse
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse

from amis_python import Api
from amis_python.build_amis.form import ViewSetForm
from amis_python.builder import Button, EventAction, Dialog, Flex, Container, Pagination, ButtonGroup, Card, BaseModel
from amis_python.builder.crud import CRUD2, CRUD2Mode, LoadType
from amis_python.builder.form import Form, InputText


# def get_dialog(func):
#     kwargs = getattr(func, 'btn_kwargs', {})
#     label = kwargs.get('label', func.__name__)
#     serializer_class = kwargs.get('serializer_class', func.viewset.serializer_class)
#
#     return Dialog(
#         title=label,
#         body=ViewSetForm(func.viewset(),serializer_class=serializer_class).to_update_form()
#     )


# def get_func_btn(func):
#     def decorator():
#         kwargs = getattr(func, 'btn_kwargs', {})
#         return Button(**kwargs)
#     return decorator
#
#
# def button(**kwargs):
#     def decorator(func):
#         func.btn = get_func_btn(func)
#         func.btn_kwargs = kwargs
#         return func
#     return decorator
def has_create_static(viewset_cls):
    """没有 request，也能粗略判断 create 会不会被拦"""
    # 取 ViewSet 上声明的权限类
    for perm_cls in getattr(viewset_cls, 'permission_classes', []):
        # 常见“只读”权限类都是这一行逻辑，直接复用
        if hasattr(perm_cls, 'has_permission'):
            # 伪造一个 POST 请求对象，只带 method 属性
            fake_request = type('FakeReq', (), {'method': 'POST'})()
            if not perm_cls().has_permission(fake_request, viewset_cls()):
                return False
    return True

def has_delete_static(viewset_cls):
    """没有 request，也能粗略判断 delete 会不会被拦"""
    for perm_cls in getattr(viewset_cls, 'permission_classes', []):
        if hasattr(perm_cls, 'has_permission'):
            # 伪造 DELETE 请求
            fake_request = type('FakeReq', (), {'method': 'DELETE'})()
            if not perm_cls().has_permission(fake_request, viewset_cls()):
                return False
    return True
def has_update_static(viewset_cls):
    """没有 request，也能粗略判断 update 会不会被拦"""
    for perm_cls in getattr(viewset_cls, 'permission_classes', []):
        if hasattr(perm_cls, 'has_permission'):
            # 伪造 PATCH 请求
            fake_request = type('FakeReq', (), {'method': 'PATCH'})()
            if not perm_cls().has_permission(fake_request, viewset_cls()):
                return False
    return True
class ViewSetCRUD:
    def __init__(self, view_set: GenericAPIView, basename=None):
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
        if not has_create_static(self.view_set.__class__):
            return None
        return Button(
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
        ))

    def get_header_toolbar(self):

        return [self.get_create_button()] + self.get_list_action_button()

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
        if not has_update_static(self.view_set.__class__):
            return None
        return Button(label="修改", level="primary",
                      action_type="dialog",
                      dialog=Dialog(
                          title="修改",
                          body=self.view_form.to_update_form(),
                          size="md"
                      ))

    def get_delete_button(self):
        if not has_delete_static(self.view_set.__class__):
            return None
        return (Button(label="删除", level="danger",
                       confirm_text="确定要删除吗？")
                .add_action(
            'click',
            EventAction(
                action_type="ajax",
                api=self.get_delete_api(),
            )
        ).add_action('click', EventAction(action_type='search', component_id=self.component_id)))

    def get_list_button(self, group=True):
        buttons = [
            *self.get_detail_action_button(),
            self.get_update_button(),
            self.get_delete_button()
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
                        self.view_form.field_to_input(field,no_required=True)
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

# from django.urls import reverse

from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse

from amis_python import Api
from amis_python.build_amis.form import ViewSetForm
from amis_python.builder import Button, EventAction, Dialog, Flex, Container, Pagination, ButtonGroup
from amis_python.builder.crud2 import CRUD2, CRUD2Mode, LoadType


class ViewSetCRUD:
    def __init__(self, view_set: GenericAPIView, basename=None):
        self.view_set = view_set
        self.serializer = view_set.get_serializer_class()()
        self.view_form = ViewSetForm(view_set, basename)
        if not basename:
            self.basename = view_set.queryset.model._meta.model_name
        else:
            self.basename = basename

        self.component_id=f"{self.basename}-crud"

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

    def get_header_toolbar(self):
        return [Button(
            label="新建",
            level="primary",
        ).add_action('click', EventAction(
            action_type="dialog",
            dialog=Dialog(
                title="新建",
                body=self.view_form.to_create_form(),
                size="md"
            )
        ))]

    def get_footer_toolbar(self):
        return [
            Pagination(
                per_page=5,
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
        return Button(label="修改", level="primary",
                      action_type="dialog",
                      dialog=Dialog(
                          title="新建",
                          body=self.view_form.to_create_form(),
                          size="md"
                      ))

    def get_delete_button(self):
        return (Button(label="删除", level="danger",
                       confirm_text="确定要删除吗？")
        .add_action(
            'click',
            EventAction(
                action_type="ajax",
                api=self.get_delete_api(),
            )
        ).add_action('click',EventAction(action_type='search', component_id=self.component_id)))

    def get_list_button(self):
        return [
            ButtonGroup(
                label="操作",
                buttons=[
                    self.get_update_button(),
                    self.get_delete_button()
                ]
            )
        ]

    def get_columns(self):
        return self.view_form.get_list_items(static=True) + self.get_list_button()

    def to_crud(self, **kwargs):
        return CRUD2(
            id=f"{self.basename}-crud",
            mode=CRUD2Mode.TABLE2,
            api=self.get_api(),
            columns=self.get_columns(),
            header_toolbar=self.get_header_toolbar(),
            footer_toolbar=self.get_footer_toolbar(),
            sync_location=True,
            primary_field="id",
            load_type=LoadType.PAGINATION,
            **kwargs
        )

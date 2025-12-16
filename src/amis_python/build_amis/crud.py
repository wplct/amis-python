# from django.urls import reverse
from http.cookiejar import debug

from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse

from amis_python import Api
from amis_python.build_amis.form import ViewSetForm
from amis_python.builder import Button, EventAction, Dialog, Flex, Container, Pagination
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

    def get_api(self):
        return Api(
            method="get",
            url=reverse(f"{self.basename}-list"),
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
                behavior= "Pagination",
                mode="normal",
                per_page_available=[
                    5,
                    10,
                    20,
                    50,
                    100
                ]
            ),
            Flex(items=[
                Container(align="left"),
                Container(align="right", body=[

                ])
            ])
        ]
    def get_list_button(self):
        return [Button(label="测试")]

    def get_columns(self):
        return self.view_form.get_list_items(static=True)+self.get_list_button()
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

# from django.urls import reverse

from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse

from amis_python import Api
from amis_python.build_amis.form import ViewSetForm
from amis_python.builder import Button, EventAction, Dialog, Flex, Container, Pagination, ButtonGroup, Card
from amis_python.builder.crud import CRUD2, CRUD2Mode, LoadType


def button(**kwargs):
    def decorator(func):
        func.button = Button(**kwargs)
        return func

    return decorator


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
        for action in self.view_set.get_extra_actions():
            if not action.detail:
                if hasattr(action, 'button'):
                    buttons.append(action.button)
                    continue
                name = action.__name__
                buttons.append(Button(
                    label=name,
                    class_name='m-r-xs',
                ))
        return buttons

    def get_detail_action_button(self):
        buttons = []
        for action in self.view_set.get_extra_actions():
            if action.detail:
                if hasattr(action, 'button'):
                    buttons.append(action.button)
                    continue
                name = action.__name__
                buttons.append(Button(
                    label=name,
                ))
        return buttons

    def get_header_toolbar(self):

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
        ))] + self.get_list_action_button()

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
                          title="修改",
                          body=self.view_form.to_update_form(),
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

    def to_crud(self, **kwargs):
        return CRUD2(
            id=f"{self.basename}-crud",
            mode=CRUD2Mode.TABLE2,
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

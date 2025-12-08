from typing import Any, Type

from django.db.models import Model
from ninja import ModelSchema

from amis_python import PageBuilder, to_api
from amis_python.builder.action import DialogActionBuilder, AjaxActionBuilder
from amis_python.builder.button import ButtonBuilder
from amis_python.builder.crud import CRUDCardsBuilder
from amis_python.builder.event import AmisEvent
from amis_python.builder.form import api_to_form, schema_to_form
from amis_python.ninja_api import PaginatedResponse, ApiResponse, amis_api
from amis_python.pagination import amis_paginate


def generate_crud_page(db_model: Type[Model], ) -> PageBuilder:
    """创建基础CRUD页面"""
    # 获取模型名称
    model_name = db_model._meta.model_name

    class CRUDSchema(ModelSchema):
        class Meta:
            model = db_model
            exclude = ('created_at','updated_at','is_deleted')

    class CreateCRUDSchema(ModelSchema):
        class Meta:
            model = db_model
            exclude = ("id",'created_at','updated_at','is_deleted')

    @amis_api.get(f"/{model_name}/list", response=ApiResponse[PaginatedResponse[CRUDSchema]])
    @amis_paginate(CRUDSchema)
    def data_list(request):
        return db_model.objects.order_by("-id")

    @amis_api.post(f"/{model_name}/create", response=ApiResponse[CreateCRUDSchema])
    def create_data(request, data: CreateCRUDSchema):
        obj = db_model.objects.create(**data.model_dump())
        return obj

    @amis_api.post(f"/{model_name}/update/" + "{id}", response=ApiResponse[CreateCRUDSchema])
    def update_data(request, id: int, data: CreateCRUDSchema):
        obj = db_model.objects.get(id=id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        obj.save()
        return obj

    @amis_api.post(f"/{model_name}/delete/" + "{id}", response=ApiResponse[Any])
    def delete_by_id(request, id: int):
        db_model.objects.filter(id=id).delete()
        return {"ok": True}

    show_form = schema_to_form(CRUDSchema, static=True, mode="inline", wrap_with_panel=False)

    return PageBuilder(
        # title=f"{db_model._meta.verbose_name}管理",
        body=[
            ButtonBuilder(label="新增", level='primary', )
            .add_action(
                AmisEvent.click,
                DialogActionBuilder(
                    dialog={
                        'title': '新增',
                        'body': [
                            api_to_form(create_data)
                        ]
                    },
                )
            ),
            {"type": "divider"},
            CRUDCardsBuilder(
                id="curd",
                api=to_api(data_list),
                multiple=True,
                card={
                    'body': [
                        show_form
                    ],
                    'actions': [
                        ButtonBuilder(label="编辑", level="link").add_action(
                            AmisEvent.click,
                            DialogActionBuilder(
                                dialog={
                                    'title': '编辑用户',
                                    'body': [
                                        api_to_form(update_data)
                                    ]
                                }
                            ),
                        ),
                        AjaxActionBuilder(label="删除", api=to_api(delete_by_id)),
                    ]
                },
            )
        ]
    )

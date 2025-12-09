from typing import Dict, List

from ninja import Body, ModelSchema
from ninja.pagination import paginate
from pydantic import BaseModel

from amis_python import register_page
from amis_python.ninja_api import amis_api, success_response, ApiResponse, PaginatedResponse
from amis_python.page.curd_card import generate_crud_page
from amis_python.pagination import AmisPagination, amis_paginate
from my_app.models import Domain


class DomainSchema(ModelSchema):
    class Meta:
        model = Domain
        fields = "__all__"


class CreateDomain(ModelSchema):
    class Meta:
        model = Domain
        fields = ["name", "description"]


@amis_api.get("/crud/initData", response=ApiResponse[PaginatedResponse[DomainSchema]])
@amis_paginate(DomainSchema)
def init_data(request):
    return Domain.objects.order_by("-id")


@amis_api.post("/crud/delete/{ids}")
def delete(request, ids: str):
    Domain.objects.filter(id__in=ids.split(",")).delete()
    return {"ok": True}


@amis_api.post("/crud/delete/{id}")
def delete_by_id(request, id: str):
    Domain.objects.filter(id=id).delete()
    return {"ok": True}


@amis_api.post("/crud/create")
def create_test_data(request, data: CreateDomain = Body(...)):
    Domain.objects.create(**data.model_dump())
    return {"ok": True}


from amis_python.builder.form import api_to_form

# page = PageBuilder(
#     title="增删改查示例",
#     body=[
#         ButtonBuilder(label="新增", level='primary', )
#         .add_action(
#             AmisEvent.click,
#             DialogActionBuilder(
#                 dialog={
#                     'title': '新增用户',
#                     'body': [
#                         api_to_form(create_test_data)
#                     ],
#                     "onEvent": {
#                         'actions': {
#                             'confirm': [
#                                 {
#                                     "actionType": "toast",
#                                     "args": {
#                                         "msg": "你的名字是"
#                                     }
#                                 },
#                             ]
#                         }
#
#                     }
#                 },
#             )
#         ),
#         {"type": "divider"},
#         CRUDCardsBuilder(
#             id="curd",
#             api=to_api(init_data),
#             multiple=True,
#             card={
#                 # 'header': {'title': '用户信息-${name}'},
#                 'body': [
#                     {
#                         "label": "id",
#                         "name": "id"
#                     },
#                     {
#                         "label": "名称",
#                         "name": "name"
#                     },
#                     {
#                         "label": "描述",
#                         "name": "description"
#                     },
#                     {
#                         "label": "创建时间",
#                         "name": "created_at"
#                     },
#                     {
#                         "label": "更新时间",
#                         "name": "updated_at"
#                     },
#                 ],
#                 'actions': [
#                     ButtonBuilder(label="编辑", level="link").add_action(
#                         AmisEvent.click,
#                         DialogActionBuilder(
#                             dialog={
#                                 'title': '编辑用户',
#                                 'body': [
#                                     api_to_form(create_test_data)
#                                 ]
#                             }
#                         ),
#                     ),
#                     AjaxActionBuilder(label="删除", api=to_api(delete_by_id)),
#
#                 ]
#             },
#             # bulk_actions=[AjaxActionBuilder(label="删除选中", api=to_api(delete))],
#             # actions=[
#             #     AjaxActionBuilder(label="测试删除", api=to_api(delete))
#             # ],
#         )
#     ]
# )
page = generate_crud_page(Domain)
register_page("卡片", "/crud/cards", page)

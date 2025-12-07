from typing import Dict

from ninja import Body
from pydantic import BaseModel

from amis_python import AppPageBuilder, register_page, PageBuilder, to_api
from amis_python.builder.action import AjaxActionBuilder
from amis_python.builder.button import ButtonBuilder
from amis_python.builder.crud import CRUDBuilder, CRUDCardsBuilder
from amis_python.builder.event import AmisEvent
from amis_python.builder.tpl import TplBuilder
from amis_python.ninja_api import amis_api, success_response


@amis_api.get("/crud/initData")
def init_data(request):
    rows = [
        {
            "id": i,
            "name": f"用户{i}",
            "email": "",
            "phone": "",
            "address": "",
        } for i in range(10)
    ]

    return success_response({
        "rows": rows,
        "count": 3
    })


@amis_api.post("/crud/delete/{ids}")
def delete(request, ids: str):
    print(ids)
    return success_response({
        "ok": True
    })


@amis_api.post("/crud/delete/{id}")
def delete_by_id(request, id: str):
    print(id)
    return success_response({
        "ok": True
    })

class CreateData(BaseModel):
    name: str
    email: str
    phone: str
    address: str


@amis_api.post("/crud/create")
def create_test_data(request,data: CreateData = Body(...)):
    print(data)
    return success_response({
        "ok": True
    })

page = PageBuilder(
    title="增删改查示例",
    toolbar=[
        ButtonBuilder(label="新增",level='primary', )
        .add_action(
                AmisEvent.click,
                AjaxActionBuilder(api=to_api(create_test_data))
            )
        ,
    ],
    body=[
        CRUDCardsBuilder(
            api=to_api(init_data),
            multiple=True,
            card={
                'header': {'title': '用户信息-${name}'},
                'body': [
                    {
                        "label": "id",
                        "name": "id"
                    },
                    {
                        "label": "姓名",
                        "name": "name"
                    },
                    {
                        "label": "邮箱",
                        "name": "email"
                    },
                    {
                        "label": "手机号",
                        "name": "phone"
                    },
                ],
                'actions': [
                    AjaxActionBuilder(label="删除", api=to_api(delete_by_id)),
                    AjaxActionBuilder(label="删除", api=to_api(delete_by_id)),
                    AjaxActionBuilder(label="删除", api=to_api(delete_by_id)),
                    AjaxActionBuilder(label="删除", api=to_api(delete_by_id)),
                ]
            },
            bulk_actions=[AjaxActionBuilder(label="测试选择删除", api=to_api(delete))],
            actions=[
                AjaxActionBuilder(label="测试删除", api=to_api(delete))
            ],
        )
    ]
)

register_page("卡片", "/crud/cards", page)

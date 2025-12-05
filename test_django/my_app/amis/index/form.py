from typing import Dict

from ninja import Router, Body

from amis_python.builder.api import api
from amis_python.builder.page import PageBuilder
from amis_python.builder.form import FormBuilder
from amis_python.builder.input import InputTextBuilder, InputEmailBuilder
from amis_python.registry import register_page

router = Router()


@router.post("/save")
def save_form(request, data: Dict = Body(...)):
    """
    保存表单数据
    """
    print(data)
    return {"status": 0, "msg": "操作成功", "data": {}}


# 创建PageBuilder实例
page = PageBuilder(
    title="表单页面",
    body=[
        FormBuilder(
            mode="horizontal",
            api=api(save_form),
            body=[
                InputTextBuilder(
                    label="Name",
                    name="name"
                ),
                InputEmailBuilder(
                    label="Email",
                    placeholder="请输入邮箱地址",
                    name="email"
                )
            ]
        )
    ]
)
# 注册页面
register_page("表单页面", "/index/form", page)

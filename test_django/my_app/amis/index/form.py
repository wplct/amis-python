from typing import Dict

from ninja import  Body

from amis_python import PageBuilder, FormBuilder, InputTextBuilder, InputEmailBuilder
from amis_python.builder.api import to_api

from amis_python.ninja_api import amis_api
from amis_python.registry import register_page

@amis_api.post("/form/save")
def save_form(request, data: Dict = Body(...)):
    """
    保存表单数据
    """
    return {"status": 0, "msg": "操作成功", "data": {}}

# 创建PageBuilder实例
page = PageBuilder(
    title="表单页面",
    body=[
        FormBuilder(
            mode="horizontal",
            api=to_api(save_form),
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

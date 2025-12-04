from amis_python.builder.page import PageBuilder
from amis_python.builder.form import FormBuilder
from amis_python.builder.input import InputTextBuilder, InputEmailBuilder
from amis_python.registry import register_page

# 创建PageBuilder实例
page = PageBuilder(
    title="表单页面",
    body=[
        FormBuilder(
            mode="horizontal",
            api="/amis/api/mock2/form/saveForm",
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
print(FormBuilder(
    mode="horizontal",
    api="/amis/api/mock2/form/saveForm",
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
).to_schema())
print(InputEmailBuilder(
    label="Email",
    placeholder="请输入邮箱地址",
    name="email"
).to_schema())
# 注册页面
register_page("表单页面", "/index/form", page)

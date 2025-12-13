from amis_python import register_page, Page
from amis_python.builder.form import Form, InputImage

page = Page(
    title="上传测试",
    body=[
        Form(
            title="上传测试",
            mode="horizontal",
            api="/api/upload",
            body=[
                InputImage(
                    receiver="/amis/upload",
                    name="image",
                    label="图片",
                )
            ],
        )
    ]
)


register_page("上传测试", "/upload",page.model_dump())
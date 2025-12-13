from amis_python import register_page, Page
from amis_python.builder import Wrapper
from amis_python.builder.form import Form, InputImage, Hidden, InputFile

page = Page(
    title="上传测试",
    body=[
        Form(
            title="上传测试",
            mode="horizontal",
            api="/api/upload",
            body=[
                Wrapper(body=[
                    InputImage(
                        receiver="/amis/upload_img",
                        name="image_img",
                        label="图片",
                        auto_fill={
                            "image": "${id}"
                        },
                    ),
                    Hidden(name="image"),
                ]),
                InputFile(
                    name="file",
                    label="文件",
                    receiver="/amis/upload",
                    auto_fill={
                        "file": "${id}"
                    },
                    drag=True,
                ),
            ],
        )
    ]
)

register_page("上传测试", "/upload", page.model_dump())

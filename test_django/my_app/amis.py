from amis_python import register_default_app
from amis_python.builder.app import AppBuilder
from amis_python.builder.page import PageBuilder

# 创建 AMIS 应用实例
app = AppBuilder(
    brand_name="测试应用",
    base_path="/amis/"
)

# 手动注册分组
app.register_page_group(label="测试分组")
app.register_page_group(label="表单分组")

# 创建并注册测试页面
app.register_page(
    path="/test",
    page=PageBuilder(
        title="测试页面",
        body=[
            {
                "type": "text",
                "text": "Hello AMIS!"
            },
            {
                "type": "button",
                "label": "测试按钮",
                "actionType": "button",
                "level": "primary"
            }
        ]
    ),
    group="测试分组",
    label="测试页面"
)

# 创建并注册表单页面
app.register_page(
    path="/form",
    page=PageBuilder(
        title="表单页面",
        body=[
            {
                "type": "form",
                "mode": "horizontal",
                "api": "/saveForm",
                "body": [
                    {
                        "label": "姓名",
                        "type": "input-text",
                        "name": "name",
                        "required": True
                    },
                    {
                        "label": "邮箱",
                        "type": "input-email",
                        "name": "email",
                        "required": True
                    },
                    {
                        "label": "年龄",
                        "type": "input-number",
                        "name": "age",
                        "min": 18,
                        "max": 100
                    },
                    {
                        "label": "性别",
                        "type": "radio",
                        "name": "gender",
                        "options": [
                            {"label": "男", "value": "male"},
                            {"label": "女", "value": "female"}
                        ],
                        "default": "male"
                    },
                    {
                        "label": "爱好",
                        "type": "checkbox",
                        "name": "hobbies",
                        "options": [
                            {"label": "阅读", "value": "reading"},
                            {"label": "运动", "value": "sports"},
                            {"label": "音乐", "value": "music"}
                        ]
                    }
                ],
                "actions": [
                    {
                        "type": "submit",
                        "label": "提交"
                    },
                    {
                        "type": "reset",
                        "label": "重置"
                    }
                ]
            }
        ]
    ),
    group="表单分组",
    label="表单页面"
)

# 注册默认应用
register_default_app(app)

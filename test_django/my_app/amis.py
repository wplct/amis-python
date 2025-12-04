from amis_python import PageBuilder
from amis_python import register_page

register_page("测试页面","/test",PageBuilder(
    title="测试页面",
    body=[
        {
            "type": "tpl",
            "tpl": "这是测试页面"
        }
    ]
))

from amis_python.builder.page import PageBuilder
from amis_python.registry import register_page

# 创建PageBuilder实例
page = PageBuilder(
    title="标题",
    remark={
        "title": "标题",
        "body": "这是一段描述问题，注意到了没，还可以设置标题。而且只有点击了才弹出来。",
        "icon": "question-mark",
        "placement": "right",
        "trigger": "click",
        "rootClose": True
    },
    body="内容部分. 可以使用 \${var} 获取变量。如: `\$date`: ${date}",
    aside="边栏部分",
    toolbar="工具栏",
    init_api="/amis/api/mock2/page/initData"
)

# 注册页面
register_page("首页", "/index/index", page)

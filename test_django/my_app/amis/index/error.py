


"""{
  "type": "page",
  "title": "标题",
  "remark": "提示 Tip",
  "body": [
    "\n            <p>`initApi` 拉取失败时，页面内容区会显示对应的错误信息。</p>\n\n            <p>其他提示示例</p>\n        ",
    {
      "type": "alert",
      "level": "success",
      "body": "温馨提示：对页面功能的提示说明，绿色为正向类的消息提示"
    },
    {
      "type": "alert",
      "level": "warning",
      "body": "您的私有网络已达到配额，如需更多私有网络，可以通过<a>工单</a>申请"
    }
  ],
  "aside": "边栏",
  "toolbar": "工具栏",
  "initApi": "/amis/api/mock2/page/initDataError"
}"""
from amis_python.builder.page import PageBuilder
from amis_python.registry import register_page

# 创建PageBuilder实例
page = PageBuilder(
    title="初始化出错",
    remark="提示 Tip",
    body=[
        "\n            <p>`initApi` 拉取失败时，页面内容区会显示对应的错误信息。</p>\n\n            <p>其他提示示例</p>\n        ",
        {
            "type": "alert",
            "level": "success",
            "body": "温馨提示：对页面功能的提示说明，绿色为正向类的消息提示"
        },
        {
            "type": "alert",
            "level": "warning",
            "body": "您的私有网络已达到配额，如需更多私有网络，可以通过<a>工单</a>申请"
        }
    ],
    aside="边栏",
    toolbar="工具栏",
    init_api="/amis/api/mock2/page/initDataError"
)

# 注册页面
print(register_page("初始化出错", "/index/error", page))
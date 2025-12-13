from amis_python.builder import Page

# 创建一个简单的 AMIS 页面组件
page = Page(
    title="测试页面",
    body=[
        {
            "type": "text",
            "text": "Hello, AMIS!"
        },
        {
            "type": "button",
            "label": "点击我",
            "onClick": {
                "actions": [
                    {
                        "actionType": "toast",
                        "args": {
                            "msg": "按钮被点击了!",
                            "type": "success"
                        }
                    }
                ]
            }
        }
    ]
)

# 调用 show() 方法，在浏览器中预览组件
page.show()

print("预览页面已在浏览器中打开")
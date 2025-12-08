from amis_python import to_api
from amis_python.builder.action import UrlActionBuilder
from amis_python.builder.event import AmisEvent
from amis_python.builder.page import PageBuilder
from amis_python.builder.form import FormBuilder
from amis_python.builder.input import InputTextBuilder
from amis_python.builder.button import ButtonBuilder


def get_login_page() -> PageBuilder:
    """
    创建登录页面配置
    """
    from .urls import login
    # 创建登录表单
    login_form = FormBuilder(
        api=to_api(login),  # 表单提交到登录API
        title="用户登录",
        body=[
            InputTextBuilder(name="username", label="用户名", required=True, placeholder="请输入用户名"),
            InputTextBuilder(name="password", label="密码", required=True, placeholder="请输入密码")
        ],
        actions=[
            ButtonBuilder(label="登录", action_type="submit", primary=True),
            ButtonBuilder(label="重置", action_type="reset")
        ],
        horizontal=False,  # 垂直布局
        mode="horizontal",
    ).add_action('submitSucc',UrlActionBuilder(url="/amis/", redirect_type="none"))
    
    # 创建登录页面
    login_page = PageBuilder(
        title="登录",
        body=[
            {
                "type": "container",
                "className": "login-container",
                "style": {
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "height": "100%",
                    "backgroundColor": "#f5f5f5"
                },
                "body": [
                    {
                        "type": "panel",
                        "className": "login-panel",
                        "style": {
                            "width": "400px",
                            "padding": "20px",
                            "backgroundColor": "#fff",
                            "borderRadius": "8px",
                            "boxShadow": "0 2px 12px 0 rgba(0, 0, 0, 0.1)"
                        },
                        "body": login_form
                    }
                ]
            }
        ]
    )
    
    return login_page

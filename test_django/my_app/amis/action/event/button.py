
from amis_python import register_page, PageBuilder, TplBuilder, InputTextBuilder, DropdownButtonBuilder, \
    ActionContainerBuilder, ColorBuilder
from amis_python.builder.action import ToastActionBuilder
from amis_python.builder.button import ButtonBuilder
from amis_python.builder.button import ButtonGroupBuilder
from amis_python.builder.button import ButtonGroupSelectBuilder
from amis_python.builder.button import ButtonToolbarBuilder

from amis_python.builder.event import AmisEvent
from amis_python.builder.form import FormBuilder


register_page("按钮类组件事件", "/action/event/button", PageBuilder(
    title="按钮类组件事件",
    regions=["body", "toolbar", "header"],
    body=[
        # 1. 普通按钮
        TplBuilder(
            tpl="1.普通按钮",
            inline=False,
            wrapper_component="h2"
        ),
        ButtonBuilder(label="普通按钮")
            .add_action(
                AmisEvent.click,
                ToastActionBuilder(msg_type="info", msg="派发点击事件")
            )
            .add_action(
                AmisEvent.mouseenter,
                ToastActionBuilder(msg_type="info", msg="派发鼠标移入事件")
            )
            .add_action(
                AmisEvent.mouseleave,
                ToastActionBuilder(msg_type="info", msg="派发鼠标移出事件")
            ),
        
        # 2. 功能按钮
        TplBuilder(
            tpl="2.功能按钮",
            inline=False,
            wrapper_component="h2"
        ),
        FormBuilder(
            debug=True,
            api="/amis/api/mock2/form/saveForm",
            body=[
                InputTextBuilder(name="name", label="名称")
            ],
            actions=[
                ButtonBuilder(label="Submit", action_type="submit")
                    .add_action(
                        AmisEvent.click,
                        ToastActionBuilder(msg_type="info", msg="派发点击事件")
                    ),
                ButtonBuilder(label="Reset", action_type="reset")
                    .add_action(
                        AmisEvent.click,
                        ToastActionBuilder(msg_type="info", msg="派发点击事件")
                    )
            ]
        ),
        
        # 3. 按钮组&按钮工具栏
        TplBuilder(
            tpl="3.按钮组&按钮工具栏",
            inline=False,
            wrapper_component="h2"
        ),
        ButtonToolbarBuilder(
            buttons=[
                ButtonBuilder(label="按钮1")
                    .add_action(
                        AmisEvent.click,
                        ToastActionBuilder(msg_type="info", msg="派发点击事件")
                    ),
                ButtonBuilder(label="按钮2")
                    .add_action(
                        AmisEvent.click,
                        ToastActionBuilder(msg_type="info", msg="派发点击事件")
                    )
            ]
        ),
        ButtonGroupBuilder(
            buttons=[
                ButtonBuilder(label="按钮1")
                    .add_action(
                        AmisEvent.click,
                        ToastActionBuilder(msg_type="info", msg="派发点击事件")
                    ),
                ButtonBuilder(label="按钮2")
                    .add_action(
                        AmisEvent.click,
                        ToastActionBuilder(msg_type="info", msg="派发点击事件")
                    )
            ]
        ),
        
        # 4. 下拉按钮
        TplBuilder(
            tpl="4.下拉按钮",
            inline=False,
            wrapper_component="h2"
        ),
        DropdownButtonBuilder(
            label="下拉按钮",
            buttons=[
                ButtonBuilder(label="按钮1")
                    .add_action(
                        AmisEvent.click,
                        ToastActionBuilder(msg_type="info", msg="派发点击事件")
                    ),
                ButtonBuilder(label="按钮2")
                    .add_action(
                        AmisEvent.click,
                        ToastActionBuilder(msg_type="info", msg="派发点击事件")
                    )
            ]
        ),
        
        # 5. 按钮点选
        TplBuilder(
            tpl="5.按钮点选",
            inline=False,
            wrapper_component="h2"
        ),
        ButtonGroupSelectBuilder(
            name="a",
            options=[
                {"label": "选项1", "value": "a"},
                {"label": "选项2", "value": "b"}
            ]
        ).add_action(
            AmisEvent.change,
            ToastActionBuilder(msg_type="info", msg="派发点选事件")
        ),
        
        # 6. 作为容器
        TplBuilder(
            tpl="6.作为容器",
            inline=False,
            wrapper_component="h2"
        ),
        ActionContainerBuilder(
            body=[
                ColorBuilder(value="#108cee")
            ]
        ).add_action(
            AmisEvent.click,
            ToastActionBuilder(msg_type="info", msg="派发点击事件")
        ).add_action(
            AmisEvent.mouseenter,
            ToastActionBuilder(msg_type="info", msg="派发鼠标移入事件")
        ).add_action(
            AmisEvent.mouseleave,
            ToastActionBuilder(msg_type="info", msg="派发鼠标移出事件")
        )
    ]
))

from amis_python import BaseBuilder
from amis_python.builder.action import ToastActionBuilder
from amis_python.builder.button import ButtonBuilder
from amis_python.builder.event import AmisEvent



def test_button():
    but = ButtonBuilder(label="普通按钮").add_action(
        AmisEvent.click,
        ToastActionBuilder(msg_type="info", msg="派发点击事件")
    ).add_action(
        AmisEvent.mouseenter,
        ToastActionBuilder(msg_type="info", msg="派发鼠标移入事件")
    ).add_action(
        AmisEvent.mouseleave,
        ToastActionBuilder(msg_type="info", msg="派发鼠标移出事件")
    )
    print(but.to_schema())



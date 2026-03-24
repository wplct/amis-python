from unittest import TestCase

from amis_python.crud import build_readonly_form, readonly_dialog_button


class CrudReadonlyTestCase(TestCase):
    def test_build_readonly_form_uses_close_action(self):
        form = build_readonly_form([{"type": "input-text", "name": "name", "label": "名称"}])
        self.assertEqual(form["type"], "form")
        self.assertEqual(form["actions"][0]["label"], "关闭")

    def test_readonly_dialog_button_wraps_form(self):
        action_button = readonly_dialog_button(
            "查看",
            body=[{"type": "input-text", "name": "name", "label": "名称", "disabled": True}],
        )
        self.assertEqual(action_button["dialog"]["body"]["type"], "form")
        self.assertEqual(action_button["dialog"]["title"], "查看数据")

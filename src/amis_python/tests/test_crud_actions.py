from unittest import TestCase

from amis_python.crud import ajax_action, button, dialog_button, download_button, form_dialog_button, reload_action


class CrudActionsTestCase(TestCase):
    def test_reload_action(self):
        action = reload_action("crud")
        self.assertEqual(action["actionType"], "reload")
        self.assertEqual(action["componentId"], "crud")

    def test_button_with_click_actions(self):
        action_button = button("刷新", on_click=[reload_action("crud")], level="primary")
        self.assertEqual(action_button["type"], "button")
        self.assertEqual(action_button["level"], "primary")
        self.assertEqual(action_button["onEvent"]["click"]["actions"][0]["componentId"], "crud")

    def test_dialog_button(self):
        action_button = dialog_button("查看", body={"type": "form", "body": []})
        self.assertEqual(action_button["actionType"], "dialog")
        self.assertEqual(action_button["dialog"]["type"], "dialog")

    def test_ajax_action_with_method(self):
        action = ajax_action("/api/demo/", method="post", confirm_text="确认吗")
        self.assertEqual(action["api"]["url"], "/api/demo/")
        self.assertEqual(action["api"]["method"], "post")
        self.assertEqual(action["confirmText"], "确认吗")

    def test_download_button(self):
        action_button = download_button(
            "导出文件",
            api={"method": "get", "url": "/api/demo/export/"},
            level="primary",
            confirm_text="确定导出吗",
        )
        self.assertEqual(action_button["actionType"], "download")
        self.assertEqual(action_button["api"]["url"], "/api/demo/export/")
        self.assertEqual(action_button["level"], "primary")
        self.assertEqual(action_button["confirmText"], "确定导出吗")

    def test_form_dialog_button(self):
        action_button = form_dialog_button(
            "上传文件",
            api={"method": "post", "url": "/api/demo/upload/"},
            fields=[{"type": "input-file", "name": "file", "label": "文件"}],
            title="上传文件",
            visible_on="${state == 1}",
        )
        self.assertEqual(action_button["label"], "上传文件")
        self.assertEqual(action_button["visibleOn"], "${state == 1}")
        dialog = action_button["onEvent"]["click"]["actions"][0]["dialog"]
        self.assertEqual("上传文件", dialog["title"])
        self.assertEqual("/api/demo/upload/", dialog["body"][0]["api"]["url"])
        self.assertEqual("input-file", dialog["body"][0]["body"][0]["type"])

from unittest import TestCase

from amis_python.builder.action import Action


class ActionTestCase(TestCase):
    """行为按钮组件测试"""
    
    def test_serialize(self):
        """测试序列化"""
        # 基本使用
        action = Action(label="发出一个请求", action_type="ajax", api="/api/mock2/form/saveForm")
        self.assertEqual(action.model_dump(), {
            'type': 'action', 
            'label': '发出一个请求', 
            'actionType': 'ajax',
            'api': '/api/mock2/form/saveForm'
        })
    
    def test_dialog_action(self):
        """测试弹框行为"""
        action = Action(label="弹个框", action_type="dialog", dialog={"title": "弹框", "body": "Hello World!"})
        self.assertEqual(action.model_dump()['actionType'], "dialog")
        self.assertEqual(action.model_dump()['dialog'], {"title": "弹框", "body": "Hello World!"})
    
    def test_confirm_action(self):
        """测试确认行为"""
        action = Action(label="确认操作", action_type="ajax", api="/api/mock2/form/saveForm", confirm_text="确认要发出这个请求？", confirm_title="确认")
        self.assertEqual(action.model_dump()['confirmText'], "确认要发出这个请求？")
        self.assertEqual(action.model_dump()['confirmTitle'], "确认")
    
    def test_copy_action(self):
        """测试复制行为"""
        action = Action(label="复制文本", action_type="copy", content="http://www.baidu.com")
        self.assertEqual(action.model_dump()['actionType'], "copy")
        self.assertEqual(action.model_dump()['content'], "http://www.baidu.com")
    
    def test_reload_action(self):
        """测试刷新行为"""
        action = Action(label="刷新组件", action_type="reload", target="crud")
        self.assertEqual(action.model_dump()['actionType'], "reload")
        self.assertEqual(action.model_dump()['target'], "crud")
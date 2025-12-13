from unittest import TestCase

from amis_python.builder.button import Button


class ButtonTestCase(TestCase):
    """按钮组件测试"""
    
    def test_serialize(self):
        """测试序列化"""
        # 基本使用
        button = Button(label="弹个框", action_type="dialog", dialog={"title": "弹框", "body": "这是个简单的弹框。"})
        self.assertEqual(button.model_dump(), {
            'type': 'button', 
            'label': '弹个框', 
            'actionType': 'dialog',
            'dialog': {"title": "弹框", "body": "这是个简单的弹框。"}
        })
    
    def test_button_level(self):
        """测试按钮样式"""
        button = Button(label="主要按钮", level="primary")
        self.assertEqual(button.model_dump()['level'], "primary")
    
    def test_button_size(self):
        """测试按钮大小"""
        button = Button(label="小按钮", size="sm")
        self.assertEqual(button.model_dump()['size'], "sm")
    
    def test_button_icon(self):
        """测试按钮图标"""
        button = Button(label="带图标按钮", icon="fa fa-plus")
        self.assertEqual(button.model_dump()['icon'], "fa fa-plus")
    
    def test_button_disabled(self):
        """测试禁用按钮"""
        button = Button(label="禁用按钮", disabled=True)
        self.assertEqual(button.model_dump()['disabled'], True)
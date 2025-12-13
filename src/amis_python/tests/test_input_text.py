from unittest import TestCase

from amis_python.builder.form.input_text import InputText


class InputTextTestCase(TestCase):
    """输入框组件测试"""
    
    def test_serialize(self):
        """测试序列化"""
        # 基本使用
        f = InputText(name="text", label="text")
        self.assertEqual(f.model_dump(), {
            'type': 'input-text', 
            'name': 'text', 
            'label': 'text'
        })
    
    def test_clearable(self):
        """测试可清除属性"""
        f = InputText(name="text", label="text", clearable=True)
        self.assertEqual(f.model_dump()['clearable'], True)
    
    def test_multiple(self):
        """测试多选属性"""
        f = InputText(name="text", label="text", multiple=True, options=["APPLE", "ORANGE", "WATERMELON"])
        self.assertEqual(f.model_dump()['multiple'], True)
        self.assertEqual(f.model_dump()['options'], ["APPLE", "ORANGE", "WATERMELON"])
    
    def test_transform(self):
        """测试转换属性"""
        f = InputText(name="text", label="text", transform={"lowerCase": True})
        self.assertEqual(f.model_dump()['transform'], {"lowerCase": True})
    
    def test_border_mode(self):
        """测试边框模式"""
        f = InputText(name="text", label="text", border_mode="none")
        self.assertEqual(f.model_dump()['borderMode'], "none")

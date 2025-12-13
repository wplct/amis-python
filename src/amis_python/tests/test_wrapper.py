from unittest import TestCase

from amis_python.builder.wrapper import Wrapper
from amis_python.builder.form.input_text import InputText


class WrapperTestCase(TestCase):
    """包裹容器组件测试"""
    
    def test_serialize(self):
        """测试序列化"""
        # 基本使用
        f = Wrapper(body="内容", class_name="b")
        self.assertEqual(f.model_dump(), {
            'type': 'wrapper', 
            'body': '内容', 
            'className': 'b'
        })
    
    def test_with_size(self):
        """测试大小属性"""
        f = Wrapper(body="内容", size="lg", class_name="b")
        self.assertEqual(f.model_dump()['size'], "lg")
    
    def test_with_style(self):
        """测试样式属性"""
        # 对象样式
        f1 = Wrapper(body="内容", style={"color": "#aaa"}, class_name="b")
        self.assertEqual(f1.model_dump()['style'], {"color": "#aaa"})
        
        # 字符串样式
        f2 = Wrapper(body="内容", style="color: #aaa;", class_name="b")
        self.assertEqual(f2.model_dump()['style'], "color: #aaa;")
    
    def test_with_component(self):
        """测试包裹组件"""
        input_text = InputText(name="text", label="文本输入")
        f = Wrapper(body=input_text, class_name="b")
        self.assertEqual(f.model_dump()['body'], {
            'type': 'input-text',
            'name': 'text',
            'label': '文本输入'
        })
    
    def test_with_array(self):
        """测试包裹数组"""
        f = Wrapper(
            body=[
                InputText(name="text1", label="文本输入1"),
                InputText(name="text2", label="文本输入2")
            ],
            class_name="b"
        )
        self.assertEqual(len(f.model_dump()['body']), 2)
        self.assertEqual(f.model_dump()['body'][0]['type'], 'input-text')
        self.assertEqual(f.model_dump()['body'][1]['type'], 'input-text')
    
    def test_with_none_size(self):
        """测试无内边距"""
        f = Wrapper(body="内容", size="none", class_name="b")
        self.assertEqual(f.model_dump()['size'], "none")

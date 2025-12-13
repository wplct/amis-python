from unittest import TestCase

from amis_python.builder.form.hidden import Hidden


class HiddenTestCase(TestCase):
    """隐藏字段组件测试"""
    
    def test_serialize(self):
        """测试序列化"""
        # 基本使用
        f = Hidden(name="id", value=1)
        self.assertEqual(f.model_dump(), {
            'type': 'hidden', 
            'name': 'id', 
            'value': 1
        })
    
    def test_string_value(self):
        """测试字符串值"""
        f = Hidden(name="name", value="test")
        self.assertEqual(f.model_dump()['value'], "test")
    
    def test_boolean_value(self):
        """测试布尔值"""
        f = Hidden(name="active", value=True)
        self.assertEqual(f.model_dump()['value'], True)
    
    def test_none_value(self):
        """测试 None 值"""
        f = Hidden(name="empty", value=None)
        self.assertEqual(f.model_dump(), {
            'type': 'hidden', 
            'name': 'empty'
        })
    
    def test_with_label(self):
        """测试带标签（虽然隐藏字段不显示标签）"""
        f = Hidden(name="id", value=1, label="ID")
        self.assertEqual(f.model_dump(), {
            'type': 'hidden', 
            'name': 'id', 
            'value': 1,
            'label': 'ID'
        })

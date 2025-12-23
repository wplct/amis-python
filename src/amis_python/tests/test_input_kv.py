from unittest import TestCase
from amis_python.builder.form import InputKV


class InputKVTestCase(TestCase):
    """InputKV组件测试"""
    
    def test_serialize(self):
        """测试基本序列化"""
        kv = InputKV(name="kv")
        self.assertEqual(kv.model_dump(), {'type': 'input-kv', 'name': 'kv'})
    
    def test_value_type(self):
        """测试valueType属性"""
        kv = InputKV(name="kv", value_type="input-number")
        self.assertEqual(kv.model_dump(), {'type': 'input-kv', 'name': 'kv', 'valueType': 'input-number'})
    
    def test_placeholders(self):
        """测试key和value的占位符"""
        kv = InputKV(
            name="css",
            key_placeholder="属性",
            value_placeholder="值"
        )
        self.assertEqual(kv.model_dump(), {
            'type': 'input-kv',
            'name': 'css',
            'keyPlaceholder': '属性',
            'valuePlaceholder': '值'
        })
    
    def test_draggable(self):
        """测试draggable属性"""
        kv = InputKV(name="css", draggable=False)
        self.assertEqual(kv.model_dump(), {'type': 'input-kv', 'name': 'css', 'draggable': False})
    
    def test_value_schema(self):
        """测试valueSchema属性"""
        kv = InputKV(
            name="css",
            value_schema={
                "type": "select",
                "options": [
                    {"label": "A", "value": "a"},
                    {"label": "B", "value": "b"}
                ]
            }
        )
        self.assertEqual(kv.model_dump(), {
            'type': 'input-kv',
            'name': 'css',
            'valueSchema': {
                "type": "select",
                "options": [
                    {"label": "A", "value": "a"},
                    {"label": "B", "value": "b"}
                ]
            }
        })
    
    def test_key_schema(self):
        """测试keySchema属性"""
        kv = InputKV(
            name="css",
            key_schema={
                "type": "select",
                "options": [
                    {"label": "Width", "value": "width"},
                    {"label": "Height", "value": "height"}
                ]
            }
        )
        self.assertEqual(kv.model_dump(), {
            'type': 'input-kv',
            'name': 'css',
            'keySchema': {
                "type": "select",
                "options": [
                    {"label": "Width", "value": "width"},
                    {"label": "Height", "value": "height"}
                ]
            }
        })

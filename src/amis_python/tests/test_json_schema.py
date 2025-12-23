from unittest import TestCase
from amis_python.builder.form import JSONSchema


class JSONSchemaTestCase(TestCase):
    """JSONSchema组件测试"""
    
    def test_serialize(self):
        """测试基本序列化"""
        js = JSONSchema(
            name="value",
            label="字段值",
            schema={
                "type": "object",
                "properties": {
                    "id": {"type": "number", "title": "ID"},
                    "name": {"type": "string", "title": "名称"}
                }
            }
        )
        self.assertEqual(js.model_dump(), {
            'type': 'json-schema',
            'name': 'value',
            'label': '字段值',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'number', 'title': 'ID'},
                    'name': {'type': 'string', 'title': '名称'}
                }
            }
        })
    
    def test_schema_string(self):
        """测试schema为字符串类型"""
        js = JSONSchema(
            name="value",
            schema="/api/mock2/json-schema"
        )
        self.assertEqual(js.model_dump(), {
            'type': 'json-schema',
            'name': 'value',
            'schema': '/api/mock2/json-schema'
        })
    
    def test_with_formula(self):
        """测试带公式配置"""
        js = JSONSchema(
            name="value",
            schema={"type": "object", "properties": {}},
            formula={
                "mode": "input-group",
                "mixedMode": True,
                "variables": []
            }
        )
        self.assertEqual(js.model_dump(), {
            'type': 'json-schema',
            'name': 'value',
            'schema': {'type': 'object', 'properties': {}},
            'formula': {
                'mode': 'input-group',
                'mixedMode': True,
                'variables': []
            }
        })
    
    def test_minimal_config(self):
        """测试最小配置"""
        js = JSONSchema(name="value")
        self.assertEqual(js.model_dump(), {
            'type': 'json-schema',
            'name': 'value'
        })

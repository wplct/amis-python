from unittest import TestCase
from amis_python.builder.crud import CRUD2, CRUD2Mode, LoadType


class CRUD2TestCase(TestCase):
    """CRUD2组件测试用例"""
    
    def test_serialize_basic(self):
        """测试基本序列化功能"""
        crud2 = CRUD2(
            mode=CRUD2Mode.TABLE2,
            api="/api/users/list",
            primary_field="id"
        )
        result = crud2.model_dump()
        self.assertEqual(result["type"], "crud2")
        self.assertEqual(result["mode"], "table2")
        self.assertEqual(result["api"], "/api/users/list")
        self.assertEqual(result["primaryField"], "id")
    
    def test_serialize_with_columns(self):
        """测试包含列配置的序列化"""
        crud2 = CRUD2(
            mode=CRUD2Mode.TABLE2,
            api="/api/users/list",
            columns=[
                {"name": "id", "label": "ID"},
                {"name": "username", "label": "用户名"}
            ]
        )
        result = crud2.model_dump()
        self.assertEqual(len(result["columns"]), 2)
        self.assertEqual(result["columns"][0]["name"], "id")
        self.assertEqual(result["columns"][1]["label"], "用户名")
    
    def test_serialize_with_filter(self):
        """测试包含筛选配置的序列化"""
        crud2 = CRUD2(
            mode=CRUD2Mode.TABLE2,
            api="/api/users/list",
            filter={
                "type": "form",
                "body": [
                    {"type": "input-text", "name": "username", "label": "用户名"}
                ]
            }
        )
        result = crud2.model_dump()
        self.assertEqual(result["filter"]["type"], "form")
        self.assertEqual(len(result["filter"]["body"]), 1)
    
    def test_serialize_with_toolbar(self):
        """测试包含工具栏配置的序列化"""
        crud2 = CRUD2(
            mode=CRUD2Mode.TABLE2,
            api="/api/users/list",
            header_toolbar=[
                {"type": "button", "label": "新增", "level": "primary"}
            ]
        )
        result = crud2.model_dump()
        self.assertEqual(len(result["headerToolbar"]), 1)
        self.assertEqual(result["headerToolbar"][0]["label"], "新增")
    
    def test_enum_values(self):
        """测试枚举值"""
        self.assertEqual(CRUD2Mode.TABLE2, "table2")
        self.assertEqual(CRUD2Mode.CARDS, "cards")
        self.assertEqual(CRUD2Mode.LIST, "list")
        
        self.assertEqual(LoadType.NONE, "")
        self.assertEqual(LoadType.PAGINATION, "pagination")
        self.assertEqual(LoadType.MORE, "more")

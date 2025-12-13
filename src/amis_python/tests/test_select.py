import unittest
from amis_python.builder.form.select import Select


class SelectTestCase(unittest.TestCase):
    """
    Select 组件测试用例
    """

    def test_serialize(self):
        """
        测试 Select 组件序列化
        """
        # 创建一个基本的 Select 组件
        select = Select(
            name="select",
            label="选择器",
            options=[
                {"label": "选项1", "value": "1"},
                {"label": "选项2", "value": "2"}
            ]
        )

        # 序列化组件
        schema = select.model_dump()

        # 验证序列化结果
        self.assertEqual(schema["type"], "select")
        self.assertEqual(schema["name"], "select")
        self.assertEqual(schema["label"], "选择器")
        self.assertEqual(len(schema["options"]), 2)
        self.assertEqual(schema["options"][0]["label"], "选项1")
        self.assertEqual(schema["options"][0]["value"], "1")

    def test_multiple_select(self):
        """
        测试多选 Select 组件
        """
        select = Select(
            name="multiple_select",
            label="多选选择器",
            options=["选项1", "选项2", "选项3"],
            multiple=True,
            check_all=True,
            max_tag_count=2
        )

        schema = select.model_dump()

        self.assertEqual(schema["multiple"], True)
        self.assertEqual(schema["checkAll"], True)
        self.assertEqual(schema["maxTagCount"], 2)

    def test_with_select_mode(self):
        """
        测试不同选择模式的 Select 组件
        """
        select = Select(
            name="tree_select",
            label="树形选择器",
            select_mode="tree",
            options=[
                {
                    "label": "父节点1",
                    "children": [
                        {"label": "子节点1", "value": "1-1"},
                        {"label": "子节点2", "value": "1-2"}
                    ]
                }
            ]
        )

        schema = select.model_dump()

        self.assertEqual(schema["selectMode"], "tree")
        self.assertIn("children", schema["options"][0])

    def test_with_source(self):
        """
        测试带有动态选项的 Select 组件
        """
        select = Select(
            name="dynamic_select",
            label="动态选择器",
            source="/api/get-options",
            searchable=True
        )

        schema = select.model_dump()

        self.assertEqual(schema["source"], "/api/get-options")
        self.assertEqual(schema["searchable"], True)
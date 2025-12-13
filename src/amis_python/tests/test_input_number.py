import unittest
from amis_python.builder.form.input_number import InputNumber


class InputNumberTestCase(unittest.TestCase):
    """
    InputNumber 组件测试用例
    """

    def test_serialize(self):
        """
        测试 InputNumber 组件序列化
        """
        # 创建一个基本的 InputNumber 组件
        input_number = InputNumber(
            name="number",
            label="数字",
            min=0,
            max=100,
            step=1,
            precision=0
        )

        # 序列化组件
        schema = input_number.model_dump()

        # 验证序列化结果
        self.assertEqual(schema["type"], "input-number")
        self.assertEqual(schema["name"], "number")
        self.assertEqual(schema["label"], "数字")
        self.assertEqual(schema["min"], 0)
        self.assertEqual(schema["max"], 100)
        self.assertEqual(schema["step"], 1)
        self.assertEqual(schema["precision"], 0)

    def test_with_prefix_suffix(self):
        """
        测试带有前缀后缀的 InputNumber 组件
        """
        input_number = InputNumber(
            name="price",
            label="价格",
            prefix="$",
            suffix="元",
            kilobit_separator=True
        )

        schema = input_number.model_dump()

        self.assertEqual(schema["prefix"], "$")
        self.assertEqual(schema["suffix"], "元")
        self.assertEqual(schema["kilobitSeparator"], True)

    def test_with_unit_options(self):
        """
        测试带有单位选项的 InputNumber 组件
        """
        input_number = InputNumber(
            name="size",
            label="尺寸",
            unit_options=["px", "%", "em"]
        )

        schema = input_number.model_dump()

        self.assertEqual(schema["unitOptions"], ["px", "%", "em"])

    def test_advanced_features(self):
        """
        测试 InputNumber 组件的高级特性
        """
        input_number = InputNumber(
            name="big_number",
            label="大数字",
            big=True,
            display_mode="enhance",
            border_mode="half"
        )

        schema = input_number.model_dump()

        self.assertEqual(schema["big"], True)
        self.assertEqual(schema["displayMode"], "enhance")
        self.assertEqual(schema["borderMode"], "half")


if __name__ == "__main__":
    unittest.main()
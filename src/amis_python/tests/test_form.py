from unittest import TestCase

from amis_python.builder.form import Form


class FormTestCase(TestCase):
    """表单组件测试基类"""
    def test_serialize(self):
        f = Form(init_api='api/mock2/page/initData')
        self.assertEqual(f.model_dump(), {'type': 'form', 'initApi': 'api/mock2/page/initData'})

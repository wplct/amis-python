import json
from django.conf import settings
import django
from django.test.utils import setup_test_environment

from amis_python.registry import register_page

# 如果尚未配置 Django 设置
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'amis_python',
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        USE_TZ=True,
        SECRET_KEY='test-secret-key',
    )
    django.setup()
    setup_test_environment()
from django.test import TestCase

from amis_python import PageBuilder,AppBuilder,register_default_app,get_default_app


class TestAppRegister(TestCase):
    # 获取默认app
    def test_get_default_app(self):
        app = get_default_app()
        self.assertEqual(app.to_schema()["brandName"], "amis-python")

    # 使用全局方法注册页面
    def test_register_page(self):
        register_page("测试页面","/test")
        register_page("测试页面","/test/abc")
        register_page("测试页面","/test/abc/abc",PageBuilder(
            title="测试页面",
        ))
        app = get_default_app()
        print(json.dumps(app.to_schema()))
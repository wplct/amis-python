from django.test import TestCase, Client
from django.urls import reverse
from amis_python.builder.app import AppBuilder
from amis_python.builder.page import PageBuilder


class AmisPythonTests(TestCase):
    """测试 amis-python 功能"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.client = Client()
        
    def test_amis_app_config(self):
        """测试 amis 应用配置生成"""
        # 创建 amis 应用实例
        amis_app = AppBuilder(brand_name="Test System")
        
        # 创建页面
        home_page = PageBuilder(title="Home Page", body=[{"type": "button", "label": "Click Me"}])
        
        # 注册页面
        amis_app.register_page("/home", home_page, label="Home")
        
        # 生成配置
        config = amis_app.to_schema()
        
        # 验证配置
        self.assertEqual(config["type"], "app")
        self.assertEqual(config["brandName"], "Test System")
        self.assertEqual(len(config["pages"]), 1)
        self.assertEqual(config["pages"][0]["type"], "app-page")
        self.assertEqual(config["pages"][0]["label"], "home")
    
    def test_page_registration(self):
        """测试页面注册和获取功能"""
        # 创建 amis 应用实例
        amis_app = AppBuilder(brand_name="Test System")
        
        # 创建页面
        home_page = PageBuilder(title="Home Page", body=[{"type": "button", "label": "Click Me"}])
        user_list_page = PageBuilder(title="User List", body=[{"type": "table", "api": "/api/users"}])
        
        # 注册页面
        amis_app.register_page("/home", home_page, label="Home")
        amis_app.register_page("/users/list", user_list_page, label="User List")
        
        # 获取页面
        retrieved_home_page = amis_app.get_page("/home")
        retrieved_user_list_page = amis_app.get_page("/users/list")
        non_existent_page = amis_app.get_page("/non-existent")
        
        # 验证页面获取
        self.assertIsNotNone(retrieved_home_page)
        self.assertEqual(retrieved_home_page.title, "Home Page")
        self.assertIsNotNone(retrieved_user_list_page)
        self.assertEqual(retrieved_user_list_page.title, "User List")
        self.assertIsNone(non_existent_page)
    
    def test_ninja_integration(self):
        """测试与 Django Ninja 的集成"""
        # 测试 amis 配置端点
        response = self.client.get("/api/amis/config")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["type"], "app")
        
        # 测试用户列表端点
        response = self.client.get("/api/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 0)

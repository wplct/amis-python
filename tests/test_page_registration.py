import unittest
from amis_python.builder.app import AppBuilder, AppPageBuilder, AppPageGroupBuilder, parse_path, generate_path
from amis_python.builder.page import PageBuilder


class TestPageRegistration(unittest.TestCase):
    """Test suite for page registration mechanism"""

    def test_parse_path(self):
        """Test parse_path function"""
        # 测试空路径
        self.assertEqual(parse_path(""), [])
        self.assertEqual(parse_path("/"), [])
        
        # 测试简单路径
        self.assertEqual(parse_path("/home"), ["home"])
        self.assertEqual(parse_path("home"), ["home"])
        
        # 测试嵌套路径
        self.assertEqual(parse_path("/users/list"), ["users", "list"])
        self.assertEqual(parse_path("users/list"), ["users", "list"])
        
        # 测试多个斜杠
        self.assertEqual(parse_path("//users//list//"), ["users", "list"])

    def test_generate_path(self):
        """Test generate_path function"""
        # 测试空路径段
        self.assertEqual(generate_path([]), "/")
        
        # 测试单个路径段
        self.assertEqual(generate_path(["home"]), "/home")
        
        # 测试多个路径段
        self.assertEqual(generate_path(["users", "list"]), "/users/list")

    def test_app_builder_register_page(self):
        """Test AppBuilder register_page method"""
        app = AppBuilder(brand_name="Test App")
        page = PageBuilder(title="Home Page", body=[{"type": "button", "label": "Click Me"}])
        
        # 注册页面
        app.register_page("/home", page, label="首页")
        
        # 验证页面已注册
        self.assertEqual(len(app.pages), 1)
        self.assertIsInstance(app.pages[0], AppPageBuilder)
        self.assertEqual(app.pages[0].label, "home")
        self.assertEqual(len(app.pages[0].children), 1)
        self.assertIsInstance(app.pages[0].children[0], PageBuilder)

    def test_app_builder_register_page_group(self):
        """Test AppBuilder register_page_group method"""
        app = AppBuilder(brand_name="Test App")
        
        # 注册页面分组
        group = app.register_page_group("/users", label="用户管理")
        
        # 验证分组已注册
        self.assertEqual(len(app.pages), 1)
        self.assertIsInstance(app.pages[0], AppPageGroupBuilder)
        self.assertEqual(app.pages[0].label, "users")
        self.assertIsInstance(group, AppPageGroupBuilder)

    def test_app_builder_get_page(self):
        """Test AppBuilder get_page method"""
        app = AppBuilder(brand_name="Test App")
        page = PageBuilder(title="Home Page", body=[{"type": "button", "label": "Click Me"}])
        
        # 注册页面
        app.register_page("/home", page, label="首页")
        
        # 获取页面
        retrieved_page = app.get_page("/home")
        
        # 验证页面获取成功
        self.assertIsNotNone(retrieved_page)
        self.assertIsInstance(retrieved_page, PageBuilder)
        self.assertEqual(retrieved_page.title, "Home Page")
        
        # 测试获取不存在的页面
        non_existent_page = app.get_page("/non-existent")
        self.assertIsNone(non_existent_page)

    def test_app_page_group_register_page(self):
        """Test AppPageGroupBuilder register_page method"""
        app = AppBuilder(brand_name="Test App")
        group = app.register_page_group("/users", label="用户管理")
        page = PageBuilder(title="User List", body=[{"type": "table", "api": "/api/users"}])
        
        # 在分组内注册页面
        group.register_page("/list", page, label="用户列表")
        
        # 验证页面已注册
        self.assertEqual(len(group.children), 1)
        self.assertIsInstance(group.children[0], AppPageBuilder)
        self.assertEqual(group.children[0].label, "list")
        self.assertEqual(len(group.children[0].children), 1)
        self.assertIsInstance(group.children[0].children[0], PageBuilder)

    def test_app_page_group_register_subgroup(self):
        """Test AppPageGroupBuilder register_subgroup method"""
        app = AppBuilder(brand_name="Test App")
        group = app.register_page_group("/admin", label="管理中心")
        
        # 注册子分组
        subgroup = group.register_subgroup("/users", label="用户管理")
        
        # 验证子分组已注册
        self.assertEqual(len(group.children), 1)
        self.assertIsInstance(group.children[0], AppPageGroupBuilder)
        self.assertEqual(group.children[0].label, "users")
        self.assertIsInstance(subgroup, AppPageGroupBuilder)

    def test_app_page_group_get_page(self):
        """Test AppPageGroupBuilder get_page method"""
        app = AppBuilder(brand_name="Test App")
        group = app.register_page_group("/users", label="用户管理")
        page = PageBuilder(title="User List", body=[{"type": "table", "api": "/api/users"}])
        
        # 注册页面
        group.register_page("/list", page, label="用户列表")
        
        # 获取页面
        retrieved_page = group.get_page("/list")
        
        # 验证页面获取成功
        self.assertIsNotNone(retrieved_page)
        self.assertIsInstance(retrieved_page, PageBuilder)
        self.assertEqual(retrieved_page.title, "User List")

    def test_app_page_builder_register_page(self):
        """Test AppPageBuilder register_page method"""
        app = AppBuilder(brand_name="Test App")
        parent_page = PageBuilder(title="Parent Page", body=[{"type": "button", "label": "Parent"}])
        
        # 注册父页面
        app_page = app.register_page("/parent", parent_page, label="父页面")
        
        # 注册子页面
        child_page = PageBuilder(title="Child Page", body=[{"type": "button", "label": "Child"}])
        app_page.register_page("/child", child_page, label="子页面")
        
        # 验证子页面已注册
        self.assertEqual(len(app_page.children), 2)  # 父页面本身和子页面
        self.assertIsInstance(app_page.children[1], AppPageBuilder)
        self.assertEqual(app_page.children[1].label, "child")
        self.assertEqual(len(app_page.children[1].children), 1)
        self.assertIsInstance(app_page.children[1].children[0], PageBuilder)

    def test_nested_page_registration(self):
        """Test nested page registration"""
        app = AppBuilder(brand_name="Test App")
        
        # 注册嵌套页面
        page1 = PageBuilder(title="Page 1", body=[{"type": "button", "label": "Page 1"}])
        page2 = PageBuilder(title="Page 2", body=[{"type": "button", "label": "Page 2"}])
        page3 = PageBuilder(title="Page 3", body=[{"type": "button", "label": "Page 3"}])
        
        app.register_page("/level1/level2/level3", page1, label="Page 1")
        app.register_page("/level1/level2/level3/page2", page2, label="Page 2")
        app.register_page("/level1/level2/level3/page3", page3, label="Page 3")
        
        # 验证页面已注册
        self.assertEqual(len(app.pages), 1)
        self.assertEqual(app.pages[0].label, "level1")
        self.assertEqual(len(app.pages[0].children), 1)
        self.assertEqual(app.pages[0].children[0].label, "level2")
        self.assertEqual(len(app.pages[0].children[0].children), 1)
        self.assertEqual(app.pages[0].children[0].children[0].label, "level3")
        self.assertEqual(len(app.pages[0].children[0].children[0].children), 3)  # 包括 page1、page2 和 page3


if __name__ == '__main__':
    unittest.main()
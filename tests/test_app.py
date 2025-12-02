import unittest
import json
from typing import List
from amis_python.builder.app import AppBuilder, AppPageBuilder, AppPageGroupBuilder
from amis_python.builder.base import BaseBuilder
from amis_python.builder.page import PageBuilder


class TestAppBuilders(unittest.TestCase):
    """Test suite for AppBuilder classes"""

    def test_app_page_builder_initialization(self):
        """Test AppPageBuilder initialization"""
        builder = AppPageBuilder(url="/test")
        
        self.assertEqual(builder.type, "page")
        self.assertIsNone(builder.label)
        self.assertIsNone(builder.schema)

    def test_app_page_builder_with_params(self):
        """Test AppPageBuilder initialization with parameters"""
        label = "Test Page"
        page = PageBuilder(title="Test Page Content")
        builder = AppPageBuilder(label=label, url="/test", schema=page)
        
        self.assertEqual(builder.label, label)
        self.assertIsInstance(builder.schema, PageBuilder)

    def test_app_page_group_builder_initialization(self):
        """Test AppPageGroupBuilder initialization"""
        builder = AppPageGroupBuilder()
        
        self.assertEqual(builder.type, "group")
        self.assertIsNone(builder.label)
        self.assertEqual(builder.children, [])

    def test_app_page_group_builder_with_params(self):
        """Test AppPageGroupBuilder initialization with parameters"""
        label = "Test Group"
        page_builder = AppPageBuilder(url="/test")
        children = [page_builder]
        builder = AppPageGroupBuilder(label=label, children=children)
        
        self.assertEqual(builder.label, label)
        self.assertEqual(len(builder.children), 1)
        self.assertIsInstance(builder.children[0], AppPageBuilder)

    def test_app_builder_initialization(self):
        """Test AppBuilder initialization"""
        pages = [AppPageGroupBuilder(label="Test Group")]
        builder = AppBuilder(pages=pages)
        
        self.assertEqual(builder.type, "app")
        self.assertEqual(builder.brand_name, "amis-python")
        self.assertIsNone(builder.api)
        self.assertIsNone(builder.logo)
        self.assertIsNone(builder.class_name)
        self.assertIsNone(builder.header)
        self.assertIsNone(builder.aside_before)
        self.assertIsNone(builder.aside_after)
        self.assertIsNone(builder.footer)
        self.assertEqual(len(builder.pages), 1)
        self.assertIsInstance(builder.pages[0], AppPageGroupBuilder)
        self.assertEqual(builder.pages[0].label, "Test Group")

    def test_app_builder_with_params(self):
        """Test AppBuilder initialization with parameters"""
        api = "/api/mock"
        brand_name = "My App"
        logo = "logo.png"
        class_name = "my-app"
        header = "Header"
        aside_before = "Aside Before"
        aside_after = "Aside After"
        footer = "Footer"
        pages = [AppPageGroupBuilder(label="Test Group")]
        
        builder = AppBuilder(
            api=api,
            brand_name=brand_name,
            logo=logo,
            class_name=class_name,
            header=header,
            aside_before=aside_before,
            aside_after=aside_after,
            footer=footer,
            pages=pages
        )
        
        self.assertEqual(builder.api, api)
        self.assertEqual(builder.brand_name, brand_name)
        self.assertEqual(builder.logo, logo)
        self.assertEqual(builder.class_name, class_name)
        self.assertEqual(builder.header, header)
        self.assertEqual(builder.aside_before, aside_before)
        self.assertEqual(builder.aside_after, aside_after)
        self.assertEqual(builder.footer, footer)
        self.assertEqual(len(builder.pages), 1)
        self.assertEqual(builder.pages[0].label, "Test Group")

    def test_app_page_builder_to_schema(self):
        """Test AppPageBuilder to_schema method"""
        label = "Test Page"
        builder = AppPageBuilder(label=label, url="/test")
        schema = builder.to_schema()
        
        expected_schema = {
            "type": "page",
            "label": label,
            "url": "/test"
        }
        
        self.assertEqual(schema, expected_schema)

    def test_app_page_group_builder_to_schema(self):
        """Test AppPageGroupBuilder to_schema method"""
        label = "Test Group"
        builder = AppPageGroupBuilder(label=label)
        schema = builder.to_schema()
        
        expected_schema = {
            "type": "group",
            "label": label,
            "children": []
        }
        
        self.assertEqual(schema, expected_schema)

    def test_app_builder_to_schema(self):
        """Test AppBuilder to_schema method"""
        pages = [AppPageGroupBuilder(label="Test Group")]
        builder = AppBuilder(pages=pages)
        schema = builder.to_schema()
        
        # 只检查关键字段，忽略默认值字段
        self.assertEqual(schema["type"], "app")
        self.assertEqual(schema["brandName"], "amis-python")
        self.assertEqual(len(schema["pages"]), 1)
        self.assertEqual(schema["pages"][0]["type"], "group")
        self.assertEqual(schema["pages"][0]["label"], "Test Group")
        self.assertEqual(schema["pages"][0]["children"], [])

    def test_app_builder_to_schema_with_params(self):
        """Test AppBuilder to_schema method with parameters"""
        api = "/api/mock"
        brand_name = "My App"
        pages = [AppPageGroupBuilder(label="Test Group")]
        
        builder = AppBuilder(api=api, brand_name=brand_name, pages=pages)
        schema = builder.to_schema()
        
        # 只检查关键字段，忽略默认值字段
        self.assertEqual(schema["type"], "app")
        self.assertEqual(schema["api"], api)
        self.assertEqual(schema["brandName"], brand_name)
        self.assertEqual(len(schema["pages"]), 1)
        self.assertEqual(schema["pages"][0]["type"], "group")
        self.assertEqual(schema["pages"][0]["label"], "Test Group")
        self.assertEqual(schema["pages"][0]["children"], [])

    def test_nested_children_to_schema(self):
        """Test nested children conversion to schema"""
        # 创建页面
        page = PageBuilder(title="Child Page Content")
        
        # 创建分组和页面
        group = AppPageGroupBuilder(label="Group")
        child_page = AppPageBuilder(label="Child Page", url="/child", schema=page)
        group.children.append(child_page)
        
        # 创建应用
        builder = AppBuilder(pages=[group])
        schema = builder.to_schema()

        expected_pages = [{
            "type": "group",
            "label": "Group",
            "children": [{
                "type": "page",
                "label": "Child Page",
                "url": "/child"
            }]
        }]
        self.assertEqual(schema["pages"], expected_pages)
    
    def test_register_page_with_group(self):
        """Test register_page method with group"""
        # 创建应用
        app = AppBuilder()
        
        # 创建分组
        group = app.register_page_group(label="Test Group")
        
        # 创建页面
        page = PageBuilder(title="Test Page")
        
        # 使用分组实例注册页面
        app_page = app.register_page(path="/test", page=page, group=group, label="Test Page")
        
        # 验证页面是否成功注册
        self.assertIsInstance(app_page, AppPageBuilder)
        self.assertEqual(app_page.label, "Test Page")
        self.assertEqual(app_page.url, "/test")
        self.assertEqual(len(group.children), 1)
        self.assertEqual(group.children[0], app_page)
    
    def test_register_page_with_group_name(self):
        """Test register_page method with group name"""
        # 创建应用
        app = AppBuilder()
        
        # 创建分组
        app.register_page_group(label="Test Group")
        
        # 创建页面
        page = PageBuilder(title="Test Page")
        
        # 使用分组名称注册页面
        app_page = app.register_page(path="/test", page=page, group="Test Group", label="Test Page")
        
        # 验证页面是否成功注册
        self.assertIsInstance(app_page, AppPageBuilder)
        self.assertEqual(app_page.label, "Test Page")
        self.assertEqual(app_page.url, "/test")
    
    def test_register_page_with_nonexistent_group(self):
        """Test register_page method with nonexistent group"""
        # 创建应用
        app = AppBuilder()
        
        # 创建页面
        page = PageBuilder(title="Test Page")
        
        # 尝试使用不存在的分组注册页面，应该抛出错误
        with self.assertRaises(ValueError) as context:
            app.register_page(path="/test", page=page, group="Nonexistent Group", label="Test Page")
        
        # 验证错误信息
        self.assertIn("Group 'Nonexistent Group' not found", str(context.exception))
    
    def test_register_duplicate_group(self):
        """Test registering duplicate group"""
        # 创建应用
        app = AppBuilder()
        
        # 创建分组
        app.register_page_group(label="Test Group")
        
        # 尝试创建同名分组，应该抛出错误
        with self.assertRaises(ValueError) as context:
            app.register_page_group(label="Test Group")
        
        # 验证错误信息
        self.assertIn("Group 'Test Group' already exists", str(context.exception))


if __name__ == '__main__':
    unittest.main()
import unittest
import json
from typing import List
from amis_python.builder.app import AppBuilder, AppPageBuilder, AppPageGroupBuilder
from amis_python.builder.base import BaseBuilder


class TestAppBuilders(unittest.TestCase):
    """Test suite for AppBuilder classes"""

    def test_app_page_builder_initialization(self):
        """Test AppPageBuilder initialization"""
        builder = AppPageBuilder()
        
        self.assertEqual(builder.type, "app-page")
        self.assertIsNone(builder.label)
        self.assertEqual(builder.children, [])

    def test_app_page_builder_with_params(self):
        """Test AppPageBuilder initialization with parameters"""
        label = "Test Page"
        children = [AppPageBuilder()]
        builder = AppPageBuilder(label=label, children=children)
        
        self.assertEqual(builder.label, label)
        self.assertEqual(len(builder.children), 1)
        self.assertIsInstance(builder.children[0], AppPageBuilder)

    def test_app_page_group_builder_initialization(self):
        """Test AppPageGroupBuilder initialization"""
        builder = AppPageGroupBuilder()
        
        self.assertEqual(builder.type, "app-group")
        self.assertIsNone(builder.label)
        self.assertEqual(builder.children, [])

    def test_app_page_group_builder_with_params(self):
        """Test AppPageGroupBuilder initialization with parameters"""
        label = "Test Group"
        children = [AppPageBuilder()]
        builder = AppPageGroupBuilder(label=label, children=children)
        
        self.assertEqual(builder.label, label)
        self.assertEqual(len(builder.children), 1)
        self.assertIsInstance(builder.children[0], AppPageBuilder)

    def test_app_builder_initialization(self):
        """Test AppBuilder initialization"""
        pages = [AppPageGroupBuilder()]
        builder = AppBuilder(pages=pages)
        
        self.assertEqual(builder.type, "app")
        self.assertEqual(builder.brandName, "amis-python")
        self.assertIsNone(builder.api)
        self.assertIsNone(builder.logo)
        self.assertIsNone(builder.className)
        self.assertIsNone(builder.header)
        self.assertIsNone(builder.asideBefore)
        self.assertIsNone(builder.asideAfter)
        self.assertIsNone(builder.footer)
        self.assertEqual(len(builder.pages), 1)
        self.assertIsInstance(builder.pages[0], AppPageGroupBuilder)

    def test_app_builder_with_params(self):
        """Test AppBuilder initialization with parameters"""
        api = "/api/mock"
        brandName = "My App"
        logo = "logo.png"
        className = "my-app"
        header = "Header"
        asideBefore = "Aside Before"
        asideAfter = "Aside After"
        footer = "Footer"
        pages = [AppPageGroupBuilder()]
        
        builder = AppBuilder(
            api=api,
            brandName=brandName,
            logo=logo,
            className=className,
            header=header,
            asideBefore=asideBefore,
            asideAfter=asideAfter,
            footer=footer,
            pages=pages
        )
        
        self.assertEqual(builder.api, api)
        self.assertEqual(builder.brandName, brandName)
        self.assertEqual(builder.logo, logo)
        self.assertEqual(builder.className, className)
        self.assertEqual(builder.header, header)
        self.assertEqual(builder.asideBefore, asideBefore)
        self.assertEqual(builder.asideAfter, asideAfter)
        self.assertEqual(builder.footer, footer)
        self.assertEqual(len(builder.pages), 1)

    def test_app_page_builder_to_schema(self):
        """Test AppPageBuilder to_schema method"""
        label = "Test Page"
        builder = AppPageBuilder(label=label)
        schema = builder.to_schema()
        
        expected_schema = {
            "type": "app-page",
            "label": label,
            "children": []
        }
        
        self.assertEqual(schema, expected_schema)

    def test_app_page_group_builder_to_schema(self):
        """Test AppPageGroupBuilder to_schema method"""
        label = "Test Group"
        builder = AppPageGroupBuilder(label=label)
        schema = builder.to_schema()
        
        expected_schema = {
            "type": "app-group",
            "label": label,
            "children": []
        }
        
        self.assertEqual(schema, expected_schema)

    def test_app_builder_to_schema(self):
        """Test AppBuilder to_schema method"""
        pages = [AppPageGroupBuilder()]
        builder = AppBuilder(pages=pages)
        schema = builder.to_schema()
        
        expected_schema = {
            "type": "app",
            "brandName": "amis-python",
            "pages": [{
                "type": "app-group",
                "children": []
            }]
        }
        
        self.assertEqual(schema, expected_schema)

    def test_app_builder_to_schema_with_params(self):
        """Test AppBuilder to_schema method with parameters"""
        api = "/api/mock"
        brandName = "My App"
        pages = [AppPageGroupBuilder()]
        
        builder = AppBuilder(api=api, brandName=brandName, pages=pages)
        schema = builder.to_schema()
        
        expected_schema = {
            "type": "app",
            "api": api,
            "brandName": brandName,
            "pages": [{
                "type": "app-group",
                "children": []
            }]
        }
        
        self.assertEqual(schema, expected_schema)

    def test_nested_children_to_schema(self):
        """Test nested children conversion to schema"""
        child_page = AppPageBuilder(label="Child Page")
        group = AppPageGroupBuilder(label="Group", children=[child_page])
        builder = AppBuilder(pages=[group])
        schema = builder.to_schema()

        # print( schema)
        expected_pages = [{
            "type": "app-group",
            "label": "Group",
            "children": [{
                "type": "app-page",
                "label": "Child Page",
                "children": []
            }]
        }]
        self.assertEqual(schema["pages"], expected_pages)


if __name__ == '__main__':
    unittest.main()
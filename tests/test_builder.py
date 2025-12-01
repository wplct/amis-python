import json
import unittest
from amis_python.builder import PageBuilder


class TestPageBuilder(unittest.TestCase):
    
    def test_page_builder_initialization(self):
        """Test PageBuilder initialization with title"""
        title = "Test Page"
        builder = PageBuilder(title=title)
        
        self.assertEqual(builder.title, title)
        self.assertEqual(builder.body, [])

    def test_page_builder_with_body(self):
        """Test PageBuilder initialization with title and body"""
        title = "Test Page"
        body = [{"type": "button", "label": "Click me"}]
        builder = PageBuilder(title=title, body=body)
        
        self.assertEqual(builder.title, title)
        self.assertEqual(builder.body, body)

    def test_page_builder_to_schema(self):
        """Test PageBuilder to_schema method"""
        title = "Test Page"
        builder = PageBuilder(title=title)
        schema = builder.to_schema()
        expected_schema = {
            "type": "page",
            "title": title,
            "body": []
        }
        print(json.dumps(schema))
        self.assertEqual(schema, expected_schema)


if __name__ == '__main__':
    unittest.main()
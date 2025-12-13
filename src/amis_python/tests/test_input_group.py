from unittest import TestCase
from amis_python.builder.form import InputGroup


class InputGroupTestCase(TestCase):
    """InputGroup component test cases"""
    
    def test_serialize_basic(self):
        """Test basic serialization"""
        input_group = InputGroup(
            name="input-group",
            label="input group"
        )
        result = input_group.model_dump(exclude_none=True)
        self.assertEqual(result, {
            "type": "input-group",
            "name": "input-group",
            "label": "input group"
        })
    
    def test_serialize_with_body(self):
        """Test serialization with body"""
        input_group = InputGroup(
            name="input-group",
            label="input group",
            body=[
                {
                    "type": "input-text",
                    "placeholder": "Search ID/Name",
                    "name": "input-group"
                },
                {
                    "type": "submit",
                    "label": "Search",
                    "level": "primary"
                }
            ]
        )
        result = input_group.model_dump(exclude_none=True)
        self.assertEqual(result, {
            "type": "input-group",
            "name": "input-group",
            "label": "input group",
            "body": [
                {
                    "type": "input-text",
                    "placeholder": "Search ID/Name",
                    "name": "input-group"
                },
                {
                    "type": "submit",
                    "label": "Search",
                    "level": "primary"
                }
            ]
        })
    
    def test_serialize_with_validation_config(self):
        """Test serialization with validation config"""
        input_group = InputGroup(
            name="input-group",
            label="input group validation",
            validation_config={
                "errorMode": "partial",
                "delimiter": ";"
            }
        )
        result = input_group.model_dump(exclude_none=True)
        self.assertEqual(result, {
            "type": "input-group",
            "name": "input-group",
            "label": "input group validation",
            "validationConfig": {
                "errorMode": "partial",
                "delimiter": ";"
            }
        })
    
    def test_serialize_with_class_name(self):
        """Test serialization with class name"""
        input_group = InputGroup(
            name="input-group",
            label="input group",
            class_name="custom-class"
        )
        result = input_group.model_dump(exclude_none=True)
        self.assertEqual(result, {
            "type": "input-group",
            "name": "input-group",
            "label": "input group",
            "className": "custom-class"
        })
    
    def test_serialize_all_properties(self):
        """Test serialization with all properties"""
        input_group = InputGroup(
            name="input-group",
            label="input group",
            body=[
                {
                    "type": "input-text",
                    "name": "group-input1"
                },
                {
                    "type": "select",
                    "name": "group-select1",
                    "options": [
                        {"label": "Option 1", "value": "1"},
                        {"label": "Option 2", "value": "2"}
                    ]
                }
            ],
            validation_config={
                "errorMode": "full",
                "delimiter": "; "
            },
            class_name="custom-class",
            disabled=True,
            required=True
        )
        result = input_group.model_dump(exclude_none=True)
        self.assertEqual(result, {
            "type": "input-group",
            "name": "input-group",
            "label": "input group",
            "body": [
                {
                    "type": "input-text",
                    "name": "group-input1"
                },
                {
                    "type": "select",
                    "name": "group-select1",
                    "options": [
                        {"label": "Option 1", "value": "1"},
                        {"label": "Option 2", "value": "2"}
                    ]
                }
            ],
            "validationConfig": {
                "errorMode": "full",
                "delimiter": "; "
            },
            "className": "custom-class",
            "disabled": True,
            "required": True
        })

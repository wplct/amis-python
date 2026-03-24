from unittest import TestCase

from rest_framework import serializers

from amis_python.crud import normalize_scene_field, render_field_schema


class _FakeCrud:
    def get_label(self, field, field_name):
        return field.label or field_name

    def _get_field_input_placeholder(self, field, field_name):
        return "请输入" + self.get_label(field, field_name)


class _HookField(serializers.CharField):
    def get_form_item(self, crud, field, field_name, _filter=False):
        return [{"type": "custom-hook", "name": field_name, "filter": _filter}]


class CrudRenderersTestCase(TestCase):
    def setUp(self):
        self.crud = _FakeCrud()

    def test_normalize_list_serializer_uses_child(self):
        serializer = serializers.ListSerializer(child=serializers.CharField(label="名称"))
        field = normalize_scene_field(serializer)
        self.assertIsInstance(field, serializers.CharField)

    def test_hook_has_priority(self):
        field = _HookField(label="名称")
        result = render_field_schema(self.crud, "form", field, "name", base_options={})
        self.assertEqual(result[0]["type"], "custom-hook")

    def test_boolean_filter_renderer(self):
        field = serializers.BooleanField(label="启用")
        result = render_field_schema(self.crud, "filter", field, "enabled")
        self.assertEqual(result["type"], "select")
        self.assertEqual(len(result["options"]), 2)

    def test_choice_column_renderer(self):
        field = serializers.ChoiceField(label="状态", choices={"a": "启用", "b": "禁用"})
        result = render_field_schema(self.crud, "column", field, "status")
        self.assertEqual(result["type"], "select")
        self.assertTrue(result["static"])

    def test_datetime_column_renderer(self):
        field = serializers.DateTimeField(label="创建时间")
        result = render_field_schema(self.crud, "column", field, "created_at")
        self.assertEqual(result["type"], "datetime")

from unittest import TestCase

from rest_framework import serializers

from amis_python.crud import (
    build_serializer_context,
    create_dialog_button,
    delete_button,
    serializer_columns,
    serializer_form_body,
    view_dialog_button,
)


class _Serializer(serializers.Serializer):
    name = serializers.CharField(label="名称")
    created_at = serializers.DateTimeField(label="创建时间", read_only=True)

    class Meta:
        fields = ["name", "created_at"]
        show_fields = ["name", "created_at"]


class _ViewSet:
    serializer_class = _Serializer


class CrudSerializerHelpersTestCase(TestCase):
    def test_serializer_columns_and_form_body(self):
        context = build_serializer_context(title="测试", name="demo", view_set=_ViewSet)
        columns = serializer_columns(context)
        create_body = serializer_form_body(context, create=True)
        readonly_body = serializer_form_body(context, readonly=True)

        self.assertEqual(["name", "created_at"], [item["name"] for item in columns])
        self.assertEqual(["name"], [item["name"] for item in create_body])
        self.assertTrue(all(item["disabled"] for item in readonly_body))

    def test_standard_buttons(self):
        form = {"type": "form", "body": []}
        create_btn = create_dialog_button(form=form)
        view_btn = view_dialog_button(form=form)
        delete_btn_cfg = delete_button(detail_api="/api/amis/demo/${object_id}/", crud_id="demo_crud")

        self.assertEqual("新增", create_btn["label"])
        self.assertEqual("查看", view_btn["label"])
        self.assertEqual("删除", delete_btn_cfg["label"])
        self.assertEqual("demo_crud", delete_btn_cfg["onEvent"]["click"]["actions"][1]["componentId"])

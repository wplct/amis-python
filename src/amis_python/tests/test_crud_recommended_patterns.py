from unittest import TestCase

from rest_framework import serializers

from amis_python.crud import (
    build_action_column,
    build_crud_page,
    build_filter_form,
    build_serializer_context,
    build_submit_form,
    create_dialog_button,
    delete_button,
    register_field_renderer,
    serializer_columns,
    serializer_filter_body,
    serializer_form_body,
    view_dialog_button,
)


class _MissionSerializer(serializers.Serializer):
    title = serializers.CharField(label="任务标题")
    status = serializers.ChoiceField(label="状态", choices=((1, "启用"), (0, "停用")))
    created_at = serializers.DateTimeField(label="创建时间", read_only=True)

    class Meta:
        fields = ["title", "status", "created_at"]
        show_fields = ["title", "status", "created_at"]


class _MissionViewSet:
    serializer_class = _MissionSerializer
    filterset_fields = ["title", "created_at__date_range"]


class _MoneyField(serializers.IntegerField):
    pass


def _money_renderer(scene, crud, field, field_name, context):
    if scene == "form":
        return [
            {
                "type": "input-number",
                "name": f"{field_name}_display",
                "label": crud.get_label(field, field_name),
                "precision": 2,
            },
            {
                "type": "formula",
                "name": field_name,
                "formula": f"{field_name}_display != null ? Math.round({field_name}_display * 100) : null",
                "initSet": True,
                "autoSet": True,
            },
        ]
    if scene == "column":
        return {
            "type": "tpl",
            "title": crud.get_label(field, field_name),
            "name": field_name,
            "placeholder": "-",
            "tpl": "${" + field_name + " / 100}元",
        }
    return None


class CrudRecommendedPatternsTestCase(TestCase):
    def test_explicit_page_composition_pattern(self):
        context = build_serializer_context(
            title="任务管理",
            name="mission",
            view_set=_MissionViewSet,
            crud_id="mission_crud",
        )

        create_form = build_submit_form(
            serializer_form_body(context, create=True),
            api=context.get_base_api(),
            reload_component_id=context.crud_id,
            dsType="api",
            feat="Insert",
            resetAfterSubmit=True,
        )
        detail_form = build_submit_form(
            serializer_form_body(context),
            api=f"put:{context.get_detail_api()}",
            reload_component_id=context.crud_id,
            dsType="api",
            feat="Insert",
            resetAfterSubmit=True,
        )

        page = build_crud_page(
            title=context.title,
            api={"url": context.get_base_api(), "method": "get"},
            columns=[
                *serializer_columns(context),
                build_action_column(
                    [
                        view_dialog_button(form=detail_form),
                        delete_button(detail_api=context.get_detail_api(), crud_id=context.crud_id),
                    ]
                ),
            ],
            filter_schema=build_filter_form(
                serializer_filter_body(context, context.view_set.filterset_fields)
            ),
            header_toolbar=[
                {
                    "type": "container",
                    "body": [create_dialog_button(form=create_form)],
                }
            ],
            crud_id=context.crud_id,
        )

        crud_schema = page["body"][0]
        self.assertEqual("mission_crud", crud_schema["id"])
        self.assertEqual(["新增"], [button["label"] for button in crud_schema["headerToolbar"][0]["body"]])
        self.assertEqual(["title", "status", "created_at", None], [item.get("name") for item in crud_schema["columns"]])
        self.assertEqual(["查看", "删除"], [button["label"] for button in crud_schema["columns"][-1]["buttons"]])
        self.assertEqual(["title", "created_at__date_range"], [item["name"] for item in crud_schema["filter"]["body"]])

    def test_external_renderer_registration_pattern(self):
        class _Serializer(serializers.Serializer):
            amount = _MoneyField(label="金额")

            class Meta:
                fields = ["amount"]
                show_fields = ["amount"]

        class _ViewSet:
            serializer_class = _Serializer

        register_field_renderer(_MoneyField, _money_renderer)

        context = build_serializer_context(title="测试", name="demo", view_set=_ViewSet)
        form_body = serializer_form_body(context, create=True)
        columns = serializer_columns(context)

        self.assertEqual(["amount_display", "amount"], [item["name"] for item in form_body])
        self.assertEqual("input-number", form_body[0]["type"])
        self.assertEqual("formula", form_body[1]["type"])
        self.assertEqual("tpl", columns[0]["type"])
        self.assertIn("/ 100", columns[0]["tpl"])

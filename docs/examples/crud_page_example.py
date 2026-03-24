from rest_framework import serializers

from amis_python.crud import (
    build_action_column,
    build_crud_page,
    build_filter_form,
    build_serializer_context,
    build_submit_form,
    create_dialog_button,
    delete_button,
    serializer_columns,
    serializer_filter_body,
    serializer_form_body,
    view_dialog_button,
)


class MissionSerializer(serializers.Serializer):
    title = serializers.CharField(label="任务标题")
    status = serializers.ChoiceField(label="状态", choices=((1, "启用"), (0, "停用")))
    created_at = serializers.DateTimeField(label="创建时间", read_only=True)

    class Meta:
        fields = ["title", "status", "created_at"]
        show_fields = ["title", "status", "created_at"]


class MissionViewSet:
    serializer_class = MissionSerializer
    filterset_fields = ["title", "created_at__date_range"]


def build_mission_page():
    context = build_serializer_context(
        title="任务管理",
        name="mission",
        view_set=MissionViewSet,
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

    return build_crud_page(
        title=context.title,
        api={"url": context.get_base_api(), "method": "get"},
        columns=[
            *serializer_columns(context),
            build_action_column(
                [
                    view_dialog_button(form=detail_form),
                    delete_button(
                        detail_api=context.get_detail_api(),
                        crud_id=context.crud_id,
                    ),
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

from rest_framework.fields import empty

from .renderers import render_field_schema


class SerializerCrudContext:
    def __init__(self, *, title, name, view_set, crud_id=None):
        self.title = title
        self.name = name
        self.view_set = view_set
        self.serializer = self.view_set.serializer_class()
        self.crud_id = crud_id or f"{self.name}_crud"

    def get_base_api(self):
        return f"/api/amis/{self.name}/"

    def get_detail_api(self, action=None):
        if action is None:
            return f"{self.get_base_api()}${{object_id}}/"
        return f"{self.get_base_api()}${{object_id}}/{action}/"

    def get_label(self, field, field_name):
        return field.label or field_name

    def _get_field_input_placeholder(self, field, field_name):
        return "请输入" + self.get_label(field, field_name)

    def get_field(self, field_name):
        return self.serializer.get_fields()[field_name]


def build_serializer_context(*, title, name, view_set, crud_id=None):
    return SerializerCrudContext(title=title, name=name, view_set=view_set, crud_id=crud_id)


def serializer_columns(context, field_names=None):
    if field_names is None:
        field_names = getattr(context.serializer.Meta, "show_fields", context.serializer.Meta.fields)
    columns = []
    for field_name in field_names:
        rendered = render_field_schema(context, "column", context.get_field(field_name), field_name)
        if rendered is not None:
            columns.append(rendered)
    return columns


def serializer_form_body(context, *, create=False, readonly=False, field_names=None):
    if field_names is None:
        field_names = context.serializer.Meta.fields
    body = []
    for field_name in field_names:
        field = context.get_field(field_name)
        if create and field.read_only:
            continue

        base_options = {
            "required": False if readonly else field.required,
            "placeholder": field.help_text or "",
            "description": field.help_text or "",
            "disabled": True if readonly else field.read_only,
        }
        if field.default != empty:
            base_options["value"] = field.default

        rendered = render_field_schema(context, "form", field, field_name, base_options=base_options)
        if rendered is None:
            continue
        if isinstance(rendered, list):
            body.extend(rendered)
        else:
            body.append(rendered)
    return body


def serializer_filter_body(context, field_names):
    body = []
    for field_name in field_names:
        if field_name.endswith("__date_range"):
            source_field_name = field_name[: -len("__date_range")]
            body.append(
                {
                    "type": "input-date-range",
                    "name": field_name,
                    "label": context.get_label(context.get_field(source_field_name), source_field_name) + "范围",
                    "size": "full",
                    "utc": True,
                }
            )
            continue
        if field_name.endswith("__date_time_range"):
            source_field_name = field_name[: -len("__date_time_range")]
            body.append(
                {
                    "type": "input-datetime-range",
                    "name": field_name,
                    "label": context.get_label(context.get_field(source_field_name), source_field_name) + "范围",
                    "size": "full",
                    "utc": True,
                }
            )
            continue
        rendered = render_field_schema(context, "filter", context.get_field(field_name), field_name)
        if rendered is not None:
            body.append(rendered)
    return body

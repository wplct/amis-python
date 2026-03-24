from rest_framework import serializers


_REGISTERED_RENDERERS = []


def register_field_renderer(field_class, renderer):
    _REGISTERED_RENDERERS.insert(0, (field_class, renderer))


def normalize_scene_field(field):
    if isinstance(field, serializers.ListSerializer):
        return field.child
    return field


def _get_label(crud, field, field_name):
    if crud and hasattr(crud, "get_label"):
        return crud.get_label(field, field_name)
    return getattr(field, "label", None) or field_name


def _get_placeholder(crud, field, field_name):
    if crud and hasattr(crud, "_get_field_input_placeholder"):
        return crud._get_field_input_placeholder(field, field_name)
    return "请输入" + _get_label(crud, field, field_name)


def _default_renderer(scene, crud, field, field_name, context):
    label = _get_label(crud, field, field_name)
    if scene == "form":
        base_options = context.get("base_options", {})
        return [{
            "type": "input-text",
            "label": label,
            "name": field_name,
            **base_options,
        }]
    if scene == "filter":
        return None
    if scene == "column":
        return {
            "type": "tpl",
            "title": label,
            "name": field_name,
            "placeholder": "-",
        }
    raise ValueError(f"Unsupported scene: {scene}")


def _char_renderer(scene, crud, field, field_name, context):
    if scene == "filter":
        return {
            "type": "input-text",
            "label": _get_label(crud, field, field_name),
            "name": field_name,
            "size": "full",
            "placeholder": _get_placeholder(crud, field, field_name),
        }
    return _default_renderer(scene, crud, field, field_name, context)


def _boolean_renderer(scene, crud, field, field_name, context):
    label = _get_label(crud, field, field_name)
    if scene == "form":
        return [{
            "type": "switch",
            "label": label,
            "name": field_name,
            **context.get("base_options", {}),
        }]
    if scene == "filter":
        return {
            "type": "select",
            "label": label,
            "name": field_name,
            "size": "full",
            "options": [
                {"label": "是", "value": True},
                {"label": "否", "value": False},
            ],
        }
    if scene == "column":
        return {
            "type": "tpl",
            "title": label,
            "name": field_name,
            "placeholder": "-",
            "tpl": "${" + field_name + " ? '是' : '否'}",
        }
    raise ValueError(f"Unsupported scene: {scene}")


def _choice_renderer(scene, crud, field, field_name, context):
    label = _get_label(crud, field, field_name)
    options = [{"label": value, "value": key} for key, value in field.choices.items()]
    if scene == "form":
        return [{
            "type": "select",
            "label": label,
            "name": field_name,
            "size": "full",
            "extractValue": True,
            "value": "",
            "options": options,
            **context.get("base_options", {}),
        }]
    if scene == "filter":
        return {
            "type": "select",
            "label": label,
            "name": field_name,
            "size": "full",
            "options": options,
        }
    if scene == "column":
        return {
            "type": "select",
            "title": label,
            "name": field_name,
            "placeholder": "-",
            "static": True,
            "options": options,
        }
    raise ValueError(f"Unsupported scene: {scene}")


def _datetime_renderer(scene, crud, field, field_name, context):
    label = _get_label(crud, field, field_name)
    if scene == "form":
        return [{
            "type": "input-datetime",
            "label": label,
            "name": field_name,
            **context.get("base_options", {}),
        }]
    if scene == "column":
        return {
            "type": "datetime",
            "title": label,
            "name": field_name,
            "placeholder": "-",
        }
    return _default_renderer(scene, crud, field, field_name, context)


def get_default_renderer_registry():
    return [
        *_REGISTERED_RENDERERS,
        (serializers.DateTimeField, _datetime_renderer),
        (serializers.BooleanField, _boolean_renderer),
        (serializers.ChoiceField, _choice_renderer),
        (serializers.CharField, _char_renderer),
        (serializers.Field, _default_renderer),
    ]


def get_field_renderer(field, registry=None):
    normalized_field = normalize_scene_field(field)
    registry = registry or get_default_renderer_registry()
    for field_class, renderer in registry:
        if isinstance(normalized_field, field_class):
            return renderer
    return _default_renderer


def render_field_by_hook(scene, crud, field, field_name, **context):
    normalized_field = normalize_scene_field(field)
    hook_name = "get_column" if scene == "column" else f"get_{scene}_item"
    if hasattr(normalized_field, hook_name):
        return getattr(normalized_field, hook_name)(crud, field, field_name)
    if scene == "filter" and hasattr(normalized_field, "get_form_item"):
        return normalized_field.get_form_item(crud, field, field_name, True)
    return None


def render_field_schema(crud, scene, field, field_name, registry=None, **context):
    hook_result = render_field_by_hook(scene, crud, field, field_name, **context)
    if hook_result is not None:
        return hook_result
    renderer = get_field_renderer(field, registry=registry)
    return renderer(scene, crud, normalize_scene_field(field), field_name, context)

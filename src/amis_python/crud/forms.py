from .helpers import ensure_list


def build_form(body, *, api=None, actions=None, mode="flex", label_align="top", **overrides):
    data = {
        "type": "form",
        "mode": mode,
        "labelAlign": label_align,
        "body": ensure_list(body),
    }
    if api is not None:
        data["api"] = api
    if actions is not None:
        data["actions"] = actions
    data.update({k: v for k, v in overrides.items() if v is not None})
    return data


def build_submit_form(
    body,
    *,
    api,
    reload_component_id,
    cancel_label="取消",
    submit_label="提交",
    mode="flex",
    label_align="top",
    **overrides,
):
    return build_form(
        body,
        api=api,
        mode=mode,
        label_align=label_align,
        actions=[
            {
                "type": "button",
                "actionType": "cancel",
                "label": cancel_label,
            },
            {
                "type": "button",
                "actionType": "submit",
                "label": submit_label,
                "level": "primary",
            },
        ],
        onEvent={
            "submitSucc": {
                "actions": [
                    {
                        "actionType": "reload",
                        "componentId": reload_component_id,
                    }
                ]
            }
        },
        **overrides,
    )

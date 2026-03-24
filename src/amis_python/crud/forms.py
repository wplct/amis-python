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

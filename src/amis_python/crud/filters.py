from .helpers import ensure_list


def build_filter_form(body, *, title="筛选", mode="inline", column_count=3, actions=None, **overrides):
    data = {
        "type": "form",
        "title": title,
        "mode": mode,
        "columnCount": column_count,
        "clearValueOnHidden": True,
        "behavior": ["SimpleQuery"],
        "body": ensure_list(body),
        "actions": actions
        if actions is not None
        else [
            {"type": "button", "label": "重置", "actionType": "reset"},
            {"type": "submit", "label": "查询", "level": "primary"},
        ],
    }
    data.update({k: v for k, v in overrides.items() if v is not None})
    return data

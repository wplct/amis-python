from .helpers import ensure_list


def reload_action(component_id):
    return {
        "actionType": "reload",
        "componentId": component_id,
    }


def ajax_action(api, method=None, data=None, output_var=None, confirm_text=None):
    api_config = api
    if method or data is not None:
        api_config = {
            "url": api,
            "method": (method or "get").lower(),
        }
        if data is not None:
            api_config["data"] = data
    action = {
        "actionType": "ajax",
        "api": api_config,
    }
    if output_var:
        action["outputVar"] = output_var
    if confirm_text:
        action["confirmText"] = confirm_text
    return action


def dialog(title, body, size="md", actions=None, **overrides):
    data = {
        "type": "dialog",
        "title": title,
        "body": body,
        "size": size,
    }
    if actions is not None:
        data["actions"] = actions
    data.update({k: v for k, v in overrides.items() if v is not None})
    return data


def button(label, *, size=None, level=None, action_type=None, on_click=None, visible_on=None, hidden_on=None, **overrides):
    data = {
        "type": "button",
        "label": label,
    }
    if size:
        data["size"] = size
    if level:
        data["level"] = level
    if action_type:
        data["actionType"] = action_type
    if on_click:
        data["onEvent"] = {
            "click": {
                "actions": ensure_list(on_click),
            }
        }
    if visible_on:
        data["visibleOn"] = visible_on
    if hidden_on:
        data["hiddenOn"] = hidden_on
    data.update({k: v for k, v in overrides.items() if v is not None})
    return data


def dialog_button(label, *, body, title=None, size="md", visible_on=None, hidden_on=None, **overrides):
    return button(
        label,
        action_type="dialog",
        visible_on=visible_on,
        hidden_on=hidden_on,
        dialog=dialog(title or label, body=body, size=size),
        **overrides,
    )

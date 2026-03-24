from .actions import dialog_button
from .forms import build_form


def build_readonly_form(body, *, actions=None, **overrides):
    return build_form(
        body,
        actions=actions if actions is not None else [{"type": "button", "actionType": "cancel", "label": "关闭"}],
        **overrides,
    )


def readonly_dialog_button(label, *, body, title="查看数据", size="md", **overrides):
    return dialog_button(
        label,
        title=title,
        body=build_readonly_form(body),
        size=size,
        **overrides,
    )

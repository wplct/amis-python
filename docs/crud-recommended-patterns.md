# 函数式 CRUD 推荐写法

`amis_python.crud` 是当前推荐的 CRUD 页面组织方式。

推荐原则：

- 页面文件显式声明 `header_toolbar`
- 页面文件显式声明操作列
- helper 只负责减少样板代码，不隐式生成“新增”“操作”等业务组织
- `Serializer` 负责字段定义
- 页面函数负责页面结构、按钮组织、业务动作拼装
- 外部项目自定义字段应通过 `register_field_renderer(...)` 接入，而不是修改库内默认 renderer

## 推荐导入

```python
from amis_python.crud import (
    build_action_column,
    build_crud_page,
    build_filter_form,
    build_readonly_form,
    build_serializer_context,
    build_submit_form,
    create_dialog_button,
    delete_button,
    serializer_columns,
    serializer_filter_body,
    serializer_form_body,
    view_dialog_button,
)
```

## 推荐页面结构

```python
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


def build_demo_page(view_set):
    context = build_serializer_context(
        title="任务管理",
        name="mission",
        view_set=view_set,
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
```

## 为什么不推荐隐式按钮

不推荐让 helper 自动推导：

- 是否显示“新增”
- 是否生成“操作”列
- 操作列里有哪些按钮

原因：

- 业务页面最终长什么样，应该在页面文件里一眼能看出来
- 显式组织更适合 AI 阅读、修改和搜索
- 页面结构稳定后，helper 只做复用，不会反过来绑架业务页面组织

## 外部字段扩展方式

如果项目里有自己的字段类型，不建议改 `amis_python.crud` 内置 renderer。
推荐在项目启动时注册：

```python
from rest_framework import serializers
from amis_python.crud import register_field_renderer


class MoneyField(serializers.IntegerField):
    pass


def render_money(scene, crud, field, field_name, context):
    if scene == "column":
        return {
            "type": "tpl",
            "title": crud.get_label(field, field_name),
            "name": field_name,
            "tpl": "${" + field_name + " / 100}元",
        }
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
                "formula": f"Math.round({field_name}_display * 100)",
                "initSet": True,
                "autoSet": True,
            },
        ]
    return None


register_field_renderer(MoneyField, render_money)
```

## 当前定位

- `crud/` 是 CRUD 页面推荐入口
- `builder/` 仍可继续使用，但不是当前 CRUD 页面推荐主路线
- 新增 CRUD 能力优先进入 `crud/`

from importlib import reload
from typing import Any, Type, Optional, List, Dict, ClassVar
from functools import wraps

from django.db.models import Model
from ninja import ModelSchema
from pydantic import BaseModel

from amis_python import PageBuilder, CRUDCardsBuilder, DividerBuilder, DialogBuilder, CRUDListBuilder, TplBuilder, \
    CRUDTableBuilder, ReloadActionBuilder
from amis_python.builder import to_api, ConfirmDialogActionBuilder
from amis_python.builder.action import DialogActionBuilder, AjaxActionBuilder
from amis_python.builder.button import ButtonBuilder
from amis_python.builder.event import AmisEvent
from amis_python.builder.form import api_to_form, schema_to_form
from amis_python.ninja_api import PaginatedResponse, ApiResponse, amis_api
from amis_python.page.curd_card import BaseCRUDPage
from amis_python.pagination import amis_paginate


class TableCRUDPage(BaseCRUDPage):
    """基类CRUD页面配置"""

    def get_detail_actions(self) -> List[Any]:
        return [
            {
                "label": "详情",
                "type": "button",
                "actionType": "dialog",
                "dialog": DialogBuilder(
                    title="详情",
                    body=[
                        api_to_form(self._apis["update"])
                    ],
                ),
            },
            ButtonBuilder(
                label="删除",
                type="button",
                level="danger",
            ).add_action(
                "click",
                ConfirmDialogActionBuilder(
                    dialog=DialogBuilder(
                        title="删除确认",
                        body="确定要删除吗？",
                    )
                )
            ).add_action(
                "click",
                AjaxActionBuilder(
                    api=to_api(self._apis['delete']),
                )
            ).add_action('click', ReloadActionBuilder(
                component_id='crud_page',
            )),
        ]

    def build_page(self) -> PageBuilder:
        """构建页面"""
        apis = self._register_apis()

        body = []

        # 头部操作
        body.extend(self.get_header_actions())
        body.append(DividerBuilder())

        # 额外组件
        body.extend(self.get_extra_components())
        # CRUD卡片
        body.append(
            CRUDTableBuilder(
                api=to_api(apis["list"]),
                source="${items}",
                columns=[
                    # {"label": "名称", "name": "name"}
                    *[{'name': field_name, 'label': field.title or field_name} for field_name, field in
                      self.list_schema.model_fields.items()],
                    {
                        'type': 'operation',
                        "label": "操作",
                        "buttons": self.get_detail_actions()
                    }
                ],
            )
        )

        return PageBuilder(
            title=self.page_title,
            body=body,
            id="crud_page",
        )


# 快速创建函数
def create_crud_page(
        model: Type[Model],
        base_url: str = None,
        verbose_name: str = None,
        **kwargs
) -> PageBuilder:
    """快速创建CRUD页面"""

    class QuickCRUDPage(BaseCRUDPage):
        pass

    page_class = QuickCRUDPage
    page_class.model = model
    if base_url:
        page_class.base_url = base_url
    if verbose_name:
        page_class.verbose_name = verbose_name

    for key, value in kwargs.items():
        setattr(page_class, key, value)

    return page_class().build_page()


# 使用示例
if __name__ == "__main__":
    from django.contrib.auth.models import User


    # 方式1：继承方式
    class UserCRUDPage(BaseCRUDPage):
        model = User
        verbose_name = "用户"
        list_exclude = ('password', 'last_login')
        create_exclude = ('id', 'password', 'last_login')
        update_exclude = ('password', 'last_login')

        def get_extra_components(self):
            return [
                ButtonBuilder(label="导出", level="success"),
                ButtonBuilder(label="导入", level="warning"),
            ]

        def get_card_actions(self):
            base_actions = super().get_detail_actions()
            base_actions.append(
                ButtonBuilder(label="重置密码", level="link").add_action(
                    AmisEvent.click,
                    DialogActionBuilder(
                        dialog=DialogBuilder(title="重置密码", body="密码重置表单")
                    )
                )
            )
            return base_actions


    user_page = UserCRUDPage().build_page()

    # 方式3：快速创建
    quick_page = create_crud_page(
        model=User,
        verbose_name="用户",
        page_title="用户管理系统",
        list_order="-date_joined"
    )

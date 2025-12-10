from importlib import reload
from typing import Any, Type, Optional, List, Dict, ClassVar
from functools import wraps

from django.db.models import Model
from ninja import ModelSchema
from pydantic import BaseModel

from amis_python import PageBuilder, CRUDCardsBuilder, DividerBuilder, DialogBuilder
from amis_python.builder import to_api
from amis_python.builder.action import DialogActionBuilder, AjaxActionBuilder
from amis_python.builder.button import ButtonBuilder
from amis_python.builder.event import AmisEvent
from amis_python.builder.form import api_to_form, schema_to_form
from amis_python.ninja_api import PaginatedResponse, ApiResponse, amis_api
from amis_python.pagination import amis_paginate


class BaseCRUDPage:
    """基类CRUD页面配置"""

    # 必填配置
    model: Type[Model] = None

    # 可选配置
    base_url: str = None
    verbose_name: str = None
    page_title: str = None

    # API端点名称
    list_api_name: str = "list"
    create_api_name: str = "create"
    update_api_name: str = "update"
    delete_api_name: str = "delete"

    # Schema配置
    list_schema: Type[ModelSchema] = None
    create_schema: Type[ModelSchema] = None
    update_schema: Type[ModelSchema] = None

    # 字段排除
    list_exclude: tuple = ('created_at', 'updated_at', 'is_deleted')
    create_exclude: tuple = ('id', 'created_at', 'updated_at', 'is_deleted')
    update_exclude: tuple = ('id','created_at', 'updated_at', 'is_deleted')

    # 排序
    list_order: str = "-id"

    # 内部状态
    _apis_registered: bool = False
    _apis: Dict[str, Any] = {}
    _schemas: Dict[str, Type[ModelSchema]] = {}

    def __init__(self, **kwargs):
        """初始化，支持覆盖类属性"""
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._validate_config()
        self._init_defaults()
        self._create_schemas()

    def _validate_config(self):
        """验证配置"""
        if not self.model:
            raise ValueError("必须指定 model")

    def _init_defaults(self):
        """初始化默认值"""
        if not self.base_url:
            self.base_url = f"/{self.model._meta.model_name}"

        if not self.verbose_name:
            self.verbose_name = self.model._meta.verbose_name

        if not self.page_title:
            self.page_title = f"{self.verbose_name}管理"

    def _create_schemas(self):
        """创建默认的Schema"""
        if not self.list_schema:
            class ListSchema(ModelSchema):
                class Meta:
                    model = self.model
                    exclude = self.list_exclude

            self.list_schema = ListSchema

        if not self.create_schema:
            class CreateSchema(ModelSchema):
                class Meta:
                    model = self.model
                    exclude = self.create_exclude

            self.create_schema = CreateSchema

        if not self.update_schema:
            class UpdateSchema(ModelSchema):
                class Meta:
                    model = self.model
                    exclude = self.update_exclude

            self.update_schema = UpdateSchema

    def _register_apis(self):
        """注册API"""
        if self._apis_registered:
            return self._apis

        # 列表API
        @amis_api.get(
            f"{self.base_url}/{self.list_api_name}",
            response=ApiResponse[PaginatedResponse[self.list_schema]]
        )
        @amis_paginate(self.list_schema)
        def data_list(request):
            return self.model.objects.order_by(self.list_order)

        # 创建API
        @amis_api.post(
            f"{self.base_url}/{self.create_api_name}",
            response=ApiResponse[self.create_schema]
        )
        def create_data(request, data: self.create_schema):
            obj = self.model.objects.create(**data.model_dump())
            return obj

        # 更新API
        @amis_api.post(
            f"{self.base_url}/{self.update_api_name}/" + "{id}",
            response=ApiResponse[self.update_schema]
        )
        def update_data(request, id: int, data: self.update_schema):
            obj = self.model.objects.get(id=id)
            for key, value in data.dict(exclude_unset=True).items():
                setattr(obj, key, value)
            obj.save()
            return obj

        # 删除API
        @amis_api.post(
            f"{self.base_url}/{self.delete_api_name}/" + "{id}",
            response=ApiResponse[Any]
        )
        def delete_by_id(request, id: int):
            self.model.objects.filter(id=id).delete()
            return {"ok": True}

        self._apis = {
            'list': data_list,
            'create': create_data,
            'update': update_data,
            'delete': delete_by_id,
        }
        self._apis_registered = True

        return self._apis

    # 钩子方法，供子类覆盖
    def get_extra_components(self) -> List[Any]:
        """获取额外的页面组件"""
        return []

    def get_detail_actions(self) -> List[Any]:
        """获取卡片操作按钮"""
        apis = self._register_apis()

        return [
            ButtonBuilder(label="编辑", level="link").add_action(
                AmisEvent.click,
                DialogActionBuilder(
                    dialog=DialogBuilder(
                        title=f'编辑{self.verbose_name}',
                        body=[api_to_form(apis['update'])]
                    )
                ),
            ),
            AjaxActionBuilder(
                label="删除",
                api=to_api(apis['delete']),
                confirmText=f"确定要删除这个{self.verbose_name}吗？"
            ),
        ]

    def get_header_actions(self) -> List[ButtonBuilder]:
        """获取头部操作按钮"""
        apis = self._register_apis()

        return [
            ButtonBuilder(label="新增", level='primary')
            .add_action(
                AmisEvent.click,
                DialogActionBuilder(
                    dialog=DialogBuilder(
                        title=f"新增{self.verbose_name}",
                        body=[api_to_form(apis['create'])],
                    ),
                )
            )
        ]

    def get_show_form(self):
        """获取展示表单"""
        return schema_to_form(
            self.list_schema,
            static=True,
            mode="inline",
            wrap_with_panel=False
        )

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
            CRUDCardsBuilder(
                id="crud_page",
                api=to_api(apis['list']),
                multiple=True,
                card={
                    'body': [self.get_show_form()],
                    'actions': self.get_detail_actions()
                },
            )
        )

        return PageBuilder(
            title=self.page_title,
            body=body
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
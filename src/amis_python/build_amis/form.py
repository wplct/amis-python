from typing import Union

from django.urls import reverse
from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.generics import GenericAPIView

from amis_python.builder import BaseModel, Wrapper
from amis_python.builder.form import Form, InputNumber, InputPassword, InputFile, InputImage, Hidden, InputText
from amis_python.schema import ImageSerializer

from amis_python.builder import Tpl


class ViewSetForm:
    def __init__(self, view_set: GenericAPIView,basename=None):
        self.view_set = view_set
        self.serializer = view_set.get_serializer_class()()
        if not basename:
            self.basename = view_set.queryset.model._meta.model_name
        else:
            self.basename = basename

    def get_field_type(self, field: Field) -> Union[str, None]:
        if isinstance(field, serializers.IntegerField):
            return 'number'
        if isinstance(field, serializers.CharField):
            return 'text'
        if isinstance(field, ImageSerializer):
            return 'image'
        return None

    def field_to_input(self, field_name: str, field: Field,static=None) -> BaseModel:
        input_type = self.get_field_type(field)
        title = field.label or field_name

        input_base_kwargs = {
            'name': field_name,
            'label': title,
            "required": field.required,
            "static": field.read_only,
        }
        if static:
            input_base_kwargs["static"] = True
        if input_type == 'number':
            return InputNumber(**input_base_kwargs)
        if input_type == 'password':
            return InputPassword(**input_base_kwargs)

        if input_type == 'file':
            return InputFile(
                receiver="/amis/upload",
                # drag=True,
                **input_base_kwargs
            )
        if input_type == 'image':
            base = input_base_kwargs.copy()
            base.pop('name', None)
            return Wrapper(body=[
                InputImage(
                    **base,
                    receiver="/amis/upload_img",
                    name=f'upload_{field_name}',
                    auto_fill={
                        field_name: {
                            "id": "${id}",
                            "name": "${name}",
                            # "url": "${url}",
                            "key": "${key}",
                        }
                    },
                    value="${"+field_name+".url}",
                ),
                Hidden(**input_base_kwargs),
            ])
        return InputText(**input_base_kwargs)

    def field_to_show(self, field_name, field_info, **kwargs):
        return Tpl(
            tpl="${"+field_name+"}"
        )

    def get_form_items(self, **kwargs):
        return [self.field_to_input(field_name, field_info, **kwargs) for field_name, field_info in
                self.serializer.get_fields().items()]

    def get_list_items(self, **kwargs):
        return [self.field_to_show(field_name, field_info, **kwargs) for field_name, field_info in
                self.serializer.get_fields().items()]




    def to_create_form(self, **kwargs):
        _kwargs = {
            # 'title': title,
            'wrap_with_panel': True,
            'api': self.get_create_api(),
            # 'actions':[]
        }
        _kwargs.update(kwargs)
        return Form(
            body=self.get_form_items(),
            **_kwargs
        )

    def to_detail_form(self, **kwargs):
        _kwargs = {
            'title': '详情',
            'wrap_with_panel': True,
            'init_api': self.get_detail_api(),
            'api': self.get_update_api(),
            # 'actions': []
        }
        _kwargs.update(kwargs)
        return Form(
            body=self.get_form_items(),
            **_kwargs
        )

    def get_create_api(self):
        return reverse(f'{self.basename}-list')

    def get_update_api(self):
        return 'patch:'+reverse(f'{self.basename}-detail', kwargs={'pk': 0}).replace('0', '${id}')

    def get_detail_api(self):
        return reverse(f'{self.basename}-detail', kwargs={'pk': 0}).replace('0', '${id}')
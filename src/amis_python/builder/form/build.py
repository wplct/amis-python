from typing import Type, Literal, Optional, Union, List, get_origin, get_args

from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict
from pydantic.fields import FieldInfo

from amis_python.builder import BaseModel
from amis_python.builder.form import Form, InputText, InputPassword, InputNumber, FormItem


class AmisExtra(PydanticBaseModel):
    """
    专门描述 amis 在 json_schema_extra 里可能出现的字段。
    想加别的 amis 属性继续往这里堆即可。
    """
    type: Optional[Literal["password", "email", "url",'image']] = None


class User(PydanticBaseModel):
    username: str = Field(..., title="用户名")
    password: str = Field(..., title="密码", json_schema_extra=AmisExtra(type="password").model_dump())
    email: str = Field(..., title="邮箱", json_schema_extra=AmisExtra(type="email").model_dump())
    age: int = Field(..., description="年龄")
    phone: str
    address: str

    model_config = ConfigDict(
        title="用户信息",
    )


class SchemaFormBuild:
    def __init__(self, schema: Type[PydanticBaseModel]):
        self.schema = schema

    def get_field_type(self, field_info: FieldInfo) -> Union[str, None]:
        if field_info.json_schema_extra and 'type' in field_info.json_schema_extra:
            return field_info.json_schema_extra['type']
        ann = field_info.annotation
        if get_origin(ann) is Union:
            args = [a for a in get_args(ann) if a is not type(None)]
            if not args:  # 全是 None，理论上不会走到这里
                return None
            ann = args[0]
        if issubclass(ann, int):
            return 'number'
        return None

    def field_to_input(self, field_name: str, field_info: FieldInfo) -> BaseModel:
        input_type = self.get_field_type(field_info)
        title = field_info.title or field_info.description or field_name

        input_base_kwargs = {
            'name': field_name,
            'label': title,
            "required": field_info.is_required(),
        }
        if input_type == 'number':
            return InputNumber(**input_base_kwargs)
        if input_type == 'password':
            return InputPassword(**input_base_kwargs)
        return InputText(**input_base_kwargs)

    def get_form_items(self) -> List[BaseModel]:
        return [self.field_to_input(field_name, field_info) for field_name, field_info in
                self.schema.model_fields.items()]

    def schema_to_form(self) -> BaseModel:
        title = self.schema.model_config.get("title")
        return Form(
            title=title,
            body=self.get_form_items(),
            wrap_with_panel=False,
            actions=[]
        )


if __name__ == '__main__':
    form = SchemaFormBuild(User).schema_to_form()
    print(form.model_dump_json())
    form.show()
    # print(schema_to_form(User))

from typing import Type

from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict

from amis_python.builder import BaseModel
from amis_python.builder.form import Form, InputText

class User(PydanticBaseModel):
    username: str = Field(..., description="用户名")
    password: str
    email: str
    phone: str
    address: str

    model_config = ConfigDict(
        title="用户信息",
    )


def schema_to_form(schema: Type[PydanticBaseModel]) -> BaseModel:
    title = schema.model_config.get("title")
    print( title)
    return Form(
        title=title,
    )


if __name__ == '__main__':
    schema_to_form(User).show()

    # print(schema_to_form(User))
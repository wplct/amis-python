from typing import Type

from pydantic import BaseModel

from amis_python.builder.form import Form, InputText

# class Form:


# def schema_to_form(schema: Type[BaseModel]) -> dict:
#     return {
#
#     }



if __name__ == '__main__':
    f = Form(body=[
        InputText(name='username', label='用户名'),
        InputText(name='password', label='密码'),
        InputText(name='email', label='邮箱'),
        InputText(name='phone', label='手机号'),
        InputText(name='address', label='地址'),
        InputText(name='zipcode', label='邮编'),
        InputText(name='city', label='城市'),
        InputText(name='country', label='国家'),
        InputText(name='birthday', label='生日'),
        InputText(name='sex', label='性别'),
    ])
    print(f.model_dump())
    print(f.model_dump_json())

    # print(schema_to_form(User))
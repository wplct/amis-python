from typing import Type

from pydantic import BaseModel

from amis_python.builder.form import Form

# class Form:


# def schema_to_form(schema: Type[BaseModel]) -> dict:
#     return {
#
#     }



if __name__ == '__main__':
    f = Form()
    print(f.model_dump())

    # print(schema_to_form(User))
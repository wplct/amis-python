from typing import Any, List

from pydantic import BaseModel

from amis_python.builder.base import BaseBuilder


class PageBuilder(BaseBuilder):
    type:str = "page"
    title: str
    body: List = []





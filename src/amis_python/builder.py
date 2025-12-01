from typing import Any, List

from pydantic import BaseModel


class PageBuilder(BaseModel):
    title: str
    body: List = []

    def __init__(self, /, **data: Any):
        super().__init__(**data)

    def to_schema(self):
        return {
            "type": "page",
            "title": self.title,
            "body": self.body
        }



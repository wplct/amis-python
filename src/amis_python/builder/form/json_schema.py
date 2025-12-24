from typing import Optional, Any, Dict, Union
from pydantic import Field

from amis_python.builder import BaseModel
from amis_python.builder.form import FormItem


class JSONSchema(FormItem):
    """
    amis JSONSchema 组件完整 Pydantic 模型
    对应组件类型: type: "json-schema"
    文档地址: /docs/zh-CN/components/form/json-schema.md
    """

    type: Optional[str] = Field("json-schema", description="指定为 json-schema 组件")
    name: Optional[str] = Field(None, description="组件名称，用于数据域通信")
    label: Optional[str] = Field(None, description="组件标题")
    # schema: Optional[Union[Dict[str, Any], str]] = Field(None, description="指定 json-schema")
    formula: Optional[Dict[str, Any]] = Field(None, description="公式配置")

from typing import Optional, Any, Dict, Union
from pydantic import Field

from amis_python.builder import BaseModel


class InputKV(BaseModel):
    """
    amis InputKV 组件完整 Pydantic 模型
    对应组件类型: type: "input-kv"
    文档地址: /docs/zh-CN/components/form/input-kv.md
    """

    type: Optional[str] = Field("input-kv", description="指定为 input-kv 组件")
    name: Optional[str] = Field(None, description="组件名称，用于数据域通信")
    value_type: Optional[str] = Field(None, description="值类型，默认 input-text")
    key_placeholder: Optional[str] = Field(None, description="key 的提示信息")
    value_placeholder: Optional[str] = Field(None, description="value 的提示信息")
    draggable: Optional[bool] = Field(None, description="是否可拖拽排序，默认 true")
    default_value: Optional[Any] = Field(None, description="默认值，默认 ''")
    auto_parse_json: Optional[bool] = Field(None, description="是否自动转换 json 对象字符串，默认 true")
    value_schema: Optional[Union[Dict[str, Any], Any]] = Field(None, description="自定义 value 的 schema")
    key_schema: Optional[Union[Dict[str, Any], Any]] = Field(None, description="自定义 key 的 schema")

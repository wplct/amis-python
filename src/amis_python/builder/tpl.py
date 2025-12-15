from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from .base import BaseModel


class Tpl(BaseModel):
    """
    amis Tpl 模板组件
    对应组件类型: tpl
    文档地址: docs/zh-CN/components/tpl.md
    
    用于在页面中动态渲染模板内容，支持模板字符串和 JavaScript 表达式。
    """

    # ==================== 基本属性 ====================
    type: Literal["tpl"] = Field("tpl", description="指定为模板组件")
    tpl: str = Field(..., description="模板字符串，支持模板语法")
    className: Optional[str] = Field(None, description="CSS 类名")
    inline: Optional[bool] = Field(None, description="是否内联显示")
    wrapperComponent: Optional[str] = Field(None, description="包装组件")
    wrapperProps: Optional[Dict[str, Any]] = Field(None, description="包装组件属性")
    raw: Optional[bool] = Field(None, description="是否原样输出，不转义")
    html: Optional[bool] = Field(None, description="是否解析 HTML")

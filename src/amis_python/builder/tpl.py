from __future__ import annotations
from typing import Optional, Literal
from pydantic import Field

from .base import BaseBuilder


class TplBuilder(BaseBuilder):
    """
    构建 AMIS 模板配置对象，对应 <Tpl> 组件。
    参考文档：https://aisuda.bce.baidu.com/amis/zh-CN/components/tpl
    
    示例：
        tpl = TplBuilder(
            tpl="1.普通按钮",
            inline=False,
            wrapper_component="h2"
        )
    """
    type: Literal["tpl"] = "tpl"
    
    # 模板内容
    tpl: str = Field(..., description="模板内容")
    
    # 其他属性
    inline: Optional[bool] = Field(True, description="是否内联")
    wrapper_component: Optional[str] = Field(None, description="包装组件", alias="wrapperComponent")
    class_name: Optional[str] = Field(None, description="指定添加 tpl 类名")

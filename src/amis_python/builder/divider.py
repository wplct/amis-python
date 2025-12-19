from typing import Optional, Literal
from pydantic import Field
from .base import BaseModel


class Divider(BaseModel):
    """Divider 组件，用于在页面中添加分隔线
    
    详细文档: https://aisuda.bce.baidu.com/amis/zh-CN/components/divider
    """
    type: Literal['divider'] = Field('divider', description="组件类型")
    orientation: Optional[Literal['left', 'center', 'right']] = Field(None, description="分割线标题的位置")
    content: Optional[str] = Field(None, description="分割线中间的内容")
    style: Optional[str] = Field(None, description="自定义样式")
    className: Optional[str] = Field(None, description="自定义 CSS 类名")

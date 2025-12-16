from typing import Optional, Literal, Dict, Any, Union, List
from pydantic import Field

from amis_python.builder.base import BaseModel


class ImageAction(BaseModel):
    """
    amis ImageAction 图片动作配置
    对应组件类型: ImageAction
    
    用于配置图片工具栏的操作项
    """
    
    # ==================== 基本属性 ====================
    key: Literal["rotateRight", "rotateLeft", "zoomIn", "zoomOut", "scaleOrigin"] = Field(..., description="操作key")
    label: Optional[str] = Field(None, description="动作名称")
    icon: Optional[str] = Field(None, description="动作icon")
    iconClassName: Optional[str] = Field(None, description="动作自定义CSS类")
    disabled: Optional[bool] = Field(None, description="动作是否禁用")


class Image(BaseModel):
    """
    amis Image 图片组件
    对应组件类型: image
    文档地址: docs/zh-CN/components/image.md
    
    用于展示图片，支持缩略图、放大预览、链接跳转等功能。
    """

    # ==================== 基本属性 ====================
    type: Literal["image", "static-image"] = Field("image", description="组件类型，在 Table、Card 和 List 中为 'image'；在 Form 中用作静态展示为 'static-image'")
    className: Optional[str] = Field(None, description="外层 CSS 类名")
    innerClassName: Optional[str] = Field(None, description="组件内层 CSS 类名")
    imageClassName: Optional[str] = Field(None, description="图片 CSS 类名")
    thumbClassName: Optional[str] = Field(None, description="图片缩率图 CSS 类名")
    height: Optional[str] = Field(None, description="图片缩率高度")
    width: Optional[str] = Field(None, description="图片缩率宽度")
    title: Optional[str] = Field(None, description="标题")
    imageCaption: Optional[str] = Field(None, description="描述")
    placeholder: Optional[str] = Field(None, description="占位文本")
    defaultImage: Optional[str] = Field(None, description="无数据时显示的图片")
    src: Optional[str] = Field(None, description="缩略图地址")
    href: Optional[str] = Field(None, description="外部链接地址")
    originalSrc: Optional[str] = Field(None, description="原图地址")
    enlargeAble: Optional[bool] = Field(None, description="支持放大预览")
    enlargeTitle: Optional[str] = Field(None, description="放大预览的标题")
    enlargeCaption: Optional[str] = Field(None, description="放大预览的描述")
    enlargeWithGallary: Optional[bool] = Field(True, description="在表格中，图片的放大功能会默认展示所有图片信息，设置为 false 将关闭放大模式下图片集列表的展示")
    thumbMode: Optional[Literal["w-full", "h-full", "contain", "cover"]] = Field("contain", description="预览图模式")
    thumbRatio: Optional[str] = Field("1:1", description="预览图比例")
    imageMode: Optional[Literal["thumb", "original"]] = Field("thumb", description="图片展示模式，可选：thumb（缩略图模式）、original（原图模式）")
    showToolbar: Optional[bool] = Field(False, description="放大模式下是否展示图片的工具栏")
    toolbarActions: Optional[List[ImageAction]] = Field(None, description="图片工具栏，支持旋转，缩放，默认操作全部开启")
    maxScale: Optional[Union[float, int, str]] = Field(None, description="执行调整图片比例动作时的最大百分比")
    minScale: Optional[Union[float, int, str]] = Field(None, description="执行调整图片比例动作时的最小百分比")

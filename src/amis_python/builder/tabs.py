from typing import Optional, Literal, List, Dict, Any, Union
from enum import Enum
from pydantic import Field

from amis_python.builder import BaseModel


class TabsMode(str, Enum):
    LINE = "line"
    CARD = "card"
    RADIO = "radio"
    VERTICAL = "vertical"
    CHROME = "chrome"
    SIMPLE = "simple"
    STRONG = "strong"
    TILED = "tiled"
    SIDEBAR = "sidebar"


class IconPosition(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class SidePosition(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class TabsItem(BaseModel):
    """
    Tabs组件的单个tab项配置
    """
    title: Optional[Union[str, Dict[str, Any]]] = Field(None, description="Tab标题，当是SchemaNode时，不支持editable为true的双击编辑")
    icon: Optional[str] = Field(None, description="Tab的图标")
    icon_position: Optional[IconPosition] = Field(None, description="Tab的图标位置", alias="iconPosition")
    tab: Optional[Union[str, Dict[str, Any], "BaseModel",Any]] = Field(None, description="内容区")
    body: Optional[Union[str, Dict[str, Any], "BaseModel",Any]] = Field(None, description="内容区")
    hash: Optional[str] = Field(None, description="设置以后将跟url的hash对应")
    reload: Optional[bool] = Field(None, description="设置以后内容每次都会重新渲染，对于crud的重新拉取很有用")
    unmount_on_exit: Optional[bool] = Field(None, description="每次退出都会销毁当前tab栏内容", alias="unmountOnExit")
    class_name: Optional[str] = Field("bg-white b-l b-r b-b wrapper-md", description="Tab区域样式", alias="className")
    tip: Optional[str] = Field(None, description="Tab提示，当开启showTip时生效，作为Tab在hover时的提示显示")
    closable: Optional[bool] = Field(False, description="是否支持删除，优先级高于组件的closable")
    disabled: Optional[bool] = Field(False, description="是否禁用")


class Tabs(BaseModel):
    """
    amis Tabs 组件完整 Pydantic 模型
    对应组件类型: type: "tabs"
    文档地址: /docs/zh-CN/components/tabs.md
    """

    type: Literal["tabs"] = Field("tabs", description="指定为Tabs渲染器")
    
    # ==================== 基础属性 ====================
    default_key: Optional[Union[str, int]] = Field(None, description="组件初始化时激活的选项卡，hash值或索引值，支持使用表达式 2.7.1 以上版本", alias="defaultKey")
    active_key: Optional[Union[str, int]] = Field(None, description="激活的选项卡，hash值或索引值，支持使用表达式，可响应上下文数据变化", alias="activeKey")
    class_name: Optional[str] = Field(None, description="外层Dom的类名", alias="className")
    links_class_name: Optional[str] = Field(None, description="Tabs标题区的类名", alias="linksClassName")
    content_class_name: Optional[str] = Field(None, description="Tabs内容区的类名", alias="contentClassName")
    tabs_mode: Optional[TabsMode] = Field(None, description="展示模式", alias="tabsMode")
    tabs: Optional[List[TabsItem]] = Field(None, description="tabs内容")
    source: Optional[str] = Field(None, description="tabs关联数据，关联后可以重复生成选项卡")
    toolbar: Optional[Union[List[Union[Dict[str, Any], "BaseModel"]], Dict[str, Any], "BaseModel"]] = Field(None, description="tabs中的工具栏")
    toolbar_class_name: Optional[str] = Field(None, description="tabs中工具栏的类名", alias="toolbarClassName")
    mount_on_enter: Optional[bool] = Field(True, description="只有在点中tab的时候才渲染", alias="mountOnEnter")
    unmount_on_exit: Optional[bool] = Field(False, description="切换tab的时候销毁", alias="unmountOnExit")
    addable: Optional[bool] = Field(False, description="是否支持新增")
    add_btn_text: Optional[str] = Field("增加", description="新增按钮文案", alias="addBtnText")
    closable: Optional[bool] = Field(False, description="是否支持删除")
    draggable: Optional[bool] = Field(False, description="是否支持拖拽")
    show_tip: Optional[bool] = Field(False, description="是否支持提示", alias="showTip")
    show_tip_class_name: Optional[str] = Field("", description="提示的类", alias="showTipClassName")
    editable: Optional[bool] = Field(False, description="是否可编辑标签名")
    scrollable: Optional[bool] = Field(True, description="是否导航支持内容溢出滚动")
    side_position: Optional[SidePosition] = Field(SidePosition.LEFT, description="sidebar模式下，标签栏位置", alias="sidePosition")
    collapse_on_exceed: Optional[int] = Field(None, description="当tabs超出多少个时开始折叠", alias="collapseOnExceed")
    collapse_btn_label: Optional[str] = Field("more", description="用来设置折叠按钮的文字", alias="collapseBtnLabel")
    swipeable: Optional[bool] = Field(False, description="是否开启手势滑动切换（移动端生效）")
    on_select: Optional[str] = Field(None, description="监听切换事件", alias="onSelect")

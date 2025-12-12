from typing import Optional, Literal, List, Dict, Union, Any
from enum import Enum

from pydantic import Field

from amis_python.builder import BaseModel


# ====================== 枚举类型 ======================

class FormMode(str, Enum):
    NORMAL = "normal"      # 默认分行展示
    HORIZONTAL = "horizontal"
    INLINE = "inline"

class LabelAlign(str, Enum):
    RIGHT = "right"
    LEFT = "left"

class SubmitTextAlign(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class InitDataTarget(str, Enum):
    WINDOW = "window"      # 写入 window
    PARENT = "parent"      # 写入父窗口
    # 也可以是任意组件路径，如 dialog:form1



class FormMessages(BaseModel):
    """表单提交成功/失败时的提示消息配置"""
    save_success: Optional[str] = Field(None, description="提交成功提示，优先级高于全局 messages.fetchSuccess")
    save_fail: Optional[str] = Field(None, description="提交失败提示，优先级高于全局 messages.fetchFailed")

class FormHorizontal(BaseModel):
    """horizontal 模式下的标签-控件宽度比例配置"""
    left: Optional[Union[int, str]] = Field(None, description="标签占几列（共12列），如 2 或 '3'")
    right: Optional[Union[int, str]] = Field(None, description="控件占几列，自动计算时可不填")
    offset: Optional[Union[int, str]] = Field(None, description="当标签没有时，控件往左偏移几列")
    justify: Optional[bool] = Field(None, description="是否两端对齐，只对内联控件生效")
    left_fixed: Optional[Union[bool, str]] = Field(None, description="是否固定左侧宽度，或指定宽度类型：xs/sm/md/lg")

class FormRedirect(BaseModel):
    """跳转配置，支持静态地址或表达式"""
    url: Optional[str] = Field(None, description="跳转地址，支持 ${xxx} 模板语法")
    blank: Optional[bool] = Field(None, description="是否新窗口打开，默认为 false")

class FormReload(BaseModel):
    """表单提交后重新加载目标组件"""
    target: Optional[str] = Field(None, description="需要重新拉取的组件名称或路径，多个用逗号分隔")
    data: Optional[Dict[str, Any]] = Field(None, description="重新加载时附加的数据范围")

class FormDebugConfig(BaseModel):
    """表单调试配置（仅开发环境有效）"""
    enable_clipboard: Optional[bool] = Field(None, description="是否启用剪贴板功能，默认 false")
    display_data_types: Optional[bool] = Field(None, description="是否显示数据类型，默认 false")

# ====================== 主模型 ======================

class Form(BaseModel):
    """
    amis Form 表单组件完整 Pydantic 模型
    对应组件类型: type: "form"
    文档地址: https://aisuda.bce.baidu.com/amis/zh-CN/components/form/index
    """

    type: Literal["form"] = Field("form", description="指定为 form 组件")

    # ==================== 基础属性 ====================
    name: Optional[str] = Field(None, description="表单名，用于数据域通信和表单提交识别")
    title: Optional[str] = Field(None, description="表单标题，默认不显示标题栏")
    mode: Optional[FormMode] = Field(None, description="表单展示方式：normal（分行，默认）、horizontal（水平排列）、inline（内联）")
    horizontal: Optional[FormHorizontal] = Field(None, description="mode=horizontal 时生效，用于控制标签和控件宽度比例")
    label_align: Optional[LabelAlign] = Field(None, description="标签对齐方式，仅在 horizontal 模式下生效，默认 right")
    label_width: Optional[Union[int, str]] = Field(None, description="标签固定宽度，支持数字（px）或字符串如 '100px'")
    body: Optional[List[Any]] = Field(None, description="表单项集合，支持任意 amis SchemaNode（input-text、input-number 等）")
    actions: Optional[List[Any]] = Field(None, description="底部操作按钮集合，默认显示【提交】和【重置】两个按钮")
    submit_text: Optional[str] = Field(None, description="提交按钮文字，默认 '提交'")
    reset_text: Optional[str] = Field(None, description="重置按钮文字，默认 '重置'")
    submit_text_align: Optional[SubmitTextAlign] = Field(None, description="按钮组整体对齐方式，默认 right")
    wrap_with_panel: Optional[bool] = Field(None, description="是否用 panel 包裹表单，默认 true")
    panel_class_name: Optional[str] = Field(None, description="外层 panel 的 className")

    # ==================== API 配置 ====================
    api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="保存接口，支持字符串 URL 字符串或完整 API 对象（含 method、url、data 等）")
    init_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="表单初始化接口，用于编辑场景回填数据")
    init_async_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="异步初始化接口（与 initApi 配合使用）")
    init_finished_field: Optional[str] = Field(None, description="初始化完成字段名，默认 'finished'")
    init_check_interval: Optional[int] = Field(None, description="轮询检查初始化完成的间隔（毫秒）")
    finished_field: Optional[str] = Field(None, description="结束轮询的标识字段名，默认 'finished'")

    # ==================== 数据行为 ====================
    init_fetch: Optional[bool] = Field(None, description="是否初始加载 initApi，默认 true（有 api 时才生效）")
    init_fetch_on: Optional[str] = Field(None, description="初始化加载条件表达式，支持 amis 表达式")
    async_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="提交后轮询检查接口，用于长任务场景")
    interval: Optional[int] = Field(None, description="轮询间隔时间（毫秒），默认 3000")
    stop_auto_refresh_when: Optional[str] = Field(None, description="停止轮询的表达式")
    silent_polling: Optional[bool] = Field(None, description="是否静默轮询（不显示 loading），默认 false")
    messages: Optional[FormMessages] = Field(None, description="自定义提交成功/失败提示消息")

    # ==================== 提交后行为 ====================
    redirect: Optional[Union[str, FormRedirect]] = Field(None, description="提交成功后跳转地址，支持字符串或对象")
    reload: Optional[Union[str, FormReload]] = Field(None, description="提交成功后刷新目标组件，支持名称或对象")
    target: Optional[str] = Field(None, description="提交成功后向目标发送数据（不刷新页面），多个用逗号分隔")
    feedback: Optional[Any] = Field(None, description="提交成功后弹出的反馈对话框，支持完整的 dialog schema")
    reset_after_submit: Optional[bool] = Field(None, description="提交成功后是否重置表单，默认 false")
    clear_after_submit: Optional[bool] = Field(None, description="提交成功后是否清空表单（比 reset 更彻底），默认 false")

    # ==================== 校验与持久化 ====================
    rules: Optional[List[Dict[str, Any]]] = Field(None, description="自定义校验规则数组，配合 validator 插件使用")
    persist_data: Optional[bool] = Field(None, description="是否开启本地持久化（localStorage），默认 false")
    persist_data_key: Optional[str] = Field(None, description="持久化存储的 key，默认使用页面 URL")
    clear_persist_data_after_submit: Optional[bool] = Field(None, description="提交成功后是否清除持久化数据，默认 false")
    required_mark: Optional[bool] = Field(None, description="是否显示必填星号，默认 true")
    prevent_enter_submit: Optional[bool] = Field(None, description="是否阻止回车提交，默认 false")
    trim_values: Optional[bool] = Field(None, description="提交前是否自动 trim 所有字符串值，默认 false")

    # ==================== 其他功能 ====================
    primary_field: Optional[str] = Field(None, description="主键字段名，默认 'id'，用于编辑场景")
    data: Optional[Dict[str, Any]] = Field(None, description="额外的表单数据，会与表单项数据合并")
    init_data_target: Optional[InitDataTarget] = Field(None, description="初始化数据写入目标，window/parent 或组件路径")
    debug: Optional[bool] = Field(None, description="是否开启调试模式（显示底部调试栏，默认 false）")
    debug_config: Optional[FormDebugConfig] = Field(None, description="调试栏详细配置")
    static: Optional[bool] = Field(None, description="是否为纯展示模式，所有表单项变为 static 状态")
    can_access_super_data: Optional[bool] = Field(None, description="是否可以访问上层数据链，默认 true")

    # ==================== 布局与样式 ====================
    class_name: Optional[str] = Field(None, description="外层 DOM className")
    style: Optional[Dict[str, Any]] = Field(None, description="自定义样式对象")
    visible: Optional[bool] = Field(None, description="是否显示")
    visible_on: Optional[str] = Field(None, description="是否显示表达式")
    hidden: Optional[bool] = Field(None, description="是否隐藏（同 visible: false）")
    hidden_on: Optional[str] = Field(None, description="是否隐藏表达式")
    disabled: Optional[bool] = Field(None, description="是否禁用整个表单")
    disabled_on: Optional[str] = Field(None, description="是否禁用表达式")
    column_count: Optional[int] = Field(None, description="控制表单显示几列")
    affix_footer: Optional[bool] = Field(None, description="是否固定底部按钮栏在浏览器底部")

    # ==================== 事件相关（预留） ====================
    on_event: Optional[Dict[str, Any]] = Field(None, description="事件动作配置，支持 onSubmitSuccess、onSubmitFail 等自定义动作")
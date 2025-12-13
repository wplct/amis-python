from typing import Optional, Literal, Dict, Any, Union
from pydantic import Field

from amis_python.builder.form.form_item import FormItem


class InputImage(FormItem):
    """
    amis InputImage 图片上传组件
    对应组件类型: input-image
    文档地址: docs/zh-CN/components/form/input-image.md
    """

    # ==================== 基本属性 ====================
    type: Literal["input-image"] = Field("input-image", description="指定为图片上传组件")

    # ==================== 上传相关属性 ====================
    receiver: Optional[Union[str, Dict[str, Any]]] = Field(None, description="上传文件接口")
    accept: Optional[str] = Field(None, description="支持的图片类型格式，请配置此属性为图片后缀，例如'.jpg,.png'，默认值为'.jpeg,.jpg,.png,.gif'")
    capture: Optional[str] = Field(None, description="用于控制 input[type=file] 标签的 capture 属性，在移动端可控制输入来源")
    max_size: Optional[int] = Field(None, description="默认没有限制，当设置后，文件大小大于此值将不允许上传。单位为B")
    max_length: Optional[int] = Field(None, description="默认没有限制，当设置后，一次只允许上传指定数量文件")
    multiple: Optional[bool] = Field(None, description="是否多选，默认值为false")
    join_values: Optional[bool] = Field(None, description="拼接值，默认值为true")
    extract_value: Optional[bool] = Field(None, description="提取值，默认值为false")
    delimiter: Optional[str] = Field(None, description="拼接符，默认值为','")
    auto_upload: Optional[bool] = Field(None, description="是否选择完就自动开始上传，默认值为true")
    hide_upload_button: Optional[bool] = Field(None, description="隐藏上传按钮，默认值为false")
    file_field: Optional[str] = Field(None, description="如果你不想自己存储，则可以忽略此属性，默认值为'file'")

    # ==================== 裁剪相关属性 ====================
    crop: Optional[Union[bool, Dict[str, Any]]] = Field(None, description="用来设置是否支持裁剪")
    crop_format: Optional[str] = Field(None, description="裁剪文件格式，默认值为'image/png'")
    crop_quality: Optional[float] = Field(None, description="裁剪文件格式的质量，用于jpeg/webp，取值在0和1之间，默认值为1")

    # ==================== 限制相关属性 ====================
    limit: Optional[Dict[str, Any]] = Field(None, description="限制图片大小，超出不让上传")

    # ==================== 样式相关属性 ====================
    frame_image: Optional[str] = Field(None, description="默认占位图地址")
    fixed_size: Optional[bool] = Field(None, description="是否开启固定尺寸,若开启，需同时设置fixedSizeClassName")
    fixed_size_class_name: Optional[str] = Field(None, description="开启固定尺寸时，根据此值控制展示尺寸。例如'h-30',即图片框高为h-30,AMIS将自动缩放比率设置默认图所占位置的宽度，最终上传图片根据此尺寸对应缩放")
    image_class_name: Optional[str] = Field(None, description="图片的CSS类名")

    # ==================== 自动填充属性 ====================
    init_auto_fill: Optional[bool] = Field(None, description="表单反显时是否执行autoFill，默认值为false")

    # ==================== 按钮相关属性 ====================
    upload_btn_text: Optional[Union[str, Dict[str, Any]]] = Field(None, description="上传按钮文案。支持tpl、schema形式配置")

    # ==================== 裁剪模式属性 ====================
    drop_crop: Optional[bool] = Field(None, description="图片上传后是否进入裁剪模式，默认值为true")
    init_crop: Optional[bool] = Field(None, description="图片选择器初始化后是否立即进入裁剪模式，默认值为false")

    # ==================== 拖拽排序属性 ====================
    draggable: Optional[bool] = Field(None, description="开启后支持拖拽排序改变图片值顺序，默认值为false")
    draggable_tip: Optional[str] = Field(None, description="拖拽提示文案，默认值为'拖拽排序'")

    # ==================== 错误提示属性 ====================
    show_error_modal: Optional[bool] = Field(None, description="校验失败后是否弹窗提醒，默认值为true")
    invalid_type_message: Optional[str] = Field(None, description="校验格式失败后的提示信息，默认值为'文件格式不正确'")
    invalid_size_message: Optional[str] = Field(None, description="校验文件大小失败时显示的文字信息，默认值为'文件大小超出限制'")

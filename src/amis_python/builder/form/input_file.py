from typing import Optional, Literal, Dict, Any, Union
from pydantic import Field

from amis_python.builder.form.form_item import FormItem


class InputFile(FormItem):
    """
    amis InputFile 文件上传组件
    对应组件类型: input-file
    文档地址: docs/zh-CN/components/form/input-file.md
    """

    # ==================== 基本属性 ====================
    type: Literal["input-file"] = Field("input-file", description="指定为文件上传组件")

    # ==================== 上传相关属性 ====================
    receiver: Optional[Union[str, Dict[str, Any]]] = Field(None, description="上传文件接口")
    accept: Optional[str] = Field(None, description="默认只支持纯文本，要支持其他类型，请配置此属性为文件后缀'.xxx'，默认值为'text/plain'")
    capture: Optional[str] = Field(None, description="用于控制 input[type=file] 标签的 capture 属性，在移动端可控制输入来源")
    as_base64: Optional[bool] = Field(None, description="将文件以base64的形式，赋值给当前组件，默认值为false")
    as_blob: Optional[bool] = Field(None, description="将文件以二进制的形式，赋值给当前组件，默认值为false")
    max_size: Optional[int] = Field(None, description="默认没有限制，当设置后，文件大小大于此值将不允许上传。单位为B")
    max_length: Optional[int] = Field(None, description="默认没有限制，当设置后，一次只允许上传指定数量文件")
    multiple: Optional[bool] = Field(None, description="是否多选，默认值为false")
    drag: Optional[bool] = Field(None, description="是否为拖拽上传，默认值为false")
    join_values: Optional[bool] = Field(None, description="拼接值，默认值为true")
    extract_value: Optional[bool] = Field(None, description="提取值，默认值为false")
    delimiter: Optional[str] = Field(None, description="拼接符，默认值为','")
    auto_upload: Optional[bool] = Field(None, description="是否选择完就自动开始上传，默认值为true")
    hide_upload_button: Optional[bool] = Field(None, description="隐藏上传按钮，默认值为false")
    state_text_map: Optional[Dict[str, Any]] = Field(None, description="上传状态文案，默认值为{ init: '', pending: '等待上传', uploading: '上传中', error: '上传出错', uploaded: '已上传', ready: '' }")
    file_field: Optional[str] = Field(None, description="如果你不想自己存储，则可以忽略此属性，默认值为'file'")
    name_field: Optional[str] = Field(None, description="接口返回哪个字段用来标识文件名，默认值为'name'")
    value_field: Optional[str] = Field(None, description="文件的值用那个字段来标识，默认值为'value'")
    url_field: Optional[str] = Field(None, description="文件下载地址的字段名，默认值为'url'")
    btn_label: Optional[str] = Field(None, description="上传按钮的文字")
    download_url: Optional[Union[bool, str]] = Field(None, description="默认显示文件路径的时候会支持直接下载，可以支持加前缀如：'http://xx.dom/filename=' ，如果不希望这样，可以把当前配置项设置为false。1.1.6版本开始支持'post:http://xxx.com/${value}'这种写法")
    use_chunk: Optional[Union[bool, Literal["auto"]]] = Field(None, description="amis所在服务器，限制了文件上传大小不得超出10M，所以amis在用户选择大文件的时候，自动会改成分块上传模式，默认值为'auto'")
    chunk_size: Optional[int] = Field(None, description="分块大小，默认值为5*1024*1024")
    start_chunk_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="startChunkApi，用于分块上传的准备工作")
    chunk_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="chunkApi，用于接收每个分块上传")
    finish_chunk_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="finishChunkApi，用于收尾分块上传")
    concurrency: Optional[int] = Field(None, description="分块上传时并行个数")
    documentation: Optional[str] = Field(None, description="文档内容")
    document_link: Optional[str] = Field(None, description="文档链接")
    init_auto_fill: Optional[bool] = Field(None, description="表单反显时是否执行，默认值为true")
    invalid_type_message: Optional[str] = Field(None, description="校验格式失败后的提示信息，可以用{{}}获取内部变量值，如{{accept}}")
    invalid_size_message: Optional[str] = Field(None, description="校验文件大小失败时显示的文字信息，可以用{{}}获取内部变量值，如{{maxSize}}")

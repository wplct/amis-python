

### 要求如下：

#### 1. **继承关系**
- 所有模型必须继承自自定义的 `BaseModel`（已提供），而非直接继承 `pydantic.BaseModel`。你先不引入，我来引入
- 主类名为 **`XXX`**（首字母大写，简洁明确，不加后缀如 `XXXModel`）。

#### 2. **字段规范**
- 所有字段类型为 `Optional[T]`，默认值为 `None`。
- **不在代码中硬编码文档默认值**（如 `title="表单"`），而是将默认值说明写在 `Field(..., description=...)` 的注释中。
- 每个字段必须包含清晰的中文 `description`，说明其用途、取值含义及文档中的默认行为。
- 字段原则上只能有一行

#### 3. **类型组织**
- 对枚举类型（如 `mode`、`labelAlign` 等）定义独立的 `str` 枚举类，命名简洁（如 `XXXMode`、`LabelAlign`）。
- 对嵌套对象（如 `horizontal`、`messages`、`debugConfig` 等）定义单独的 `BaseModel` 子类，命名清晰（如 `XXXHorizontal`, `XXXMessages`）。
- 所有辅助类应紧邻主类 `XXX` 定义，或按逻辑分组放置。

#### 4. **全局配置（已封装在 BaseModel 中）**
```python
class Config:
    alias_generator = camelize                 # 自动 snake_case → camelCase
    allow_population_by_field_name = True      # 支持通过原字段名或别名传参
    exclude_none = True                        # 序列化时忽略 None 字段
```

#### 5. **命名规范**
- 类名使用 **PascalCase**，简洁明确：  
  ✅ `XXX`, `XXXMode`, `XXXHorizontal`  
  ❌ `AmisXXX`, `XXXConfig`, `XXXComponent`
- 枚举值使用 **UPPER_SNAKE_CASE**：  
  ✅ `XXXMode.NORMAL`  
  ❌ `XXXMode.normal`
- 字段名使用 **snake_case**（Pydantic 原生风格），由 `alias_generator` 自动转为 camelCase 输出。

#### 6. **覆盖范围**
- 必须完整实现文档“属性表”中列出的所有属性（包括基础、API、校验、持久化、事件等）。
- 复杂类型（如 `API`、`SchemaNode`）可用 `Union[str, dict]` 或预留 `Any`，但需注释说明。

---

### 提供的基类（请直接使用）：
```python
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field
import re

def camelize(snake_str: str) -> str:
    """将 snake_case 转换为 camelCase，例如 label_width → labelWidth"""
    components = snake_str.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])

class BaseModel(PydanticBaseModel):
    """amis 组件通用基类，统一处理序列化行为"""
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
        exclude_none = True
```

---

### 示例片段（供参考风格）：不是你要实现的，你实现的在url里
```python
from typing import Optional, Literal, List, Union, Any
from enum import Enum

class FormMode(str, Enum):
    NORMAL = "normal"
    HORIZONTAL = "horizontal"
    INLINE = "inline"

# ====================== 主模型 ======================

class Form(BaseModel):
    """
    amis Form 表单组件完整 Pydantic 模型
    对应组件类型: type: "form"
    文档地址: https://aisuda.bce.baidu.com/amis/zh-CN/components/form/index
    """

    type: Literal["form"] = Field("form", description="指定为 form 组件", const=True)

    # ==================== 基础属性 ====================
    name: Optional[str] = Field(None, description="表单名，用于组件间数据通信及表单提交")
    title: Optional[str] = Field(None, description="表单标题，默认为空（不显示标题栏）")
    mode: Optional[FormMode] = Field(None, description="表单布局模式：''（默认分行）、'horizontal'（水平）、'inline'（内联）")
    horizontal: Optional[FormHorizontal] = Field(None, description="当 mode=horizontal 时有效，用于配置标签与控件宽度比例")
    label_align: Optional[LabelAlign] = Field(None, description="标签对齐方式，仅在 horizontal 模式下生效，默认 right")
    label_width: Optional[Union[int, str]] = Field(None, description="标签自定义宽度，支持像素或数字（如 120 或 '120px'）")
    body: Optional[List[Any]] = Field(None, description="表单项集合，支持任意表单控件 SchemaNode 数组")
    actions: Optional[List[Any]] = Field(None, description="表单操作按钮集合，默认显示【提交】和【重置】")
    submit_text: Optional[str] = Field(None, description="提交按钮文字，默认为 '提交'")
    reset_text: Optional[str] = Field(None, description="重置按钮文字，默认为 '重置'")
    submit_text_align: Optional[SubmitTextAlign] = Field(None, description="按钮组对齐方式，默认 right")

    # ==================== API 配置 ====================
    api: Optional[Union[str, Dict[str, Any]]] = Field(None,description="表单提交接口，支持字符串 URL 或完整 API 对象（如 {method: 'post', url: '/save'}）")
```

请基于以上规范，生成完整、可运行、注释完备的 `XXX` 模型代码。
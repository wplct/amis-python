# amis-python 组件开发规范

## 1. 核心设计与功能

### 1.1 基础架构
- 所有组件必须继承自自定义的 `BaseModel`（位于 `amis_python.builder` 中）或其子类
- `BaseModel` 基于 Pydantic 构建，提供自动序列化能力：
  - snake_case 自动转换为 camelCase（如 `label_width` → `labelWidth`）
  - 支持通过原字段名或别名传参
  - 序列化时自动忽略 `None` 字段
  - 递归处理嵌套组件

### 1.2 核心类说明
- `BaseModel`: 基于 Pydantic 的通用基类，处理序列化行为

## 2. 组件开发规范

### 2.1 继承关系
- 所有模型必须继承自 `BaseModel` 或其子类，而非直接继承 `pydantic.BaseModel`
- 主类名使用**`XXX`**（首字母大写，简洁明确，不加后缀如 `XXXModel`）

### 2.2 字段规范
- 所有字段类型为 `Optional[T]`，默认值为 `None`
- 不在代码中硬编码文档默认值，而是将默认值说明写在 `Field(..., description=...)` 中
- 每个字段必须包含清晰的中文 `description`，说明其用途、取值含义及文档中的默认行为
- 字段原则上只占一行
- **特别强调**：所有值默认都是 `None`（即不输出到最终的 JSON 配置中），除了 `type` 字段，文档中描述的默认值应仅在 `description` 中说明，而不应在代码中硬编码

### 2.3 类型组织
- 枚举类型：定义独立的 `str` 枚举类，命名简洁（如 `XXXMode`、`LabelAlign`）
- 嵌套对象：定义单独的 `BaseModel` 子类，命名清晰（如 `XXXHorizontal`, `XXXMessages`）
- 辅助类应紧邻主类 `XXX` 定义，或按逻辑分组放置
- 复杂类（如 API）：可直接使用已定义的类或留待用户导入，无需重复定义

### 2.4 命名规范
- 类名：PascalCase，简洁明确：
  ✅ `XXX`, `XXXMode`, `XXXHorizontal`
  ❌ `AmisXXX`, `XXXConfig`, `XXXComponent`
- 枚举值：UPPER_SNAKE_CASE：
  ✅ `XXXMode.NORMAL`
  ❌ `XXXMode.normal`
- 字段名：snake_case（Pydantic 原生风格），由 `alias_generator` 自动转为 camelCase 输出

### 2.5 覆盖范围
- 必须完整实现文档“属性表”中列出的所有属性（包括基础、API、校验、持久化、事件等）
- 复杂类型（如 `API`、`SchemaNode`）可用 `Union[str, Dict]` 或预留 `Any`，但需注释说明

## 3. 测试规范

### 3.1 测试框架
- 使用 `unittest` 框架编写测试用例
- 测试文件命名为 `test_*.py`
- 测试类命名为 `XXXTestCase`

### 3.2 测试要求
- 每个组件必须包含基本的序列化测试
- 测试用例应验证：
  - 组件类型是否正确
  - 字段是否正确转换为 camelCase
  - 序列化结果是否符合预期
  - 核心功能是否正常工作

### 3.3 测试示例
```python
from unittest import TestCase
from amis_python.builder.form import Form

class FormTestCase(TestCase):
    """表单组件测试基类"""
    def test_serialize(self):
        f = Form(init_api='api/mock2/page/initData')
        self.assertEqual(f.model_dump(), {'type': 'form', 'initApi': 'api/mock2/page/initData'})
```

## 4. 代码示例

### 4.1 完整组件示例
```python
from typing import Optional, Literal, List, Dict, Union, Any
from enum import Enum
from pydantic import Field

from amis_python.builder import BaseModel

# ====================== 枚举类型 ======================

class XXXMode(str, Enum):
    NORMAL = "normal"      # 默认分行展示
    HORIZONTAL = "horizontal"  # 水平排列
    INLINE = "inline"       # 内联展示

# ====================== 嵌套模型 ======================

class XXXNested(BaseModel):
    """嵌套配置示例"""
    field1: Optional[str] = Field(None, description="字段1说明")
    field2: Optional[int] = Field(None, description="字段2说明")

# ====================== 主模型 ======================

class XXX(BaseModel):
    """
    amis XXX 组件完整 Pydantic 模型
    对应组件类型: type: "xxx"
    文档地址: https://aisuda.bce.baidu.com/amis/zh-CN/components/xxx/index
    """

    type: Literal["xxx"] = Field("xxx", description="指定为 xxx 组件")

    # ==================== 基础属性 ====================
    name: Optional[str] = Field(None, description="组件名称，用于数据域通信")
    title: Optional[str] = Field(None, description="组件标题")
    mode: Optional[XXXMode] = Field(None, description="组件展示模式")
    nested: Optional[XXXNested] = Field(None, description="嵌套配置")

    # ==================== API 配置 ====================
    # 可使用已定义的 API 类或留待用户导入
    api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="API 配置，支持字符串 URL 或完整 API 对象")
    init_api: Optional[Union[str, Dict[str, Any]]] = Field(None, description="初始化数据接口")

    # ==================== 其他属性 ====================
    visible: Optional[bool] = Field(None, description="是否显示组件")
    disabled: Optional[bool] = Field(None, description="是否禁用组件")
```

## 5. 开发与运行

### 5.1 命令规范
- Python 命令使用 uv 执行，例如：`uv run app.py`
- 运行测试：`uv run pytest`

### 5.2 目录结构
- 组件代码：`src/amis_python/builder/xxx/xxx.py`
- 测试代码：`src/amis_python/tests/test_xxx.py`
- 文档：`docs/zh-CN/components/xxx/index.md`

## 6. 注意事项

- 所有组件必须声明 `type` 字段，使用 `Literal` 类型确保类型安全
- 优先使用 Pydantic v2 语法
- 保持代码简洁，避免冗余注释
- 确保测试覆盖率，验证核心功能
- 严格遵循 AMIS 组件文档的属性定义
- 复杂类（如 API）可直接使用已定义的类或留待用户导入

## 7. 部署与使用

- 作为 Python 包安装到 Django 项目中使用
- 支持直接在 Django 项目中导入和使用
- 自动序列化生成符合 AMIS 规范的 JSON 配置

# 总结

本规范旨在提供清晰、统一的 amis-python 组件开发指南，确保组件的一致性、可维护性和易用性。遵循本规范可以快速开发高质量的 AMIS 组件，与 Django 框架深度集成，为用户提供优雅的页面渲染解决方案。
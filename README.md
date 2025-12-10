# amis-python

amis-python 是一个为 Django 提供优雅解决方案的库，可以使用 AMIS 渲染页面。它允许开发者使用 Pythonic 的方式构建 AMIS 组件，并将其集成到 Django 项目中。

## 功能特性

- **Pythonic 的 AMIS 组件构建方式**：使用 Python 代码构建 AMIS 组件，无需直接编写 JSON 配置
- **Django 集成**：与 Django 框架深度集成，支持直接在 Django 项目中使用
- **自动序列化**：将 Python 对象自动转换为符合 AMIS 规范的 JSON
- **类型安全**：使用 Pydantic 和 Literal 类型确保组件配置的正确性
- **易于扩展**：支持自定义组件和扩展现有组件
- **支持分组和页面注册**：允许开发者组织和管理多个页面
- **Django Ninja 集成**：支持与 Django Ninja 框架集成

## 适用场景

- 快速构建管理后台
- 构建数据可视化仪表板
- 快速开发表单页面
- 构建复杂的交互式页面
- 集成 AMIS 到 Django 项目中

## 安装

```bash
# 使用 uv 安装
uv add amis-python

# 使用 pip 安装
pip install amis-python
```

## 快速开始

### Django 项目使用示例

#### 1. 配置步骤

1. 在 Django 项目的 `settings.py` 中添加 `amis_python` 到 `INSTALLED_APPS`：

```python
INSTALLED_APPS = [
    # ...
    'amis_python',
]
```

2. 在项目的 `urls.py` 中添加 amis-python 的路由：

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('amis/', include('amis_python.urls')),
]
```

#### 2. 访问应用

启动 Django 服务器后，访问以下 URL 查看 AMIS 应用：

- 首页：`http://localhost:8000/amis/`
- 应用配置：`http://localhost:8000/amis/config/`
- 页面配置：`http://localhost:8000/amis/page/home/`

### Django Ninja 集成

如果你的项目使用 Django Ninja，可以使用 `AmisNinja` 类来集成 amis-python：

```python
from ninja import NinjaAPI
from amis_python import AppBuilder, AmisNinja
from amis_python.builder.page import PageBuilder

# 创建 Django Ninja API
api = NinjaAPI()

# 创建 AMIS 应用
app = AppBuilder(brand_name="My App")

# 注册页面
app.register_page_group(label="首页分组")
app.register_page(
    path="/home",
    page=PageBuilder(title="首页"),
    group="首页分组",
    label="首页"
)

# 集成 amis-python
amis_ninja = AmisNinja(api)
amis_ninja.register_amis_app(app, prefix="/amis")
```

## 组件组织

amis-python 按照 AMIS 组件的功能和类型，将组件组织在不同的目录中，便于开发者查找和使用：

### 核心组件分类

| 分类 | 目录 | 包含组件 | 用途 |
|------|------|----------|------|
| 基础组件 | `base/` | `BaseBuilder`, `AmisApiObject` | 所有组件的基类和API对象 |
| 布局组件 | `layout/` | `PageBuilder` | 页面布局相关组件 |
| 容器组件 | `container/` | `ActionContainerBuilder`, `CRUDBuilder`, `DialogBuilder` | 容器类组件，用于组织其他组件 |
| 表单组件 | `form/` | `FormBuilder`, `FormItemBuilder`, `OptionsBuilder`, `InputTextBuilder`, `InputEmailBuilder`, `InputPasswordBuilder`, `InputDatetimeBuilder` | 表单相关组件，用于构建表单 |
| 通用组件 | `general/` | `ColorBuilder`, `DividerBuilder`, `TplBuilder` | 通用组件，可在各种场景使用 |
| 按钮组件 | `button/` | `ButtonBuilder`, `ButtonGroupBuilder` | 按钮相关组件 |
| 动作组件 | `action/` | `ActionBuilder`, `AjaxActionBuilder` | 动作相关组件，用于触发操作 |
| 应用组件 | `app/` | `AppBuilder`, `AppPageBuilder` | 应用相关组件，用于构建整个应用 |

### 组件开发规则

1. **命名规范**：使用下划线命名而非驼峰命名，例如 `class_name` 而非 `className`
2. **默认值规则**：属性默认值应该使用 `None`，默认值信息写在注释中，例如 `disabled: Optional[bool] = None  # 是否禁用，默认：False`
3. **类型安全**：每个组件必须使用 Literal 类型指定 `type` 字段
4. **继承关系**：组件应继承自 `BaseBuilder`
5. **文档完善**：每个组件必须包含完整的 docstring，说明组件用途、参考文档和使用示例


### 组件导入示例

可以通过以下方式导入所需的组件：

```python
# 从 amis_python 直接导入（推荐）
from amis_python import PageBuilder, FormBuilder, InputTextBuilder

# 从具体模块导入
from amis_python.builder.layout import PageBuilder
from amis_python.builder.form import FormBuilder, InputTextBuilder
```

## 使用注意事项

1. **默认应用注册**：必须调用 `register_default_app()` 函数注册默认应用，否则会出现 "Default amis app not registered" 错误。

2. **分组注册**：页面必须通过分组注册，不能直接注册到应用。可以使用 `register_page_group()` 函数注册分组。

3. **页面路径**：页面路径必须以 `/` 开头，如 `/home`、`/users/list`。

4. **组件类型**：每个组件必须指定 `type` 字段，使用 Literal 类型确保类型安全。

5. **嵌套组件**：支持嵌套组件，amis-python 会自动递归将嵌套组件转换为符合 AMIS 规范的 JSON。

## 依赖说明

- Python 3.8+
- Django 3.2+
- Pydantic 2.0+
- Django Ninja (可选)

## 开发

### 安装依赖

```bash
uv install
```

### 运行测试

```bash
uv run python -m unittest tests/test_app.py -v
```

### 运行测试项目

```bash
cd test_django
uv run python manage.py runserver
```

## 项目结构

```
amis-python/
├── src/                    # 主源码目录
│   └── amis_python/        # 主要的 Python 包
│       ├── builder/        # AMIS 组件构建器
│       │   ├── action/     # 动作组件
│       │   ├── app/        # 应用组件
│       │   ├── base.py     # 基础构建器
│       │   ├── button/     # 按钮组件
│       │   ├── container/  # 容器组件
│       │   ├── form/       # 表单组件
│       │   ├── general/    # 通用组件
│       │   ├── layout/     # 布局组件
│       │   └── api.py      # API 构建器
│       ├── static/         # 静态文件
│       ├── views.py        # Django 视图
│       ├── urls.py         # Django URL 配置
│       └── ninja.py        # Django Ninja 集成
├── tests/                  # 单元测试目录
├── test_django/            # Django 测试项目
└── README.md               # 项目文档
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT

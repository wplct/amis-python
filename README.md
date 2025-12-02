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

#### 2. 创建 AMIS 应用

在你的应用中创建一个 `amis.py` 文件，用于配置 AMIS 应用：

```python
from amis_python import register_default_app
from amis_python.builder.app import AppBuilder
from amis_python.builder.page import PageBuilder

# 创建 AMIS 应用实例
app = AppBuilder(
    brand_name="我的应用"
)

# 注册分组
app.register_page_group(label="首页分组")
app.register_page_group(label="表单分组")

# 注册首页
app.register_page(
    path="/home",
    page=PageBuilder(
        title="首页",
        body=[
            {
                "type": "text",
                "text": "欢迎使用 amis-python！"
            },
            {
                "type": "button",
                "label": "测试按钮",
                "actionType": "button",
                "level": "primary"
            }
        ]
    ),
    group="首页分组",
    label="首页"
)

# 注册表单页面
app.register_page(
    path="/form",
    page=PageBuilder(
        title="表单页面",
        body=[
            {
                "type": "form",
                "mode": "horizontal",
                "api": "/save-form",
                "body": [
                    {
                        "label": "姓名",
                        "type": "input-text",
                        "name": "name",
                        "required": True
                    },
                    {
                        "label": "邮箱",
                        "type": "input-email",
                        "name": "email",
                        "required": True
                    }
                ],
                "actions": [
                    {
                        "type": "submit",
                        "label": "提交"
                    },
                    {
                        "type": "reset",
                        "label": "重置"
                    }
                ]
            }
        ]
    ),
    group="表单分组",
    label="表单页面"
)

# 注册默认应用
register_default_app(app)
```

3. 在应用的 `apps.py` 中导入 `amis.py` 文件，确保应用启动时注册 AMIS 应用：

```python
from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_app'
    
    def ready(self):
        # 导入 amis.py 文件，确保应用启动时注册 AMIS 应用
        from . import amis
```

#### 4. 访问应用

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
│       │   ├── app/        # App 相关构建器
│       │   ├── api.py      # API 构建器
│       │   ├── base.py     # 基础构建器
│       │   └── page.py     # Page 构建器
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

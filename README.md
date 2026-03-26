# amis-python

amis-python 是一个为 Django 提供优雅解决方案的库，可以使用 AMIS 渲染页面。它允许开发者使用 Pythonic 的方式构建 AMIS 组件，并将其集成到 Django 项目中。

## 功能特性

- **用户认证系统**：内置登录、登出和用户信息管理功能
- **默认无模型上传**：内置文件/图片上传接口基于 Django storage，不要求额外的文件模型
- **页面注册机制**：支持从 Python 代码或 JSON 文件注册 AMIS 页面
- **API 包装装饰器**：提供 `amis_wrap`、`amis_paginate`、`amis_filter`、`amis_search` 等装饰器，简化 API 与 AMIS 的集成
- **函数式 CRUD helper**：提供 `amis_python.crud`，用于显式组织 CRUD 页面、表单、筛选和动作按钮
- **Django 集成**：与 Django 框架深度集成，支持直接在 Django 项目中使用
- **Django Ninja 集成**：支持与 Django Ninja 框架集成，提供 API 响应格式化和认证支持

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
```

## 快速开始

### 推荐路线

如果你是在写后台 CRUD 页面，当前推荐优先使用 `amis_python.crud` 的函数式 helper，而不是继续扩展深继承 builder。

推荐文档见：

- [`docs/crud-recommended-patterns.md`](docs/crud-recommended-patterns.md)
- [`docs/examples/crud_page_example.py`](docs/examples/crud_page_example.py)

### 1. 配置步骤

1. 在 Django 项目的 `settings.py` 中添加 `amis_python` 到 `INSTALLED_APPS`：

```python
INSTALLED_APPS = [
    # ...
    'amis_python',
]
```

2. 在项目的 `urls.py` 中添加 amis-python 和 Django Ninja 的路由：

```python
from django.urls import path, include
from ninja import NinjaAPI

# 创建 Django Ninja API
api = NinjaAPI()

urlpatterns = [
    # ...
    path('api/v1/', api.urls),  # Django Ninja API 路由
    path('amis/', include('amis_python.urls')),  # amis-python 路由
]
```

### 2. API 包装装饰器使用示例

使用 `amis_wrap`、`amis_paginate`、`amis_filter` 和 `amis_search` 装饰器简化 API 与 AMIS 的集成：

```python
from ninja import Router
from django.contrib.auth import authenticate
from amis_python import amis_wrap, amis_paginate, amis_filter, amis_search
from amis_python.ninja_api import ApiResponse

router = Router()

@router.get('/list', auth=authenticate)
@amis_wrap()
@amis_paginate()
@amis_filter()
@amis_search('title', 'content','source')
def list_messages(request):
    # 你的 API 逻辑
    return {
        "items": [
            {"id": 1, "title": "消息1", "content": "内容1", "source": "来源1"},
            {"id": 2, "title": "消息2", "content": "内容2", "source": "来源2"}
        ],
        "total": 2
    }
```

### 3. 页面注册示例

从 JSON 文件加载页面配置并注册：

```python
import json
from pathlib import Path
from amis_python import register_page

# 获取当前 .py 文件所在目录
current_dir = Path(__file__).parent

# 构造 JSON 文件的绝对路径
json_path = current_dir / "message.json"

# 读取 JSON
with open(json_path, encoding="utf-8") as f:
    page = json.load(f)

# 注册页面
register_page("消息管理", "/message/message", page)
```

### 4. 访问应用

启动 Django 服务器后，访问以下 URL 查看 AMIS 应用：

- 首页：`http://localhost:8000/amis/`
- 登录配置：`http://localhost:8000/amis/login/config/`
- 应用配置：`http://localhost:8000/amis/config/`
- 页面配置：`http://localhost:8000/amis/page/{page_path}`
- 文件上传：`http://localhost:8000/amis/upload`
- 图片上传：`http://localhost:8000/amis/upload_img`

## 核心组件

amis-python 提供了以下核心组件，用于构建和管理 AMIS 应用：

### 主要组件

| 组件名称 | 用途 |
|----------|------|
| `BaseModel` | 所有组件的基类，提供基本的序列化功能 |
| `Api` | AMIS API 配置对象，用于定义 API 请求 |
| `Page` | 页面构建器，用于创建 AMIS 页面布局 |
| `AppBuilder` | 应用构建器，用于创建和管理 AMIS 应用 |
| `AppPageGroupBuilder` | 页面分组构建器，用于组织页面 |
| `AppPageBuilder` | 应用页面构建器，用于定义应用中的页面 |

### 组件导入示例

可以通过以下方式导入所需的组件：

```python
# 从 amis_python 直接导入（推荐）
from amis_python import Api, Page, AppBuilder, register_page

# 从具体模块导入
from amis_python.builder.layout import Page
from amis_python.builder.app import AppBuilder
from amis_python.builder.api import Api
```

### Api 组件使用示例

使用 `Api` 组件定义 API 请求配置：

```python
from amis_python import Api

# 创建一个 GET 请求 API 配置
api_config = Api(
    url="/api/messages",
    method="get",
    cache=3000,  # 缓存 3 秒
    headers={
        "Authorization": "Bearer ${token}"
    }
)

# 创建一个 POST 请求 API 配置
post_api = Api(
    url="/api/messages",
    method="post",
    data_type="json",
    data={
        "title": "${title}",
        "content": "${content}"
    }
)
```

### 页面构建示例

使用 `PageBuilder` 和 `Api` 组件创建页面：

```python
from amis_python import Page, Api

# 创建一个带有初始数据 API 的页面
page = Page(
    title="消息列表",
    init_api=Api(
        url="/api/messages",
        method="get"
    ),
    body=[
        # 页面内容组件
    ]
)
```

## 使用注意事项

1. **默认应用注册**：必须调用 `register_default_app()` 函数注册默认应用，否则会出现 "Default amis app not registered" 错误。

2. **页面路径**：页面路径必须以 `/` 开头，如 `/home`、`/message/message`。

3. **API 装饰器顺序**：使用 API 包装装饰器时，建议按照 `@amis_wrap()`、`@amis_paginate()`、`@amis_filter()`、`@amis_search()` 的顺序使用。

4. **上传接口**：当前默认上传实现基于 Django 的 `default_storage`，不会自动创建文件元数据模型记录；文件上传返回存储路径，图片上传返回可访问 URL。

## 依赖说明

- Python 3.11 至 3.12
- Django 3.2+
- Pydantic 2.0+
- Django Ninja (可选)

## 开发

### 安装依赖

```bash
uv sync
```

### 运行测试

```bash
cd src
uv run python manage.py test amis_python.tests.test_views -v 2
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
│   ├── amis_python/        # 主要的 Python 包
│   ├── manage.py           # Django 测试入口
│   ├── test_settings.py    # 测试 settings
│   └── test_urls.py        # 测试 URL 挂载
├── test_django/            # Django 测试项目
└── README.md               # 项目文档
```

说明：

- 写 CRUD 页面时，优先使用 `src/amis_python/crud/`
- `builder/` 仍然可用，但不是当前 CRUD 主推荐路线
- 涉及 Django API 链路的验证，优先使用 `src/manage.py test`

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT

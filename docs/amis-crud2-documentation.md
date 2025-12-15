# CRUD2 组件文档

CRUD2 是 AMIS 框架中用于实现增删改查功能的核心组件，是 CRUD 组件的升级版，提供了更强大的功能和更好的使用体验。

## 目录

- [概述](#概述)
- [基本用法](#基本用法)
- [配置项](#配置项)
- [数据展示模式](#数据展示模式)
- [筛选和搜索](#筛选和搜索)
- [工具栏配置](#工具栏配置)
- [分页配置](#分页配置)
- [事件处理](#事件处理)
- [示例代码](#示例代码)
- [注意事项](#注意事项)

## 概述

CRUD2 组件是一个功能强大的数据容器组件，支持以下特性：

- **多种展示模式**：表格（table2）、卡片（cards）、列表（list）
- **完整的数据操作**：增、删、改、查
- **灵活的筛选功能**：简单查询、高级查询、模糊查询
- **批量操作**：批量编辑、批量删除
- **分页支持**：传统分页、加载更多、前端分页
- **数据选择**：单选、多选、跨页选择
- **工具栏自定义**：头部和底部工具栏可自由配置
- **事件系统**：丰富的事件回调和动作支持

## 基本用法

### 最简单的 CRUD2 配置

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/data/list",
  "columns": [
    {
      "name": "id",
      "label": "ID"
    },
    {
      "name": "name",
      "label": "名称"
    },
    {
      "name": "status",
      "label": "状态"
    }
  ]
}
```

## 配置项

### 基础配置

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| type | string | 'crud2' | 组件类型，必须设置为 'crud2' |
| mode | string | 'table2' | 展示模式：'table2'、'cards'、'list' |
| api | string\|object | - | 数据接口配置 |
| source | string | - | 静态数据源，支持变量表达式 |
| primaryField | string | 'id' | 主键字段名 |

### 数据加载配置

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| loadType | string | 'pagination' | 数据加载模式：''、'pagination'、'more' |
| perPage | number | 10 | 每页显示条数（加载更多模式） |
| loadDataOnce | boolean | false | 是否前端分页模式 |
| syncLocation | boolean | true | 是否同步查询条件到地址栏 |
| pageField | string | 'page' | 页码字段名 |
| perPageField | string | 'perPage' | 每页条数字段名 |

### 选择配置

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| selectable | boolean | false | 是否可选择行 |
| multiple | boolean | false | 是否支持多选 |
| showSelection | boolean | true | 是否显示已选数据区域 |
| keepItemSelectionOnPageChange | boolean | false | 翻页时是否保留选择 |

### 接口配置

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| quickSaveApi | string\|object | - | 快速编辑批量保存接口 |
| quickSaveItemApi | string\|object | - | 单行快速编辑保存接口 |
| saveOrderApi | string\|object | - | 拖拽排序保存接口 |

### 样式配置

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| autoFillHeight | boolean | false | 是否自动填充高度 |
| headerToolbar | array | - | 头部工具栏配置 |
| footerToolbar | array | - | 底部工具栏配置 |
| headerToolbarClassName | string | - | 头部工具栏 CSS 类名 |
| footerToolbarClassName | string | - | 底部工具栏 CSS 类名 |

### 高级配置

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| interval | number | - | 自动刷新间隔（毫秒） |
| silentPolling | boolean | false | 是否静默拉取数据 |
| stopAutoRefreshWhen | string | - | 停止自动刷新的条件表达式 |
| pullRefresh | object | - | 下拉刷新配置（移动端） |
| autoJumpToTopOnPagerChange | boolean | true | 翻页时是否自动回到顶部 |

## 数据展示模式

### 表格模式（table2）

表格模式是最常用的展示方式，支持排序、筛选、分页等功能。

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "columns": [
    {
      "name": "id",
      "label": "ID",
      "sortable": true
    },
    {
      "name": "username",
      "label": "用户名",
      "sortable": true
    },
    {
      "name": "email",
      "label": "邮箱"
    },
    {
      "name": "status",
      "label": "状态",
      "type": "mapping",
      "map": {
        "0": "禁用",
        "1": "启用"
      }
    },
    {
      "name": "operation",
      "label": "操作",
      "type": "operation",
      "buttons": [
        {
          "type": "button",
          "label": "编辑",
          "level": "link",
          "actionType": "dialog",
          "dialog": {
            "title": "编辑用户",
            "body": {
              "type": "form",
              "api": "put:/api/users/${id}",
              "initApi": "get:/api/users/${id}",
              "body": [
                {
                  "type": "input-text",
                  "name": "username",
                  "label": "用户名"
                },
                {
                  "type": "input-text",
                  "name": "email",
                  "label": "邮箱"
                }
              ]
            }
          }
        },
        {
          "type": "button",
          "label": "删除",
          "level": "link",
          "actionType": "ajax",
          "confirmText": "确定要删除该用户吗？",
          "api": "delete:/api/users/${id}"
        }
      ]
    }
  ]
}
```

### 卡片模式（cards）

卡片模式适合展示富媒体内容或需要更大展示空间的场景。

```json
{
  "type": "crud2",
  "mode": "cards",
  "api": "/api/products/list",
  "card": {
    "type": "card2",
    "body": [
      {
        "type": "container",
        "body": [
          {
            "type": "tpl",
            "tpl": "${name}",
            "inline": false,
            "wrapperComponent": "h3",
            "style": {
              "margin": "0 0 10px 0"
            }
          },
          {
            "type": "tpl",
            "tpl": "价格：￥${price}",
            "inline": true,
            "style": {
              "color": "#ff6600",
              "fontSize": "18px",
              "fontWeight": "bold"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "tpl",
            "tpl": "${description}",
            "inline": false,
            "style": {
              "color": "#666"
            }
          }
        ]
      }
    ],
    "actions": [
      {
        "type": "button",
        "label": "查看详情",
        "actionType": "dialog",
        "dialog": {
          "title": "产品详情",
          "body": {
            "type": "form",
            "body": [
              {
                "type": "static-text",
                "name": "name",
                "label": "产品名称"
              },
              {
                "type": "static-text",
                "name": "price",
                "label": "价格"
              },
              {
                "type": "static-text",
                "name": "description",
                "label": "描述"
              }
            ]
          }
        }
      }
    ]
  }
}
```

### 列表模式（list）

列表模式适合文本内容较多的场景。

```json
{
  "type": "crud2",
  "mode": "list",
  "api": "/api/articles/list",
  "listItem": {
    "body": [
      {
        "type": "container",
        "body": [
          {
            "type": "tpl",
            "tpl": "${title}",
            "inline": false,
            "wrapperComponent": "h3",
            "style": {
              "margin": "0 0 10px 0"
            }
          },
          {
            "type": "tpl",
            "tpl": "作者：${author} | 发布时间：${publishTime}",
            "inline": false,
            "style": {
              "color": "#999",
              "fontSize": "12px",
              "marginBottom": "10px"
            }
          },
          {
            "type": "tpl",
            "tpl": "${summary}",
            "inline": false,
            "style": {
              "color": "#666",
              "lineHeight": "1.6"
            }
          }
        ]
      }
    ],
    "actions": [
      {
        "type": "button",
        "label": "阅读全文",
        "level": "link",
        "actionType": "url",
        "url": "/article/${id}",
        "blank": true
      }
    ]
  }
}
```

## 筛选和搜索

### 简单查询（SimpleQuery）

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "filter": {
    "type": "form",
    "title": "查询条件",
    "mode": "horizontal",
    "columnCount": 3,
    "body": [
      {
        "type": "input-text",
        "name": "username",
        "label": "用户名",
        "placeholder": "请输入用户名"
      },
      {
        "type": "select",
        "name": "status",
        "label": "状态",
        "options": [
          {
            "label": "全部",
            "value": ""
          },
          {
            "label": "启用",
            "value": "1"
          },
          {
            "label": "禁用",
            "value": "0"
          }
        ]
      },
      {
        "type": "input-date-range",
        "name": "createTime",
        "label": "创建时间",
        "placeholder": "请选择创建时间范围"
      }
    ],
    "actions": [
      {
        "type": "reset",
        "label": "重置"
      },
      {
        "type": "submit",
        "level": "primary",
        "label": "查询"
      }
    ]
  },
  "columns": [
    // ... 列配置
  ]
}
```

### 模糊查询（FuzzyQuery）

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "headerToolbar": [
    {
      "type": "flex",
      "direction": "row",
      "justify": "flex-start",
      "alignItems": "stretch",
      "items": [
        {
          "type": "container",
          "align": "left",
          "behavior": ["Insert", "BulkEdit", "BulkDelete"],
          "style": {
            "flexGrow": 1,
            "flex": "1 1 auto",
            "position": "static",
            "display": "flex",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            "alignItems": "stretch",
            "justifyContent": "flex-start",
            "flexBasis": "auto"
          }
        },
        {
          "type": "container",
          "align": "right",
          "behavior": ["FuzzyQuery"],
          "body": [
            {
              "type": "search-box",
              "name": "keywords",
              "placeholder": "请输入关键词搜索",
              "className": "m-r-xs"
            }
          ],
          "style": {
            "flexGrow": 1,
            "flex": "1 1 auto",
            "position": "static",
            "display": "flex",
            "flexBasis": "auto",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            "alignItems": "stretch",
            "justifyContent": "flex-end"
          }
        }
      ]
    }
  ],
  "columns": [
    // ... 列配置
  ]
}
```

### 高级查询（AdvancedQuery）

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "filter": {
    "type": "form",
    "title": "高级查询",
    "mode": "horizontal",
    "columnCount": 2,
    "behavior": ["AdvancedQuery"],
    "body": [
      {
        "type": "group",
        "body": [
          {
            "type": "input-text",
            "name": "username",
            "label": "用户名",
            "placeholder": "请输入用户名"
          },
          {
            "type": "input-text",
            "name": "email",
            "label": "邮箱",
            "placeholder": "请输入邮箱"
          }
        ]
      },
      {
        "type": "group",
        "body": [
          {
            "type": "select",
            "name": "status",
            "label": "状态",
            "options": [
              {
                "label": "全部",
                "value": ""
              },
              {
                "label": "启用",
                "value": "1"
              },
              {
                "label": "禁用",
                "value": "0"
              }
            ]
          },
          {
            "type": "input-date-range",
            "name": "createTime",
            "label": "创建时间",
            "placeholder": "请选择创建时间范围"
          }
        ]
      }
    ],
    "actions": [
      {
        "type": "reset",
        "label": "重置"
      },
      {
        "type": "submit",
        "level": "primary",
        "label": "查询"
      }
    ]
  },
  "columns": [
    // ... 列配置
  ]
}
```

## 工具栏配置

### 头部工具栏（headerToolbar）

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "headerToolbar": [
    {
      "type": "flex",
      "direction": "row",
      "justify": "flex-start",
      "alignItems": "stretch",
      "style": {
        "position": "static"
      },
      "items": [
        {
          "type": "container",
          "align": "left",
          "behavior": ["Insert", "BulkEdit", "BulkDelete"],
          "wrapperBody": false,
          "style": {
            "flexGrow": 1,
            "flex": "1 1 auto",
            "position": "static",
            "display": "flex",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            "alignItems": "stretch",
            "justifyContent": "flex-start",
            "flexBasis": "auto"
          },
          "body": [
            {
              "type": "button",
              "label": "新增",
              "level": "primary",
              "className": "m-r-xs",
              "behavior": "Insert",
              "onEvent": {
                "click": {
                  "actions": [
                    {
                      "actionType": "dialog",
                      "dialog": {
                        "type": "dialog",
                        "title": "新增用户",
                        "body": {
                          "type": "form",
                          "api": "post:/api/users",
                          "body": [
                            {
                              "type": "input-text",
                              "name": "username",
                              "label": "用户名"
                            },
                            {
                              "type": "input-text",
                              "name": "email",
                              "label": "邮箱"
                            }
                          ]
                        }
                      }
                    }
                  ]
                }
              }
            },
            {
              "type": "button",
              "label": "批量删除",
              "level": "danger",
              "behavior": "BulkDelete",
              "onEvent": {
                "click": {
                  "actions": [
                    {
                      "actionType": "ajax",
                      "api": "delete:/api/users/${ids|raw}",
                      "confirmText": "确定要批量删除选中的记录吗？"
                    }
                  ]
                }
              }
            }
          ]
        },
        {
          "type": "container",
          "align": "right",
          "behavior": ["FuzzyQuery"],
          "body": [
            {
              "type": "search-box",
              "name": "keywords",
              "placeholder": "请输入关键词搜索"
            }
          ],
          "style": {
            "flexGrow": 1,
            "flex": "1 1 auto",
            "position": "static",
            "display": "flex",
            "flexBasis": "auto",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            "alignItems": "stretch",
            "justifyContent": "flex-end"
          }
        }
      ]
    }
  ],
  "columns": [
    // ... 列配置
  ]
}
```

### 底部工具栏（footerToolbar）

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "footerToolbar": [
    {
      "type": "flex",
      "direction": "row",
      "justify": "flex-start",
      "alignItems": "stretch",
      "style": {
        "position": "static"
      },
      "items": [
        {
          "type": "container",
          "align": "left",
          "body": [
            {
              "type": "tpl",
              "tpl": "共 ${total} 条记录"
            }
          ],
          "style": {
            "flexGrow": 1,
            "flex": "1 1 auto",
            "position": "static",
            "display": "flex",
            "flexBasis": "auto",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            "alignItems": "stretch",
            "justifyContent": "flex-start"
          }
        },
        {
          "type": "container",
          "align": "right",
          "body": [
            {
              "type": "pagination",
              "behavior": "Pagination",
              "layout": ["total", "perPage", "pager"],
              "perPage": 10,
              "perPageAvailable": [10, 20, 50, 100],
              "align": "right"
            }
          ],
          "style": {
            "flexGrow": 1,
            "flex": "1 1 auto",
            "position": "static",
            "display": "flex",
            "flexBasis": "auto",
            "flexDirection": "row",
            "flexWrap": "nowrap",
            "alignItems": "stretch",
            "justifyContent": "flex-end"
          }
        }
      ]
    }
  ],
  "columns": [
    // ... 列配置
  ]
}
```

## 分页配置

### 传统分页模式

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "loadType": "pagination",
  "footerToolbar": [
    {
      "type": "pagination",
      "behavior": "Pagination",
      "layout": ["total", "perPage", "pager", "go"],
      "perPage": 10,
      "perPageAvailable": [10, 20, 50, 100],
      "align": "right"
    }
  ],
  "columns": [
    // ... 列配置
  ]
}
```

### 加载更多模式

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "loadType": "more",
  "perPage": 10,
  "footerToolbar": [
    {
      "type": "button",
      "behavior": "loadMore",
      "label": "加载更多",
      "onEvent": {
        "click": {
          "actions": [
            {
              "componentId": "crud2-id",
              "groupType": "component",
              "actionType": "loadMore"
            }
          ]
        }
      }
    }
  ],
  "columns": [
    // ... 列配置
  ]
}
```

### 前端分页模式

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "loadDataOnce": true,
  "loadType": "pagination",
  "footerToolbar": [
    {
      "type": "pagination",
      "behavior": "Pagination",
      "layout": ["total", "perPage", "pager"],
      "perPage": 10,
      "perPageAvailable": [10, 20, 50, 100],
      "align": "right"
    }
  ],
  "columns": [
    // ... 列配置
  ]
}
```

## 事件处理

### 支持的事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| selectedChange | 选择项改变时触发 | selectedItems, unSelectedItems |
| columnSort | 列排序时触发 | column, order |
| columnFilter | 列筛选时触发 | column, filter |
| columnSearch | 列搜索时触发 | column, search |
| columnToggled | 列显示/隐藏时触发 | columns |
| orderChange | 拖拽排序时触发 | moved, rows |
| rowClick | 行点击时触发 | row, index |
| rowDbClick | 行双击时触发 | row, index |
| rowMouseEnter | 鼠标进入行时触发 | row, index |
| rowMouseLeave | 鼠标离开行时触发 | row, index |
| selected | 行选中时触发 | row, index |

### 事件配置示例

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/users/list",
  "onEvent": {
    "selectedChange": {
      "actions": [
        {
          "actionType": "toast",
          "msg": "已选择 ${selectedItems|length} 项"
        }
      ]
    },
    "rowClick": {
      "actions": [
        {
          "actionType": "dialog",
          "dialog": {
            "title": "用户详情",
            "body": {
              "type": "form",
              "initApi": "get:/api/users/${row.id}",
              "body": [
                {
                  "type": "static-text",
                  "name": "username",
                  "label": "用户名"
                },
                {
                  "type": "static-text",
                  "name": "email",
                  "label": "邮箱"
                }
              ]
            }
          }
        }
      ]
    }
  },
  "columns": [
    // ... 列配置
  ]
}
```

### 动作（Actions）

CRUD2 组件支持以下动作：

| 动作名 | 说明 | 参数 |
|--------|------|------|
| search | 数据查询 | query: 查询条件 |
| loadMore | 加载更多数据 | - |
| startAutoRefresh | 启动自动刷新 | - |
| stopAutoRefresh | 停止自动刷新 | - |
| reload | 重新加载数据 | - |

### 动作调用示例

```json
{
  "type": "page",
  "body": [
    {
      "type": "button",
      "label": "刷新数据",
      "onEvent": {
        "click": {
          "actions": [
            {
              "componentId": "my-crud2",
              "groupType": "component",
              "actionType": "reload"
            }
          ]
        }
      }
    },
    {
      "type": "crud2",
      "id": "my-crud2",
      "mode": "table2",
      "api": "/api/users/list",
      "columns": [
        // ... 列配置
      ]
    }
  ]
}
```

## 示例代码

### 完整的 CRUD2 示例

```json
{
  "type": "page",
  "body": [
    {
      "type": "crud2",
      "id": "user-crud2",
      "mode": "table2",
      "dsType": "api",
      "syncLocation": false,
      "primaryField": "id",
      "loadType": "pagination",
      "api": {
        "url": "/api/users/list",
        "method": "post",
        "data": {
          "pageSize": 10,
          "pageNum": 1,
          "&": "$$"
        }
      },
      "filter": {
        "type": "form",
        "title": "用户查询",
        "mode": "horizontal",
        "columnCount": 3,
        "clearValueOnHidden": true,
        "behavior": ["SimpleQuery"],
        "body": [
          {
            "type": "input-text",
            "name": "username",
            "label": "用户名：",
            "placeholder": "请输入用户名"
          },
          {
            "type": "select",
            "name": "status",
            "label": "状态：",
            "options": [
              {
                "label": "全部",
                "value": ""
              },
              {
                "label": "启用",
                "value": "1"
              },
              {
                "label": "禁用",
                "value": "0"
              }
            ]
          },
          {
            "type": "input-date-range",
            "name": "createTime",
            "label": "创建时间：",
            "placeholder": "请选择创建时间范围"
          }
        ],
        "actions": [
          {
            "type": "reset",
            "label": "重置"
          },
          {
            "type": "submit",
            "level": "primary",
            "label": "查询"
          }
        ]
      },
      "headerToolbar": [
        {
          "type": "flex",
          "direction": "row",
          "justify": "flex-start",
          "alignItems": "stretch",
          "style": {
            "position": "static"
          },
          "items": [
            {
              "type": "container",
              "align": "left",
              "behavior": ["Insert", "BulkEdit", "BulkDelete"],
              "wrapperBody": false,
              "style": {
                "flexGrow": 1,
                "flex": "1 1 auto",
                "position": "static",
                "display": "flex",
                "flexDirection": "row",
                "flexWrap": "nowrap",
                "alignItems": "stretch",
                "justifyContent": "flex-start",
                "flexBasis": "auto"
              },
              "body": [
                {
                  "type": "button",
                  "label": "新增用户",
                  "level": "primary",
                  "className": "m-r-xs",
                  "behavior": "Insert",
                  "onEvent": {
                    "click": {
                      "actions": [
                        {
                          "actionType": "dialog",
                          "dialog": {
                            "type": "dialog",
                            "title": "新增用户",
                            "body": {
                              "type": "form",
                              "api": "post:/api/users",
                              "body": [
                                {
                                  "type": "input-text",
                                  "name": "username",
                                  "label": "用户名",
                                  "required": true
                                },
                                {
                                  "type": "input-text",
                                  "name": "email",
                                  "label": "邮箱",
                                  "required": true
                                },
                                {
                                  "type": "input-password",
                                  "name": "password",
                                  "label": "密码",
                                  "required": true
                                }
                              ]
                            }
                          }
                        }
                      ]
                    }
                  }
                }
              ]
            },
            {
              "type": "container",
              "align": "right",
              "behavior": ["FuzzyQuery"],
              "body": [
                {
                  "type": "search-box",
                  "name": "keywords",
                  "placeholder": "请输入关键词搜索"
                }
              ],
              "style": {
                "flexGrow": 1,
                "flex": "1 1 auto",
                "position": "static",
                "display": "flex",
                "flexBasis": "auto",
                "flexDirection": "row",
                "flexWrap": "nowrap",
                "alignItems": "stretch",
                "justifyContent": "flex-end"
              }
            }
          ]
        }
      ],
      "footerToolbar": [
        {
          "type": "flex",
          "direction": "row",
          "justify": "flex-start",
          "alignItems": "stretch",
          "style": {
            "position": "static"
          },
          "items": [
            {
              "type": "container",
              "align": "left",
              "body": [
                {
                  "type": "tpl",
                  "tpl": "共 ${total} 条记录"
                }
              ],
              "style": {
                "flexGrow": 1,
                "flex": "1 1 auto",
                "position": "static",
                "display": "flex",
                "flexBasis": "auto",
                "flexDirection": "row",
                "flexWrap": "nowrap",
                "alignItems": "stretch",
                "justifyContent": "flex-start"
              }
            },
            {
              "type": "container",
              "align": "right",
              "body": [
                {
                  "type": "pagination",
                  "behavior": "Pagination",
                  "layout": ["total", "perPage", "pager"],
                  "perPage": 10,
                  "perPageAvailable": [10, 20, 50, 100],
                  "align": "right"
                }
              ],
              "style": {
                "flexGrow": 1,
                "flex": "1 1 auto",
                "position": "static",
                "display": "flex",
                "flexBasis": "auto",
                "flexDirection": "row",
                "flexWrap": "nowrap",
                "alignItems": "stretch",
                "justifyContent": "flex-end"
              }
            }
          ]
        }
      ],
      "columns": [
        {
          "name": "id",
          "label": "ID",
          "type": "text",
          "width": 80,
          "sortable": true
        },
        {
          "name": "username",
          "label": "用户名",
          "type": "text",
          "sortable": true
        },
        {
          "name": "email",
          "label": "邮箱",
          "type": "text"
        },
        {
          "name": "status",
          "label": "状态",
          "type": "mapping",
          "map": {
            "0": "<span class='label label-danger'>禁用</span>",
            "1": "<span class='label label-success'>启用</span>"
          }
        },
        {
          "name": "createTime",
          "label": "创建时间",
          "type": "datetime",
          "sortable": true
        },
        {
          "name": "operation",
          "label": "操作",
          "type": "operation",
          "buttons": [
            {
              "type": "button",
              "label": "编辑",
              "level": "link",
              "actionType": "dialog",
              "dialog": {
                "title": "编辑用户",
                "body": {
                  "type": "form",
                  "api": "put:/api/users/${id}",
                  "initApi": "get:/api/users/${id}",
                  "body": [
                    {
                      "type": "input-text",
                      "name": "username",
                      "label": "用户名",
                      "required": true
                    },
                    {
                      "type": "input-text",
                      "name": "email",
                      "label": "邮箱",
                      "required": true
                    },
                    {
                      "type": "select",
                      "name": "status",
                      "label": "状态",
                      "options": [
                        {
                          "label": "启用",
                          "value": "1"
                        },
                        {
                          "label": "禁用",
                          "value": "0"
                        }
                      ]
                    }
                  ]
                }
              }
            },
            {
              "type": "button",
              "label": "删除",
              "level": "link",
              "actionType": "ajax",
              "confirmText": "确定要删除该用户吗？",
              "api": "delete:/api/users/${id}"
            }
          ]
        }
      ],
      "rowSelection": {
        "rowClick": true,
        "fixed": true,
        "columnWidth": 40
      },
      "selectable": true,
      "multiple": true,
      "showSelection": true,
      "keepItemSelectionOnPageChange": false,
      "autoFillHeight": true,
      "bordered": true,
      "sticky": true,
      "onEvent": {
        "selectedChange": {
          "actions": [
            {
              "actionType": "toast",
              "msg": "已选择 ${selectedItems|length} 项"
            }
          ]
        }
      }
    }
  ]
}
```

## 注意事项

### 1. 主键字段配置

CRUD2 组件需要配置 `primaryField` 来标识每行数据的唯一性，默认为 `id`。如果数据源的主键字段不是 `id`，需要显式配置：

```json
{
  "type": "crud2",
  "primaryField": "userId",
  // ... 其他配置
}
```

### 2. 同步地址栏

`syncLocation` 默认值为 `true`，会将查询条件和分页信息同步到地址栏。当页面中有多个 CRUD2 组件时，建议只保留一个同步地址栏，避免相互影响：

```json
{
  "type": "crud2",
  "syncLocation": false,
  // ... 其他配置
}
```

### 3. 跨页选择

如果需要跨页选择数据，需要开启 `keepItemSelectionOnPageChange`：

```json
{
  "type": "crud2",
  "selectable": true,
  "multiple": true,
  "keepItemSelectionOnPageChange": true,
  // ... 其他配置
}
```

### 4. 前端分页

当数据量不大时，可以使用前端分页模式：

```json
{
  "type": "crud2",
  "api": "/api/data/list",
  "loadDataOnce": true,
  "loadType": "pagination",
  // ... 其他配置
}
```

### 5. 自动刷新

CRUD2 支持定时自动刷新数据：

```json
{
  "type": "crud2",
  "api": "/api/data/list",
  "interval": 5000,
  "silentPolling": true,
  "stopAutoRefreshWhen": "${total > 100}",
  // ... 其他配置
}
```

### 6. 下拉刷新（移动端）

CRUD2 支持移动端下拉刷新：

```json
{
  "type": "crud2",
  "api": "/api/data/list",
  "loadType": "more",
  "pullRefresh": {
    "disabled": false,
    "showIcon": true,
    "showText": true,
    "iconType": "loading-outline",
    "color": "#777777",
    "dataAppendTo": "bottom",
    "contentText": {
      "normalText": "点击加载更多",
      "pullingText": "加载中...",
      "loosingText": "释放立即刷新",
      "loadingText": "加载中...",
      "successText": "加载成功",
      "completedText": "没有更多数据了"
    }
  },
  // ... 其他配置
}
```

### 7. 自定义列

CRUD2 支持动态列配置，可以通过 `columns` 配置实现：

```json
{
  "type": "crud2",
  "mode": "table2",
  "api": "/api/data/list",
  "columns": [
    {
      "name": "id",
      "label": "ID",
      "sortable": true,
      "toggled": true
    },
    {
      "name": "name",
      "label": "名称",
      "sortable": true,
      "quickEdit": {
        "type": "input-text",
        "saveImmediately": true
      }
    },
    {
      "name": "status",
      "label": "状态",
      "type": "mapping",
      "map": {
        "0": "禁用",
        "1": "启用"
      }
    }
  ]
}
```

### 8. 数据格式

CRUD2 期望的数据格式：

```json
{
  "status": 0,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "status": 1,
        "createTime": "2024-01-01 12:00:00"
      }
    ],
    "total": 100
  }
}
```

### 9. 性能优化

- 对于大数据量场景，建议使用后端分页
- 开启 `autoFillHeight` 可以优化表格高度
- 使用 `loadDataOnce` 可以优化小数据量的分页体验
- 合理配置 `perPage` 避免一次性加载过多数据

### 10. 调试

开启调试模式可以查看更多信息：

```json
{
  "type": "crud2",
  "api": "/api/data/list",
  "debug": true,
  // ... 其他配置
}
```

## 总结

CRUD2 是 AMIS 框架中功能最强大的组件之一，提供了完整的增删改查功能。通过灵活的配置，可以满足各种复杂的数据管理需求。建议在实际项目中根据具体场景选择合适的展示模式和配置项。

---

**文档版本**: 1.0  
**最后更新**: 2025-12-15  
**AMIS 版本**: 6.x+

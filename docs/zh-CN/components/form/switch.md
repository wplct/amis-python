---
title: Switch 开关
description:
type: 0
group: null
menuName: Switch 开关
icon:
order: 57
---

## 基本使用

```schema: scope="body"
{
    "type": "form",
    "api": "/api/mock2/form/saveForm",
    "body": [
        {
            "name": "switch",
            "type": "switch",
            "label": "开关"
        }
    ]
}
```

## 不同大小

```schema: scope="body"
{
    "type": "form",
    "api": "/api/mock2/form/saveForm",
    "body": [
        {
            "name": "switch-sm",
            "type": "switch",
            "label": "小尺寸",
            "size": "sm"
        },
        {
            "name": "switch-md",
            "type": "switch",
            "label": "中尺寸",
            "size": "md"
        },
        {
            "name": "switch-lg",
            "type": "switch",
            "label": "大尺寸",
            "size": "lg"
        }
    ]
}
```

## 不同状态

### 默认选中

```schema: scope="body"
{
    "type": "form",
    "api": "/api/mock2/form/saveForm",
    "body": [
        {
            "name": "switch-checked",
            "type": "switch",
            "label": "默认选中",
            "checked": true
        }
    ]
}
```

### 禁用状态

```schema: scope="body"
{
    "type": "form",
    "api": "/api/mock2/form/saveForm",
    "body": [
        {
            "name": "switch-disabled",
            "type": "switch",
            "label": "禁用",
            "disabled": true
        },
        {
            "name": "switch-disabled-checked",
            "type": "switch",
            "label": "禁用且选中",
            "disabled": true,
            "checked": true
        }
    ]
}
```

## 自定义文本

```schema: scope="body"
{
    "type": "form",
    "api": "/api/mock2/form/saveForm",
    "body": [
        {
            "name": "switch-custom-text",
            "type": "switch",
            "label": "自定义文本",
            "onText": "开启",
            "offText": "关闭"
        }
    ]
}
```

## 自定义颜色

```schema: scope="body"
{
    "type": "form",
    "api": "/api/mock2/form/saveForm",
    "body": [
        {
            "name": "switch-custom-color",
            "type": "switch",
            "label": "自定义颜色",
            "onBackgroundColor": "#10B981",
            "offBackgroundColor": "#EF4444"
        }
    ]
}
```

## 自定义值

```schema: scope="body"
{
    "type": "form",
    "api": "/api/mock2/form/saveForm",
    "debug": true,
    "body": [
        {
            "name": "switch-custom-value",
            "type": "switch",
            "label": "自定义值",
            "checkedValue": "enabled",
            "unCheckedValue": "disabled"
        }
    ]
}
```

## 属性表

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| type | `string` | `"switch"` | 指定为开关组件 |
| checked | `boolean` | `false` | 是否默认选中 |
| disabled | `boolean` | `false` | 是否禁用 |
| checkedValue | `any` | `true` | 选中时的值 |
| unCheckedValue | `any` | `false` | 未选中时的值 |
| size | `"sm" | "md" | "lg"` | `"md"` | 开关大小 |
| onText | `string` | `"开启"` | 选中时显示的文本 |
| offText | `string` | `"关闭"` | 未选中时显示的文本 |
| onBorderColor | `string` | | 选中时边框颜色 |
| offBorderColor | `string` | | 未选中时边框颜色 |
| onBackgroundColor | `string` | | 选中时背景颜色 |
| offBackgroundColor | `string` | | 未选中时背景颜色 |

## 事件表

| 事件名称 | 事件参数 | 说明 |
| --- | --- | --- |
| change | `value: any` 组件的值 | 开关状态变化时触发 |

### change

```schema: scope="body"
{
    "type": "form",
    "debug": true,
    "body": [
        {
            "name": "switch-change",
            "type": "switch",
            "label": "开关变化事件",
            "onEvent": {
                "change": {
                    "actions": [
                        {
                            "actionType": "toast",
                            "args": {
                                "msg": "开关状态变为: ${event.data.value}"
                            }
                        }
                    ]
                }
            }
        }
    ]
}
```

## 动作表

| 动作名称 | 动作配置 | 说明 |
| --- | --- | --- |
| toggle | - | 切换开关状态 |
| checked | `checked: boolean` | 设置开关为选中或未选中状态 |
| disable | `disabled: boolean` | 设置开关为禁用或启用状态 |

### toggle

```schema: scope="body"
{
    "type": "form",
    "debug": true,
    "body": [
        {
            "name": "switch-toggle",
            "id": "switch-toggle",
            "type": "switch",
            "label": "切换开关",
            "value": true
        },
        {
            "type": "button",
            "label": "切换状态",
            "onEvent": {
                "click": {
                    "actions": [
                        {
                            "actionType": "toggle",
                            "componentId": "switch-toggle"
                        }
                    ]
                }
            }
        }
    ]
}
```

### checked

```schema: scope="body"
{
    "type": "form",
    "debug": true,
    "body": [
        {
            "name": "switch-checked-action",
            "id": "switch-checked-action",
            "type": "switch",
            "label": "设置选中状态",
            "value": false
        },
        {
            "type": "button",
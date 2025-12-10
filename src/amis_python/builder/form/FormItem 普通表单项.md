**表单项** 是组成一个表单的基本单位，它具有的一些特性会帮助我们更好地实现表单操作。

> 所有派生自`FormItem`的组件，都具有`FormItem`的特性。

## 基本用法

最基本的表单项配置像这样：

-   `name`: **必填属性**，标识表单数据域中，当前表单项值的`key`，这个 name 可以是深层结构，比如 `aa.bb`
-   `type`: **必填属性**，标识表单项类型
-   `label`: 标识表单项的标签

> 所有表单项都只可以配置在`form`组件中，即`form`的`body`属性中。

## 表单项展示

### 内联模式

通过配置`"mode": "inline"`，标识当前表单项使用内联模式。

### 表单项尺寸

可以配置`size`，来调整表单项的尺寸，支持`'xs' | 'sm' | 'md' | 'lg' | 'full'`，如下：

> 不同组件的`size`效果可能会有所不同，具体请参考对应的组件文档。

### 表单项标签

设置`label`属性来配置表单项标签。

当表单为水平布局时，左边即便是不设置`label`为了保持对齐也会留空，如果想要去掉空白，请设置成`false`。

### 表单项标签提示

配置`labelRemark`可以实现标签描述提示

其它配置请参考 [Remark](https://aisuda.bce.baidu.com/amis/zh-CN/components/remark)。

### 配置禁用

##### 静态配置

通过配置`"disabled": true`来禁用表单项

##### 通过条件配置是否禁用

你也通过[表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression)配置`disabledOn`，来实现在某个条件下禁用当前表单项.

### 配置显隐

##### 静态配置

通过配置`"hidden": true`或者`"visible": false`来禁用表单项

上例中的`text2`被隐藏了。

##### 通过条件配置显隐

你也通过[表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression)配置`hiddenOn`，来实现在某个条件下禁用当前表单项.

> `visible`和`hidden`，`visibleOn`和`hiddenOn`除了判断逻辑相反以外，没有任何区别

### 配置静态展示

> 2.4.0 及以上版本

##### 静态配置

通过配置`"static": true`来将表单项以静态形式展示  
可以在[示例页](https://aisuda.bce.baidu.com/amis/examples/form/switchDisplay)查看支持静态展示的表单项的展示方式

##### 通过条件配置静态/输入态

也可以通过[表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression)配置`staticOn`，来实现在某个条件下将当前表单项状态的的自动切换.

##### 自定义展示态的展示方式

通过配置`staticSchema`，可以自定义静态展示时的展示方式

##### 限制选择器类组件的展示数量

下拉选择器、多选框等组件，当选项过多静态展示时，若全部展示会占用页面很多空间，所以默认进行了限制（10 个）  
可以通过配置`staticSchema.limit`，可以自定义静态展示时的数量

##### 通过事件动作切换表单项状态

也支持使用 事件动作 切换表单项的 输入态和展示态（静态），也可以使用动作对整个表单进行状态切换

##### 表单项静态展示优先级

1.  表单项配置为`static: true` 时，始终保持静态展示；

2.  表单项配置为`static: false` 或 `不配置` 时，跟随父表单的状态；

3.  使用 `事件动作` 切换表单项 的 静态/展示态，优先级最高，将无视 `schema` 配置

## 表单项值

表单项值，即表单项通过用户交互发生变化后，更新表单数据域中同`name`变量值.

如上例，更改姓名表单项值，可以改变表单数据域中`name`变量的值。

也支持链式配置 `name`属性，例如：`aaa.bbb`

观察上例，这样更改表单项值，会改变数据域中`person.name`的值

```
{
  "person": {
    "name": "xxx"
  }
}
```

## 配置默认值

通过配置`value`属性，可以设置表单项的默认值。

> 1.10.0 及之后版本（备注：可通过 1.9.1-beta.12 及之后版本提前试用）

`value`支持表达式，也就是说可以直接配置类似于这样的语法：`${xxx}`，如果想要获取当前数据域中的某个变量，可以设置该表单项`value`为`${name1}`，如下：

`value`也支持表达式运算，可以配置类似于这样的语法：`${num1 + 2}`，如下：

`value`表达式支持[namespace](https://aisuda.bce.baidu.com/amis/docs/concepts/data-mapping#namespace)，可以配置类似于这样的语法：`${window:document.title}`，意思是从全局变量中取页面的标题。如下：

**tip：** value 表达式（`${xxx}`）支持 模板字符串、链式取值、过滤器，详细用法参考[数据映射](https://aisuda.bce.baidu.com/amis/docs/concepts/data-mapping)。

我们也可以不设置 value 表达式，通过 name 来映射当前数据域中某个字段。比如我们表单数据域中有变量`"text1": "hello world!"`，然后我们设置表达项`"name": "text1"`，这样就可以自动映射值了。如下：

关于优先级问题，当我们同时设置了 value 表达式`${xxx}`和`name`值映射，会优先使用 value 表达式`${xxx}`。只有当 value 为普通字符串`非${xxx}`时，才会使用`name`值映射。如下：

**tip：** 默认在解析表达式时，遇到`$`字符会尝试去解析该变量并替换成对应变量，如果你想输出纯文本`"${xxx}"`，那么需要在`$`前加转义字符`"\\"`，即`"\\${xxx}"`，如下所示：

## 隐藏时删除表单项值

默认情况下，在通过 `hiddenOn` 或 `visibleOn` 配置显隐交互时，被隐藏的表单项值，不会在当前表单数据域中删除，例如：

观察上例，在调整 `number` 数量大于 1 时，`文本` 表单项会隐藏，但是对应的表单数据域中的 `text` 变量值仍存在。

如果想要实现隐藏表单项后，在当前表单数据域中删除该表单项对应的值，那么可以在当前表单项上配置 `"clearValueOnHidden": true`。

再次观察上例，当 `文本` 表单项隐藏时，对应的 `text` 变量也会被删除掉。

> 注意: 如果有其他同 name 的表达项的存在，即使其他表单项值没有隐藏，也会在数据域中删掉该值。

## 表单项必填

### 静态配置

通过配置`"required": true`来标识该表单项为必填。

### 满足条件校验必填

你也通过[表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression)配置`requiredOn`，来实现在某个条件下使当前表单项必填。

## 格式校验

可以配置`validations`属性，指定校验当前表单项值的格式

可以通过对象形式配置

同样也可以配置多个格式校验，按顺序进行校验，中途校验不通过就会终止

### 字符串形式（不推荐）

也可以配置字符串形式来指定，如下例，输入不合法的值，点击提交会报错并显示报错信息。（注意日期时间类的校验规则不支持字符串形式）

也可以指定多个格式校验，中间用`逗号`分隔。

如果需要配置参数，例如显示最大值或最小值，则在格式标识符后`:`和参数

### 自定义校验信息

amis 会有默认的报错信息，如果你想自定义校验信息，配置`validationErrors`属性

如果需要获取当前格式校验配置的参数，可以使用`$1`

默认的校验信息如下，可以直接配置文字，也可用多语言中的 key。参考：[https://github.com/baidu/amis/blob/master/packages/amis-ui/src/locale/zh-CN.ts#L250](https://github.com/baidu/amis/blob/master/packages/amis-ui/src/locale/zh-CN.ts#L250)

```
{
  isEmail: 'validate.isEmail',
  isRequired: 'validate.isRequired',
  isUrl: 'validate.isUrl',
  isInt: 'validate.isInt',
  isAlpha: 'validate.isAlpha',
  isNumeric: 'validate.isNumeric',
  isAlphanumeric: 'validate.isAlphanumeric',
  isFloat: 'validate.isFloat',
  isWords: 'validate.isWords',
  isUrlPath: 'validate.isUrlPath',
  matchRegexp: 'validate.matchRegexp',
  minLength: 'validate.minLength',
  maxLength: 'validate.maxLength',
  maximum: 'validate.maximum',
  lt: 'validate.lt',
  minimum: 'validate.minimum',
  gt: 'validate.gt',
  isJson: 'validate.isJson',
  isLength: 'validate.isLength',
  notEmptyString: 'validate.notEmptyString',
  equalsField: 'validate.equalsField',
  equals: 'validate.equals',
  isPhoneNumber: 'validate.isPhoneNumber',
  isTelNumber: 'validate.isTelNumber',
  isZipcode: 'validate.isZipcode',
  isId: 'validate.isId',
  /* 日期时间相关校验规则 2.2.0 及以上版本生效 */
  isDateTimeSame: 'validate.isDateTimeSame',
  isDateTimeBefore: 'validate.isDateTimeBefore',
  isDateTimeAfter: 'validate.isDateTimeAfter',
  isDateTimeSameOrBefore: 'validate.isDateTimeSameOrBefore',
  isDateTimeSameOrAfter: 'validate.isDateTimeSameOrAfter',
  isDateTimeBetween: 'validate.isDateTimeBetween',
  isTimeSame: 'validate.isTimeSame',
  isTimeBefore: 'validate.isTimeBefore',
  isTimeAfter: 'validate.isTimeAfter',
  isTimeSameOrBefore: 'validate.isTimeSameOrBefore',
  isTimeSameOrAfter: 'validate.isTimeSameOrAfter',
  isTimeBetween: 'validate.isTimeBetween',
  isVariableName: 'validate.isVariableName'
}
```

### 表单项值发生变化即校验

默认校验是当进行行为操作时，对表单项进行校验，如果你想每次表单项的值发生变化的时候就校验，请配置`"validateOnChange": true`

### 支持的格式校验

| 规则名称 | 说明 | 定义 | 版本 |
| --- | --- | --- | --- |
| `isEmail` | 必须是 Email。 | `(value: any) => boolean` |  |
| `isUrl` | 必须是 Url。 | `(value: any) => boolean` |  |
| `isNumeric` | 必须是 数值。 | `(value: any) => boolean` |  |
| `isAlpha` | 必须是 字母。 | `(value: any) => boolean` |  |
| `isAlphanumeric` | 必须是 字母或者数字。 | `(value: any) => boolean` |  |
| `isInt` | 必须是 整形。 | `(value: any) => boolean` |  |
| `isFloat` | 必须是 浮点形。 | `(value: any) => boolean` |  |
| `isLength:length` | 是否长度正好等于设定值。 | `(value: any) => boolean` |  |
| `minLength:length` | 最小长度。 | `(value: any, length: number) => boolean` |  |
| `maxLength:length` | 最大长度。 | `(value: any, length: number) => boolean` |  |
| `maximum:number` | 最大值。 | `(value: any, maximum: number) => boolean` |  |
| `minimum:number` | 最小值。 | `(value: any, minimum:number) => boolean` |  |
| `equals:xxx` | 当前值必须完全等于 xxx。 | `(value: any, targetValue: any) => boolean` |  |
| `equalsField:xxx` | 当前值必须与 xxx 变量值一致。 | `(value: any, field: string) => boolean` |  |
| `isJson` | 是否是合法的 Json 字符串。 | `(value: any) => boolean` |  |
| `isUrlPath` | 是 url 路径。 | `(value: any) => boolean` |  |
| `isPhoneNumber` | 是否为合法的手机号码 | `(value: any) => boolean` |  |
| `isTelNumber` | 是否为合法的电话号码 | `(value: any) => boolean` |  |
| `isZipcode` | 是否为邮编号码 | `(value: any) => boolean` |  |
| `isId` | 是否为身份证号码，支持 18 位和 15 位验证，单个验证请使用 `isId18` / `isId15` | `(value: any) => boolean` |  |
| `matchRegexp:/foo/` | 必须命中某个正则。 | `(value: any, regexp: string | RegExp) => boolean` |  |
| `matchRegexp${n}:/foo/` | 必须命中某个正则。 设置正则表达式时属性名需以 `matchRegexp` 开头，`n`支持`1-9`，且 `validations` 及 `validationsErrors` 中属性名需匹配。 | `(value: any, regexp: string | RegExp) => boolean` |  |
| `isDateTimeSame` | 日期和目标日期相同，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetDate: any, granularity?: string) => boolean` | `2.2.0` |
| `isDateTimeBefore` | 日期早于目标日期，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetDate: any, granularity?: string) => boolean` | `2.2.0` |
| `isDateTimeAfter` | 日期晚于目标日期，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetDate: any, granularity?: string) => boolean` | `2.2.0` |
| `isDateTimeSameOrBefore` | 日期早于目标日期或和目标日期相同，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetDate: any, granularity?: string) => boolean` | `2.2.0` |
| `isDateTimeSameOrAfter` | 日期晚于目标日期或和目标日期相同，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetDate: any, granularity?: string) => boolean` | `2.2.0` |
| `isDateTimeBetween` | 日期处于目标日期范围，支持指定粒度和区间的开闭形式，默认到毫秒 `millisecond`，左右开区间`'()'` | `(value: any, lhs: any, rhs: any, granularity?: string, inclusivity?: '()' | '[)' | '(]' | '[]') => boolean` | `2.2.0` |
| `isTimeSame` | 时间和目标时间相同，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetTime: any, granularity?: string) => boolean` | `2.2.0` |
| `isTimeBefore` | 时间早于目标时间，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetTime: any, granularity?: string) => boolean` | `2.2.0` |
| `isTimeAfter` | 时间晚于目标时间，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetTime: any, granularity?: string) => boolean` | `2.2.0` |
| `isTimeSameOrBefore` | 时间早于目标时间或和目标时间相同，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetTime: any, granularity?: string) => boolean` | `2.2.0` |
| `isTimeSameOrAfter` | 时间晚于目标时间或和目标时间相同，支持指定粒度，默认到毫秒 `millisecond` | `(value: any, targetTime: any, granularity?: string) => boolean` | `2.2.0` |
| `isTimeBetween` | 时间处于目标时间范围，支持指定粒度和区间的开闭形式，默认到毫秒 `millisecond`，左右开区间`'()'` | `(value: any, lhs: any, rhs: any, granularity?: string, inclusivity?: '()' | '[)' | '(]' | '[]') => boolean` | `2.2.0` |
| `isVariableName` | 是否为合法的变量名，默认规则为 `/^[a-zA-Z_]+[a-zA-Z0-9]*$/` 可以自己指定如 `{isVariableName: /^a.*$/}` | `(value: any) => boolean` | `2.5.0` |

#### 验证只允许 http 协议的 url 地址

> 1.4.0 及以上版本

isUrl 可以配置如下参数

-   schemes 协议，默认是为： `['http', 'https', 'ftp', 'sftp']`
-   allowLocal 是否允许填写本地地址
-   allowDataUrl 是否允许 dataUrl

### 自定义校验函数

可以自己写代码扩展表单验证，请参考 [这里](https://aisuda.bce.baidu.com/amis/zh-CN/docs/extend/addon#%E6%89%A9%E5%B1%95%E8%A1%A8%E5%8D%95%E9%AA%8C%E8%AF%81)

## 服务端校验

### 通过表单提交接口

也可以通过表单提交接口返回错误信息，实现服务端校验

点击提交，api 接口返回中，需要在 errors 变量中，返回某个表单项的报错信息，`key`值为该表单项的`name`值。

如上，接口返回的格式如下，提交后，`test2`表达项会显示报错信息

```
{
  "status": 422, // 返回非0状态码
  "msg": "",
  "errors": {
    "test2": "服务器端说，这个有错误。"
  },
  "data": null
}
```

#### Combo 校验

Combo 类型的表单项，要实现服务端校验，可以使用 `路径key` 来定位要显示报错信息的表单项，例如 `a[0].b` 定位到 a combo 的第一项中 b 表单项。

例如有如下表单，点击提交，查看效果：

接口返回如下

```
{
  "status": 422,
  "msg": "",
  "errors": {
    "combo1": "服务器端说，这个combo1有问题",
    "combo1[1].a": "服务器端说，这个combo1的第二项中的a有问题", // 或 combo1.1.a
    "combo2": "服务器端说，这个combo2有问题",
    "combo2.b": "服务器端说，这个combo2中的b有问题"
  },
  "data": null
}
```

#### Table 校验

Table 类型的表单项，要实现服务端校验，可以使用 `路径key` 来定位要显示报错信息的表单项，例如 `a[0].b` 定位到 a table 的第一项中 b 表单项。

例如有如下表单，点击提交，查看效果：

接口返回如下

```
{
  "status": 422,
  "msg": "",
  "errors": {
    "table": "表格有问题",
    "table[0].a": "表格的第一项中的 a 有问题",
    "table[1].b": "表格的第二项中的 b 有问题",
    "combo.table[0].b": "Combo中表格的第一项中的 b 有问题",
    "combo.table[1].a": "Combo中表格的第二项中的 a 有问题"
  },
  "data": null
}
```

### 通过表单项校验接口

可以在表单项上，配置校验接口 `validateApi`，实现单个表单项后端校验。

校验接口显示校验信息返回格式如下：

```
{
  "status": 422,
  "errors": "当前用户已存在"
}
```

-   `status`: 返回 `0` 表示校验成功，`422` 表示校验失败;
-   `errors`: 返回 `status` 为 `422` 时，显示的校验失败信息;

### 配置自动填充

通过配置 "autoFill.api" 为自动填充数据源接口地址；amis 可以将返回数据自动填充到表单中，例如如下配置；

自动填充接口返回格式如下： 注意：amis 仅处理接口返回结果仅有一项的数据，默认自动填充相关字段

```
{
  "status": 0,
  "data": {
    "rows": [
      {
        "key": "value",
        "key1": "value1"
      }
    ]
  }
}
```

或者是

```
{
  "status": 0,
  "data": {
    "key": "value",
    "key1": "value1"
  }
}
```

### 配置参照录入

设置 autoFill.showSuggestion 为 true；同时在 autoFill 中配置如下示例参数，可以进行数据的参照录入「当前表单项聚焦或者值变化时弹出 dialog/drawer/popOver 供用户操作」例如如下配置

fillMapping 配置 支持变量取值和表达式； 如下配置中，如果想一次选中多条数据并映射可如下配置表达式，其中 items 默认为选中的 1 至 N 条数据： 仅挑选 platform,version 字段追加数据并去重：combo：'${UNIQ(CONCAT(combo, ARRAYMAP(items, item => {platform: item.platform, version: item.version})))}' 数据替换并去重：combo：'${UNIQ(ARRAYMAP(items, item => {platform: item.platform, version: item.version}))}' 数据替换：combo: ${items}

`autoFill.defaultSelection` 可以用来配置默认选中

## 及时获取其他表单项的值

默认为了提高性能，给表单项下发的数据不是最新，只有自己的值变化才是最新的，如果想及时的获取其他表单项的值，比如描述中想获取其他表单项值来展示不同的描述。需要配置 `strictMode` 为 false。

## 属性表

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| type | `string` |  | 指定表单项类型 |
| className | `string` |  | 表单最外层类名 |
| inputClassName | `string` |  | 表单控制器类名 |
| labelClassName | `string` |  | label 的类名 |
| name | `string` |  | 字段名，指定该表单项提交时的 key |
| value | `string` |  | 表单默认值 |
| label | [模板](https://aisuda.bce.baidu.com/amis/docs/concepts/template) 或 `false` |  | 表单项标签 |
| labelAlign | `"right" | "left"` | `"right"` | 表单项标签对齐方式，默认右对齐，仅在 `mode`为`horizontal` 时生效 |
| labelRemark | [Remark](https://aisuda.bce.baidu.com/amis/zh-CN/components/remark) |  | 表单项标签描述 |
| description | [模板](https://aisuda.bce.baidu.com/amis/docs/concepts/template) |  | 表单项描述 |
| placeholder | `string` |  | 表单项描述 |
| inline | `boolean` |  | 是否为 内联 模式 |
| strictMode | `boolean` |  | 通过配置 false 可以及时获取所有表单里面的数据，否则可能会有不同步 |
| submitOnChange | `boolean` |  | 是否该表单项值发生变化时就提交当前表单。 |
| disabled | `boolean` |  | 当前表单项是否是禁用状态 |
| disabledOn | [表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression) |  | 当前表单项是否禁用的条件 |
| visible | [表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression) |  | 当前表单项是否禁用的条件 |
| visibleOn | [表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression) |  | 当前表单项是否禁用的条件 |
| required | `boolean` |  | 是否为必填。 |
| requiredOn | [表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression) |  | 通过[表达式](https://aisuda.bce.baidu.com/amis../Types#%E8%A1%A8%E8%BE%BE%E5%BC%8F)来配置当前表单项是否为必填。 |
| validations | [表达式](https://aisuda.bce.baidu.com/amis/docs/concepts/expression) |  | 表单项值格式验证，支持设置多个，多个规则用英文逗号隔开。 |
| validateApi | [表达式](https://aisuda.bce.baidu.com/amis/docs/types/api) |  | 表单校验接口 |
| autoFill | [SchemaNode](https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/schemanode) |  | 数据录入配置，自动填充或者参照录入 |
| autoFill.showSuggestion | `boolean` |  | true 为参照录入，false 自动填充 |
| autoFill.api | [表达式](https://aisuda.bce.baidu.com/amis/docs/types/api) |  | 自动填充接口/参照录入筛选 CRUD 请求配置 |
| autoFill.silent | `boolean` |  | 是否展示数据格式错误提示，默认为 true |
| autoFill.fillMappinng | [SchemaNode](https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/schemanode) |  | 自动填充/参照录入数据映射配置，键值对形式，值支持变量获取及表达式 |
| autoFill.trigger | `string` |  | showSuggestion 为 true 时，参照录入支持的触发方式，目前支持 change「值变化」｜ focus 「表单项聚焦」 |
| autoFill.mode | `string` |  | showSuggestion 为 true 时，参照弹出方式 dialog, drawer, popOver |
| autoFill.labelField | `string` |  | showSuggestion 为 true 时，设置弹出 dialog,drawer,popOver 中 picker 的 labelField |
| autoFill.position | `string` |  | showSuggestion 为 true 时，参照录入 mode 为 popOver 时，可配置弹出位置 |
| autoFill.size | `string` |  | showSuggestion 为 true 时，参照录入 mode 为 dialog 时，可设置大小 |
| autoFill.columns | `Array<Column>` |  | showSuggestion 为 true 时，数据展示列配置 |
| autoFill.filter | [SchemaNode](https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/schemanode) |  | showSuggestion 为 true 时，数据查询过滤条件 |
| static | `boolean` |  | `2.4.0` 当前表单项是否是静态展示，目前支持静[支持静态展示的表单项](https://aisuda.bce.baidu.com/amis/zh-CN/components/form/formitem#%E6%94%AF%E6%8C%81%E9%9D%99%E6%80%81%E5%B1%95%E7%A4%BA%E7%9A%84%E8%A1%A8%E5%8D%95%E9%A1%B9) |
| staticClassName | `string` |  | `2.4.0` 静态展示时的类名 |
| staticLabelClassName | `string` |  | `2.4.0` 静态展示时的 Label 的类名 |
| staticInputClassName | `string` |  | `2.4.0` 静态展示时的 value 的类名 |
| staticSchema | [SchemaNode](https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/schemanode) |  | `2.4.0` 自定义静态展示方式 |
| staticSchema.limit | `number` | 10 | `2.4.0` select、checkboxes 等选择类组件多选时展示态展示的数量 |

## 支持静态展示的表单项

可以在[示例页](https://aisuda.bce.baidu.com/amis/examples/form/switchDisplay)查看支持静态展示的表单项的展示方式

-   form 表单
-   button-group-select 按钮点选
-   chained-select 链式下拉框
-   chart-radios 图表单选框
-   checkbox 勾选框
-   checkboxes 复选框
-   combo 组合
-   input-kv 键值对
-   input-array 数组输入框
-   input-city 城市选择器
-   input-color 颜色选择器
-   input-date 日期选择器
-   input-date-range 日期范围选择器
-   input-datetime-range 日期时间选择器
-   input-time-range 时间范围选择器
-   input-group 输入框组合
-   input-month-range 月份范围
-   input-number 数字输入
-   input-quarter-range 季度范围
-   input-range 滑块
-   input-rating 评分
-   input-tag 标签选择器
-   input-text 输入框
-   input-password 密码输入框
-   input-email 邮箱输入框
-   input-url url 输入框
-   native-date native 日期选择器
-   native-time native 时间选择器
-   native-number native 数字输入
-   input-tree 树形选择器
-   input-year-range 年份范围
-   list-select 列表选择器
-   location-picker 地理位置
-   matrix-checkboxes 矩阵勾选
-   nested-select 级联选择器
-   radios 单选框
-   select 下拉框
-   multi-select 多选下拉框
-   switch 开关
-   tabs-transfer 组合穿梭器
-   tabs-transfer-picker 组合穿梭选择器
-   textarea 多行输入框
-   transfer 穿梭器
-   transfer-picker 穿梭选择器
-   tree-select 属性选择器
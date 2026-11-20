# 应用清单

`.easyvrui`采用UTF-8 JSON格式。Desktop和File Manager通过SDK读取清单，在调用方所在的计算机启动应用。清单内的相对路径与子进程工作目录以清单所在目录为基准。内置普通应用的清单与对应程序同处安装目录的`app/...`。例如`app/demo/python/easyvrui_demo_python.easyvrui`的`launch.script`为`main.py`。

## 清单结构

```json
{
    "id": "example",
    "name":
    {
        "en": "Example",
        "zh": "示例",
        "ja": "サンプル"
    },
    "type": "application",
    "icon":
    {
        "path": "example.ico"
    },
    "launch":
    {
        "runtime": "native",
        "executable": "example.exe",
        "argument_list": []
    }
}
```

|字段|规则|
|---|---|
|`id`|应用标识；省略时取清单文件名（不含扩展名）|
|`name`|多语言名称对象，必须包含非空的`en`字段|
|`type`|可选`application`、`desktop`、`layout`或`ime`，默认为`application`|
|`icon`|可选图标对象，需包含`path`或`base64`之一|
|`launch`|必填启动配置对象|

上表列出了全部合法的顶层字段。单实例协调由应用自身负责。

语言匹配顺序为：先匹配完整系统语言，再逐级剥离区域或脚本子标签，最后回退到`en`（例如`zh-Hant-TW`依次尝试`zh-hant-tw`、`zh-hant`、`zh`、`en`）。语言标签不区分大小写，下划线视为连字符；归一化后若存在重复标签则报错。

`icon.path`指向外部图片文件；`icon.base64`则直接内嵌Windows图片解码器支持的PNG、ICO等文件内容（标准Base64字符串）。示例如下：

```json
{
    "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScLttAAAAABJRU5ErkJggg=="
}
```

## 原生程序

当`launch.runtime`为`native`时，使用以下启动字段：

|字段|规则|
|---|---|
|`runtime`|必填，固定为`native`|
|`executable`|必填，可执行文件路径（相对路径以清单所在目录为基准）|
|`argument_list`|可选字符串参数数组，默认`[]`|

## Python程序

当`launch.runtime`为`python`时，使用以下启动字段：

|字段|规则|
|---|---|
|`runtime`|必填，固定为`python`|
|`script`|必填，Python主脚本路径，相对路径以清单所在目录为基准|
|`argument_list`|可选字符串参数数组，默认`[]`|

```json
{
    "id": "python_example",
    "name":
    {
        "en": "Python Example",
        "zh": "Python示例",
        "ja": "Pythonサンプル"
    },
    "launch":
    {
        "runtime": "python",
        "script": "main.py",
        "argument_list": []
    }
}
```

SDK通过PATH中的`python.exe`执行`python.exe -B <主脚本> <参数列表>`，主脚本须存在。SDK优先从清单目录向上查找安装根目录，再从启动方所在的框架目录查找。找到安装后，将`sdk/api/python/`前置到子进程的`PYTHONPATH`并保留原值，同时将`EASYVRUI_NATIVE_DIR`设为该目录。SDK还设置`PYTHONDONTWRITEBYTECODE=1`。应用脚本直接`import easyvrui`，解释器须匹配安装的x64原生扩展及CPython版本。

## 参数与连接信息

`argument_list`中的参数按原样逐项透传，完整保留空字符串、空格、引号、反斜线与Unicode文本。调用`launch_application(manifest_path, extra_argument_list)`时，额外参数会追加到清单参数之后；名称、标识、路径及参数中均不允许出现NUL字符。

如果清单和额外参数均未指定远程连接选项，SDK会自动把当前调用进程的`--easyvrui-host=`、`--easyvrui-port=`、`--easyvrui-access-credential=`与`--easyvrui-public-key-fingerprint=`继承给子进程；若需主动指定，请按[远程SDK连接规则](./engine_protocol)提供完整配置。

## Desktop应用列表

Desktop读取两份配置。安装器将内置应用登记在`app/desktop/config.json`。用户配置位于`%USERPROFILE%\easyvrui\desktop\config.json`，未设置`USERPROFILE`时使用`HOME`。

各自的`application_list`记录清单路径，相对路径以对应配置文件所在目录为基准。系统配置示例如下。

```json
{
    "application_list":
    [
        "../demo/cpp/easyvrui_demo_cpp.easyvrui",
        "../form_designer/easyvrui_form_designer.easyvrui"
    ]
}
```

Desktop读取有效普通应用清单，在内存中按应用`id`合并，比较时忽略ID中的ASCII字母大小写。系统配置优先，各文件内的重复项采用第一条有效记录。清单或启动入口失效时跳过该项。刷新会重新读取两份配置。

添加应用时，Desktop检查该ID在合并后的列表中是否已存在。添加和移除只更新用户配置。系统配置由安装器生成，内置应用的登记路径由该文件管理。

## File Manager文件关联

File Manager从`app/file_manager/file_manager.json`读取`association_map`。键为带`.`的文件扩展名，不区分大小写。值为`.easyvrui`清单路径，相对路径以File Manager可执行文件所在目录为基准。为已安装的Form Designer配置文件关联时，可在该对象中加入以下映射：

```json
{
    "association_map":
    {
        ".easyvruifrm": "../form_designer/easyvrui_form_designer.easyvrui"
    }
}
```

在File Manager中双击`.easyvrui`会启动对应应用。双击已关联扩展名的文件时，SDK会将该文件的绝对路径作为额外参数传给目标应用。

# 应用清单

`.easyvrui`采用标准UTF-8 JSON格式。Desktop和File Manager通过SDK读取清单并在调用方所在机器启动应用；清单中的相对路径及子进程工作目录均以清单所在目录为基准。

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
        "run_as_administrator": false,
        "argument_list": []
    }
}
```

|字段|规则|
|---|---|
|`id`|应用标识；省略时取清单文件名（不含扩展名）|
|`name`|多语言名称对象，必须包含非空的`en`字段|
|`type`|可选`application`、`desktop`、`layout`或`ime`，默认为`application`|
|`icon`|可选图标对象，恰包含`path`或`base64`中的一个成员|
|`launch`|必填启动配置对象，按`runtime`对应下表提供字段|

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
|`run_as_administrator`|可选布尔值，默认`false`。启用后要求以管理员权限启动，并与`launch_application()`调用参数取逻辑或|
|`argument_list`|可选字符串参数数组，默认`[]`|

## Python程序

当`launch.runtime`为`python`时，使用以下启动字段：

|字段|规则|
|---|---|
|`runtime`|必填，固定为`python`|
|`script`|必填，Python主脚本路径|
|`run_as_administrator`|可选布尔值，默认`false`。启用后要求以管理员权限启动，并与`launch_application()`调用参数取逻辑或|
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

SDK调用PATH中的`python.exe`执行`python.exe -B <主脚本> <参数列表>`。清单指定的主脚本须存在，应用可直接导入`easyvrui`，例如`repo/app/demo/python/main.py`。启动已安装应用时，SDK将安装目录下的`sdk/api/python`前置到子进程的`PYTHONPATH`，保留其原值。SDK还将当前原生框架目录通过`EASYVRUI_NATIVE_DIR`传给子进程，并设置`PYTHONDONTWRITEBYTECODE=1`。

## 参数与连接信息

`argument_list`中的参数按原样逐项透传，完整保留空字符串、空格、引号、反斜线与Unicode文本。调用`launch_application(manifest_path, extra_argument_list, run_as_administrator)`时，额外参数会追加到清单参数之后，`run_as_administrator`与清单字段取逻辑或；普通权限调用方请求管理员启动时返回权限不足错误（`administrator_privilege_required`）。名称、标识、路径及参数中均不允许出现NUL字符。

如果清单和额外参数均未指定远程连接选项，SDK会自动把当前调用进程的`--easyvrui-host=`、`--easyvrui-port=`、`--easyvrui-access-credential=`与`--easyvrui-public-key-fingerprint=`继承给子进程；若需主动指定，请按[远程SDK连接规则](/reference/engine_protocol)提供完整配置。

## Desktop应用列表

Desktop读取两份配置。安装器将内置应用登记在`app/desktop/config.json`。用户配置位于`%USERPROFILE%\easyvrui\desktop\config.json`，未设置`USERPROFILE`时使用`HOME`。

各自的`application_list`记录清单路径，相对路径以对应配置文件所在目录为基准。安装器生成的系统配置如下：

```json
{
    "application_list":
    [
        "../demo/cpp/easyvrui_demo_cpp.easyvrui",
        "../demo/python/easyvrui_demo_python.easyvrui",
        "../easyvrscreen/easyvrscreen.easyvrui",
        "../file_manager/easyvrui_file_manager.easyvrui",
        "../form_designer/easyvrui_form_designer.easyvrui",
        "../task_manager/easyvrui_task_manager.easyvrui"
    ]
}
```

Desktop在内存中按应用`id`合并，重复ID优先采用系统配置。失效清单会跳过。界面上的添加和移除操作只更新用户配置，刷新重新读取两份配置。

## File Manager配置与文件关联

File Manager从其可执行文件同目录的`file_manager.json`中读取视图设置（`view_mode`、`computer_view_mode`、`folder_view_mode_map`）和文件关联`association_map`。`association_map`的键为带`.`的文件扩展名（不区分大小写），值为`.easyvrui`清单路径（相对路径以File Manager所在目录为基准）。安装器初始化的`association_map`为空对象，以下为手动配置关联的示例：

```json
{
    "association_map":
    {
        ".easyvruifrm": "../form_designer/easyvrui_form_designer.easyvrui"
    }
}
```

在File Manager中双击`.easyvrui`会直接启动对应应用；双击已关联扩展名的文件时，则会启动对应应用并将该文件的绝对路径作为额外参数传入。当可执行文件同目录放置了`form_designer.easyvrui`且配置中尚未登记`.easyvruifrm`时，File Manager会自动补上该默认关联。地址栏同时支持映射网络驱动器以及`\\server`格式的网络共享枚举与目录浏览。

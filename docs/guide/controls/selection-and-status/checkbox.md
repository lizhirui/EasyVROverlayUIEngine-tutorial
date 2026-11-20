# checkbox

`checkbox`表示可以独立切换的布尔选项，例如是否播放通知声音。多个`checkbox`可同时选中，也可分别恢复到未选中状态。

继承[公共控件接口](/guide/controls/common-api#control)和[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

默认`checked = False`、可聚焦且启用。空白方框是未选中标记，截图为其填写了文字。

![checkbox默认外观](/images/zh/checkbox_default.png)

## 属性对比

四行依次展示未选中、选中、选中后禁用、字体与配色。禁用和选中可同时成立，检查标记和文字亮度分别表示这两个状态。

![checkbox属性对比](/images/zh/checkbox_comparison.png)

## 接口参考

C++属性通过表中的访问方法读写，Python通过同名属性访问。表中的事件参数采用C++类型名，Python对应类型省略`_t`后缀。公共成员见[基础接口](/guide/controls/common-api)。

### 属性

|属性|C++|用途与默认值|
|---|---|---|
|`text`|`get_text`、`set_text`|选项说明，默认空字符串。|
|`checked`|`get_checked`、`set_checked`|布尔选中状态，初始为假。|
|`focusable`|`is_focusable`|可进入焦点顺序。|

### 方法

|Python|C++|用途|
|---|---|---|
|`checkbox(name)`|`checkbox(name)`|创建一个独立的二值选项。|

### 事件

|事件|触发条件与参数|
|---|---|
|`on_text_changed`|显示文字实际变化，参数为`event_args_t`。|
|`on_checked_changed`|`checked`实际变化，包括用户交互与程序设值。参数为`event_args_t`。|
|`on_click`|继承的激活事件。持久化选中状态时使用`on_checked_changed`。|

## 独立例程

初始只选中“显示未读状态”。勾选“播放通知声音”后，另一项保持选中，状态文字更新。再次切换可关闭通知声音。

先按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程仓库根目录打开已配置MSVC的x64 CMD，使用实际安装的SDK路径。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/checkbox/cpp -B .work/example_checkbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_checkbox --config Release
.work\example_checkbox\Release\tutorial_checkbox.exe
```

上面的可执行文件路径对应Visual Studio生成器。使用单配置Ninja时，可执行文件直接位于构建目录。

<<< ../../../../examples/guide/controls/selection-and-status/checkbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\checkbox\python\run.cmd
```

<<< ../../../../examples/guide/controls/selection-and-status/checkbox/python/checkbox_demo.py

### 运行效果

![checkbox独立例程运行效果](/images/zh/checkbox_demo.png)

## 常见问题与实践

- 初始化时先从配置恢复`checked`，再订阅`on_checked_changed`，避免把恢复状态当作新操作。
- 统一用状态事件处理持久化。批量恢复多个选项时，可以在业务层将多次变化合并成一次保存。
- 当前接口提供两个布尔状态。对于明确的互斥选项使用[radiobutton](./radiobutton)。

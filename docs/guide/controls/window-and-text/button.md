# button

`button`把一次用户操作映射到一个明确命令，例如应用设置、确认或重新编辑。使用能描述操作结果的简短文字，并在命令暂不可执行时更新`enabled`。

继承[公共控件接口](/guide/controls/common-api#control)和[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

默认可聚焦、可见、启用，`text`初始为空，已设置的文字按控件矩形居中绘制。截图仅填写文字和矩形。

![button默认外观](/images/zh/button_default.png)

## 属性对比

四行依次展示默认、字体与配色、禁用与焦点边框。保持同一文字可直接比较状态差异。对齐来自控件固定绘制规则。

![button属性对比](/images/zh/button_comparison.png)

## 接口参考

C++属性通过表中的访问方法读写，Python通过同名属性访问。表中的事件参数采用C++类型名，Python对应类型省略`_t`后缀。公共成员见[基础接口](/guide/controls/common-api)。

### 属性

|属性|C++|用途与默认值|
|---|---|---|
|`text`|`get_text`、`set_text`|读写显示文字，默认空字符串。|
|`focusable`、`enabled`、`tab_index`|`is_focusable`、`get_enabled`、`set_enabled`、`get_tab_index`、`set_tab_index`|可聚焦，默认启用。`tab_index`参与所在`window`的Tab顺序。|

### 方法

|Python|C++|用途|
|---|---|---|
|`button(name)`|`button(name)`|创建一个`button`。|
|`focus()`、`activate()`|`focus()`、`activate()`|继承接口。前者请求焦点，后者程序化触发激活路径。|

### 事件

|事件|触发条件与参数|
|---|---|
|`on_text_changed`|标题文字实际变化，参数为`event_args_t`。|
|`on_click`|继承的激活事件，参数为`event_args_t`。|
|`on_focus_in`、`on_focus_out`、`on_enabled_changed`|继承事件，适合观察焦点和可用状态。|

## 独立例程

单击“提交设置”后，状态文字更新，提交入口被禁用，“重新编辑”变为可用。单击“重新编辑”恢复初始状态。

先按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程仓库根目录打开已配置MSVC的x64 CMD，使用实际安装的SDK路径。

### C++

```bat
cmake -S examples/guide/controls/window-and-text/button/cpp -B .work/example_button -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_button --config Release
.work\example_button\Release\tutorial_button.exe
```

上面的可执行文件路径对应Visual Studio生成器。使用单配置Ninja时，可执行文件直接位于构建目录。

<<< ../../../../examples/guide/controls/window-and-text/button/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\button\python\run.cmd
```

<<< ../../../../examples/guide/controls/window-and-text/button/python/button_demo.py

### 运行效果

![button独立例程运行效果](/images/zh/button_demo.png)

## 常见问题与实践

- 提交网络或磁盘任务时先更新可用状态，完成后通过`begin_invoke()`刷新UI，避免占用事件回调处理时间。
- 把业务调用放在`on_click`，这样点击与程序化激活共享一条路径。连续启用多个`button`时设置清晰的`tab_index`。
- 临时禁用与永久移除分别使用`enabled`和容器集合操作，给禁用状态留出可读的提示。

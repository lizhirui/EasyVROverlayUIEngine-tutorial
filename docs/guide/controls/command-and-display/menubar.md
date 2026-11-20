# menubar

`menubar`把命令组织成窗口顶部的层级菜单。根`menuitem`形成顶部入口，子`menuitem`形成命令或子菜单。将`menubar`赋给`window.menu`，由`window`管理布局、焦点和命令访问。 继承成员见[容器接口](/guide/controls/common-api#container-control)。

## 默认外观

默认行高32逻辑像素，使用SDK字体。截图添加“任务”“视图”两个根`menuitem`，保留标准位置与关闭状态。

![menubar默认外观](/images/zh/menubar_default.png)

## 属性对比

对比图使用42逻辑像素行高和自定义字体。上图按住`Alt`，根菜单的`T`与`V`出现下划线。下图在单按`Alt`后用方向键展开“任务”，子项的助记符也显示下划线，同时可看到`Ctrl+R`快捷键、勾选状态和禁用状态。

![menubar属性对比](/images/zh/menubar_comparison.png)

## 助记符与键盘导航

在`menuitem.text`中以`&`标记下一字符，例如`任务(&T)`显示为“任务(T)”。按住`Alt`或处于菜单键盘导航时，下划线标出`T`。单独按下再松开`Alt`可进入或退出菜单导航。进入时可用方向键移动，用助记键选择，或用`Enter`执行当前命令。需要显示字符`&`时写成`&&`。

在实体键盘模式下，`Alt+Shift`切换IME语言并保留当前`textbox`的编辑焦点。为同级`menuitem`分配不同助记键，使用`shortcut`为常用命令提供直接执行的快捷键。

## 接口参考

C++用表中的方法读写属性，Python按同名属性访问。回调接收`source`与`event`。表中各强类型参数继承`event_args_t`，基础参数本身没有附加字段。Python类型名省略`_t`。

### 属性

|属性|C++访问方法|类型、默认值与用途|
|---|---|---|
|`font`、`row_height`|`get_font`、`set_font`、`get_row_height`、`set_row_height`|字体与正逻辑像素行高，默认行高32。|
|`open`|`get_is_open`|Python只读属性，表示菜单导航状态。|
|`owning_menubar`|`get_menubar`|只读，查询所属`menubar`。|
|`control_list`|`get_control_list`|根`menuitem`集合。子菜单内容放在对应项目的`control_list`。|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|继承的开关。关闭可见性或交互会影响活动菜单分支。|
|`focusable`|`is_focusable`|只读，支持菜单焦点。|

### 方法

|方法|用途|
|---|---|
|`menubar(name)`|构造菜单对象并赋给`window.menu`。|
|`open_menu()`、`close(restore_focus=True)`|Python进入或退出菜单状态。C++进入方法为`open()`，关闭时同样可选择恢复焦点。|
|`is_submenu_open(item)`|查询指定子菜单是否打开。C++方法为`get_is_submenu_open(item)`。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_font_changed`、`on_row_height_changed`|`event_args_t`|字号或行高配置变化。|
|`on_opening`、`on_closed`|`event_args_t`|菜单开始和关闭通知。|
|`on_item_added`、`on_item_removed`|`menu_item_event_args_t`|子项的集合操作，包含`item`、`index`。|

## menuitem

|属性|用途|
|---|---|
|`text`|显示文字。可用`&`指定助记键。|
|`icon`|可选的`drawing_image`。|
|`shortcut`|命令快捷键，例如`Ctrl+R`。|
|`checkable`、`checked`|控制可勾选与当前选中状态。|
|`separator`|显示分隔项。|
|`open`|Python只读属性，查询该项的子菜单是否打开。C++通过所属`menubar`查询。|
|`control_list`|管理子`menuitem`，形成嵌套菜单。|

使用`menuitem(name)`创建。C++属性使用`get_`、`set_`访问。项目事件包括`on_text_changed`、`on_icon_changed`、`on_shortcut_changed`、`on_checkable_changed`、`on_checked_changed`、`on_separator_changed`、`on_opening`、`on_closed`和继承的`on_click`，参数为`event_args_t`。子集合同样提供`on_item_added`和`on_item_removed`。

## 独立例程

打开“任务”并选择“刷新记录”。命令处理函数更新状态文字。在获得键盘输入的窗口内也可单按`Alt`，用方向键展开菜单，再用`Enter`执行命令，或直接按`Ctrl+R`。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程根目录的x64开发者CMD中执行命令，并替换示例中的SDK安装路径。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/menubar/cpp -B .work/example_menubar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_menubar --config Release
.work\example_menubar\Release\tutorial_menubar.exe
```

使用单配置Ninja时，从构建目录直接运行可执行文件。

<<< ../../../../examples/guide/controls/command-and-display/menubar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\menubar\python\run.cmd
```

<<< ../../../../examples/guide/controls/command-and-display/menubar/python/menubar_demo.py

### 运行效果

![menubar独立例程运行效果](/images/zh/menubar_demo.png)

## 常见问题与布局实践

- 顶部区域由`window.menu`布局。正文控件须预留标题栏以及菜单所在高度。
- 将同一业务命令集中在`on_click`，激光、助记键和快捷键可共享逻辑。
- 命令名称应适合各语言的长度。给子菜单的快捷键触发文字和图标留出边距。

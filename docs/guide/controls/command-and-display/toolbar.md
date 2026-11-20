# toolbar

`toolbar`在固定矩形中按顺序放置`toolbar_button`，适合即用操作。容器负责尺寸、间距、裁剪和按键布局。按钮集合由`button_list`公开。 继承成员见[容器接口](/guide/controls/common-api#container-control)。

## 默认外观

图中加入两个图标和一个分隔项。控件使用默认工具尺寸、间距和配色。

![toolbar默认外观](/images/zh/toolbar_default.png)

## 属性对比

上方保留默认尺寸和间距。下方使用56逻辑像素的工具尺寸、14逻辑像素间距，并禁用右侧操作项。

![toolbar属性对比](/images/zh/toolbar_comparison.png)

## 接口参考

C++用表中的方法读写属性，Python按同名属性访问。回调接收`source`与`event`。表中各强类型参数继承`event_args_t`，基础参数本身没有附加字段。Python类型名省略`_t`。

### 属性

|属性|C++访问方法|类型、默认值与用途|
|---|---|---|
|`button_list`|`get_button_list`|`toolbar_button_collection`，管理按钮顺序和归属。|
|`tool_size`、`spacing`|`get_tool_size`、`set_tool_size`、`get_spacing`、`set_spacing`|工具尺寸默认40逻辑像素，须为正整数。间距默认6.0逻辑像素，须为非负有限值。|
|`focusable`|`is_focusable`|只读，容器和条目有各自的焦点规则。|

### 方法

|方法|用途|
|---|---|
|`toolbar(name)`|构造。|
|`button_list.add(item)`、`button_list.insert(index,item)`|追加或插入操作项。|
|`button_list.add_separator(name)`|Python按名称追加分隔项。C++先用`get_button_list().add(name)`创建条目，再调用该条目的`set_separator(true)`。|
|`button_list.remove(item)`、`button_list.clear()`|移除或清空条目。C++先调用`get_button_list()`。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_tool_size_changed`、`on_spacing_changed`|`event_args_t`|尺寸和间距实际变化。|

## toolbar_button

|成员|用途|
|---|---|
|`toolbar_button(name)`|创建可加入`button_list`的条目。|
|`icon`、`get_icon/set_icon`|读写可选`drawing_image`。|
|`separator`、`get_separator/set_separator`|控制条目是否作为分隔项。|
|`enabled`、`tooltip_text`|继承的交互开关和悬停说明。|
|`on_icon_changed`、`on_click`|参数均为`event_args_t`，表示图标变化与业务命令激活。|

通过`toolbar_button_collection`按索引或名称访问条目。按钮的普通矩形由所属`toolbar`管理。

## 独立例程

点击蓝色图标触发“已请求预览”。图标由4字节RGBA数据创建，悬停说明标识命令用途。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程根目录的x64开发者CMD中执行命令，并替换示例中的SDK安装路径。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/toolbar/cpp -B .work/example_toolbar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_toolbar --config Release
.work\example_toolbar\Release\tutorial_toolbar.exe
```

使用单配置Ninja时，从构建目录直接运行可执行文件。

<<< ../../../../examples/guide/controls/command-and-display/toolbar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\toolbar\python\run.cmd
```

<<< ../../../../examples/guide/controls/command-and-display/toolbar/python/toolbar_demo.py

### 运行效果

![toolbar独立例程运行效果](/images/zh/toolbar_demo.png)

## 常见问题与布局实践

- 为图标命中区域预留宽高。条目总宽度增长时增加容器宽度或减少当前同时显示的操作数。
- 将分隔项用于区分不同任务。用`enabled`表现暂不可用的命令。
- 用`tooltip_text`说明图标含义。图像本身通过共享绘图资源使用。

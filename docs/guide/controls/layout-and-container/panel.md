# panel

`panel`以父子关系组织一组控件，适合把连接状态、局部参数、操作区或一组互斥选项放在一起。添加到`control_list`的子控件使用相对于`panel`的坐标，移动`panel`时随组移动。

继承的通用成员见[容器接口](/guide/controls/common-api#container-control)。

## 默认外观

默认绘制控件背景和边框。空`panel`只显示其矩形轮廓，加入子控件后使用该组的局部坐标绘制。

![panel默认外观](/images/zh/panel_default.png)

## 属性对比

左侧保留默认边框、背景与标题。右侧修改`background_color`，并在内部加入另一层带背景的`panel`。默认边框取决于SDK渲染样式，自定义边框可以在派生控件的渲染中绘制。

![panel属性对比](/images/zh/panel_comparison.png)

## 接口参考

Python使用表中的属性名。C++通过对应方法读写，并使用`control_base &source`和表中类型的引用订阅事件。无附加字段的`event_args_t`表示状态已更新，回调通过`source`读取新值。Python对应事件类型名省略`_t`。

### 属性

|属性|C++|类型、默认值与用途|
|---|---|---|
|`rect`|`get_rect`、`set_rect`|继承的逻辑矩形，子控件位置相对于该矩形。|
|`background_color`|`get_background_color`、`set_background_color`|继承的RGBA背景色，默认使用SDK控件背景色。|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|继承的显示与交互开关。可以用来控制一组控件。|
|`control_list`|`get_control_list`|只读集合入口，用于增删、排序和索引直接子控件。|
|`active_item_list`|`get_active_item_list`|只读，当前活动子控件列表。|

### 方法

|Python|C++|用途|
|---|---|---|
|`panel(name)`|`panel(name)`|构造普通容器。|
|`control_list.add(item)`|`get_control_list().add(item)`|把子控件加入该层父级。|
|`control_list.remove(item)`|`get_control_list().remove(item)`|把子控件移出集合并返回对象。|
|`show()`、`hide()`|`show()`、`hide()`|显示或隐藏这一组内容。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|直接子控件增加或移除。`item`是控件，`index`是集合位置。|
|`on_background_color_changed`、`on_visible_changed`、`on_enabled_changed`|`event_args_t`|继承的背景或状态变化。|
|`on_moved`、`on_size_changed`|`event_args_t`|继承的位置或尺寸变化。|

## 独立例程

主`panel`分组展示同步服务。内层`panel`显示连接详情，单击“隐藏连接详情”可整体收起，再单击可恢复。效果图显示恢复后的界面。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。以下命令在教程仓库根目录的x64开发者CMD中执行。把示例SDK路径改为实际安装位置。

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/panel/cpp -B .work/example_panel -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_panel --config Release
.work\example_panel\Release\tutorial_panel.exe
```

Visual Studio生成器把可执行文件放在`Release`子目录。单配置Ninja生成器直接输出到构建目录。

<<< ../../../../examples/guide/controls/layout-and-container/panel/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\panel\python\run.cmd
```

<<< ../../../../examples/guide/controls/layout-and-container/panel/python/panel_demo.py

### 运行效果

![panel独立例程效果](/images/zh/panel_demo.png)

## 常见问题与布局实践

- 嵌套时逐层使用父级坐标。查询最终表面矩形可读取`absolute_rectangle`，布局配置继续使用`rect`。
- `panel`适合固定尺寸分组。内容超出可视区域且需要滚动时使用[scrollpanel](./scrollpanel)。
- 同一直接父容器内的[radiobutton](../selection-and-status/radiobutton)组成一组。用不同`panel`隔离独立的选项组。

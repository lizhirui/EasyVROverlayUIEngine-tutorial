# scrollpanel

`scrollpanel`是带裁剪视口的容器，适合滚动查看日志、设置和其他跨越单屏的控件。子控件的局部矩形决定内容范围，滚动偏移改变其在视口内的位置。视口外的区域由SDK裁剪。

继承的通用成员见[容器接口](/guide/controls/common-api#container-control)。

## 默认外观

默认水平和垂直滚动条开关都为真，偏移均从0开始。空视口使用标准背景和边框，开关为真时会为相应滚动条保留区域。

![scrollpanel默认外观](/images/zh/scrollpanel_default.png)

## 属性对比

两侧使用相同的6行记录与相同视口。左侧位于顶部，显示前3行。右侧已向下滚动，显示后续记录。两侧的内容超界部分均在视口边缘裁剪。

![scrollpanel属性对比](/images/zh/scrollpanel_comparison.png)

## 接口参考

Python使用表中的属性名。C++通过对应方法读写，并使用`control_base &source`和表中类型的引用订阅事件。无附加字段的`event_args_t`表示状态已更新，回调通过`source`读取新值。Python对应事件类型名省略`_t`。

### 属性

|属性|C++|类型、默认值与用途|
|---|---|---|
|`horizontal_scrollbar_visible`|`get_horizontal_scrollbar_visible`、`set_horizontal_scrollbar_visible`|默认真。控制横向滚动条及其占用的视口面积。|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`、`set_vertical_scrollbar_visible`|默认真。控制纵向滚动条及纵向摇杆滚动。|
|`control_list`|`get_control_list`|只读的子控件集合入口。直接子控件的矩形参与计算内容范围。|
|`visible`、`enabled`|`set_visible`、`set_enabled`|继承的读写开关。隐藏或禁用会停止滚动条拖动。|

### 方法

|Python|C++|用途|
|---|---|---|
|`scrollpanel(name)`|`scrollpanel(name)`|构造可裁剪、可滚动的容器。日常应用通过滚动条与手柄控制视口。|
|`control_list.add(item)`|`get_control_list().add(item)`|添加使用内容坐标的子控件。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_horizontal_scrollbar_visible_changed`、`on_vertical_scrollbar_visible_changed`|`event_args_t`|相应滚动条开关实际改变。|
|`on_viewport_changed`|`event_args_t`|继承的视口变化通知。滚动或内容变化影响视口时可触发。|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|子控件加入或移出，参数含`item`及`index`。|

## 独立例程

“同步日志”按局部纵坐标排列6条日志。启用纵向滚动，关闭横向滚动条。将激光指向日志区域后向下拨动摇杆，或拖动纵向滚动条。效果图显示滚动后的记录。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。以下命令在教程仓库根目录的x64开发者CMD中执行。把示例SDK路径改为实际安装位置。

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/scrollpanel/cpp -B .work/example_scrollpanel -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_scrollpanel --config Release
.work\example_scrollpanel\Release\tutorial_scrollpanel.exe
```

Visual Studio生成器把可执行文件放在`Release`子目录。单配置Ninja生成器直接输出到构建目录。

<<< ../../../../examples/guide/controls/layout-and-container/scrollpanel/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\scrollpanel\python\run.cmd
```

<<< ../../../../examples/guide/controls/layout-and-container/scrollpanel/python/scrollpanel_demo.py

### 运行效果

![scrollpanel独立例程效果](/images/zh/scrollpanel_demo.png)

## 常见问题与布局实践

- 给可见滚动条和控件内容留出空间。只需要上下滚动时可关闭横向滚动条，释放底部视口区域。
- 滚动依赖超出视口的内容。检查子控件的实际位置及尺寸，特别是内容末端是否超出可见范围。
- 将子控件隐藏后，其矩形仍参与内容范围计算。需要缩短滚动区域时更新子控件矩形或从集合移除对应控件。
- 偏移属于受保护的实现接口。普通应用用用户交互滚动，用`on_viewport_changed`观察变化。示意图在WARP测试宿主中把偏移设置到完整行边界，以展示裁剪效果。

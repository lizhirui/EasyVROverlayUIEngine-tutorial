# window

`window`是应用提交给Engine的顶层空间表面，也是子控件的容器。设置工具、状态面板和模态对话框都可以从`window`开始。每个`window`拥有独立的尺寸、显示状态和空间参考对象。

继承[公共控件接口](/guide/controls/common-api#control)和[容器接口](/guide/controls/common-api#container-control)。

## 默认外观

新建`window`时的标题来自构造名称，逻辑尺寸为640×360，状态为隐藏，参考对象为`world`。调用`show()`后标题栏显示默认图标、跟踪选择入口和关闭入口。截图只调整了表面尺寸，并用`label`标明观察项。

![window默认外观](/images/zh/window_default.png)

## 属性对比

|位置|属性变化|观察结果|
|---|---|---|
|左上|默认标题栏|显示标准标题、跟踪选择入口和关闭入口|
|右上|`title_foreground_color`、`title_background_color`和`title_font`|标题改用暖色大号粗体，标题栏背景独立配置|
|左下|`show_close_button = False`|隐藏标题栏的关闭入口|
|右下|`show_title_bar = False`|隐藏整条标题栏，内容区可以上移|

![window属性对比](/images/zh/window_comparison.png)

## 接口参考

C++属性通过表中的访问方法读写，Python通过同名属性访问。表中的事件参数采用C++类型名，Python对应类型省略`_t`后缀。公共成员见[基础接口](/guide/controls/common-api)。

### 属性

|属性|C++|用途与默认值|
|---|---|---|
|`title`|`get_title`、`set_title`|标题文字，初始为构造名称。|
|`title_foreground_color`、`title_background_color`|`get_title_foreground_color`、`set_title_foreground_color`、`get_title_background_color`、`set_title_background_color`|标题文字与背景色，分别默认为`0xFFFFFFFF`和`0x244565FF`。激活状态也会影响标题栏配色。|
|`title_font`|`get_title_font`、`set_title_font`|标题字体，默认Segoe UI、20逻辑像素。|
|`icon`|`get_icon`、`set_icon`|标题图标，初始为SDK图标，赋`None`或空`shared_ptr`可清除。|
|`menu`|`get_menu`、`set_menu`|与标题栏下方命令区域关联的`menubar`，初始为空。|
|`show_title_bar`、`show_close_button`|`get_show_title_bar`、`set_show_title_bar`、`get_show_close_button`、`set_show_close_button`|标题栏和标准关闭入口的显示开关，初始为真。|
|`tracking_mode_set`|`get_tracking_mode_set`、`set_tracking_mode_set`|允许在标题栏切换的模式，默认包含`world`、`body`、`left`、`right`、`head`。空集合隐藏入口。|
|`movable`、`resizable`、`curvature_adjustable`|`get_movable`、`set_movable`、`get_resizable`、`set_resizable`、`get_curvature_adjustable`、`set_curvature_adjustable`|分别控制手柄移动与旋转、交互缩放、交互曲率调整，初始为真。|
|`physical_scale`|`get_physical_scale`、`set_physical_scale`|正有限缩放倍数，初始为1.0。每逻辑像素基准为1毫米，首次显示时可从来源继承未显式配置的缩放。|
|`physical_width`、`physical_height`|`get_physical_width`、`get_physical_height`|只读，表面展开宽度与高度，单位为米。|
|`curvature`|`get_curvature`、`set_curvature`|曲率，单位为米的倒数，默认0.0为平面。曲率与展开宽度的积须小于`2π`。|
|`position`、`rotation`|`get_position`、`set_position`、`get_rotation`、`set_rotation`|初始均为零。位置为相对于参考对象的左上角偏移，单位为米，旋转为XYZ欧拉角，单位为度。|
|`startup_position`|`get_startup_position`、`set_startup_position`|首次定位方式，默认为`center`。`none`使用配置的参考对象和位姿。|
|`reference_object`|`get_reference_object`、`set_reference_object`|空间参考对象，默认`world`。|
|`world_transform`|`get_world_transform`|只读，表示表面中心的世界位姿。参考不可用时返回`None`或空`optional`。|
|`loaded`、`closed`|`get_loaded`、`get_closed`|只读，分别表示完成首次加载及已关闭，初始为假。|
|`auxiliary`|`get_auxiliary`、`set_auxiliary`|辅助表面标志，初始为假。IME和layout会话中的表面由Engine关联到输入区。|
|`dialog_result`|`get_dialog_result`、`set_dialog_result`|初始为`none`。模态期间赋有效结果会关闭窗口并返回该结果。|
|`visible`、`rect`|`get_visible`、`set_visible`、`get_rect`、`set_rect`|继承的显示状态和逻辑矩形。构造后隐藏，初始尺寸为640×360。|

### 方法

|Python|C++|用途|
|---|---|---|
|`window(name)`|`window(name)`|构造顶层表面。|
|`show()`、`hide()`|`show()`、`hide()`|显隐表面。首次`show()`触发加载，后续显隐保留窗口。|
|`close(force=False)`|`close(force=false)`|请求关闭。返回是否已关闭，强制关闭会跳过取消环节。|
|`activate()`|`activate()`|请求激活现有表面。|
|`show_dialog(owner_window)`|`show_dialog(owner_window)`|同步运行自身模态循环，暂时阻止直接所有者的交互，关闭时返回`dialog_result`。|
|`set_size(width,height)`|`set_size(width,height)`|设置正的逻辑宽高。|
|`reparent(reference,keep_world=False)`|`reparent(reference,keep_world=false)`|切换参考对象，可选择保存世界位姿。|
|`is_tracking_available(mode)`|`get_is_tracking_available(mode)`|查询指定参考对象是否可用。|
|`center_at_view(distance)`|`center_at_view(distance)`|按给定米数在视线前方居中，返回定位结果。|
|`get_default_icon()`|`get_default_icon()`|静态方法，获取SDK默认图标。|

### 事件

|事件|触发条件与参数|
|---|---|
|`on_title_changed`、`on_title_foreground_color_changed`、`on_title_background_color_changed`、`on_title_font_changed`|标题文字、配色或字体改变。|
|`on_icon_changed`、`on_menu_changed`|图标或关联的`menubar`变化。|
|`on_show_title_bar_changed`、`on_show_close_button_changed`、`on_tracking_mode_set_changed`|标题栏、关闭入口或跟踪选择集合变化。|
|`on_movable_changed`、`on_resizable_changed`、`on_curvature_adjustable_changed`|空间交互开关变化。|
|`on_rotation_changed`、`on_curvature_changed`、`on_startup_position_changed`、`on_reference_object_changed`|旋转、曲率、启动定位方式或参考对象变化。三维位置变化使用继承的`on_moved`。|
|`on_load`、`on_shown`、`on_hidden`|分别在首次加载、显示和隐藏时触发。|
|`on_closing`、`on_closed`|关闭前使用`cancel_event_args_t`，可设置`cancel`；成功后触发`on_closed`。|
|`on_render_failed`|提交绘制失败，参数为`render_error_event_args_t`。|
|`on_tracking_lost`、`on_tracking_restored`|参考对象丢失或恢复。|
|`on_activated`、`on_deactivated`|当前表面激活或失去激活。|
|`on_move_start`、`on_move_end`、`on_resize_start`、`on_resize_end`、`on_curvature_adjust_start`、`on_curvature_adjust_end`|交互移动、缩放、调整曲率的开始和结束。结束事件使用`interaction_end_event_args_t`。|

## 独立例程

启动后单击“切换标题栏配色”，观察标题栏背景变化，再单击一次可恢复初始配色。关闭窗口后事件循环退出。

先按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程仓库根目录打开已配置MSVC的x64 CMD，使用实际安装的SDK路径。

### C++

```bat
cmake -S examples/guide/controls/window-and-text/window/cpp -B .work/example_window -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_window --config Release
.work\example_window\Release\tutorial_window.exe
```

上面的可执行文件路径对应Visual Studio生成器。使用单配置Ninja时，可执行文件直接位于构建目录。

<<< ../../../../examples/guide/controls/window-and-text/window/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\window\python\run.cmd
```

<<< ../../../../examples/guide/controls/window-and-text/window/python/window_demo.py

### 运行效果

![window独立例程运行效果](/images/zh/window_demo.png)

## 常见问题与实践

- 逻辑坐标与物理位姿分别配置。修改物理摆放使用`position`、`rotation`和`reference_object`，调整控件布局使用`rect`或`set_size()`。
- 显式控制首帧位姿时先设`startup_position = none`。已有表面换参考系并保持位置时使用`reparent(..., keep_world=True)`。
- `hide()`适合临时收起。`close()`结束实例生命周期，再打开同样的界面时创建新实例。隐藏标准关闭入口后，应在应用流程中保留明确的关闭操作。
- `show_dialog()`使用同应用中可交互的其他`window`作为所有者。对话框实例应在首次显示前进入模态模式。

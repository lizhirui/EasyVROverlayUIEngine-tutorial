# Python API参考

控件用法与完整示例见[控件目录](/guide/)。窗口、事件与线程调度分别见[window](/guide/controls/window-and-text/window)和[强类型事件与多线程调度](/guide/07_events_dialogs_threading)。

普通控件的name采用`type_用途`，例如`button_ok`。设计器导出的公开控件成员与对应name同名，可直接通过`button_ok`访问；窗体类名对应设计文件名。

本文介绍`easyvrui`的公开接口及调用规则。方法签名省略`self`。

## 1.导入与运行约定

### 1.1.应用组成

安装后的Python应用使用安装根目录下的`sdk/api/python/`。该目录集中存放`easyvrui/`、静态链接的`engine_interface_native*.pyd`和`requirements.txt`。解释器须匹配安装记录中的CPython版本和x64架构。由Desktop或File Manager通过SDK启动清单时，子进程的`PYTHONPATH`会前置此目录并保留原值，`EASYVRUI_NATIVE_DIR`也指向此目录。从CMD直接运行示例时，先将此目录前置到`PYTHONPATH`。

从源码开发时，可将`repo/sdk/api/python/`加入模块搜索路径，并用`EASYVRUI_NATIVE_DIR`指定构建出的扩展所在目录。加载器还支持从`EASYVRUI_ENGINE_INTERFACE`所指库文件的父目录查找扩展。自行构建采用DLL链接的扩展时，需部署匹配的`engine_interface.dll`。安装器部署的扩展已包含原生实现。

Python API运行部分使用标准库和预编译扩展。应用自己的Python依赖记录在对应应用目录的`requirements.txt`。示例应用位于`repo/app/demo/python`，其控件派生类属于应用示例。

```python
from easyvrui import button, rect, run, window

window_main = window("window_main")
window_main.title = "Example"
button_ok = button("button_ok")
button_ok.rect = rect(40, 90, 180, 44)
button_ok.text = "OK"
window_main.control_list.add(button_ok)
window_main.show()
run("example")
```

### 1.2.模块与命名空间

`import easyvrui`提供公开入口。子模块中的控件和值类型引用同一原生类。

|导入位置|公开接口|
|---|---|
|`easyvrui`|控件、值类型、事件、绘图、对话框、应用函数和输入组件|
|`easyvrui.application`|`run`、`set_application_name`、`pump`、输入界面及应用管理函数|
|`easyvrui.application_management`|应用清单、启动、运行快照及会话与窗口管理|
|`easyvrui.control`|控件及其集合|
|`easyvrui.common.color/rect/font`|颜色、矩形和字体|
|`easyvrui.common.error`|语言选择和本地化异常|
|`easyvrui.geometry`|`vec3`、`quat`、`pose`|
|`easyvrui.dialog`|标准对话框函数、文件筛选及消息框枚举|
|`easyvrui.event`|`event_container`和强类型事件参数|
|`easyvrui.render`|`render_context`、`drawing_path`、`drawing_image`、`drawing_fill_rule`|
|`easyvrui.input`|`input_provider`、角色、输入事件和组件状态|

下表列出`easyvrui`顶层应用接口。

|名称|名称|名称|名称|
|---|---|---|---|
|`application_entry`|`application_runtime`|`application_snapshot`|`application_type`|
|`application_window`|`blank`|`button`|`cancel_event_args`|
|`checkbox`|`close_application_window`|`color`|`color_dialog`|
|`combobox`|`combobox_dropdown_style`|`container_control`|`control`|
|`control_base`|`control_collection`|`control_collection_event_args`|`control_input_event_args`|
|`control_input_type`|`controller_event_args`|`dialog_result`|`drawing_fill_rule`|
|`drawing_image`|`drawing_path`|`drawing_path_operation`|`drawing_path_segment`|
|`engine_error`|`error_diagnostic`|`error_key`|`event_args`|
|`event_container`|`file_filter`|`file_open_dialog`|`file_save_dialog`|
|`font`|`font_dialog`|`get_application_directory`|`get_application_snapshot_list`|
|`get_error_diagnostic`|`get_error_language`|`get_error_message`|`get_language_key`|
|`get_localized_error`|`get_preferred_ui_language`|`get_reference_object_type_name`|`grid`|
|`grid_cell`|`grid_cell_event_args`|`grid_cell_render`|`grid_column`|
|`grid_column_event_args`|`grid_selection_mode`|`hide_input_ui`|`image`|
|`image_stretch_mode`|`input_event`|`input_event_type`|`input_provider`|
|`input_provider_state`|`input_role`|`input_ui_state`|`inputbox`|
|`interaction_end_event_args`|`item_collection`|`item_control`|`key_event_args`|
|`keyboard_key`|`keyboard_modifier`|`label`|`language_key`|
|`language_pack`|`launch_application`|`listbox`|`listview`|
|`listview_cell_collection`|`listview_column`|`listview_column_collection`|`listview_column_event_args`|
|`listview_item`|`listview_item_collection`|`listview_item_event_args`|`localized_invalid_argument`|
|`localized_runtime_error`|`measure_text`|`menu_container`|`menu_item_event_args`|
|`menubar`|`menuitem`|`messagebox`|`messagebox_button`|
|`messagebox_button_set`|`messagebox_icon`|`numericupdown`|`orientation`|
|`panel`|`parse_keyboard_key`|`parse_reference_object_type`|`pointer_event_args`|
|`pose`|`progressbar`|`property_changed_event_args`|`provider_info`|
|`pump`|`quat`|`radiobutton`|`read_application_entry`|
|`rect`|`reference_object`|`reference_object_type`|`render_context`|
|`render_error_event_args`|`render_rectangle`|`render_style`|`request_application_snapshot_list`|
|`request_close_application_window`|`request_error`|`request_terminate_application`|`run`|
|`screen`|`scroll_event_args`|`scrollpanel`|`select_error_language`|
|`selection_control`|`set_application_name`|`show_input_ui`|`slider`|
|`splitter`|`startup_position`|`tab_position`|`tabcontrol`|
|`tabpage`|`tabpage_collection`|`tabpage_event_args`|`terminate_application`|
|`text_control`|`text_input_event_args`|`textbox`|`toolbar`|
|`toolbar_button`|`toolbar_button_collection`|`tree_node`|`tree_node_collection`|
|`tree_node_event_args`|`treeview`|`vec3`|`window`|

### 1.3.设计文件导出布局

生成的Python布局文件使用`import easyvrui`。全部非root控件以`self.<control.name>`公开，属性名与控件name完全一致；名称在整份设计中唯一，符合C++与Python标识符规则，并避开root SDK公开入口。

生成类自身只有`__init__`，默认name使用设计根节点的名称，例如`def __init__(self, name = "sample_form"):`。构造函数创建控件，通过`control_list`或`page_list`建立归属关系，再初始化属性和值记录。

图像与图标调用`easyvrui.drawing_image.load_file()`等SDK绘图资源接口。业务类持有生成窗体实例，通过同名属性绑定事件、读取和修改控件属性。

Form Designer是独立app，设计文件扩展名为`.easyvruifrm`，可导出Python和C++设计代码。属性面板propertygrid属于该app内部派生控件，普通应用使用通用grid。生成的Python设计类通过公开API创建控件、配置属性并组装容器。

### 1.4.参数、返回值与数据类型

接口表使用Python类型描述。绑定中明确声明名称的参数可使用关键字实参；部分直接映射的方法只注册了位置参数。下文签名中的`/`表示应按位置调用，以函数签名中的位置参数标记为准。

|类型|调用约定|
|---|---|
|`str`|Unicode文本；控件名称、显示文本、字体族等均使用普通Python字符串|
|`int`|无符号64位字段接受`0`至`2**64-1`；颜色接受`0`至`2**32-1`；有符号64位字段接受`-(2**63)`至`2**63-1`|
|`float`|对应双精度数值；空间位置、旋转角度、缩放和绘图坐标按接口要求校验有限性及范围|
|`bool`|开关；应用代码应传`True`或`False`|
|`None`|没有对象、没有选中项或可选值缺失；具体含义见对应接口|
|`list`、`set`|从属性读取时通常得到快照；修改快照后需要重新赋回属性。专门的集合类型见集合章节|

文本位置按Unicode码点计数，与Python的`len(text)`和切片索引一致。组合字符、变体选择符及多码点表情可能占多个位置；用户交互中的光标移动与删除会按文本边界处理，程序设置选区时应使用合法文本位置。

### 1.5.对象、线程与更新

在创建线程上操作控件和窗口。容器中的对象属于同一应用运行环境。`begin_invoke()`用于从其他线程安排创建线程上的工作，实际执行依赖应用继续调用`run()`或`pump()`。回调应尽快返回；耗时工作可移交后台线程，再通过`begin_invoke()`更新控件。

普通控件构造函数统一为`类型(name: str)`。`name`不能为空，不能包含空字符；构造后只读。同一集合内名称唯一，重复添加名称会抛出异常。一个控件同时只能有一个父容器，也不能形成循环父子关系。

控件属性在应用内读写。影响显示的属性修改会安排重新绘制；自定义绘图依赖的普通Python成员变化后，调用`invalidate()`。应用循环处理输入、事件和待提交更新。`render()`返回后，本次绘图由框架统一提交；绘图回调中按顺序调用绘图接口即可。

## 2.基础值类型

### 2.1.rect

导入：`from easyvrui import rect`。

构造：`rect(left: int = 0, top: int = 60, width: int = 160, height: int = 40)`。

|成员|读写|用途|
|---|---|---|
|`left: int`|读写|逻辑矩形左边位置|
|`top: int`|读写|逻辑矩形上边位置|
|`width: int`|读写|逻辑宽度|
|`height: int`|读写|逻辑高度|
|`a == b -> bool`|运算符|逐字段比较|

四个字段均为无符号64位整数。独立`rect`对象保存自己的值；从`control.rect`取得的对象是与该控件关联的视图，因此`button_ok.rect.left = 80`会直接更新控件。将独立矩形赋给`control.rect`时按值写入。控件矩形要求`width > 0`、`height > 0`。

普通子控件的位置相对于父容器；窗口的`rect.left/top`不参与空间定位，窗口位置使用`position`。

### 2.2.color

构造为`color(value: int | color = 0)`。颜色整数使用`0xRRGGBBAA`，高24位为RGB，最低8位为透明度。透明度`0`完全透明，`255`完全不透明。

|成员|用途|
|---|---|
|`value: int`|读写完整颜色值，范围为无符号32位整数|
|`r: int`、`g: int`、`b: int`、`a: int`|读写红、绿、蓝、透明度分量，范围为`0`至`255`|
|`rgba: list[int]`|只读，依次返回红、绿、蓝、透明度|
|`hex_string: str`|只读，带`0x`前缀的八位十六进制颜色文本|
|`color.create_from_rgba(r: int, g: int, b: int, a: int = 255) -> color`|按四个分量构造颜色|
|`color.create_from_hex(text: str) -> color`|解析八位十六进制颜色文本，支持`0x`前缀|
|`create_with_alpha(alpha: int, /) -> color`|返回替换透明度后的新颜色|
|`int(value)`、`value.__index__()`|取得完整颜色整数|
|`str(value)`|取得十六进制颜色文本|
|`a == b`|比较完整颜色值|

控件颜色属性接受颜色整数和`color`对象，读取时返回`int`。绘图方法的颜色参数使用整数，可通过`int(color_object)`转换。

### 2.3.font

构造为`font(family: str = "Segoe UI", size: int = font.DEFAULT_SIZE, bold: bool = False, italic: bool = False)`。类常量`font.DEFAULT_SIZE`为`18`。

|成员|用途|
|---|---|
|`family: str`|读写系统字体族名称|
|`size: int`|读写逻辑字号，类型为无符号64位整数|
|`bold: bool`|读写粗体状态|
|`italic: bool`|读写斜体状态|
|`a == b`|逐字段比较|

将字体赋给控件时，`family`须非空且不含空字符，`size`须大于`0`。读取控件的`font`属性会得到独立的字体值。修改字号时，可先取得`style = textbox_text.font`，再设置`style.size = 22`并将`style`赋回控件。

### 2.4.vec3

构造为`vec3(x: float = 0.0, y: float = 0.0, z: float = 0.0)`。`x/y/z`均可读写。

|成员|用途|
|---|---|
|`a == b`|逐分量近似比较|
|`a + b -> vec3`、`a - b -> vec3`|逐分量加减|
|`value * scalar -> vec3`、`scalar * value -> vec3`|乘标量|
|`calculate_dot_product(other: vec3, /) -> float`|点积|
|`calculate_cross_product(other: vec3, /) -> vec3`|叉积|
|`length: float`|只读，向量长度|
|`normalized: vec3`|只读，返回同方向的单位向量。方向为零、过小或含非有限数值时抛出异常|
|`vec3.is_equal(left: float, right: float) -> bool`|按照双精度epsilon和数值规模近似比较两个标量|

空间位置用米，窗口欧拉角用度。修改窗口位置时整体赋值，例如`window_main.position = vec3(0.1, 0.0, 0.0)`。

### 2.5.quat

构造为`quat(x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0)`。`x/y/z/w`均可读写，默认值表示单位旋转。

|成员|用途|
|---|---|
|`a * b -> quat`|组合旋转，先应用`b`，再应用`a`|
|`length: float`|只读，四元数的长度|
|`normalized: quat`|只读，单位四元数|
|`inverse: quat`|只读，逆旋转|
|`euler: vec3`|只读，以度表示的XYZ欧拉角|
|`rotate(value: vec3, /) -> vec3`|旋转向量|
|`slerp(target: quat, amount: float) -> quat`|沿四元数最短弧插值，进度`0.0`对应当前旋转，`1.0`对应目标旋转|
|`quat.create_from_axis_angle(axis: vec3, angle: float) -> quat`|绕指定单位轴旋转，角度单位为度|
|`quat.create_from_axis_basis(a: vec3, b: vec3, c: vec3, /) -> quat`|从旋转后的三个正交基轴构造旋转|
|`quat.create_from_euler(angles: vec3) -> quat`|从以度表示的XYZ欧拉角构造旋转|

欧拉角组合满足`Rz * Ry * Rx`。读取`euler`时可能得到等价角度。

### 2.6.pose

构造为`pose(position: vec3 = vec3(), rotation: quat = quat())`。`position/rotation`均可读写。

|成员|用途|
|---|---|
|`a * b -> pose`、`a @ b -> pose`|组合位姿，先应用`b`，再应用`a`|
|`inverse: pose`|只读，逆位姿|
|`matrix: tuple[tuple[float, ...], ...]`|只读，按行返回4×4齐次变换矩阵，最后一列包含平移分量|
|`transform_point(value: vec3, /) -> vec3`|把局部点转换到该位姿所处参考系|

窗口的可配置位置和旋转分别为`position`与`rotation`。

## 3.控件继承树和公共约定

```text
control_base
└── control
    ├── blank
    ├── text_control
    │   ├── button
    │   │   └── toolbar_button
    │   ├── checkbox
    │   ├── selection_control
    │   │   ├── item_control
    │   │   │   ├── combobox
    │   │   │   └── listbox
    │   │   ├── grid
    │   │   ├── listview
    │   │   └── treeview
    │   ├── label
    │   ├── numericupdown
    │   ├── radiobutton
    │   ├── textbox
    ├── container_control
    │   ├── menu_container
    │   │   ├── menubar
    │   │   └── menuitem
    │   ├── panel
    │   │   └── tabpage
    │   ├── scrollpanel
    │   ├── splitter
    │   ├── tabcontrol
    │   ├── toolbar
    │   └── window
    ├── image
    ├── progressbar
    ├── screen
    └── slider
```

派生类继承祖先公开的属性、方法和事件；blank的实例隐藏规则见对应章节。普通控件通过`类型(name: str)`创建。`control_base`为Python派生类提供`super().__init__(name: str, type: str)`，直接创建control_base实例会抛TypeError。`menu_container(name: str, type: str)`提供菜单容器基类的构造入口。Python控件派生方式见“绘图与自定义控件”。

Python接入适配提供`control/text_control/selection_control/item_control/container_control`的`(name: str, type: str)`构造重载，供自定义派生类型指定类型名；这些类型的单参数构造仍使用各自原生类型名。

### 3.1.属性访问

使用点号读取属性，例如`textbox_entry.text`，使用赋值修改可写属性，例如`textbox_entry.text = "Hello"`。

`control_list`和`page_list`为可直接操作的集合入口，通过集合方法修改归属；`item_list`是字符串项目可直接操作的集合，整体赋值可替换文本列表。其他普通列表或集合属性通常返回快照，修改后需要重新赋回。事件成员通过`+=/-=`订阅。

### 3.2.control_base

Python派生类在构造函数中调用`super().__init__(name, type)`完成原生基类初始化。

|属性|读写|用途|
|---|---|---|
|`name: str`|只读|构造时确定的对象名称|
|`tag: str`|读写|应用保存的字符串标记，默认为空字符串。值改变时触发`on_tag_changed`，回调签名为`handler(source, event_args)`|
|`type: str`|只读|对象的控件类型名称；Python派生类沿用对应原生控件类型|
|`disposed: bool`|只读|是否已经释放，初始为`False`|
|`id: int`|只读|对象编号|
|`parent: container_control \| None`|只读|直接父容器|

|签名|用途|
|---|---|
|`invalidate() -> None`|请求重新绘制|
|`dispose() -> None`|释放对象及其相关资源；容器会连带处理子对象|
|`begin_invoke(callback: Callable[[], None], /) -> None`|安排在对象创建线程执行回调；对象失效后尚未执行的调用会取消|
|`process_input(event: control_input_event_args, /) -> None`|处理分发给对象的输入；可由派生类覆盖|

|事件|用途|
|---|---|
|`on_disposed`|对象释放。参数为`event_args`。|
|`on_property_changed`|属性发生变化时触发，`event.property_name`为变化的属性名。参数为`property_changed_event_args`。|

### 3.3.control

通用可视控件，增加矩形、背景、可见性、可用性及Tab顺序。

|属性|类型与初始值|用途|
|---|---|---|
|`rect`|`rect(0, 60, 160, 40)`|控件逻辑矩形，可修改子字段|
|`tooltip_text`|`str = ""`|悬停提示。窗口在激光指向控件时显示文字|
|`background_color`|`int = 0x162738FF`|背景色|
|`visible`|`bool = True`|是否显示|
|`enabled`|`bool = True`|是否接受交互|
|`tab_index`|`int = 0`|Tab导航排序，使用无符号64位整数|

|签名|用途|
|---|---|
|`show() -> None`|显示控件|
|`hide() -> None`|隐藏控件|
|`focus() -> None`|请求将焦点转移到该控件|
|`activate() -> None`|执行控件的程序化激活动作，例如触发按钮点击或项目选择|
|`focusable: bool`|查询是否可获得键盘焦点；普通`control`默认`False`，派生类可覆盖|
|`absolute_rectangle: rect`|返回窗口内的控件逻辑矩形。|
|`get_input_rectangle() -> rect`|返回独立矩形，描述控件本地输入区域，派生类可覆盖。|
|`focused: bool`|查询焦点状态。|
|`owning_window: window \| None`|返回所属窗口。|
|`get_content_top() -> float`|取得顶部内容偏移；普通控件为`0.0`，窗口会计入标题栏及控制环|
|`render(context: render_context, /) -> None`|绘制控件主体，可覆盖|
|`render_overlay(context: render_context, /) -> None`|绘制弹出菜单等覆盖内容，可覆盖|

Tab导航只选择当前窗口可见、可用、可聚焦的控件，`Tab`前进、`Shift+Tab`后退。`tab_index = 0`按坐标排序；可显式指定正值控制顺序。具体排序及循环规则见后面的焦点章节。

|事件|用途|
|---|---|
|`on_background_color_changed`|背景色变化。参数为`event_args`。|
|`on_visible_changed`|可见性变化。参数为`event_args`。|
|`on_enabled_changed`|可用性变化。参数为`event_args`。|
|`on_tab_index_changed`|Tab顺序变化。参数为`event_args`。|
|`on_moved`|二维位置变化；窗口中还用于通知三维位置变化。参数为`event_args`。|
|`on_size_changed`|逻辑尺寸变化；窗口物理比例变化也会发出尺寸通知。参数为`event_args`。|
|`on_pointer_enter`|激光指针进入。参数为`pointer_event_args`。|
|`on_pointer_leave`|激光指针离开。参数为`pointer_event_args`。|
|`on_pointer_move`|激光指针移动。参数为`pointer_event_args`。|
|`on_pointer_down`|激光触发按下。参数为`pointer_event_args`。|
|`on_pointer_up`|激光触发松开。参数为`pointer_event_args`。|
|`on_click`|完成点击。参数为`event_args`。|
|`on_scroll`|滚动输入。参数为`scroll_event_args`。|
|`on_viewport_changed`|滚动视口变化时触发。参数为`event_args`。|
|`on_focus_in`|获得焦点。参数为`event_args`。|
|`on_focus_out`|失去焦点。参数为`event_args`。|
|`on_key_down`|键盘按下。参数为`key_event_args`。|
|`on_key_up`|键盘松开。参数为`key_event_args`。|

#### blank

`blank(name: str)`可从`easyvrui`、`easyvrui.control`或`easyvrui.control.blank`导入，继承control，用于保存命名矩形占位。

|基本属性|调用规则|
|---|---|
|`name: str`|构造时指定，只读|
|`rect: rect`|可读写；可更新矩形子字段|

on_moved、on_size_changed、on_property_changed和on_disposed保持可用；`dispose()`、`disposed`、`invalidate()`和`begin_invoke(callback)`沿用基类生命周期与调度规则。对象标识与释放状态查询遵循control_base约定。

|实例隐藏入口|行为|
|---|---|
|`visible/enabled/background_color/tab_index`|读取或赋值均抛出AttributeError|
|`show/hide/focus/activate/focusable`|实例访问抛出AttributeError|
|`render/render_overlay/process_input/get_input_rectangle/get_content_top`|实例访问抛出AttributeError|
|背景色、可见性、可用性、Tab顺序变化事件，以及激光、点击、滚动、焦点、键盘和手柄事件|实例访问抛出AttributeError|

原生对象仍可由框架经control基类接口管理；原生布局将`visible`和`enabled`视为`False`。Python实例通过blank的属性访问入口遵守上表的隐藏规则。

```python
from easyvrui import blank, rect

blank_content = blank("blank_content")
blank_content.rect = rect(24, 80, 600, 320)
```

### 3.4.text_control

提供文字显示相关样式。该基类只增加样式；具体的`text`由`label/button/textbox/combobox`等类型提供。

|属性|类型与初始值|用途|
|---|---|---|
|`foreground_color`|`int = 0xD1DEF0FF`|文字前景色|
|`font`|`font()`|文字字体|

事件：`on_foreground_color_changed`在前景色改变时触发；`on_font_changed`在字体改变时触发。

### 3.5.selection_control

`selection_control`可从`easyvrui`、`easyvrui.control`或`easyvrui.control.selection_control`导入，继承`text_control`。`item_control`、`grid`、`listview`和`treeview`继承该层，`listbox/combobox`继承`item_control`。Python自定义派生类可实现`clear_selection()`并覆写`is_blank_at(local_left, local_top)`；从具体控件派生时可通过`super()`复用原生实现。

|成员|用途|
|---|---|
|`clear_selection_on_blank_click: bool = False`|空白点击时是否清除项选择，用于空白点击的选择策略|
|`on_clear_selection_on_blank_click_changed`|空白点击取消选择的设置变化时触发。参数为`event_args`。|
|`is_blank_at(local_left, local_top) -> bool`|查询本地坐标是否为项目区域中的空白，可覆盖|
|`clear_selection() -> None`|清除项选择；自定义selection_control派生类负责实现|

listbox、treeview、grid和listview的项目区域空白点击会退出文本编辑、关闭IME/layout，并保留集合控件的键盘导航焦点。配置为True时清除项选择；False时保留项选择。表头、滚动条、列宽调节区及弹出选项按各自功能处理。切换到另一个文本框时，一次点击完成焦点与输入界面的转移；按钮等控件保留各自的焦点及Tab行为。

### 3.6.item_control

带字符串项目、单项选择和按行滚动的基类，默认可聚焦。

|属性|类型与初始值|读写及用途|
|---|---|---|
|`item_list`|`item_collection`，初始为空|可修改集合；整体赋值接受`list[str]`|
|`selected_index`|`int = -1`|读写；`-1`表示未选择，其余值须是已有项目下标|
|`selected_item`|`str = ""`|只读；当前选中项目，未选择时为空字符串|
|`row_height`|`int = 32`|读写；每行的逻辑高度，须大于`0`|

修改项目集合可能清除超出范围的选中项，并将滚动位置限制在有效范围。事件为`on_item_list_changed`、`on_selected_index_changed`、`on_selection_changed`、`on_row_height_changed`，分别通知项目、索引、选择、滚动和行高变化。

### 3.7.container_control、panel和tabpage

`container_control`继承`control`。普通子控件统一由可直接操作的集合管理：

|成员|用途|
|---|---|
|`active_item_list: list[control]`|查询当前参与显示和交互的直接控件。|
|`control_list: control_collection`|只读集合入口|
|`on_control_added`|控件加入时触发。通过`control_collection_event_args`读取控件`item`及其索引`index`。|
|`on_control_removed`|控件移出时触发。通过`control_collection_event_args`读取控件`item`及移出前的索引`index`。|

```python
from easyvrui import button, panel

panel_main = panel("panel_main")
button_ok = button("button_ok")
button_ok.text = "OK"
panel_main.control_list.add(button_ok)
button_same = panel_main.control_list["button_ok"]
button_removed = panel_main.control_list.remove(button_ok)
panel_main.control_list.add(button_removed)
```

`panel(name)`是普通容器。`tabpage(name)`是选项卡的内容容器，页面正文通过自己的`control_list`组装。页面归属由`tabcontrol.page_list`管理。

|页签属性或事件|用途|
|---|---|
|`text: str = ""`|页签标题，修改后刷新所属`tabcontrol`|
|`on_text_changed`|页签标题变化时触发。参数为`event_args`。|

## 4.具体控件

### 4.1.label

继承`text_control`。构造：`label(name: str)`。

|成员|用途|
|---|---|
|`text: str = ""`|读写显示文字|
|`on_text_changed`|文字变化。参数为`event_args`。|

标签用于显示文字，默认不参与键盘导航。

### 4.2.button

继承`text_control`。构造：`button(name: str)`。

|成员|用途|
|---|---|
|`text: str = ""`|读写按钮文字|
|`on_text_changed`|文字变化。参数为`event_args`。|
|继承的`on_click`|执行按钮业务逻辑|

按钮可聚焦。按钮点击处理函数可设置所属窗口的`dialog_result`属性结束模态。

### 4.3.textbox

继承`text_control`。构造：`textbox(name: str)`。可聚焦并提供文本选择、编辑和滚动。

|属性|类型与初始值|读写及用途|
|---|---|---|
|`text`|`str = ""`|读写；文本内容|
|`read_only`|`bool = False`|读写；限制交互编辑|
|`selectable`|`bool = True`|读写；是否允许光标、选择和交互输入|
|`multiline`|`bool = False`|读写；开启多行编辑与Enter换行|
|`horizontal_scrollbar_visible`|`bool = False`|读写；横向滚动条显示开关|
|`vertical_scrollbar_visible`|`bool = False`|读写；纵向滚动条显示开关|
|`max_length`|`int = 0`|读写；码点数量上限，`0`表示不限制|
|`selection_start`|`int = 0`|读写；选区较小端位置|
|`selection_length`|`int = 0`|读写；选区码点长度|
|`selected_text`|`str = ""`|读写，读取当前选区文本。赋值以程序方式替换选区，包括只读文本框|
|`can_undo`、`can_redo`|`bool = False`|只读；当前编辑历史是否支持撤销或重做|

|签名|用途|
|---|---|
|`select(start: int, length: int = 0) -> None`|按起始位置和长度选择；长度为`0`时移动插入位置|
|`undo() -> bool`|撤销一次编辑。成功时返回`True`|
|`redo() -> bool`|重做一次编辑。成功时返回`True`|

文本设置和替换应用多行及长度约束；`\r\n`和`\r`归一化为`\n`，单行模式移除换行。过滤及截断保留完整文本边界。选区位置限制在有效范围内，非边界位置按选择方向调整。滚动条开关与`multiline`分别控制显示和换行能力。

`read_only = True`允许保留光标、选择和复制，交互输入及删除保持文本不变。`selectable = False`时控件仍可获得焦点，文本光标、选择、输入编辑和IME/layout界面均停用；应用仍可通过`text`属性更新显示内容。

|事件|用途|
|---|---|
|`on_text_changed`|文本内容变化。参数为`event_args`。|
|`on_read_only_changed`|只读开关变化。参数为`event_args`。|
|`on_selectable_changed`|选择及交互输入开关变化。参数为`event_args`。|
|`on_selection_changed`|选区或插入位置变化。参数为`event_args`。|
|`on_max_length_changed`|长度限制变化。参数为`event_args`。|
|`on_multiline_changed`|多行开关变化。参数为`event_args`。|
|`on_horizontal_scrollbar_visible_changed`|横向滚动条开关变化。参数为`event_args`。|
|`on_vertical_scrollbar_visible_changed`|纵向滚动条开关变化。参数为`event_args`。|
|`on_text_input`|文本编辑输入通知|

纵向内容可滚动时，将激光指向文本框后，使用对应手柄摇杆上下滚动，偏转幅度决定速度；也可拖动滚动条。

文本编辑器拥有焦点时，Ctrl+Z撤销修改，Ctrl+Y或Ctrl+Shift+Z恢复修改。这些按键优先于应用菜单快捷键。

### 4.4.combobox

继承`item_control`。构造：`combobox(name: str)`。

|属性|类型与初始值|用途|
|---|---|---|
|`dropdown_style`|`combobox_dropdown_style.dropdown_list`|`dropdown`可编辑，`dropdown_list`从列表选择|
|`dropped_down`|`bool = False`|下拉列表是否展开，可读写|
|`text`|`str = ""`|显示或编辑的文本；选择已有项时同步为该项目|

事件为`on_dropdown_style_changed`、`on_text_changed`；项目和选择事件继承自`item_control`。

`dropdown_list`时，非空`text`必须匹配已有项目；设为空字符串可清除选择。`dropdown`时，新文本可以使`selected_index`变为`-1`。选中项目始终通过`selected_index/selected_item`读取。下拉列表由单击展开；仅激光当前指向项显示悬停高亮。

### 4.5.listbox

继承`item_control`。构造：`listbox(name: str)`。本层将默认`row_height`改为`30`，其余公开属性、方法和事件使用继承接口。

超过可显示行数时自动提供纵向滚动条。激光指向列表时，可用对应手柄摇杆上下滚动，也可拖动滚动条。`selected_index = -1`取消选择。

### 4.6.tabcontrol

继承`container_control`。构造：`tabcontrol(name: str)`。

|属性|类型与初始值|读写及用途|
|---|---|---|
|`page_list`|`tabpage_collection`，初始为空|只读集合入口，管理页面及页签文字|
|`selected_index`|`int = -1`|读写；当前页面下标，`-1`表示无选中页|
|`page_close_button_visible`|`bool = False`|读写；是否显示页签关闭按钮|
|`selected_page`|`tabpage \| None`|只读；当前页面对象|
|`tab_position`|`tab_position.top`|读写；接受枚举或`"top"/"bottom"/"left"/"right"`字符串|
|`tab_size`|`int = 36`|读写；页签栏厚度，须大于`0`|
|`tab_font`|`font()`|读写；页签字体|
|`tab_foreground_color`|`int = 0xD1DEF0FF`|读写；普通页签文字颜色|
|`tab_background_color`|`int = 0x162738FF`|读写；普通页签背景色|
|`selected_tab_foreground_color`|`int = 0xFFFFFFFF`|读写；选中页签文字颜色|
|`selected_tab_background_color`|`int = 0x316B9AFF`|读写；选中页签背景色|

`tab_position`枚举可从`easyvrui`导入，成员为`top/bottom/left/right`。

页面通过`page_list.add(page)`添加，页签外观和活动页面由`tabcontrol`管理。主内容区域沿用容器背景，悬停效果作用于具体页签。`tabcontrol`统一使用`page_list`；访问其`control_list`，包括经基类入口调用，会抛出包含`page_list_required`诊断的`RuntimeError`。

|事件|用途|
|---|---|
|`on_selected_index_changed`|选中页下标变化。参数为`event_args`。|
|`on_selection_changed`|页面选择变化。参数为`event_args`。|
|`on_tab_position_changed`|页签栏位置变化。参数为`event_args`。|
|`on_tab_size_changed`|页签栏厚度变化。参数为`event_args`。|
|`on_tab_font_changed`|页签字体变化。参数为`event_args`。|
|`on_tab_foreground_color_changed`|普通页签文字颜色变化。参数为`event_args`。|
|`on_tab_background_color_changed`|普通页签背景色变化。参数为`event_args`。|
|`on_selected_tab_foreground_color_changed`|选中页签文字颜色变化。参数为`event_args`。|
|`on_selected_tab_background_color_changed`|选中页签背景色变化。参数为`event_args`。|
|`on_page_added`|页面加入；数据包含`page/index/text`。参数为`tabpage_event_args`。|
|`on_page_removed`|页面移出；数据包含`page/index`。参数为`tabpage_event_args`。|
|`on_page_text_changed`|页签标题变化时触发。通过`tabpage_event_args.page.text`读取当前标题。|
|`on_page_close`|请求关闭页签时触发。通过`tabpage_event_args`读取页签`page`及其索引`index`。|
|`on_page_close_button_visible_changed`|页签关闭按钮的显示设置变化。参数为`event_args`。|

`page`事件字段为页面对象的数值标识，`index`从`0`开始。通过集合获得页面对象。

```python
from easyvrui import label, rect, tabcontrol, tabpage

tabcontrol_main = tabcontrol("tabcontrol_main")
tabcontrol_main.rect = rect(20, 80, 560, 260)
tabpage_general = tabpage("tabpage_general")
label_info = label("label_info")
label_info.rect = rect(20, 20, 300, 36)
label_info.text = "General settings"
tabpage_general.control_list.add(label_info)
tabpage_general.text = "General"
tabcontrol_main.page_list.add(tabpage_general)
tabcontrol_main.selected_index = 0
```

点击页签关闭图标或在页签聚焦时按Delete触发`on_page_close`。应用确认保存后从`page_list`移除`event.page`。

### 4.7.window

继承`container_control`。构造：`window(name: str)`。窗口初始隐藏，`title`初始为`name`，`rect`初始为`rect(0, 0, 640, 360)`，`background_color`初始为`0x0D1624FF`。

`startup_position`枚举可从`easyvrui`、`easyvrui.control`或`easyvrui.control.window`导入，成员为`none/center`。

center首次定位与来源窗口平行、中心对齐，并沿朝向头显的法线前移；模态窗口使用直接父窗口。没有有效来源时按头显居中，初始距离取`max(1.2, max(physical_width, physical_height))`米。Engine结合各会话可见普通窗口安排初始深度，响应由SDK事件循环同步到position/rotation。启动定位只应用一次，后续隐藏和显示保留当前位姿。none使用配置的参考对象与位姿。输入组件辅助窗口由Engine关联输入区定位。

|属性|类型与初始值|读写及用途|
|---|---|---|
|`title`|`str = name`|读写；标题文字|
|`title_foreground_color`|`int = 0xFFFFFFFF`|读写；标题文字颜色|
|`title_background_color`|`int = 0x244565FF`|读写；标题栏背景色|
|`title_font`|`font("Segoe UI", 20)`|读写；标题字体|
|`icon`|`drawing_image \| None，默认原生图标`|读写；标题栏左侧图标，等比缩放并垂直居中；设为None时标题直接使用左侧空间|
|`window.get_default_icon() -> drawing_image`|静态方法，读取原生默认图标；赋给icon恢复默认值|
|`curvature`|`float = 0.0`|读写；圆柱曲面的曲率，单位为米的倒数，0表示平面|
|`physical_scale`|`float = 1.0`|读写；逻辑像素物理尺寸的缩放倍数，须为正有限数；1倍时每逻辑像素为1毫米|
|`position`|`vec3()`|读写；窗口左上角相对于参考对象的位置偏移，单位为米|
|`rotation`|`vec3()`|读写；XYZ欧拉角，单位为度|
|`reference_object`|`reference_object()`|读写；包含`type: reference_object_type`的参考目标记录，默认world|
|`show_title_bar`|`bool = True`|读写；是否显示标题栏|
|`tracking_mode_set`|`set[reference_object_type]`|读写；标题栏跟踪选择器中的模式集合，初始包含`world/body/left/right/head`|
|`show_close_button`|`bool = True`|读写；标题栏关闭按钮|
|`movable`|`bool = True`|读写；是否允许通过手柄移动和旋转|
|`resizable`|`bool = True`|读写；是否允许交互缩放|
|`startup_position`|`startup_position.center`|读写；接受枚举或`"none"/"center"`字符串。none使用初始位置和姿态；center首次显示时优先与来源窗口平行居中并向头显前移，无有效来源时按头显居中|
|`curvature_adjustable`|`bool = True`|读写；控制左下角曲率按钮的显示和交互，关闭时立即取消当前拖动及摇杆调整，重新启用后松开trigger再按可开始调整|

`physical_scale = 1.0`时每逻辑像素对应1毫米。`rect.width * physical_scale / 1000.0`是表面展开宽度，曲面窗口中对应展开弧长。`curvature`记为k、展开宽度记为W：属性合法域为有限`k >= 0`且`k * W < 2π`；设置曲率和缩放时均须满足这一关系。通过窗口左下角手柄入口交互调节时，采用160°的安全弧角上限；该交互上限与属性合法域分别处理。左右下角入口由trigger按住，直到松开保持选中和激光捕获；曲率用摇杆左右调节，大小用摇杆上下调节，左下角双击恢复平面。

`reference_object_type`枚举包含`world/body/head/left/right`。`reference_object()`构造默认world记录，`reference_object(type)`接收该枚举；记录的`type`可读写。`get_reference_object_type_name(value: reference_object_type) -> str`返回名称，`parse_reference_object_type(value: str) -> reference_object_type`解析名称。两个reference_object记录按type比较；与枚举比较时使用`item.reference_object.type`，与名称比较时使用`get_reference_object_type_name(item.reference_object.type)`。

Python接入适配允许`reference_object`赋值及`reparent()`参数使用reference_object记录、reference_object_type枚举或五种模式名称字符串；读取reference_object始终返回记录。`tracking_mode_set`赋值接受`set`或`frozenset`，元素可为枚举，也可使用接入适配的模式字符串或reference_object记录；读取返回枚举集合快照。空集合隐藏切换按钮，需要添加模式时整体赋回。

|其他状态属性|读写及用途|
|---|---|
|`closed: bool`|只读；是否已关闭，初始为`False`|
|`loaded: bool`|只读；是否已经首次显示，初始为`False`|
|`dialog_result: dialog_result`|读写，进入模态时重置为`none`。模态期间赋非`none`的值会关闭窗口，直接关闭返回`cancel`|
|`physical_width: float`|只读；展开宽度，等于`rect.width * physical_scale / 1000`|
|`physical_height: float`|只读；实际高度，等于`rect.height * physical_scale / 1000`|
|`auxiliary: bool`|读写；辅助输入表面标志，初始为`False`；IME/layout会话的窗口自动成为辅助表面，并由Engine维护位置、参考和跟随输入窗口的缩放|

|签名|用途|
|---|---|
|`show() -> None`|显示普通窗口；首次显示触发加载事件|
|`hide() -> None`|隐藏窗口并取消相应交互；结束该窗口的活动模态状态|
|`activate() -> None`|请求激活该窗口|
|`show_dialog(owner_window: window) -> dialog_result`|同步显示模态窗口，期间禁用直接所有者并继续分发UI事件。关闭后返回结果枚举|
|`close(force: bool = False) -> bool`|请求关闭窗口，成功时返回`True`。force为True时跳过关闭取消回调|
|`set_size(width: int, height: int, /) -> None`|设置逻辑矩形宽高，须大于`0`|
|`reparent(reference: reference_object \| reference_object_type \| str, keep_world: bool = False) -> None`|更换参考对象；传入keep_world=True时保持世界位姿|
|`world_transform: pose \| None`|读取当前可解析的世界位姿；跟踪参考不可用时可为`None`|
|`is_tracking_available(mode: reference_object_type) -> bool`|查询指定参考模式当前是否可以跟踪|
|`center_at_view(distance: float, /) -> bool`|在视线前方指定米数处居中窗口，定位成功时返回`True`|

`world_transform`返回窗口表面中心的世界位姿。`position`配置左上角偏移。直接赋值`reference_object`后，现有偏移按新参考系解释。需要保持世界位姿时使用`reparent(reference, keep_world = True)`。

`show_dialog(owner_window)`要求所有者是同一UI运行时内可交互的其他窗口，对话框须隐藏、尚未关闭且未进入模态。调用在同一UI线程进入嵌套消息循环，直接所有者暂时失去交互资格。可从按钮或菜单事件调用，并用当前可交互对话框作为下一层所有者。渲染提交期间调用会报错。详见[会话与嵌套模态循环](/advanced/04_session_and_context)。

进入模态时将`dialog_result`重置为`dialog_result.none`。设置其他结果会请求关闭。处理器取消关闭时，对话框保持活动，结果恢复到设置前的值。结果仍为`none`时通过标题栏关闭按钮或`close()`成功关闭，返回`dialog_result.cancel`。调用方可保留窗口实例，在返回后读取控件值。

首次显示普通新窗口时，仅在未显式设置`physical_scale`时，依次从同session的模态owner、当前事件分发窗口、正在执行on_load的窗口、当前输入窗口、活动窗口和最近可见普通窗口中确定来源并继承其缩放。显式设置的值优先，包括1.0；显示后可再次设置比例。相同倍率下，相同逻辑尺寸的控件具有相同物理尺寸；`set_size()`改变逻辑画布及对应的物理尺寸。

|参考对象|用途|
|---|---|
|`"world"`|位于引擎世界参考空间，用户移动或转头时保持空间位置|
|`"head"`|跟随头部位置和旋转|
|`"left"`|跟随左手控制器参考姿态|
|`"right"`|跟随右手控制器参考姿态|
|`"body"`|跟随经过颈部枢轴补偿的位置，保持校准时的朝向；转头可观察周围窗口|

`startup_position = startup_position.none`且`position = vec3()`、`rotation = vec3()`时，世界模式窗口左上角位于初始正前方参考中心。

center的模态窗口使用直接父窗口；其它center窗口优先沿用SDK提供的同session来源，来源省略时由Engine采用当前选中的可见普通表面，可跨session用于Desktop启动其它App。Engine沿来源的正面或背面朝向头显的法线安排初始深度，完成响应同步最终position/rotation；后续隐藏与显示保持已确定的姿态。

`Ctrl+Alt+Pause`将Body中心及World整体布局映射到当前头显，系统报告为`Ctrl+Alt+Break`时作用相同。`Ctrl+Pause`显示或隐藏引擎配置中的Desktop应用。

可移动窗口在World和Body模式支持侧握键单手抓取；双手分别抓住外围不同控制点时进行约束轴旋转。窗口前后两面均可显示及交互，背面文字为正面镜像。窗口逻辑尺寸足够大且启用移动时，外围控制环占用逻辑矩形内侧空间；布置子控件时可参考`get_content_top()`避开标题栏。

|事件|用途|
|---|---|
|`on_title_changed`|标题变化。参数为`event_args`。|
|`on_title_foreground_color_changed`|标题文字颜色变化。参数为`event_args`。|
|`on_title_background_color_changed`|标题栏背景色变化。参数为`event_args`。|
|`on_title_font_changed`|标题字体变化。参数为`event_args`。|
|`on_icon_changed`|标题图标对象改变或清空。参数为`event_args`。|
|`on_rotation_changed`|三维旋转变化。参数为`event_args`。|
|`on_curvature_changed`|曲率变化。参数为`event_args`。|
|`on_curvature_adjust_start`|曲率交互调整开始。参数为`event_args`。|
|`on_curvature_adjust_end`|曲率交互调整结束。参数为`interaction_end_event_args`。|
|`on_reference_object_changed`|参考对象变化。参数为`event_args`。|
|`on_show_title_bar_changed`|标题栏显示开关变化。参数为`event_args`。|
|`on_tracking_mode_set_changed`|标题栏允许的模式集合变化。参数为`event_args`。|
|`on_show_close_button_changed`|关闭按钮开关变化。参数为`event_args`。|
|`on_movable_changed`|移动开关变化。参数为`event_args`。|
|`on_resizable_changed`|缩放开关变化。参数为`event_args`。|
|`on_startup_position_changed`|启动定位方式变化。参数为`event_args`。|
|`on_curvature_adjustable_changed`|曲率交互调整开关变化。参数为`event_args`。|
|`on_load`|第一次显示时加载，每个窗口一次。参数为`event_args`。|
|`on_shown`|从隐藏状态显示。参数为`event_args`。|
|`on_hidden`|隐藏。参数为`event_args`。|
|`on_closing`|关闭前询问；可写`event.cancel = True`取消普通关闭。参数为`cancel_event_args`。|
|`on_closed`|完成关闭；数据可包含关闭`reason`。参数为`event_args`。|
|`on_render_failed`|绘制提交失败。参数为`render_error_event_args`。|
|`on_tracking_lost`|参考对象跟踪丢失。参数为`event_args`。|
|`on_tracking_restored`|参考对象跟踪恢复。参数为`event_args`。|
|`on_activated`|窗口激活。参数为`event_args`。|
|`on_deactivated`|窗口失去激活。参数为`event_args`。|
|`on_move_start`|移动或约束旋转开始。参数为`event_args`。|
|`on_move_end`|移动或约束旋转结束。参数为`interaction_end_event_args`。|
|`on_resize_start`|交互缩放开始。参数为`event_args`。|
|`on_resize_end`|交互缩放结束。参数为`interaction_end_event_args`。|

三维位置变化使用继承的`on_moved`，物理宽度变化使用继承的`on_size_changed`。窗口隐藏或关闭会取消抓取、指针捕获及关联输入界面。关闭后需要创建新窗口实例再次显示。

### 4.8.checkbox和radiobutton

两者继承`text_control`，构造为`checkbox(name)`和`radiobutton(name)`。读写属性为`text: str = ""`和`checked: bool = False`；文字变化触发`on_text_changed`，勾选状态变化触发`on_checked_changed`。颜色和字体沿用继承属性。点击checkbox切换勾选；radiobutton用于同一父容器中的互斥选项。

### 4.9.numericupdown

继承`text_control`，构造为`numericupdown(name)`。中间文本区可编辑数值，上下三角按钮分别获得悬停和焦点；点击调节按钮保持数值操作焦点，文本输入界面只关联文本编辑区域。

|属性|初始值与约束|
|---|---|
|`value: float`|0.0，有限数，限制在最小值与最大值之间|
|`minimum: float`|0.0，须小于maximum|
|`maximum: float`|100.0，须大于minimum|
|`step: float`|1.0，正有限数|
|`decimal_places: int`|0，范围0至17，控制显示的小数位数|

相关事件为`on_value_changed/on_minimum_changed/on_maximum_changed/on_step_changed/on_decimal_places_changed`。修改上下限时会相应限制当前值。

### 4.10.slider和progressbar

两者继承`control`，构造只需name。公开`minimum: int = 0`、`maximum: int = 100`、`value: int = 0`，整数使用有符号64位范围。minimum严格小于maximum，value限制在该范围内；事件为`on_minimum_changed/on_maximum_changed/on_value_changed`。

`slider`还提供`orientation: orientation = orientation.horizontal`，只接受`orientation.horizontal`或`orientation.vertical`；事件包括`on_orientation_changed/on_drag_start/on_drag_end`。拖动滑块或键盘导航修改value。`progressbar`按范围显示进度。

### 4.11.listview

`listview(name)`继承`selection_control`，按行呈现多列文字。点击表头触发`on_column_click`，应用据此排序。拖动表头分隔线可以调整宽度。

|接口|用途|
|---|---|
|`listview_column(text = "", width = 100)`|`text`和`width`可读写。宽度为正，修改会重排视图。|
|`listview_item(cell_list = [], icon = None, tag = "")`|`cell_list`保存各列文字，`icon`显示在首列，`tag`保存应用标签。|
|`column_list: listview_column_collection`|列集合，支持原地修改和整体赋值。|
|`item_list: listview_item_collection`|行集合，支持原地修改和整体赋值。|
|`selected_index: int`、`selected_item: listview_item \| None`|读写主选择，空选择对应`-1`及`None`。|
|`select_item(index, extend = False, toggle = False)`|按下标选择行。多选时可扩展选区或切换目标行。|
|`selected_item_list: list[listview_item]`、`multi_select: bool`|读取选区对象、设置多选。|
|`row_height`、`header_height`|读写行高和表头高度，`header_height = 0`隐藏表头。|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|读取当前可见行数与滚动条状态。|
|`on_item_list_changed`、`on_column_list_changed`、`on_column_width_changed`|视图内容及列宽变化。|
|`on_selection_changed`、`on_row_double_click`、`on_column_click`|选择变化、激活行及点击表头。|

`item.cell_list`是`listview_cell_collection`。可以用`item.cell_list[0] = "Updated"`修改单元格，也可以整体赋值。列表按行对象保持选区，排序时将同一批行对象按新顺序赋回。

### 4.12.treeview与tree_node

`treeview(name)`继承`selection_control`。根节点通过`node_list: tree_node_collection`管理，`selected_node: tree_node | None`读写当前选中对象。`row_height`和`vertical_scrollbar_visible`为只读属性。

`tree_node(text = "", expanded = False, tag = "")`提供同名读写属性。`parent`返回父节点或`None`，`node_list`管理子节点。通过`expand()`和`collapse()`调整展开状态。每个节点同时归属一个树集合。

树视图提供`on_node_list_changed`、`on_selection_changed`、`on_node_expanded`、`on_node_collapsed`和`on_node_activated`。节点事件的数据字段`node`是节点标签。

```python
root = easyvrui.tree_node("Project", expanded = True, tag = "root")
child = easyvrui.tree_node("Engine")
root.node_list.append(child)
tree = easyvrui.treeview("treeview_project")
tree.node_list.append(root)
tree.selected_node = child
```

### 4.13.scrollpanel和splitter

`scrollpanel(name)`继承`container_control`，通过`control_list`添加普通控件。可写`horizontal_scrollbar_visible/vertical_scrollbar_visible`默认均为True，各有对应的变化事件。滚动范围由内容决定，视口变化发出`on_viewport_changed`。

`splitter(name)`继承`container_control`，集合至多容纳两个面板控件，顺序对应第一侧和第二侧。

|属性|用途|
|---|---|
|`orientation: orientation = orientation.vertical`|`orientation.vertical`以竖直分隔条划分左右区域。`orientation.horizontal`以水平分隔条划分上下区域。|
|`split_position: float = 0.5`|分隔比例，有限且位于0.0至1.0之间|

相关事件为`on_orientation_changed/on_split_position_changed/on_split_start/on_split_end`。布局由容器计算，拖动分隔条更新split_position。

### 4.14.image和screen

`image(name)`继承`control`：

|成员|用途|
|---|---|
|`source: drawing_image \| None`|图像对象|
|`stretch_mode: image_stretch_mode = image_stretch_mode.contain`|读写，接受`image_stretch_mode`的`fill/contain/cover/none`|

fill填满矩形，contain保持比例完整显示，cover保持比例覆盖矩形并裁剪，none使用图像原尺寸。事件为`on_source_changed/on_stretch_mode_changed/on_source_unavailable`。

`screen(name)`继承`control`，用于显示屏幕实时图像：

|成员|用途|
|---|---|
|`screen_id: int = 0`|屏幕标识|
|`screen_available: bool`|只读，当前屏幕是否可用，初始False|
|`on_screen_id_changed`|屏幕选择变化。参数为`event_args`。|
|`on_screen_unavailable/on_screen_restored`|屏幕不可用及恢复|

画面按控件矩形显示，鼠标指针随屏幕画面显示。原始画面清晰度与控件逻辑尺寸相关；需要逐像素显示时，将screen控件宽高设置为对应显示器分辨率。窗口的physical_scale独立控制其物理大小。

### 4.15.图标工具栏与悬停提示

`toolbar`、`toolbar_button`、`toolbar_button_collection`可从`easyvrui`或`easyvrui.control`导入，也可从各自同名子模块导入。`toolbar`构造函数只接收不可变的`name`。`toolbar`继承`container_control`。

`toolbar_button(name)`继承`button`，是工具栏项目，由`toolbar.button_list`管理。每个按钮将图标、点击区域和悬停提示作为一个整体显示。

|对象|属性|用途|
|---|---|---|
|`toolbar`|`tool_size: int = 40`|正方形工具格边长，必须为正整数|
|`toolbar`|`spacing: float = 6.0`|有限非负间距|
|`toolbar`|`button_list: toolbar_button_collection`|只读，工具按钮及分隔线的可直接操作的集合|
|`toolbar_button`|`icon: drawing_image \| None`|工具图标|
|`toolbar_button`|继承的`tooltip_text: str = ""`|悬停提示，空字符串关闭提示|
|`toolbar_button`|`enabled: bool = True`|是否可执行|
|`toolbar_button`|`separator: bool = False`|显示为细分隔线|

`toolbar`提供`on_tool_size_changed/on_spacing_changed`；`toolbar_button`提供`on_click/on_icon_changed`以及继承的对象事件。工具栏管理布局，按钮响应悬停和点击。

```python
from easyvrui import drawing_image, toolbar, toolbar_button

toolbar_main = toolbar("toolbar_main")
toolbar_main.rect.width = 200
toolbar_main.rect.height = 40
button_add = toolbar_button("toolbar_button_add")
button_add.icon = drawing_image(1, 1, bytes([120, 210, 255, 255]))
button_add.tooltip_text = "Add an item"
toolbar_main.button_list.add(button_add)
button_separator = toolbar_button("toolbar_button_separator")
button_separator.separator = True
toolbar_main.button_list.add(button_separator)
window_main.control_list.add(toolbar_main)
textbox_entry.tooltip_text = "Enter the text to translate."
```

示例中的`window_main`和`textbox_entry`由应用创建，目标文本框属于该窗口。独立tooltip默认零矩形，随目标悬停显示和消失。文本按字素边界换行，提示框限制在窗口内容区域内，高度不足时显示省略号。

### 4.16.菜单栏与菜单项

`menu_container`继承`container_control`，是`menubar`和`menuitem`的公共基类。两种控件均以名称构造。

`window.menu`读写`menubar`或`None`，变化触发`on_menu_changed`。菜单栏位于标题栏下方。它同时属于窗口的`control_list`：通过集合添加菜单栏、移出当前菜单栏或清空集合时，`menu`关联同步更新；设置`menu`也同步集合归属。菜单位置使用集合中的实际索引，每个窗口使用一个菜单栏。

```python
from easyvrui import menubar, menuitem

menubar_main = menubar("menubar_main")
menuitem_file = menuitem("menuitem_file")
menuitem_file.text = "File"
menuitem_save = menuitem("menuitem_save")
menuitem_save.text = "Save"
menuitem_save.shortcut = "Ctrl+S"
menuitem_file.control_list.add(menuitem_save)
menubar_main.control_list.add(menuitem_file)
window_main.menu = menubar_main
```

示例中的`window_main`由应用创建；执行回调通过`menuitem_save.on_click += handler`注册。

|对象|属性、方法及用途|
|---|---|
|`menu_container`|继承普通`control_list`；集合只接收`menuitem`；`owning_menubar`取得所属菜单栏；`on_item_added/on_item_removed`通知集合变化|
|`menuitem`|读写`text/shortcut/checkable/checked/separator/icon`。只读属性`open: bool`表示当前子菜单是否展开。通过`control_list`管理下级菜单|
|`menubar`|读写`font/row_height`；`open_menu()`和`close(restore_focus = True)`控制展开状态；`open`和`is_submenu_open(item)`查询展开状态|

菜单项提供`on_text_changed/on_icon_changed/on_shortcut_changed/on_checkable_changed/on_checked_changed/on_separator_changed`；菜单栏提供`on_font_changed/on_row_height_changed`。两者均有`on_opening/on_closed`，菜单项执行使用继承的`on_click`。

### 4.17.grid

`grid`继承`selection_control`，提供多列数据、选择和编辑。

|类型|接口|
|---|---|
|`grid_column(text = "", width = 100, editable = True)`|可写字段`text/width/editable`|
|`grid_cell(row = 0, column = 0)`|可写字段`row/column`，索引从0开始|
|`grid_selection_mode`|`cell/row`|
|`grid_cell_render`|渲染回调记录。`cell/rectangle/value/selected/hovered/editing`均可读写，`rectangle`的类型为`render_rectangle`|

单元格值支持`str`、有符号64位范围的`int`、有限`float`和`bool`。`grid(name)`的可写属性为`column_list/row_count/selected_index/selection_mode/multi_select/row_height/header_height/read_only/edit_text`；只读属性为`editing/edit_cell/edit_error/selected_cell_list`。

|方法|用途|
|---|---|
|`grid[row, column]`读写|数据读写|
|`set_data_provider(row_count, reader, writer = None)`|reader(row, column)返回值；writer(row, column, value)处理写入|
|`refresh_data()`|通知外部数据已更新|
|`set_cell_renderer(renderer)`|renderer(context, cell)绘制可见单元格；None恢复默认|
|`set_edit_validator(validator)`|validator(cell, value)校验编辑；None清除校验器|
|`get_value_text(value)`|静态方法，将值转为文本|
|`select_cell(row, column, extend = False, toggle = False)`、`clear_selection()`、`is_cell_selected(row, column)`|选择控制|
|`get_cell_at(left, top)`|查询本地坐标命中的单元格|
|`get_cell_rectangle(row, column) -> render_rectangle`|查询指定单元格的矩形|
|`vertical_scrollbar_visible/horizontal_scrollbar_visible`|滚动条状态|
|`visible_row_count`|当前可见行数|
|`set_column_width(column, value)`|调整列宽|
|`begin_edit(row, column)`、`commit_edit()`、`commit_edit(value)`、`cancel_edit()`|编辑生命周期，begin/commit返回bool|

writer和validator可返回`None`表示成功、bool表示结果、字符串表示失败原因，或`(bool, str)`同时给出结果与原因。数据提供器的写入需由writer更新实际数据源。派生类可覆盖`read_cell_value(row, column)`、`write_cell_value(row, column, value)`和`render_cell(context, cell)`；写入覆盖采用相同返回约定。

事件为`on_column_list_changed/on_column_width_changed/on_column_click/on_selection_changed/on_cell_double_click/on_cell_value_changed/on_row_height_changed/on_header_height_changed/on_edit_started/on_edit_committed/on_edit_cancelled/on_edit_failed`。事件使用与其它控件相同的`+=/-=`订阅方式。

单击可编辑单元格即可编辑，IME定位到当前编辑单元格的可见矩形。只读列用于选择和查看。`selection_mode`接受`grid_selection_mode.cell/row`或`"cell"/"row"`字符串。表头背景铺满控件宽度，列标题超长时显示省略号；`header_height = 0`隐藏表头。

列宽默认100。`column_list`返回独立的列记录。赋值给`column_list`或调用`set_column_width()`时，列宽须为正且整组列宽之和须在有符号64位整数范围内。校验成功后才应用列布局并发出对应事件。

读取`column_list`得到快照，修改后需重新赋回。Grid单元格只读时用于选择和查看；可编辑单元格单击进入编辑，切换单元格协调焦点及输入界面。多选通过`multi_select`启用，Ctrl逐项切换、Shift扩展选择；实体键盘修饰键仅在实体捕获模式参与交互。

## 5.集合接口

### 5.1.control_collection

通过普通容器的`control_list`获得。集合保持顺序，并支持按不可变`name`查找；名称查找使用映射，通常接近常数时间。`control_collection(owner: container_control)`可构造与owner关联的独立集合，供派生类型扩展；owner原有的control_list入口仍指向其内置集合。

|签名或操作|返回值与用途|
|---|---|
|`add(item: control)`、`append(item: control)`|返回加入的原对象，追加到末尾|
|`insert(index: int, item: control)`|返回加入的原对象，在指定位置插入|
|`extend(item_list: Iterable[control], /) -> None`|依次追加；中途出错时已追加项保留|
|`remove(key: str \| int \| control, /) -> control`|按名称、下标或对象移出并返回对象|
|`remove_at(index: int)`、`pop(index: int = -1) -> control`|按下标移出，默认最后一项|
|`clear() -> None`|移出全部子控件|
|`collection[key] -> control`|按名称或下标查询；缺失名称抛`KeyError`，越界抛`IndexError`|
|`del collection[key]`|按名称、下标或对象移出，返回值忽略|
|`index_of(key: str \| int \| control, /) -> int`|取得项目位置；整数参数会校验并转换为实际下标|
|`key in collection`|按名称或对象身份检查|
|`len(collection)`|项目数量|
|`iter(collection)`|遍历当时的对象列表快照|

读取和删除允许负下标，`-1`表示末尾。插入时负下标先加当前长度，再限制在`0`至长度之间；大于末尾的位置追加到最后。使用`collection[start:stop:step]`获取切片，`list(collection)`获取快照。移出与`dispose()`用途不同：移出后仍可保留并使用对象，满足条件时可加入其他容器。

Python派生集合可覆盖`insert(self, index, item)`、`remove(self, index)`和`clear(self)`，原生虚调用会分发到对应Python方法；覆盖方法中可调用super的同名方法完成基类操作。Python接入的`append/extend/pop`和负下标是集合使用适配。

集合视图保留所属owner的Python引用，查询得到的借用引用按绑定维护其依赖关系。Python派生控件由原生集合持有时，其重载方法和实例属性保持有效。owner、集合及Python附加属性形成的引用环参与GC；移出的共享对象可独立持有，`dispose()`用于显式结束原生对象及其资源。

### 5.2.tabpage_collection

通过`tabcontrol.page_list`获得。`tabpage_collection`继承`control_collection`，共享同一份页面存储，标题由页面自身保存。`tabpage_collection(owner: tabcontrol)`可构造与owner关联的独立页面集合；owner原有的page_list入口保持原对象。插入项目必须是`tabpage`，通过下标或名称查询页面对象。

|签名或操作|返回值与用途|
|---|---|
|`add(page: tabpage)`、`append(page: tabpage)`|追加并返回页面|
|`insert(index: int, page: tabpage)`|返回页面，在指定位置插入|
|`extend(page_list: Iterable[tabpage], /) -> None`|依次追加各页面|
|`remove(key: str \| int \| tabpage, /) -> control`|移出并返回页面|
|`remove_at(index: int)`、`pop(index: int = -1) -> control`|移出并返回指定页面|
|`clear() -> None`|清空全部页面|
|`collection[key] -> tabpage`、`del collection[key]`|查询或移出页面|
|`index_of(key: str \| int \| tabpage, /) -> int`|页面下标|
|`key in collection`|按名称或页面对象检查|
|`len(collection)`、`bool(collection)`|数量及空状态|
|`iter(collection)`|遍历页面快照|

删除和插入页面后，选中页下标按实际页面关系调整。同一集合名称唯一。移除操作返回持有动态类型的控件对象；实际仍为原tabpage，可直接加入另一个page_list。`list(collection)`返回页面引用快照。

页面集合支持覆盖`insert(self, index, page)`及继承的移除扩展点。

### 5.3.item_collection

`item_collection`从`easyvrui.control`导入，是原生`item_collection`类型的别名；实例由`combobox.item_list`、`listbox.item_list`或`item_control.item_list`提供。内容为字符串，允许重复文本。该集合的Python包装保留所属控件引用，并参与引用环GC。

|签名或操作|返回值与用途|
|---|---|
|`add(value: str, /) -> None`、`append(value: str, /) -> None`|追加字符串|
|`insert(index: int, value: str, /) -> None`|插入；负下标及超出末尾的位置按集合插入规则处理|
|`extend(value_list: Iterable[str], /) -> None`|依次追加|
|`assign(value_list: list[str], /) -> None`|替换全部内容|
|`remove(value: str \| int, /) -> str`|移除第一个匹配字符串，或指定下标项，返回被移除文本|
|`remove_at(index: int)`、`pop(index: int = -1) -> str`|移除并返回指定项目|
|`clear() -> None`|清空|
|`collection[index_or_value]`|按下标或文本读取；支持负下标、切片|
|`collection[index] = value`|替换指定文本|
|`del collection[index]`|移除指定项目|
|`index_of(value: str, /) -> int`|第一个匹配文本的下标；找不到时报错|
|`value in collection`|检查是否包含文本|
|`len(collection)`、`bool(collection)`|数量及空状态|
|`iter(collection)`|遍历文本快照|

### 5.4.toolbar_button_collection

`toolbar.button_list`提供工具栏按钮集合。通过`len(collection)`和`bool(collection)`查询数量和空状态，`item in collection`按名称或对象检查成员，`collection[index_or_name]`支持整数、负数、切片及名称。通过`index_of(item)`取得位置，`add(item)`、`add_button(item)`和`insert(index, item)`接受按钮对象或名称字符串，`add_separator(name)`添加分隔线，`remove(item)`、`remove_at(index)`和`clear()`移出项目。迭代使用快照。

`listview_column_collection`、`listview_item_collection`、`listview_cell_collection`和`tree_node_collection`支持长度、包含、正负下标、切片和迭代。用`append/add/insert`添加，`remove/remove_at/clear`移出，`assign`替换全部内容。单元格集合还支持下标赋值和删除。

### 5.5.菜单集合

菜单使用与普通容器相同的`control_collection`，支持按名称或索引查找，以及`add/insert/remove/clear`。多级菜单由菜单项嵌套组成。`separator = True`显示分隔线；`checkable/checked`控制勾选；`shortcut`记录快捷键，`&A`或`(&A)`表示助记键。

## 6.强类型事件

### 6.1.订阅方式与event_container

控件的`on_xxx`成员提供`event_container`。事件容器通过对象获得；回调接收来源控件`source`和事件参数`event`。形参签名为`handler(source, event)`。

```python
def button_ok_click(source, event):
    source.text = "Clicked"

button_ok.on_click += button_ok_click
button_ok.on_click -= button_ok_click
```

|签名或操作|用途|
|---|---|
|`add(callback) -> int`|追加回调并返回订阅token|
|`remove(callback_or_token) -> bool`|移除一个匹配回调或token；成功为`True`|
|`event += callback`|追加回调，保留同一个事件对象|
|`event -= callback_or_token`|移除回调或token，保留同一个事件对象|
|`clear() -> None`|移除全部回调|
|`len(event)`|订阅数量|
|`event.call(source, args)`、`event(source, args)`|向当前订阅者分发事件|
|`bool(event) -> bool`|存在订阅时为`True`|

按注册顺序执行，同一回调可注册多次；每次移除只处理一个匹配订阅。订阅标识用于移除指定回调。输入组件的`on_state_changed/on_input`使用相同的订阅操作，回调参数分别为`input_ui_state`、`input_event`。

### 6.2.事件参数

参数类可从`easyvrui`或`easyvrui.event`导入。下表中`event_args`为空基类，其余18种参数类均继承它。例如`issubclass(cancel_event_args, event_args)`为`True`。回调期间设置相应参数的`event.cancel`或`event.handled`，原生分派会读取回写的状态。集合及树节点参数提供可读取的对象引用，索引从0开始。

|参数类型|字段|用途|
|---|---|---|
|`event_args`|无|点击、焦点、窗口生命周期和各专属属性变化。|
|`cancel_event_args`|`cancel: bool`|关闭窗口前设置`cancel`可取消普通关闭。强制关闭始终执行。|
|`key_event_args`|`key: str`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`、`handled: bool`|键名、修饰键和消费状态。|
|`text_input_event_args`|`text: str`、`handled: bool`|提交的文本和消费状态。|
|`pointer_event_args`|`hand: str`、`left: float`、`top: float`、`x: float`、`y: float`、`captured: bool`、`cancelled: bool`、`handled: bool`、`has_position: bool`、`has_local_position: bool`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`|包含手别、窗口坐标`left/top`、控件局部坐标`x/y`和修饰键。用`has_position`和`has_local_position`判断对应坐标是否有效。|
|`scroll_event_args`|`hand: str`、`delta_x: float`、`delta_y: float`、`handled: bool`|手别、横纵滚动量和消费状态。|
|`interaction_end_event_args`|`cancelled: bool`|移动、缩放、曲率调整或拖动结束。`cancelled`表示操作被取消。|
|`property_changed_event_args`|`property_name: str`|`property_name`为变化的属性名。通过`source`读取当前值。|
|`control_collection_event_args`|`item: control &#124; None`、`index: int`|集合中的控件与索引。整表通知的`item`为空。|
|`menu_item_event_args`|`item: menuitem &#124; None`、`index: int`|菜单项与索引。|
|`tabpage_event_args`|`page: tabpage &#124; None`、`index: int`|页签对象与索引。|
|`listview_column_event_args`|`column: listview_column &#124; None`、`index: int`|ListView列对象与索引。整表通知的`column`为空。|
|`listview_item_event_args`|`item: listview_item &#124; None`、`index: int`|ListView项对象与索引。整表通知的`item`为空。|
|`grid_column_event_args`|`index: int`、`width: int`|Grid列索引与宽度。点击表头时通过`index`读取列索引。|
|`grid_cell_event_args`|`row: int`、`column: int`、`error: str`|Grid单元格行列索引。编辑失败时`error`包含错误说明。|
|`tree_node_event_args`|`node: tree_node &#124; None`|操作的树节点。取消选择时`node`为空。|
|`render_error_event_args`|`message: str`|渲染异常的消息。|
|`controller_event_args`|`hand: str`、`trigger: bool`、`grip: bool`、`joystick_x: int`、`joystick_y: int`、`joystick_pressed: bool`、`primary: bool`、`secondary: bool`|手柄按键和摇杆状态。摇杆轴范围为0至255，`primary`为左手X或右手A，`secondary`为左手Y或右手B。|
|`control_input_event_args`|`type: control_input_type`、`hand: str`、`key: str`、`text: str`、`left: float`、`top: float`、`x: float`、`y: float`、`steps: int`、`horizontal: bool`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`、`captured: bool`、`cancelled: bool`、`handled: bool`、`has_position: bool`、`has_local_position: bool`|派生控件的输入分派参数。通过`type`区分输入，按类型读取字段，设置`handled`可标记已消费。|

`control_input_type`的取值为`none`、`click`、`focus_in`、`focus_out`、`pointer_enter`、`pointer_leave`、`pointer_move`、`pointer_down`、`pointer_up`、`scroll`、`key_down`、`key_up`、`text_input`、`controller_input`。

## 7.绘图与自定义控件

### 7.1.render_context

`render_context`从`easyvrui`或`easyvrui.render`导入。上下文由`render(context)`和`render_overlay(context)`提供，仅在当前绘制回调内有效。

`render_rectangle`是浮点绘图矩形记录，提供可写的`left/top/width/height`字段；`render_rectangle()`各字段初始为0.0，`render_rectangle(left, top, width, height)`按参数构造。`get_rectangle()`、`get_popup_rectangle()`和`get_inset_rectangle()`返回此记录。Python绘图接入同时接受该记录或四个数的序列`(left, top, width, height)`作为矩形参数。

`context.rectangle`是当前控件在绘制画布中的矩形元组，是Python接入的便捷属性。绘图坐标使用同一画布参考系；画控件局部内容时，将局部偏移加到返回的`left/top`。

|属性或签名|用途|
|---|---|
|`rectangle: tuple[float, float, float, float]`|只读；当前owner的绘图矩形|
|`owner: control`|只读；当前绘制的控件|
|`get_rectangle(item: control) -> render_rectangle`|获取指定控件的绘图矩形|
|`get_popup_rectangle(item: item_control) -> render_rectangle`|读取项目控件的弹出区域矩形|
|`is_hovered(item: control) -> bool`|查询控件是否处于悬停状态|
|`is_hovered(item: control, rectangle) -> bool`|查询指定控件的给定矩形是否处于悬停状态|
|`is_focused(item: control) -> bool`|查询控件的视觉焦点|
|`is_blinking() -> bool`|查询当前插入点闪烁周期是否显示|
|`is_active(item: window) -> bool`|查询窗口是否为当前激活窗口|
|`is_blocked(item: window) -> bool`|查询窗口是否受到模态关系阻挡|
|`is_close_button_hovered(item: window) -> bool`|查询窗口关闭按钮的悬停状态|
|`get_hovered_item(item: item_control) -> int`|返回指向的项目下标，未命中为-1|
|`fill(rectangle, color: int) -> None`|填充矩形|
|`outline(rectangle, color: int, thickness: float = 1.0) -> None`|绘制矩形边框|
|`draw_line(x1: float, y1: float, x2: float, y2: float, color: int, thickness: float = 2.0) -> None`|绘制线段|
|`fill_ellipse(center_x: float, center_y: float, radius_x: float, radius_y: float, color: int) -> None`|填充椭圆|
|`outline_ellipse(center_x: float, center_y: float, radius_x: float, radius_y: float, color: int, thickness: float = 1.0) -> None`|绘制椭圆边框|
|`fill_circle(center_x: float, center_y: float, radius: float, color: int) -> None`|填充圆|
|`draw_circle(center_x: float, center_y: float, radius: float, color: int, thickness: float = 1.0) -> None`|绘制圆边框|
|`fill_rounded_rectangle(rectangle, radius_x: float, radius_y: float, color: int) -> None`|填充圆角矩形|
|`outline_rounded_rectangle(rectangle, radius_x: float, radius_y: float, color: int, thickness: float = 1.0) -> None`|绘制圆角矩形边框|
|`draw_text(value: str, font: font, rectangle, color: int, center: bool = False) -> None`|绘制文字，`center=True`居中|
|`measure(text: str, font: font) -> float`|测量文字宽度|
|`draw_image(image: drawing_image, rectangle, opacity: float = 1.0) -> None`|将图像绘制到目标矩形|
|`draw_screen(screen_id: int, rectangle) -> None`|绘制指定显示器的实时画面|
|`fill_path(path: drawing_path, color: int) -> None`|填充路径|
|`outline_path(path: drawing_path, color: int, thickness: float = 1.0) -> None`|绘制路径轮廓|
|`push_clip(rectangle) -> None`|压入裁剪矩形；与已有裁剪共同限制后续绘图|
|`pop_clip() -> None`|恢复上一层裁剪，须与压入匹配|
|`render_control_list(item: window) -> None`|按窗口集合顺序绘制普通控件|
|`render_overlay_list(item: window) -> None`|绘制窗口内控件的浮层|
|`render_control(item: control) -> None`|调用指定控件的主体绘图入口|
|`render_control_overlay(item: control) -> None`|调用指定控件的浮层绘图入口|
|`render_context.get_inset_rectangle(rectangle, left_padding: float, right_padding: float, top_padding: float = 0.0, bottom_padding: float = 0.0) -> render_rectangle`|静态调用，按四边内边距计算矩形|
|`context.get_inset_rectangle(item: control, left_padding: float, right_padding: float) -> render_rectangle`|实例调用，按指定控件的绘图矩形计算左右内缩|
|`draw_control(item: control, highlight: bool = True) -> None`|绘制通用控件背景和边框；`highlight`控制悬停、焦点样式|
|`get_foreground(item: text_control) -> int`|获取考虑可用状态后的文字颜色|

坐标须为有限数。宽高、半径不能为负；线宽须大于`0`；图像透明度范围为`0.0`至`1.0`。绘图颜色使用`0xRRGGBBAA`整数。裁剪只约束后续绘制，不更改控件矩形。

实例的`get_inset_rectangle()`也接受静态形式的矩形参数。左右内边距均须显式提供；静态调用可独立进行矩形计算，实例调用遵循当前绘图回调的有效期。

绘图查询采用视觉焦点。输入排空期间可以先取消焦点外观，逻辑焦点在排空完成后切换。

### 7.2.drawing_path

构造：`drawing_path()`。默认填充规则为`drawing_fill_rule.even_odd`。

|签名或属性|用途|
|---|---|
|`fill_rule: drawing_fill_rule`|读写填充规则|
|`segment_list: list[drawing_path_segment]`|只读路径段快照|
|`clear() -> None`|清空路径段|
|`move_to(x: float, y: float) -> drawing_path`|移动到新子路径起点|
|`line_to(x: float, y: float) -> drawing_path`|添加直线|
|`quadratic_to(control_x: float, control_y: float, end_x: float, end_y: float) -> drawing_path`|添加二次贝塞尔曲线|
|`cubic_to(control1_x: float, control1_y: float, control2_x: float, control2_y: float, end_x: float, end_y: float) -> drawing_path`|添加三次贝塞尔曲线|
|`arc_to(end_x: float, end_y: float, radius_x: float, radius_y: float, rotation_degree: float = 0.0, clockwise: bool = True, large_arc: bool = False) -> drawing_path`|添加到指定终点的椭圆弧；指定半径、椭圆旋转角、方向及是否取大弧|
|`close() -> drawing_path`|闭合当前子路径|

路径添加方法和`close()`返回当前路径，支持链式调用。每个子路径从`move_to()`开始；空路径或刚刚闭合之后，需要先`move_to()`再追加其他路径段。坐标须为有限数，圆弧半径不能为负。`clear()`清除路径段并保留填充规则。`drawing_fill_rule`枚举包含`even_odd`奇偶填充、`non_zero`非零绕数填充。

从`easyvrui`导入`drawing_path_segment`。`segment_list`中的路径段具有以下字段。

|字段|用途|
|---|---|
|`operation: drawing_path_operation`|`move/line/quadratic/cubic/arc/close`之一|
|`value_list: list[float]`|固定六个数值槽；`move/line`使用`x,y`；`quadratic`使用控制点与终点四个值；`cubic`使用两个控制点与终点六个值；`arc`使用终点、半径和旋转角前五个值|
|`clockwise: bool`|圆弧是否顺时针|
|`large_arc: bool`|圆弧是否选择大弧|

### 7.3.drawing_image

构造：`drawing_image(width: int, height: int, pixel_data)`。

`pixel_data`接受连续的单字节缓冲区，例如`bytes/bytearray/memoryview`。图像逐行排列，每个像素依次为R、G、B、A四个字节；长度必须恰好为`width * height * 4`。宽高须大于`0`。

|成员|用途|
|---|---|
|`width: int`|只读像素宽度|
|`height: int`|只读像素高度|
|`rgba_data: bytes`|只读，RGBA像素字节副本|
|`load_file(path: str) -> drawing_image`|静态方法，加载系统支持的图像文件，ICO选取最大图像帧|
|`load_memory(data: bytes) -> drawing_image`|静态方法，从完整编码图像字节加载|
|`load_ico(data: bytes) -> drawing_image`|静态方法，检查ICO文件头并从内存加载图标|
|`encode_ico() -> bytes`|保留RGBA像素，无损生成PNG单图ICO；宽高各为1～256像素|

### 7.4.派生控件的扩展点

普通控件可在Python中派生，应用状态保存在自己的成员中。Python中的方法名与下面的覆盖签名一致；绘图由框架调用，回调返回后统一提交。

|覆盖签名|职责|
|---|---|
|`render(self, context)`|绘制主体；可用`super().render(context)`绘制原生基类主体|
|`render_overlay(self, context)`|绘制弹出层；可调用基类同名绘图方法|
|`is_focusable(self) -> bool`|定义是否参与焦点导航|
|`get_content_top(self) -> float`|定义内容顶部偏移|
|`get_input_rectangle(self) -> rect`|返回控件本地输入区域|
|`process_input(self, event)`|处理输入，按对应事件规则设置`event.handled`；调用`super().process_input(event)`保留基类处理|

容器派生类还有三个布局钩子，由原生框架调用：

|覆盖签名|返回值及作用|
|---|---|
|`get_active_control_list(self) -> list[control]`|当前参与布局、绘制和命中的控件列表|
|`is_control_active(self, item: control) -> bool`|指定控件是否处于活动状态|
|`get_managed_control_rectangle(self, item: control, rectangle: rect) -> rect \| None`|给出受容器管理的逻辑矩形；None沿用原矩形|

布局钩子属于protected扩展点，Python派生类可覆盖，并在派生类方法内通过super调用相应原生基类实现。默认集合的读取使用`control_list`，Tab使用`page_list`。窗口基类绘制通过上下文的`render_control_list`安排控件绘制。

```python
from easyvrui import control

class meter_control(control):
    def __init__(self, name):
        super().__init__(name)
        self.value = 0.5

    def render(self, context):
        left, top, width, height = context.rectangle
        context.fill((left, top, width, height), self.background_color)
        context.fill((left, top, width * self.value, height), 0x30B080FF)

    def set_value(self, value):
        self.value = max(0.0, min(1.0, value))
        self.invalidate()
```

`selection_control`派生类可覆写`is_blank_at(local_left, local_top)`和`clear_selection()`。Grid派生类可覆写`read_cell_value/write_cell_value/render_cell`，签名和写入结果约定见grid章节。

## 8.应用循环、连接与输入界面

### 8.1.运行函数

|签名|用途|
|---|---|
|`run(application_name: str) -> None`|以`application_name`为会话名称运行普通窗口应用循环；没有已加载且未关闭的窗口，或运行环境停止时返回|
|`set_application_name(application_name: str) -> None`|登记会话名称，必填且为非空字符串；`run(application_name)`已包含这一步，独立主循环在首次`pump()`之前调用|
|`pump(timeout_millisecond: int = 0) -> bool`|分派消息和回调，推进定时状态，提交待更新窗口。可按参数等待指定毫秒，循环仍可继续时返回`True`|
|`show_input_ui(window: window, rectangle: rect \| Sequence[int], completion = None) -> None`|为关联窗口开启输入界面；矩形顺序为`left, top, width, height`|
|`hide_input_ui(completion = None) -> None`|请求收起当前输入界面，完成排空后结束旧输入路径|
|`get_application_directory() -> pathlib.Path`|定位应用资源目录。|
|`measure_text(text: str, font: font) -> float`|按指定字体测量文本宽度，单位为逻辑像素。|

应用循环在UI线程执行事件、异步完成通知和本地投递的回调。原生连接分别保存服务端事件与异步响应，消息泵按收包顺序合并两队列。内部同步请求只等待自己的响应，期间到达的事件由后续消息循环处理。实现见[IPC、TLS与连接队列](/advanced/03_ipc_tls_protocol)。

会话名称标识引擎应用列表中的本程序，也是窗口归属的跟踪依据。名称必填且为非空字符串；连接建立后名称固定，再次传入不同的名称会抛出异常。未显式命名时，SDK使用可执行文件名作为会话名称。

输入矩形使用窗口逻辑坐标，表示文本编辑区域。关联窗口须为当前可交互的普通应用窗口；layout/IME会话及辅助窗口不能开启应用输入区。`completion`为`Callable[[bool], None]`或`None`，接收操作是否成功；请求发出后继续运行应用循环处理完成通知。已显示的窗口即使隐藏也仍可使`run(application_name)`继续运行；应用结束时关闭窗口。

可编辑文本控件的焦点变化会由控件框架协调输入界面；应用需要自定义输入区域时使用上述函数。引擎按当前窗口路由键盘，窗口内部焦点由控件框架分发。`Pause`切换物理键盘拦截模式，只有编辑区需要显示虚拟键盘和IME界面。

激活编辑控件后，输入区下方的辅助输入条显示语言、IME名称和“输入法切换”按钮。点击按钮后先收起输入界面，再打开模态选择对话框：layout列表独立选择，语言列表用于过滤IME列表。对话框保留各语言的暂选，点击“确定”应用选择，也可将选中的IME设为默认项。取消会放弃暂选，关闭后返回原编辑控件。实体键盘模式且存在有效当前窗口时，`Alt+Shift`切换语言并恢复该语言上次使用的IME，`Ctrl+Shift`在当前语言内切换IME。

窗口显示期间，SDK将本进程的Ctrl+C作为界面快捷键处理。最后一个显示窗口关闭后恢复控制台处理。Ctrl+Break沿用控制台行为。

### 8.2.本地与远程连接

使用窗口或高层应用接口时按需建立连接。本地应用通过本地发现信息连接引擎。远程连接参数由启动命令行提供，Python API沿用同一组参数：

|参数|用途|
|---|---|
|`--easyvrui-host=值`|主机名、IPv4或裸IPv6地址|
|`--easyvrui-port=值`|端口，省略为`49537`|
|`--easyvrui-access-credential=值`|接入凭据|
|`--easyvrui-public-key-fingerprint=值`|服务端公钥SHA-256指纹|

使用`--name=value`形式；与应用自身参数放在同一条命令行。出现任一远程参数即按远程方式校验，主机、凭据及指纹必填，参数不能重复或为空；端口范围为`1`至`65535`。例如：

```cmd
python my_vr_app.py --easyvrui-host=192.0.2.10 --easyvrui-port=49537 --easyvrui-access-credential="my credential" --easyvrui-public-key-fingerprint=0000000000000000000000000000000000000000000000000000000000000000
```

连接与证书验证失败通过异常报告。应用层使用窗口、绘图及输入接口即可；完整消息字段定义见[Engine协议参考](./engine_protocol)。

### 8.3.应用列表与结束

可从`easyvrui`或`easyvrui.application_management`导入应用管理接口。清单读取与进程启动在调用进程所在机器上完成，因此应用与Engine可以位于不同机器。单实例由应用自身实现。应用管理快照包含经验证的引擎本机会话及其窗口，包含Desktop，过滤输入组件。查询和结束操作要求经验证的引擎本机会话，Desktop和输入组件受结束操作保护。

|签名|用途|
|---|---|
|`read_application_entry(manifest_path: str \| Path, language: str = "") -> application_entry`|读取清单并按指定语言选择名称。语言为空时采用系统语言，最终回退到`en`|
|`launch_application(manifest_path: str, extra_argument_list: Sequence[str] \| None = None) -> int`|读取`.easyvrui`清单并在本机启动该应用，返回新进程PID；`extra_argument_list`追加到清单声明的参数之后。清单缺失或启动失败抛出异常|
|`get_application_snapshot_list() -> list[application_snapshot]`|查询引擎返回的会话快照列表|
|`terminate_application(session_id: int) -> bool`|结束目标会话对应的进程，返回引擎给出的操作结果|
|`close_application_window(session_id: int, window_id: int) -> bool`|请求目标会话正常关闭指定窗口，返回事件是否送达|
|`request_application_snapshot_list(completion) -> None`|异步查询应用快照。|
|`request_terminate_application(session_id, completion) -> None`|异步请求结束应用。|
|`request_close_application_window(session_id, window_id, completion) -> None`|异步请求正常关闭窗口。|

完成回调在应用UI线程执行，接收`(result, error)`。快照查询结果为列表，结束应用或关闭窗口的结果为布尔值。成功时`error`为`None`。

#### `application_entry`

`read_application_entry()`会填充以下读写属性。路径以清单所在目录为基准。字段规则见[应用清单](./application_manifest)。

|属性|用途|
|---|---|
|`id: str`、`name: str`|应用ID和完成语言匹配后的显示名称|
|`icon_path: Path \| None`、`icon_data: bytes`|外部图标路径和内嵌图标的文件字节|
|`runtime: application_runtime`|默认`native`，表示启动原生程序。`python`表示启动Python主脚本|
|`executable: Path \| None`、`script: Path \| None`|解析后的原生程序路径或Python脚本路径|
|`argument_list: list[str]`|清单声明的启动参数|
|`type: application_type`|取值为`application`、`desktop`、`layout`或`ime`，默认`application`|

#### `application_snapshot`

|属性|用途|
|---|---|
|`session_id: int`|引擎分配的会话标识|
|`process_id: int`|会话对应的进程号|
|`name: str`|会话名称|
|`window_list: list[application_window]`|该会话登记的窗口列表|
|`memory_bytes: int`|进程内存占用字节数|
|`cpu_percent: float`|进程CPU占用百分比|
|`gpu_percent: float`|进程GPU占用百分比|

#### `application_window`

|属性|用途|
|---|---|
|`id: int`|窗口标识|
|`name: str`|创建窗口时提供的应用内窗口名称|
|`title: str`|窗口标题栏文本|
|`visible: bool`|窗口当前是否可见|

### 8.4.焦点与Tab

默认按钮、文本框、组合框和列表可获得焦点；普通容器和标签通常不参与Tab导航。导航跳过隐藏、禁用及非活动页面中的控件。正数`tab_index`先按数值升序排列，随后排列`tab_index = 0`的自动项目；相同索引按窗口绝对逻辑坐标的`top`升序、再按`left`升序排列，位置也相同时保持遍历顺序。因此自动导航按从上到下的行序，在同一高度从左到右。反向导航使用`Shift+Tab`，到达边界后循环。

文本框切换焦点后，相应输入区域也会更新；切换当前窗口时收起之前的输入界面。自定义控件通过`focusable`声明是否参与焦点导航，通过`process_input()`或`on_key_down/on_key_up`处理按键。

## 9.标准对话框

从`easyvrui`或`easyvrui.dialog`导入下列函数。调用等待用户完成并返回结果，等待期间持续处理界面活动。owner是直接父窗口；模态期间禁用该父窗口。对话框继承其physical_scale，采用World与center定位。

|签名|返回值|
|---|---|
|`color_dialog(color: int = 0x000000ff, title: str = "", default_color: int = 0x000000ff, owner: window \| None = None) -> int \| None`|确定返回`0xRRGGBBAA`，取消返回None|
|`font_dialog(font: font = font(), title: str = "", default_font: font = font(), owner: window \| None = None) -> font \| None`|确定返回系统字体，取消返回None|
|`messagebox(message: str, title: str = "", button_set = messagebox_button_set.ok, icon = messagebox_icon.none, default_button = dialog_result.none, owner: window \| None = None) -> dialog_result`|选中的标准按钮|
|`messagebox(message: str, title: str, button_list: list[messagebox_button], icon = messagebox_icon.none, default_button_name: str = "", owner: window \| None = None) -> str`|选中按钮的name|
|`inputbox(prompt: str, title: str = "", default_text: str = "", max_length: int = 0, owner: window \| None = None) -> str \| None`|确定返回文字，取消返回None；空字符串和文字cancel都是有效输入|

`messagebox_button(name = "", text = "")`保存按钮标识与显示文字。消息框枚举成员及数值与C++一致：

|枚举|成员|
|---|---|
|`messagebox_icon`|`none=0`、`error=0x10`、`question=0x20`、`warning=0x30`、`information=0x40`|
|`messagebox_button_set`|`ok=0`、`ok_cancel=1`、`abort_retry_ignore=2`、`yes_no_cancel=3`、`yes_no=4`、`retry_cancel=5`|
|`dialog_result`|`none=0`、`ok=1`、`cancel=2`、`abort=3`、`retry=4`、`ignore=5`、`yes=6`、`no=7`|

### 9.1.文件对话框

```python
file_open_dialog(title = "", initial_directory = None, initial_filename = "", filter_list = [], filter_index = 0, multi_select = False, confirm_text = "", owner = None, directory_changed = None, filter_changed = None)
file_save_dialog(title = "", initial_directory = None, initial_filename = "", filter_list = [], filter_index = 0, default_extension = "", confirm_overwrite = True, confirm_text = "", owner = None, directory_changed = None, filter_changed = None)
```

打开返回`list[pathlib.Path]`，取消返回空列表。保存返回`pathlib.Path`，取消返回`None`。`initial_directory=None`使用记忆目录。`directory_changed`接收路径，`filter_changed`接收从0开始的筛选索引。两个回调接收初始值和后续变化。

`file_filter(name, pattern_list)`定义筛选名称与文件模式。`confirm_text`为空时使用本地化按钮文字。保存时可通过`default_extension`补全扩展名，通过`confirm_overwrite`控制覆盖确认。

```python
import easyvrui

path = easyvrui.file_save_dialog(title = "保存", initial_filename = "window1", filter_list = [easyvrui.file_filter("EasyVRUI UI", ["*.easyvruifrm"])], default_extension = "easyvruifrm", owner = owner)
```

### 9.2.language_pack

`language_pack.current`取得SDK当前语言包。内置文字随SDK编入Python原生扩展，默认按系统语言选择。`language_pack.load_directory(path)`可显式从指定目录加载自定义语言包。该目录以`en.json`提供基础文字，其它文件按语言代码命名。

|属性或操作|用途|
|---|---|
|`locale: str`|读取或设置当前语言代码|
|`available_locale_list: list[str]`|当前语言包提供的语言代码|
|`key_list: list[str]`|`locale`下可查询的语言键|
|`len(pack)`、`key in pack`|语言键数量及成员查询|
|`pack[key]`|读取文字，缺失键抛出`KeyError`|
|`pack.format(key, *args)`|将参数代入`{0}`、`{1}`等占位项|

## 10.独立layout与IME应用

### 10.1.枚举与组件信息

|类型|枚举成员|
|---|---|
|`input_role`|`layout`虚拟键盘布局、`ime`输入法|
|`input_provider_state`|`stopped`未启动、`starting`启动中、`running`运行中|

`provider_info()`可构造默认记录，字段只读：

|字段|类型与默认值|用途|
|---|---|---|
|`id`|`int = 0`|引擎中的组件标识|
|`name`|`str = ""`|显示名称|
|`language`|`str = "en"`|IME语言代码，常用zh/en/ja，也支持其它非空代码；layout记录沿用默认值|
|`role`|`input_role.ime`|组件角色|
|`state`|`input_provider_state.stopped`|启动状态|
|`configured`|`bool = False`|是否来自持久配置|
|`active`|`bool = False`|是否为查询会话当前选择的组件|
|`default_provider`|`bool = False`|是否为持久默认IME|
|`process_id`|`int = 0`|组件进程ID|
|`error`|`str = ""`|组件最近的错误信息|

列表记录是快照。配置组件退出后保留记录并变为未启动；动态注册且未写入配置的组件退出后从列表移除。

IME的language用于语言分组，layout的协议记录省略该字段。Python的provider_info.language为只读字符串；选择某个IME同时确定当前输入语言。

### 10.2.input_ui_state

构造：`input_ui_state()`。

|读写字段|默认值与用途|
|---|---|
|`active: bool`|`False`；组件是否处于当前活动输入路径|
|`physical: bool`|`False`；当前是否为物理键盘模式|
|`rectangle: render_rectangle \| None`|`None`；当前组件辅助窗口的定位矩形，顺序为`left/top/width/height`|

物理键盘模式下布局界面收起，layout状态的`rectangle`可为`None`。IME根据状态决定是否显示自己的提示窗口；英文空壳IME可以完全没有界面。

### 10.3.input_event

构造：`input_event()`。字段可写：

|字段|默认值与用途|
|---|---|
|`event_type: str`|`""`；按键事件使用`"key_down"/"key_up"`，文本提交使用`"ime_submit"`|
|`key: str`|`""`；逻辑键名|
|`text: str`|`""`；与当前输入有关的文本|
|`shift: bool`|`False`；Shift状态|
|`ctrl: bool`|`False`；Ctrl状态|
|`alt: bool`|`False`；Alt状态|
|`meta: bool`|`False`；Windows/Meta键状态|
|`handled: bool`|`False`；IME将其设为`True`以消费事件|

只读属性`type`返回`input_event_type`，其成员为`unknown`、`key_down`、`key_up`和`ime_submit`。

### 10.4.input_provider

构造：`input_provider()`。普通应用可以查询组件，layout和IME应用则创建组件对象并注册。建议派生此类覆盖处理函数。

|属性|用途|
|---|---|
|`provider_list: list[provider_info]`|只读；组件最近收到的列表快照|
|`role: input_role`|只读；当前注册角色，未注册时初始为`ime`|
|`input_ui_state: input_ui_state`|只读；当前输入路径状态的快照|
|`session_id: int`|只读；当前会话编号，未连接时为0|
|`connected: bool`|只读；组件连接状态|
|`draining: bool`|只读；组件是否正在排空输入|
|`active: bool`|只读；当前状态的`active`|
|`physical: bool`|只读；当前状态的`physical`|

|签名|用途|
|---|---|
|`register_provider(role: input_role = input_role.ime, default_provider: bool = False, name: str = "", language: str = "en") -> None`|发起组件注册；后续应用循环处理注册结果，`default_provider`表示申请成为默认组件。language仅用于IME，须为非空语言代码，默认en|
|`send_event(event: input_event) -> None`|向当前输入路径发送事件|
|`commit_text(text: str, /) -> None`|IME提交最终文本；layout调用会报角色错误|
|`begin_input_task() -> None`|登记一个尚未完成的输入异步任务|
|`finish_input_task() -> None`|完成一个已登记任务；必须与开始配对|
|`run() -> None`|运行输入组件循环；未注册时按默认IME角色发起注册|
|`process_state(state: input_ui_state, /) -> None`|可覆盖；处理活动路径、模式和定位变化|
|`process_input(event: input_event, /) -> None`|可覆盖；处理IME收到的键盘输入|
|`process_drain() -> None`|可覆盖；完成排空所需的应用工作|

注册后的会话固定为layout或IME角色；组件窗口由框架和Engine标记为辅助表面，Engine按关联输入区自动定位并继承缩放，设置的`reference_object`由Engine忽略。这些窗口用于键盘、候选或提示界面。普通应用通过`show_input_ui()`开启输入区。

输入状态回调先执行`process_state()`，再触发`on_state_changed`。IME按键先执行`process_input()`，再触发`on_input`；最终`handled=False`时按键会继续转发到应用，`handled=True`时由IME消费。提交文本用`commit_text()`。layout发送按键给IME，再由IME处理或转发。IME候选和组合状态由IME应用自行维护。

|事件|回调签名与用途|
|---|---|
|`on_state_changed`|`callback(state: input_ui_state) -> None`，输入路径状态变化|
|`on_input`|`callback(event: input_event) -> None`，IME收到按键；可修改`handled`|

停用、切换和收起输入界面时，组件收到排空通知。异步任务应提前用`begin_input_task()`登记，输出提交后用`finish_input_task()`完成；排空期间等待旧任务和待发结果完成，之后由组件接口完成确认。`process_drain()`适合结束自己的缓冲工作。未注册、未激活或已完成排空确认后的发送不会进入有效输入路径。

```python
from easyvrui import input_provider, input_role

class english_ime(input_provider):
    def process_input(self, event):
        if ((((event.event_type == "key_down") and event.text) and (not event.ctrl)) and (not event.alt)) and (not event.meta):
            self.commit_text(event.text)
            event.handled = True

ime_english = english_ime()
ime_english.register_provider(input_role.ime, name = "EasyVRUI English", language = "en")
ime_english.run()
```

该示例仅演示处理与转发接口。实际应用应结合对应键的按下、松开和修饰状态保持事件配对，并按所需键盘布局决定文本映射。

## 11.语言和异常

|签名|用途|
|---|---|
|`get_error_language() -> str`|读取当前错误提示语言|
|`select_error_language(language: str, /) -> None`|切换提示语言，支持`zh/en/ja`|
|`get_localized_error(key: str, *argument_list) -> str`|按语言键取得提示文字，并将格式参数转换为字符串|

这三个函数均可从`easyvrui`或`easyvrui.common.error`导入。初始语言根据系统首选语言选择。

|类型或函数|用途|
|---|---|
|`error_diagnostic(location = None, condition = "")`|根据调用位置或给定的`error_diagnostic`构造诊断。也可用`error_diagnostic(file, line, column, function, condition)`指定各字段|
|`engine_error(key: error_key, argument_list = [], location = None, condition = "")`|引擎错误，继承`RuntimeError`。只读`key`是`error_key`枚举值|
|`request_error(language_key: str, message: str, argument_list: list[str], diagnostic)`|请求错误，继承`RuntimeError`。`diagnostic`可使用现有诊断对象或带诊断字段的异常|
|`localized_invalid_argument(key: language_key, argument_list = [], location = None, expression = "")`|本地化参数错误，继承`ValueError`。只读`key`是`language_key`枚举值|
|`localized_runtime_error(key: language_key, argument_list = [], location = None, expression = "")`|本地化运行错误，继承`RuntimeError`。只读`key`是`language_key`枚举值|
|`get_error_diagnostic(error: BaseException) -> error_diagnostic`|读取异常携带的诊断，普通异常使用调用位置生成诊断|
|`get_error_message(error: BaseException) -> str`|读取或生成带诊断信息的单行异常文本|

`error_diagnostic`和上述四种异常都提供`get_message(key = "", detail = "")`，用于根据现有来源、给定的错误键和说明格式化单行诊断。它们共享以下只读属性。

|属性|用途|
|---|---|
|`file: str`|诊断来源文件|
|`line: int`|行号|
|`column: int`|列号|
|`function: str`|函数名称|
|`condition: str`|失败条件|

异常另有只读属性`language_key: str`和`argument_list: list[str]`，分别记录语言键字符串和格式参数列表。`str(error)`返回异常的完整文本，格式为`文件:行号:列号: error: 条件 [错误键] 说明`，其中错误键和说明按实际信息显示。

## 12.控件属性索引

以下属性按声明它们的控件类型排列。派生控件继承基类属性。

|定义层级|属性|访问|
|---|---|---|
|`control`|`rect`|读写|
|`control`|`background_color`|读写|
|`control`|`visible`|读写|
|`control`|`enabled`|读写|
|`control`|`tab_index`|读写|
|`text_control`|`foreground_color`|读写|
|`text_control`|`font`|读写|
|`selection_control`|`clear_selection_on_blank_click`|读写|
|`item_control`|`selected_index`|读写|
|`item_control`|`selected_item`|只读|
|`item_control`|`row_height`|读写|
|`label`|`text`|读写|
|`button`|`text`|读写|
|`textbox`|`multiline`|读写|
|`textbox`|`max_length`|读写|
|`textbox`|`text`|读写|
|`textbox`|`read_only`|读写|
|`textbox`|`selectable`|读写|
|`textbox`|`horizontal_scrollbar_visible`|读写|
|`textbox`|`vertical_scrollbar_visible`|读写|
|`textbox`|`selection_start`|读写|
|`textbox`|`selection_length`|读写|
|`textbox`|`selected_text`|读写|
|`textbox`|`can_undo`、`can_redo`|只读|
|`combobox`|`dropdown_style`、`dropped_down`|读写|
|`combobox`|`text`|读写|
|`tabcontrol`|`selected_index`|读写|
|`tabcontrol`|`tab_position`|读写|
|`tabcontrol`|`tab_size`|读写|
|`tabcontrol`|`page_close_button_visible`|读写|
|`tabcontrol`|`tab_font`|读写|
|`tabcontrol`|`tab_foreground_color`|读写|
|`tabcontrol`|`tab_background_color`|读写|
|`tabcontrol`|`selected_tab_foreground_color`|读写|
|`tabcontrol`|`selected_tab_background_color`|读写|
|`window`|`title`|读写|
|`window`|`title_foreground_color`|读写|
|`window`|`title_background_color`|读写|
|`window`|`title_font`|读写|
|`window`|`physical_scale`|读写|
|`window`|`curvature`|读写|
|`window`|`startup_position`|读写|
|`window`|`curvature_adjustable`|读写|
|`window`|`position`|读写|
|`window`|`rotation`|读写|
|`window`|`reference_object`|读写|
|`window`|`show_title_bar`|读写|
|`window`|`tracking_mode_set`|读写|
|`window`|`show_close_button`|读写|
|`window`|`movable`|读写|
|`window`|`resizable`|读写|
|`checkbox`|`checked`|读写|
|`radiobutton`|`checked`|读写|
|`numericupdown`|`value`|读写|
|`numericupdown`|`minimum`|读写|
|`numericupdown`|`maximum`|读写|
|`numericupdown`|`step`|读写|
|`numericupdown`|`decimal_places`|读写|
|`slider`|`minimum`|读写|
|`slider`|`maximum`|读写|
|`slider`|`value`|读写|
|`slider`|`orientation`|读写|
|`progressbar`|`minimum`|读写|
|`progressbar`|`maximum`|读写|
|`progressbar`|`value`|读写|
|`treeview`|`selected_node`|读写|
|`scrollpanel`|`horizontal_scrollbar_visible`|读写|
|`scrollpanel`|`vertical_scrollbar_visible`|读写|
|`image`|`stretch_mode`|读写|
|`splitter`|`orientation`|读写|
|`splitter`|`split_position`|读写|
|`screen`|`screen_id`|读写|
|`grid`|`selection_mode`|读写|
|`grid`|`multi_select`|读写|
|`grid`|`row_height`|读写|
|`grid`|`header_height`|读写|
|`grid`|`read_only`|读写|
|`grid`|`selected_index`|读写|
|`grid`|`row_count`|读写|
|`menuitem`|`text`|读写|
|`menuitem`|`shortcut`|读写|
|`menuitem`|`checkable`|读写|
|`menuitem`|`checked`|读写|
|`menuitem`|`separator`|读写|
|`menubar`|`font`|读写|
|`menubar`|`row_height`|读写|
|`toolbar_button`|`separator`|读写|
|`toolbar_button`|`enabled`|读写|
|`toolbar_button`|`tooltip_text`|读写|
|`toolbar`|`tool_size`|读写|
|`toolbar`|`spacing`|读写|
|`item_control`|`item_list`|读写|
|`window`|`icon`|读写|
|`menuitem`|`icon`|读写|
|`toolbar_button`|`icon`|读写|
|`image`|`source`|读写|
|`listview`|`column_list`|读写|
|`listview`|`item_list`|读写|
|`grid`|`column_list`|读写|

## 13.Python运算符协议索引

|协议方法|使用入口|
|---|---|
|`__eq__`|`vec3/font/rect/color/reference_object`的同类型值比较|
|`__add__`、`__sub__`|向量加减|
|`__mul__`、`__rmul__`|向量与标量相乘；四元数、位姿组合|
|`__matmul__`|位姿的`@`组合|
|`__int__`、`__index__`、`__str__`|颜色的整数、索引整数、文本转换|
|`__len__`、`__contains__`、`__getitem__`、`__delitem__`、`__iter__`|集合的长度、包含、索引、删除和遍历|
|`__setitem__`|字符串项目集合和`grid[row, column]`的下标赋值|
|`__iadd__`、`__isub__`、`__bool__`|事件容器的追加、移除及有无订阅检查|

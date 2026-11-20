# C++API接口参考

控件用法与完整示例见[控件目录](/guide/)。窗口接口示例见[window](/guide/controls/window-and-text/window)，标准对话框用法见[内建对话框](/guide/09_builtin_dialogs)。

普通控件的name采用`type_用途`，例如`button_ok`。设计器导出的公开控件成员与对应name同名，可直接通过`button_ok`访问；窗体类名对应设计文件名。

本文对应`repo/sdk/api/cpp/include`中的公开头文件。安装后使用`sdk/api/cpp/include/`下的公开头，通过`#include <easyvrui.h>`可引入全部公开接口。库与CMake导出位于`sdk/engine_interface/`。

## 使用约定

### 命名空间与链接

窗口、控件、事件、几何和应用接口位于`easyvrui`命名空间，包括`get_preferred_ui_language()`。`drawing_image`和`drawing_path`位于全局命名空间。

使用C++20，将API头与同一构建版本的库配套使用。内置C++应用默认链接`sdk/engine_interface/lib/engine_interface_static.lib`并使用静态CRT。静态库调用方定义`ENGINE_INTERFACE_STATIC`。选择DLL时，使用`lib/engine_interface.lib`导入库，并部署同一SDK的`bin/engine_interface.dll`，消费者须采用兼容的动态CRT。CMake辅助配置位于`sdk/engine_interface/lib/cmake/EngineInterface/`。C++接口使用标准库字符串、容器及回调，调用程序须匹配编译器、标准库、构建配置和ABI。

声明中的`ENGINE_INTERFACE_API`是导出标记，以下签名省略该标记。头文件中为方便使用而引入的`using std::...`按标准库原义理解。

### 类型、单位与返回值

|约定|含义|
|---|---|
|`u32string`、`std::u32string`、`U"..."`|Unicode码点序列，用于控件名、界面文字和字体名称|
|`string`、`std::string`|在本API明确表示文本时使用UTF-8；协议键、诊断和Base64另按对应接口解释|
|`uint32_t color`|按`0xRRGGBBAA`排列；Alpha=0完全透明，Alpha=255不透明|
|`rectangle_t`|无符号整数逻辑坐标，字段顺序为`left`、`top`、`width`、`height`|
|`render_rectangle_t`|double逻辑坐标，允许绘图使用浮点位置|
|`window.position`|相对于参考目标的偏移，单位米|
|`window.rotation`与欧拉角接口|XYZ旋转，单位度；组合顺序为Rz×Ry×Rx|
|`physical_scale`|逻辑像素物理尺寸的缩放倍数；1倍时每逻辑像素对应1毫米|
|`index`、`start`|通常从0开始，具体参见对应接口|
|文本选择位置|UTF-32码点偏移；实际选择、移动和删除会对齐字素边界|
|`optional<T>`|有值时提供T，无值时为`nullopt`|
|对象指针|可能为`nullptr`的情况在接口说明中列出|
|`const T &`|借用只读引用，其有效期依赖原对象及后续修改|
|`void`|通过对象状态、事件或完成回调交付效果|

`std::u32string`中的一个元素是一个码点。一个可见字素可能由多个码点组成；文本选区的长度依然以码点计数。

### 线程、生命周期与事件

控件在创建时归属于当前UI线程。窗口、容器、文本和消息循环操作在所属线程执行。后台工作完成后，通过`control_base::begin_invoke(callback)`投递更新。普通事件由应用消息循环分派，`show_dialog()`通过同线程的嵌套循环继续分派。内部同步请求仅等待自身响应，期间到达的事件留在队列中，由后续消息循环处理。

控件构造只要求`name`。名称必须非空且不含U+0000，文字应由有效Unicode标量组成；名称构造后只读；同一个控件容器中的名称唯一，不同容器可以使用相同名称。容器允许按名称取得对象。对象只能有一个父级，控件层级不得成环。

`add(control &)`等引用重载由调用方保证对象存活；`add(shared_ptr<control>)`等重载由容器保留共享所有权。`remove`和`clear`表示移出容器，`dispose`表示释放对象。`hide`保留窗口供再次显示，`close`走关闭及模态完成流程。

控件事件使用`event_container<参数类型>`，回调签名为`void(control_base &source, 参数类型 &event)`。使用`add`可取得取消订阅的token；使用`+=`可直接注册。

```cpp
#include <easyvrui.h>
#include <memory>

using namespace std;

int main()
{
    easyvrui::set_application_name(U"demo");
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    auto button_ok = make_shared<easyvrui::button>(U"button_ok");
    button_ok->set_rect(easyvrui::rectangle_t{24u, 80u, 200u, 44u});
    button_ok->set_text(U"确定");
    button_ok->on_click += [](easyvrui::control_base &source, easyvrui::event_args_t &)
    {
        source.invalidate();
    };

    window_main->get_control_list().add(button_ok);
    window_main->show();
    easyvrui::run(U"demo");
    return 0;
}
```

后续代码片段沿用上例的头文件和using namespace std，并在所属应用函数内执行；window_main表示调用方持有的`shared_ptr<window>`，owner表示有效的window引用。

窗口显示期间，SDK将本进程的Ctrl+C作为界面快捷键处理。最后一个显示窗口关闭后恢复控制台处理。Ctrl+Break沿用控制台行为。

### 继承关系与属性读写

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

派生类继承其祖先全部public成员；后文每个类型列出自身声明的public成员及重载，protected成员单列，继承的同名方法按C++覆盖与名称隐藏规则使用。`text_control`提供文字前景色与字体；普通`control`和容器提供背景色。窗口标题、页签标题各有独立文字外观属性。

属性通过`get_xxx()`和`set_xxx(value)`读取与修改。各setter校验并设置属性，值变化时触发对应事件。

Tab导航针对当前窗口内可聚焦、可见、启用并处于活动页面的控件。正数tab_index先按数值升序排列；0排在其后。同组按窗口绝对top升序、再按left升序排列，位置相同保留遍历顺序。Tab向前、Shift+Tab向后，首尾循环。Pause切换实体键盘拦截模式；文本焦点控制IME/layout的显示，其他可聚焦控件仍可接收按键。

激活编辑控件后，输入区下方的辅助输入条显示语言、IME名称和“输入法切换”按钮。点击按钮后先排空并收起输入界面，再打开模态对话框；layout独立选择，语言列表决定IME列表的过滤范围。各语言暂选在点击“确定”后应用，取消时丢弃；关闭后返回原编辑控件。实体键盘模式且存在有效当前窗口时，Alt+Shift切换语言并恢复该语言上次使用的IME，Ctrl+Shift切换当前语言内的IME。

### 强类型事件

控件通过第一个参数提供事件来源，第二个参数的类型由事件成员声明决定。普通事件使用`event_args_t`，其余18种控件事件参数公开继承该基类。带取消或消费标记的事件允许回调更新`cancel`或`handled`，分发流程读取更新后的值。容器事件提供实际对象，索引以0开始。

### 远程连接启动参数

连接入口读取当前进程启动参数，所有远程选项使用`--name=value`形式：

|参数|用途与默认值|
|---|---|
|`--easyvrui-host=地址`|远程主机名、IPv4或裸IPv6地址，例如`::1`；使用远程模式时必填|
|`--easyvrui-port=端口`|十进制端口，默认49537，有效范围1至65535|
|`--easyvrui-access-credential=凭据`|远程接入凭据，必填|
|`--easyvrui-public-key-fingerprint=指纹`|服务公钥SHA-256十六进制指纹，必填|

应用可在同一命令行提供自己的启动参数。本地程序使用自动发现；普通控件创建和`run(application_name)`入口使用当前连接配置。协议消息定义见[Engine协议参考](./engine_protocol)。

### 设计文件导出布局

生成的C++布局类继承设计root对应的SDK类型，全部非root控件引用均为public成员，成员名与各自control.name完全一致。嵌套容器、页签和菜单中的控件共同使用该生成类的成员命名空间，因此名称须在整份设计中唯一，符合C++与Python标识符规则，并避开root SDK公开入口。

生成类自身只定义构造函数。普通导出将声明和实现分别写入同名`.h`与`.cpp`。构造函数创建控件、加入对应集合并初始化属性，默认name参数使用设计根节点的名称，例如`const std::u32string &name = U"sample_form"`。业务类持有生成窗体实例，通过同名成员绑定事件、读取和修改控件属性。

图像与图标复用SDK的`drawing_image::load_file()`等绘图资源加载接口；值记录通过SDK类型直接构造，资源文件随导出结果部署。

## 公开头文件索引

|模块|头文件|
|---|---|
|绘图|`drawing_image.h`、`drawing_path.h`、`easyvrui/render/render_context.h`、`easyvrui/render/render_style.h`|
|应用入口|`easyvrui/application.h`、`easyvrui/application_manage.h`|
|模态窗口结果|`easyvrui/dialog/dialog_result.h`|
|基础值与文字工具|`easyvrui/common/color.h`、`easyvrui/common/error.h`、`easyvrui/common/error_diagnostic.h`、`easyvrui/common/keyboard_key.h`、`easyvrui/common/u32string_hash.h`、`easyvrui/common/value.h`|
|标准对话框|`easyvrui/dialog/color_dialog.h`、`easyvrui/dialog/file_open_dialog.h`、`easyvrui/dialog/file_save_dialog.h`、`easyvrui/dialog/font_dialog.h`、`easyvrui/dialog/inputbox.h`、`easyvrui/dialog/messagebox.h`|
|活行列与树节点|`easyvrui/control/listview_column.h`、`easyvrui/control/listview_column_collection.h`、`easyvrui/control/listview_item.h`、`easyvrui/control/listview_item_collection.h`、`easyvrui/control/listview_cell_collection.h`、`easyvrui/control/tree_node.h`、`easyvrui/control/tree_node_collection.h`|
|事件|`easyvrui/event/event_args.h`、`easyvrui/event/event_container.h`、`easyvrui/event/event_signal.h`|
|空间几何|`easyvrui/geometry/pose.h`、`easyvrui/geometry/quat.h`、`easyvrui/geometry/vec3.h`|
|输入组件|`easyvrui/input/input_provider.h`|
|错误与语言|`easyvrui/localization/error.h`、`easyvrui/localization/language_pack.h`、`easyvrui/localization/request_error.h`|
|聚合入口|`easyvrui.h`|
|导出配置|`engine_interface_api.h`|

普通应用使用控件public接口，派生控件使用本文件各节列出的protected扩展点。

## 应用入口

### `easyvrui.h`

常用控件、应用、事件和绘图接口的聚合入口。普通窗口应用通常从此头文件开始。

公开包含目录共有76个头文件，含聚合入口`easyvrui.h`。各接口的声明位置见下文。

### `easyvrui/application.h`

窗口应用的事件循环、资源查询和输入区控制入口。

#### 自由函数与类型别名

|声明|用途与返回值|
|---|---|
|`void show_input_ui(window &item, const rectangle_t &rectangle, std::function<void(bool)> completion = {})`|为item窗口的逻辑输入区rectangle唤起IME/layout；completion接收表示操作是否成功的布尔值。|
|`void hide_input_ui(std::function<void(bool)> completion = {})`|收起当前输入区及关联IME/layout；completion接收表示操作是否成功的布尔值。|
|`void set_application_name(const std::u32string &application_name)`|设置非空会话名称。连接建立后可重复设置已注册的名称。|
|`void run(const std::u32string &application_name)`|以必填的非空名称注册会话，并运行窗口应用的事件循环。窗口全部结束或运行环境停止时返回。|
|`bool pump(uint64_t timeout_millisecond = 0u)`|分派消息和回调，提交待更新窗口，并按需等待指定毫秒。返回false表示循环结束。|
|`std::filesystem::path get_application_directory()`|返回应用目录，可据此定位资源。|
|`double measure_text(const std::u32string &text, const font_t &font)`|按指定字体测量文本宽度，单位为逻辑像素。|

应用消息循环在UI线程分派服务端事件、异步完成通知和本地投递的回调，再推进定时状态并提交待更新窗口。连接分别保存异步响应和服务端事件，消息泵合并两队列时保留收包顺序。例如旧输入文本先分派，之后才调用输入区关闭的完成回调。内部同步响应按请求ID单独交付。实现见[IPC、TLS与连接队列](/advanced/03_ipc_tls_protocol)。

### `easyvrui/application_manage.h`

`application_entry_t.name`保存匹配后的名称，`icon_path`保存图标路径，`icon_data`保存内嵌图片的原始文件字节。`language`为空时匹配系统语言并回退`en`。清单字段见[应用清单](./application_manifest)。

应用清单读取、本机启动、应用快照查询与结束入口。

#### 自由函数与类型别名

|声明|用途与返回值|
|---|---|
|`application_entry_t read_application_entry(const std::filesystem::path &manifest_path, const std::u32string &language = {})`|读取`.easyvrui`清单并解析为启动描述，清单缺失或字段非法时抛出异常。|
|`uint32_t launch_application(const std::filesystem::path &manifest_path, const std::vector<std::u32string> &extra_argument_list = {})`|在调用进程所在机器上读取清单并启动该应用，返回新进程PID；extra_argument_list追加到清单声明的参数之后。Python条目通过PATH中的python.exe执行清单指定的脚本。启动失败抛出异常。|
|`std::vector<application_snapshot_t> get_application_snapshot_list()`|查询引擎返回的本机已验证应用快照列表，含会话名称与窗口列表。|
|`bool terminate_application(uint64_t session_id)`|结束目标会话对应的进程，返回引擎给出的操作结果。|
|`bool close_application_window(uint64_t session_id, uint64_t window_id)`|请求目标会话正常关闭指定窗口，返回事件是否送达。|
|`void request_application_snapshot_list(std::function<void(std::vector<application_snapshot_t>, std::exception_ptr)> completion)`|异步查询应用快照。|
|`void request_terminate_application(uint64_t session_id, std::function<void(bool, std::exception_ptr)> completion)`|异步请求结束目标应用。|
|`void request_close_application_window(uint64_t session_id, uint64_t window_id, std::function<void(bool, std::exception_ptr)> completion)`|异步请求正常关闭目标窗口。|

清单解析与启动都在SDK本地完成，因此程序与引擎可以位于不同机器。单实例由应用自身实现。实例协调由目标app使用进程实例锁等方式执行。应用列表与结束操作要求经验证的引擎本机会话；列表包含Desktop，过滤输入组件。Desktop和输入组件受结束操作保护。

异步回调在应用UI线程执行。快照回调接收快照列表和`exception_ptr`，操作回调接收布尔结果和`exception_ptr`。成功时异常指针为空，失败时可重新抛出以取得诊断。

#### `application_type_t`

声明：`enum class application_type_t`。

`application`表示普通应用，`ime`与`layout`表示输入组件，`desktop`表示桌面。

|声明|用途与调用语义|
|---|---|
|`application`|普通应用。|
|`ime`|独立输入法。|
|`layout`|独立键盘布局。|
|`desktop`|桌面应用。|

#### `application_runtime_t`

声明：`enum class application_runtime_t`。

native使用本机可执行文件，python使用Python主脚本。

|声明|用途与调用语义|
|---|---|
|`native`|启动本机可执行文件。|
|`python`|启动Python主脚本。|

#### `application_entry_t`

声明：`struct application_entry_t`。

解析后的应用清单，路径按清单所在目录解析；name已经按指定或系统语言匹配，缺失匹配项时回退en。

|声明|用途与调用语义|
|---|---|
|`std::u32string id`|清单中的应用ID。|
|`std::u32string name`|按语言匹配后的应用显示名称。|
|`std::filesystem::path icon_path`|外部图标路径。|
|`std::vector<uint8_t> icon_data`|内嵌图像原始文件字节。|
|`std::filesystem::path executable`|本机程序或Python解释器路径。|
|`application_runtime_t runtime = application_runtime_t::native`|启动运行时，默认native。|
|`std::filesystem::path script`|Python主脚本路径。|
|`std::vector<std::u32string> argument_list`|追加给目标程序的参数列表。|
|`application_type_t type = application_type_t::application`|应用类型，默认`application`。|

#### `application_window_t`

声明：`struct application_window_t`。

应用快照中的窗口记录，id为全局窗口ID，name为固定内部名称，title为实际窗口标题，visible为显示状态。

|声明|用途与调用语义|
|---|---|
|`uint64_t id = 0u`|全局窗口ID。|
|`std::u32string name`|窗口构造时的固定名称。|
|`std::u32string title`|用户看到的实际窗口标题。|
|`bool visible = false`|窗口当前是否显示。|

#### `application_snapshot_t`

声明：`struct application_snapshot_t`。

经Engine验证的本机应用会话快照，包含会话ID、进程ID、名称、窗口列表、内存字节数与CPU/GPU百分比。

|声明|用途与调用语义|
|---|---|
|`uint64_t session_id = 0u`|Engine会话ID。|
|`uint32_t process_id = 0u`|本机进程ID。|
|`std::u32string name`|会话注册名称。|
|`std::vector<application_window_t> window_list`|该会话的窗口列表。|
|`uint64_t memory_bytes = 0u`|进程内存用量，单位字节。|
|`double cpu_percent = 0.0`|进程CPU使用率百分比。|
|`double gpu_percent = 0.0`|进程GPU使用率百分比。|

## 基础值与空间几何

### `easyvrui/common/value.h`

字体、控件矩形和方向枚举。

#### 自由函数与类型别名

|声明|用途与返回值|
|---|---|

#### `font_t`

声明：`struct font_t`。

纯数据字体值，family为系统字体名称，size为uint64_t逻辑字号且必须大于0；默认Segoe UI、18、bold=false、italic=false。operator==逐字段比较。

|声明|用途与调用语义|
|---|---|
|`static constexpr uint64_t DEFAULT_SIZE = uint64_t{18u}`|font_t默认逻辑字号。|
|`u32string family = U"Segoe UI"`|系统字体家族名称。|
|`uint64_t size = DEFAULT_SIZE`|字体逻辑字号。|
|`bool bold = false`|是否加粗。|
|`bool italic = false`|是否斜体。|
|`bool operator==(const font_t &other) const = default`|按对应成员值比较是否相等，返回bool。|

#### `rectangle_t`

声明：`struct rectangle_t`。

纯数据控件矩形，所有字段为uint64_t。声明默认值为left=0、top=60、width=160、height=40；控件setter要求宽高均为正。operator==逐字段比较。

|声明|用途与调用语义|
|---|---|
|`uint64_t left = 0u`|矩形左边的横坐标。|
|`uint64_t top = 60u`|矩形上边的纵坐标。|
|`uint64_t width = 160u`|矩形宽度，单位为逻辑像素。|
|`uint64_t height = 40u`|矩形高度，单位为逻辑像素。|
|`bool operator==(const rectangle_t &other) const = default`|按对应成员值比较是否相等，返回bool。|

### `easyvrui/common/color.h`

RRGGBBAA颜色值及分量、十六进制和透明度操作。

#### `color_t`

声明：`struct color_t`。

默认value=0，即完全透明黑色；32位排列为RRGGBBAA，最低8位为透明度，0完全透明、255不透明。

|声明|用途与调用语义|
|---|---|
|`uint32_t value = 0u`|32位RRGGBBAA颜色值。|
|`color_t() = default`|构造本类型实例；参数含义见本类型说明及签名。|
|`explicit color_t(uint32_t value)`|构造本类型实例；参数含义见本类型说明及签名。|
|`std::array<uint8_t, 4u> get_rgba() const`|按R、G、B、A顺序返回4个8位分量。|
|`std::string get_hex() const`|返回0x开头的RRGGBBAA十六进制颜色字符串。|
|`color_t create_with_alpha(uint8_t alpha) const`|保留RGB并替换alpha，返回新的颜色值。|
|`bool operator==(const color_t &other) const = default`|按对应成员值比较是否相等，返回bool。|

### `easyvrui/geometry/vec3.h`

三维向量。

#### `vec3_t`

声明：`struct vec3_t`。

默认零向量。operator==逐分量进行按double精度缩放的近似比较，非有限值比较返回false。

|声明|用途与调用语义|
|---|---|
|`double x = 0.0`|向量的X分量。|
|`double y = 0.0`|向量的Y分量。|
|`double z = 0.0`|向量的Z分量。|
|`static bool is_equal(double left, double right)`|以double精度阈值和数值尺度比较有限浮点数；非有限值返回false。|
|`bool operator==(const vec3_t &other) const`|按三个double分量进行近似比较，使用is_equal规则。|
|`vec3_t operator+(vec3_t b) const`|逐分量相加，返回新vec3_t。|
|`vec3_t operator-(vec3_t b) const`|逐分量相减，返回新vec3_t。|
|`vec3_t operator*(double scalar) const`|所有分量乘以scalar，返回新向量。|
|`double calculate_dot_product(vec3_t b) const`|返回与b的点积。|
|`vec3_t calculate_cross_product(vec3_t b) const`|返回与b的叉积。|
|`double get_length() const`|返回三维向量长度。|
|`vec3_t get_normalized() const`|返回单位长度向量；零值、过小值和非有限输入抛出异常。|

### `easyvrui/geometry/quat.h`

四元数旋转。

#### `quat_t`

声明：`struct quat_t`。

默认单位旋转{x=0,y=0,z=0,w=1}。轴角和欧拉角接口使用度；create_from_euler组合为Rz×Ry×Rx。get_inverse/rotate以规范化旋转解释当前值。

|声明|用途与调用语义|
|---|---|
|`double x = 0.0`|四元数的X分量。|
|`double y = 0.0`|四元数的Y分量。|
|`double z = 0.0`|四元数的Z分量。|
|`double w = 1.0`|四元数的实部分量；单位旋转为1。|
|`quat_t operator*(quat_t b) const`|组合当前四元数与b，b对应旋转首先作用。|
|`quat_t get_normalized() const`|返回单位四元数；零值、过小值和非有限输入抛出异常。|
|`quat_t get_inverse() const`|返回表示逆旋转的四元数。|
|`vec3_t rotate(vec3_t v) const`|用当前四元数旋转向量v，返回旋转结果。|
|`static quat_t get_axis(vec3_t v, double angle)`|按单位轴v和angle度创建轴角四元数；调用方提供单位轴。|
|`static quat_t create_from_euler(vec3_t v)`|按XYZ角度创建旋转，组合为Rz×Ry×Rx。|
|`vec3_t get_euler_angle_vector() const`|返回与当前四元数等价的XYZ欧拉角，单位度；不同角度组合可能表示同一姿态。|
|`static quat_t create_from_axis_basis(vec3_t a, vec3_t b, vec3_t c)`|按三个轴基向量a/b/c创建并归一化旋转。|
|`static quat_t blend(quat_t a, quat_t b, double t)`|对a/b进行最短同向的归一化线性插值，t通常取0至1。|

### `easyvrui/geometry/pose.h`

位置与四元数旋转的组合位姿。

#### `pose_t`

声明：`struct pose_t`。

默认position为零、rotation为单位四元数。a*b表示将b的局部位姿组合到a中；transform_point执行旋转再平移。

|声明|用途与调用语义|
|---|---|
|`vec3_t position`|三维平移。|
|`quat_t rotation`|以四元数表示位姿旋转。|
|`pose_t operator*(const pose_t &b) const`|组合当前位姿与b，b首先作用，再由当前位姿变换。|
|`pose_t get_inverse() const`|返回逆位姿。|
|`vec3_t transform_point(vec3_t v) const`|将局部点v变换到当前位姿的父参考系。|

### `easyvrui/control/reference_object.h`

可选的窗口参考目标为`world`、`body`、`head`、`left`和`right`。Engine根据关联输入区定位IME/layout的辅助表面。

#### 自由函数与类型别名

|声明|用途与返回值|
|---|---|
|`u32string get_reference_object_type_name(reference_object_type_t value)`|把参考目标枚举转换为Unicode名称。|
|`reference_object_type_t parse_reference_object_type(const u32string &value)`|把Unicode名称解析为参考目标；无效名称抛出异常。|

#### `reference_object_type_t`

声明：`enum class reference_object_type_t`。

|声明|用途与调用语义|
|---|---|
|`world`|世界空间参考。|
|`body`|跟随身体位置并保持已校准朝向的参考，可通过reset_body_center重新校准。|
|`head`|头显参考，跟随位置和旋转。|
|`left`|左手柄参考。|
|`right`|右手柄参考。|

#### `reference_object_t`

声明：`struct reference_object_t`。

|声明|用途与调用语义|
|---|---|
|`reference_object_type_t type = reference_object_type_t::world`|参考目标类别。|
|`bool operator==(const reference_object_t &other) const = default`|按对应成员值比较是否相等，返回bool。|

## 事件与值容器

### `easyvrui/event/event_signal.h`

按注册顺序调用的泛型事件链。

#### `event_signal<source_type, argument_type_list...>`

声明：`class event_signal`。

模板参数为source_type和argument_type_list...，处理函数签名为void(source_type &, argument_type_list &...)。add返回注册token；remove和operator-=使用token，operator+=返回事件链引用。call按注册顺序调用；当前调用使用处理函数列表快照，本轮增删在下一次调用体现。回调异常向调用方传播。事件链由所属对象线程使用。

|声明|用途与调用语义|
|---|---|
|`uint64_t add(std::function<void(source_type &, argument_type_list &...)> callback)`|注册非空回调并返回uint64_t token，供后续remove或operator-=使用。|
|`event_signal &operator+=(std::function<void(source_type &, argument_type_list &...)> callback)`|注册callback并返回事件链引用，适合C#式追加语法；需要撤销时优先调用add保留token。|
|`bool remove(uint64_t token)`|删除token指定的处理函数；找到返回true，否则false。|
|`event_signal &operator-=(uint64_t token)`|移除token对应处理函数，并返回事件链引用。|
|`void clear()`|移除全部处理函数。|
|`bool is_empty() const`|查询事件链是否有零个订阅。|
|`void call(source_type &source, argument_type_list &...argument_list) const`|按注册顺序，以source和引用参数调用当前事件链；回调返回void。|

### `easyvrui/event/event_container.h`

以control_base为事件源的事件链类型别名。

#### 自由函数与类型别名

|声明|用途与返回值|
|---|---|
|`using event_container = event_signal<control_base, argument_type_list...>`|template<typename... argument_type_list>的别名，事件源固定为control_base。|

### `easyvrui/event/event_args.h`

`event_args_t`为空基类。下表其余18种结构体均公开继承`event_args_t`。每个事件以其声明的具体参数类型调用订阅者。

|参数类型|字段|用途|
|---|---|---|
|`event_args_t`|无|点击、焦点、窗口生命周期和各专属属性变化。|
|`cancel_event_args_t`|`bool cancel = false`|关闭窗口前设置`cancel`可取消普通关闭。强制关闭始终执行。|
|`key_event_args_t`|`std::u32string key`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`、`bool handled = false`|键名、修饰键和消费状态。|
|`text_input_event_args_t`|`std::u32string text`、`bool handled = false`|提交的文本和消费状态。|
|`pointer_event_args_t`|`std::u32string hand`、`double left = 0.0`、`double top = 0.0`、`double x = 0.0`、`double y = 0.0`、`bool captured = false`、`bool cancelled = false`、`bool handled = false`、`bool has_position = false`、`bool has_local_position = false`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`|包含手别、窗口坐标`left/top`、控件局部坐标`x/y`和修饰键。用`has_position`和`has_local_position`判断对应坐标是否有效。|
|`scroll_event_args_t`|`std::u32string hand`、`double delta_x = 0.0`、`double delta_y = 0.0`、`bool handled = false`|手别、横纵滚动量和消费状态。|
|`interaction_end_event_args_t`|`bool cancelled = false`|移动、缩放、曲率调整或拖动结束。`cancelled`表示操作被取消。|
|`property_changed_event_args_t`|`std::u32string property_name`|`property_name`为变化的属性名。通过`source`读取当前值。|
|`control_collection_event_args_t`|`control *item = nullptr`、`size_t index = 0u`|集合中的控件与索引。整表通知的`item`为空。|
|`menu_item_event_args_t`|`menuitem *item = nullptr`、`size_t index = 0u`|菜单项与索引。|
|`tabpage_event_args_t`|`tabpage *page = nullptr`、`size_t index = 0u`|页签对象与索引。|
|`listview_column_event_args_t`|`std::shared_ptr<listview_column> column`、`size_t index = 0u`|ListView列对象与索引。整表通知的`column`为空。|
|`listview_item_event_args_t`|`std::shared_ptr<listview_item> item`、`size_t index = 0u`|ListView项对象与索引。整表通知的`item`为空。|
|`grid_column_event_args_t`|`size_t index = 0u`、`uint64_t width = 0u`|Grid列索引与宽度。点击表头时通过`index`读取列索引。|
|`grid_cell_event_args_t`|`uint64_t row = 0u`、`uint64_t column = 0u`、`std::u32string error`|Grid单元格行列索引。编辑失败时`error`包含错误说明。|
|`tree_node_event_args_t`|`tree_node *node = nullptr`|操作的树节点。取消选择时`node`为空。|
|`render_error_event_args_t`|`std::string message`|渲染异常的消息。|
|`controller_event_args_t`|`std::u32string hand`、`bool trigger = false`、`bool grip = false`、`uint8_t joystick_x = 128u`、`uint8_t joystick_y = 128u`、`bool joystick_pressed = false`、`bool primary = false`、`bool secondary = false`|手柄按键和摇杆状态。摇杆轴范围为0至255，`primary`为左手X或右手A，`secondary`为左手Y或右手B。|
|`control_input_event_args_t`|`control_input_type_t type = control_input_type_t::none`、`std::u32string hand`、`std::u32string key`、`std::u32string text`、`double left = 0.0`、`double top = 0.0`、`double x = 0.0`、`double y = 0.0`、`int64_t steps = 0`、`bool horizontal = false`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`、`bool captured = false`、`bool cancelled = false`、`bool handled = false`、`bool has_position = false`、`bool has_local_position = false`|派生控件的输入分派参数。通过`type`区分输入，按类型读取字段，设置`handled`可标记已消费。|

`control_input_type_t`的取值为`none`、`click`、`focus_in`、`focus_out`、`pointer_enter`、`pointer_leave`、`pointer_move`、`pointer_down`、`pointer_up`、`scroll`、`key_down`、`key_up`、`text_input`、`controller_input`。

## 控件基类与容器

### `easyvrui/control/control_base.h`

控件标识、父级、生命周期、属性访问和基础事件。

#### `control_base`

声明：`class control_base : public std::enable_shared_from_this<control_base>`。

身份与生命周期基类，继承`std::enable_shared_from_this<control_base>`。构造函数为protected，供派生类调用。name和type在构造后只读；get_id()为运行时编号。控件不可复制。对象操作遵循所属UI线程约束，跨线程更新使用begin_invoke。继承的shared_from_this()和weak_from_this()遵循标准库共享所有权规则；引用方式管理的控件通常使用容器及控件接口访问。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_disposed`|对象释放时触发。|
|`event_container<property_changed_event_args_t> on_property_changed`|属性值变化时触发。property_name为变化的属性名。|
|`virtual ~control_base()`|析构对象，结束其资源或引用的生命周期。|
|`virtual uint64_t get_id() const`|读取运行时分配的对象编号。|
|`virtual control_base *get_parent() const`|读取父对象指针，顶层对象为nullptr。|
|`virtual bool get_disposed() const`|读取对象是否已释放。|
|`virtual void invalidate()`|请求重绘所属窗口；适用于自定义状态改变后刷新画面。|
|`virtual void dispose()`|释放控件及关联运行时资源；释放后停止使用该对象。|
|`virtual void begin_invoke(std::function<void()> callback)`|将callback排入对象所属UI线程；对象在执行前释放时跳过回调。|
|`virtual const u32string &get_name() const`|读取构造时确定的名称。|
|`virtual const u32string &get_type() const`|读取对象类型名称。|
|`virtual const u32string &get_tag() const`|读取应用保存的字符串标记，默认空字符串。|
|`virtual void set_tag(const u32string &value)`|设置标记。值改变时触发`on_tag_changed`。|
|`event_container<event_args_t> on_tag_changed`|标记变化时触发，回调接收来源控件和无附加数据的`event_args_t`。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`virtual std::shared_ptr<control_base> get_retained_owner()`|返回操作期间保留对象生命期所需的共享引用。|
|`virtual bool notify_property_changed(std::u32string_view name, bool changed, event_container<event_args_t> *specific = nullptr, bool redraw = true)`|属性发生变化时触发通知并返回true。redraw控制是否请求重绘。|
|`control_base(const u32string &name, const u32string &type)`|构造对象；参数、默认状态和约束见本类型说明。|
|`virtual void process_input(control_input_event_args_t &event)`|处理控件输入事件的虚函数；可派生扩展，通过event.type区分输入类型。|

### `easyvrui/control/control.h`

可视控件公共属性和输入事件。

#### `control`

声明：`class control : public control_base`。

可直接构造的可视基类。默认rect为{0,60,160,40}，visible=true、enabled=true、tab_index=0；默认不接受焦点。背景色默认0x162738FF。容器内坐标使用相对父级的逻辑单位。

继承`control_base`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_background_color_changed`|背景色变化时触发。|
|`event_container<event_args_t> on_visible_changed`|可见状态变化时触发。|
|`event_container<event_args_t> on_enabled_changed`|可用状态变化时触发。|
|`event_container<event_args_t> on_tab_index_changed`|Tab焦点顺序变化时触发。|
|`event_container<event_args_t> on_moved`|逻辑位置或窗口空间位置改变时触发；以源对象的当前属性为准。|
|`event_container<event_args_t> on_size_changed`|rect宽高改变时触发。|
|`event_container<pointer_event_args_t> on_pointer_enter`|激光进入控件时触发。|
|`event_container<pointer_event_args_t> on_pointer_leave`|激光离开控件时触发。|
|`event_container<pointer_event_args_t> on_pointer_move`|激光在控件上的指向变化时触发。|
|`event_container<pointer_event_args_t> on_pointer_down`|激光扳机按下时触发。|
|`event_container<pointer_event_args_t> on_pointer_up`|激光扳机释放或捕获取消时触发，cancelled表示是否取消。|
|`event_container<event_args_t> on_click`|完成控件点击或默认激活时触发。|
|`event_container<scroll_event_args_t> on_scroll`|滚动输入到达控件时触发。|
|`event_container<event_args_t> on_viewport_changed`|滚动视口变化时触发|
|`event_container<event_args_t> on_focus_in`|控件获得键盘焦点时触发。|
|`event_container<event_args_t> on_focus_out`|控件失去键盘焦点时触发。|
|`event_container<key_event_args_t> on_key_down`|按键按下时触发；参数包含键名、修饰键和消费状态。|
|`event_container<key_event_args_t> on_key_up`|按键释放时触发。|
|`explicit control(const u32string &name)`|构造对象；参数、默认状态和约束见本类型说明。|
|`virtual bool is_focusable() const`|查询控件类型是否可接收焦点；实际焦点还受visible、enabled和窗口模态状态影响。|
|`virtual const rectangle_t &get_rect() const`|读取相对父级的逻辑矩形。|
|`virtual void set_rect(const rectangle_t &value)`|设置相对父级的逻辑矩形。|
|`virtual uint32_t get_background_color() const`|读取背景色，格式0xRRGGBBAA。|
|`virtual void set_background_color(uint32_t value)`|设置背景色，格式0xRRGGBBAA。|
|`virtual const u32string &get_tooltip_text() const`|读取悬停提示，默认空字符串。|
|`virtual void set_tooltip_text(const u32string &value)`|设置悬停提示。|
|`event_container<event_args_t> on_tooltip_text_changed`|提示文字改变时触发。|
|`virtual bool get_visible() const`|读取可见状态。|
|`virtual void set_visible(bool value)`|设置可见状态。|
|`virtual bool get_enabled() const`|读取可交互状态。|
|`virtual void set_enabled(bool value)`|设置可交互状态。|
|`virtual uint64_t get_tab_index() const`|读取Tab焦点顺序，默认0。|
|`virtual void set_tab_index(uint64_t value)`|设置Tab焦点顺序，默认0。|
|`~control() override`|析构对象，结束其资源或引用的生命周期。|
|`virtual void show()`|显示控件或窗口，并触发对应的可见性与窗口生命周期行为。|
|`virtual void hide()`|隐藏控件或窗口。相关焦点、捕获和输入区按窗口状态释放。|
|`virtual void focus()`|请求将键盘焦点移到本控件。|
|`virtual void activate()`|激活本对象所属窗口；窗口重载激活自身。|
|`virtual rectangle_t get_absolute_rectangle() const`|返回控件在窗口内的逻辑矩形。|
|`virtual bool get_focused() const`|查询控件是否拥有焦点。|
|`virtual std::shared_ptr<window> get_owning_window() const`|返回控件所属窗口，尚未归属窗口时返回空指针。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`rectangle_t rect`|派生类可访问的相对父级的逻辑矩形；常规赋值使用setter以产生变化通知。|
|`uint32_t background_color = render_style::CONTROL_BACKGROUND_COLOR`|派生类可访问的背景色，格式0xRRGGBBAA；常规赋值使用setter以产生变化通知。|
|`bool visible = true`|派生类可访问的可见状态；常规赋值使用setter以产生变化通知。|
|`bool enabled = true`|派生类可访问的可交互状态；常规赋值使用setter以产生变化通知。|
|`uint64_t tab_index = 0u`|派生类可访问的Tab焦点顺序，默认0；常规赋值使用setter以产生变化通知。|
|`size_t focus_target_index = 0u`|当前内部聚焦区域索引，初始0。|
|`virtual size_t get_focus_target_count() const`|返回控件内部可聚焦区域数量，供数字按钮和页签箭头等复合控件覆盖。|
|`virtual size_t get_focus_target_index() const`|读取当前内部聚焦区域的索引。|
|`virtual void set_focus_target_index(size_t value)`|设置当前内部聚焦区域索引。|
|`control(const u32string &name, const u32string &type)`|构造对象；参数、默认状态和约束见本类型说明。|
|`virtual void refresh_layout()`|刷新控件布局，派生类覆盖时保留必要的基类处理。|
|`virtual rectangle_t get_input_rectangle() const`|返回控件本地坐标中的输入区；默认覆盖整个控件，派生编辑控件可缩小到实际编辑区域。|
|`virtual double get_content_top() const`|读取正文起始的逻辑top偏移。|
|`void notify_viewport_changed()`|请求重绘并发出`on_viewport_changed`事件。|
|`virtual void render(render_context &context) const`|使用context绘制控件正文。派生类可重载以实现自定义外观。|
|`virtual void render_overlay(render_context &context) const`|绘制控件浮层，例如组合框弹出菜单。|

### `easyvrui/control/blank.h`

#### `blank`

声明：`class blank : public control`。

命名矩形占位对象。基本配置为构造时只读的name与可修改的rect；几何变化事件、属性变化通知及对象生命周期接口沿用基类。可通过get_control_list().add()加入普通容器。

|声明|用途与调用语义|
|---|---|
|`explicit blank(const u32string &name)`|以唯一名称构造占位对象，name在实例存活期间固定|
|`~blank() override`|结束对象生命周期|
|`const u32string &get_name() const`|继承的名称读取接口|
|`const rectangle_t &get_rect() const`、`void set_rect(const rectangle_t &value)`|继承的矩形读取和设置接口|
|`on_moved`、`on_size_changed`|分别通知left/top及width/height变化|
|`on_property_changed`|属性变化通知。通过`event.property_name`读取名称，通过来源控件读取当前值|
|`on_disposed`、`get_disposed()`、`dispose()`|对象释放通知、状态与释放入口|
|`invalidate()`、`begin_invoke(callback)`|继承的刷新请求和创建线程调度接口|

通过blank类型直接访问visible、enabled、background_color、tab_index及对应访问器、显隐、聚焦、激活和交互事件受private访问约束。绘图与输入处理由框架调用内部钩子。

容器和框架仍可持有普通control基类引用。经control引用调用虚函数时，get_visible()、get_enabled()和is_focusable()始终返回false，visible和enabled的setter保持该状态。名称、矩形、几何事件与生命周期接口保持可用。

### `easyvrui/control/text_control.h`

带文字控件的字体与前景色。

#### `text_control`

声明：`class text_control : public control`。

字体与前景色基类，构造函数为protected。默认前景色0xD1DEF0FF，字体为Segoe UI、18、普通字重和非斜体。文字内容由具体控件定义。

继承`control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_foreground_color_changed`|文字前景色变化时触发。|
|`event_container<event_args_t> on_font_changed`|字体变化时触发。|
|`virtual uint32_t get_foreground_color() const`|读取文字前景色，格式0xRRGGBBAA。|
|`virtual void set_foreground_color(uint32_t value)`|设置文字前景色，格式0xRRGGBBAA。|
|`virtual const font_t &get_font() const`|读取文字字体。|
|`virtual void set_font(const font_t &value)`|设置文字字体。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`uint32_t foreground_color = render_style::TEXT_FOREGROUND_COLOR`|派生类可访问的文字前景色，格式0xRRGGBBAA；常规赋值使用setter以产生变化通知。|
|`font_t font`|派生类可访问的文字字体；常规赋值使用setter以产生变化通知。|
|`text_control(const u32string &name, const u32string &type)`|构造对象；参数、默认状态和约束见本类型说明。|

### `easyvrui/control/container_control.h`

可容纳子控件的基类及统一容器访问接口。

#### `container_control`

声明：`class container_control : public control`。

容器基类，构造函数为protected。get_control_list()返回活的control_collection，统一管理元素、名称索引和所有权。普通容器通过该集合操作；tabcontrol公开独立的page_list供应用管理页面。

继承`control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`event_container<control_collection_event_args_t> on_control_added`|添加子控件时触发，包含控件对象`item`和索引`index`。|
|`event_container<control_collection_event_args_t> on_control_removed`|移除子控件时触发，包含控件对象`item`和索引`index`。|
|`virtual control_collection &get_control_list()`|返回属于该容器的可直接操作的集合；可查询、索引、添加、插入、移除和清空。const重载提供只读集合访问。|
|`virtual const control_collection &get_control_list() const`|返回属于该容器的可直接操作的集合；可查询、索引、添加、插入、移除和清空。const重载提供只读集合访问。|
|`virtual std::vector<control *> get_active_item_list() const`|返回当前参与显示和交互的直接控件列表。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`container_control(const std::u32string &name, const std::u32string &type)`|构造对象；参数、默认状态和约束见本类型说明。|
|`virtual void validate_control(const control &item) const`|插入前检查元素类型及本容器的额外约束；失败时抛出异常，集合保持原状。|
|`virtual void notify_control_added(control &item, size_t index)`|元素加入后通知所属容器，index为真实集合索引。|
|`virtual void notify_control_removed(control &item, size_t index)`|元素移除后通知所属容器，index为移除前的真实索引。|
|`virtual void notify_control_list_cleared()`|集合完成清空时通知所属容器。|
|`virtual std::vector<control *> get_active_control_list() const`|返回当前参与显示和交互的元素；派生容器可过滤非活动页面。|
|`virtual bool is_control_active(const control &item) const`|判断指定元素是否参与该容器当前的显示与交互。|
|`virtual std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const`|返回容器安排的矩形；nullopt表示沿用元素自身矩形。|
|`virtual std::optional<int64_t> get_selection_index_at(double left, double top, const rectangle_t &rectangle) const`|根据本地位置和容器矩形取得选择索引；未命中返回nullopt。|

### `easyvrui/control/control_collection.h`

有序、按名称索引的控件容器。

#### `control_collection`

声明：`class control_collection`。

持有有序子控件，名称在当前容器内唯一。index从0开始；insert越过末尾时追加。按name查询为平均O(1)，按位置取得元素为O(1)，中间插入和移除需移动有序项。引用重载不接管对象销毁，调用方保证对象比容器中的引用活得更久；shared_ptr重载保留共享所有权。remove解除父关系并返回对象；引用添加时返回值可能不拥有对象。共享指针为空、重名、已有父级或形成环都会失败。

|声明|用途与调用语义|
|---|---|
|`explicit control_collection(container_control &owner)`|构造本类型实例；参数含义见本类型说明及签名。|
|`virtual ~control_collection()`|析构对象，结束其资源或引用的生命周期。|
|`size_t get_size() const`|返回集合项数。|
|`bool is_empty() const`|查询控件集合是否为空。|
|`bool contains(const control &item) const`|按实例查找指定控件。|
|`bool contains(const u32string &name) const`|按名称查找控件。|
|`control &get_control(size_t index) const`|按index或name返回控件引用；不存在时抛出异常。|
|`control &get_control(const u32string &name) const`|按index或name返回控件引用；不存在时抛出异常。|
|`size_t get_index(const control &item) const`|返回对象或文字在集合中的0起始位置；不存在时抛出异常。|
|`const vector<control *> &get_item_list() const`|返回当前集合的只读有序列表；该引用的有效性随所属容器生命周期和后续修改变化。|
|`virtual void insert(size_t index, control &item)`|在index位置插入；index不小于当前数量时追加。具体元素类型、所有权和重名约束见所属容器说明。|
|`virtual void insert(size_t index, std::shared_ptr<control> item)`|在index位置插入；index不小于当前数量时追加。具体元素类型、所有权和重名约束见所属容器说明。|
|`void add(control &item)`|追加项目；对象引用方式由调用方保证存活，shared_ptr方式由容器保留共享所有权。|
|`void add(std::shared_ptr<control> item)`|追加项目；对象引用方式由调用方保证存活，shared_ptr方式由容器保留共享所有权。|
|`virtual std::shared_ptr<control> remove(size_t index)`|移除指定元素并返回其shared_ptr；共享添加时转交该引用，引用添加时返回不接管销毁的引用。|
|`std::shared_ptr<control> remove(control &item)`|移除指定元素并返回其shared_ptr；共享添加时转交该引用，引用添加时返回不接管销毁的引用。|
|`std::shared_ptr<control> remove(const u32string &name)`|移除指定元素并返回其shared_ptr；共享添加时转交该引用，引用添加时返回不接管销毁的引用。|
|`virtual void clear()`|从集合移除全部控件。|
|`control &operator[](size_t index) const`|按0起始位置或名称取得对象引用，行为与get_control/get_page一致。|
|`control &operator[](const u32string &name) const`|按0起始位置或名称取得对象引用，行为与get_control/get_page一致。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`container_control &get_owner() const`|返回集合所属容器的引用。|
|`void release_control_list() noexcept`|释放集合持有的引用，供派生集合析构阶段使用。|
|`virtual void notify_control_added(control &item, size_t index)`|派生集合的添加通知，item已加入，index为实际索引。|
|`virtual void notify_control_removed(control &item, size_t index, bool clearing)`|派生集合的移除通知；clearing表示本次操作来自clear。|

### `easyvrui/control/panel.h`

普通子控件面板。

#### `panel`

声明：`class panel : public container_control`。

普通内容面板，只增加名称构造方式，继承container_control全部公共接口。

继承`container_control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`explicit panel(const u32string &name)`|构造对象；参数、默认状态和约束见本类型说明。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`panel(const u32string &name, const u32string &type)`|构造对象；参数、默认状态和约束见本类型说明。|

### `easyvrui/control/selection_control.h`

#### `selection_control`

声明：`class selection_control : public text_control`。

集合选择控件的抽象基类，继承字体与前景色。派生类定义项目区空白命中及清除选择。Listbox、TreeView、Grid和ListView的项目空白区按此规则退出文本编辑、收起IME/layout，并保留键盘导航焦点。启用`clear_selection_on_blank_click`时同时清除项选择。表头、列宽调节区、滚动条和弹出选项各自处理点击。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_clear_selection_on_blank_click_changed`|空白点击选择规则变化时触发。|
|`virtual bool get_clear_selection_on_blank_click() const`|读取点击项目区空白时是否清除项选择，默认false。|
|`virtual void set_clear_selection_on_blank_click(bool value)`|设置点击项目区空白时是否清除项选择，默认false。|
|`virtual bool is_blank_at(double local_left, double local_top) const`|判断控件本地位置是否为空白，具体项目区域由派生类决定。|
|`virtual void clear_selection() = 0`|纯虚函数，由具体集合控件实现清空选择。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`selection_control(const std::u32string &name, const std::u32string &type)`|构造实例；参数和约束见本类型说明。|

## 文字与项目控件

### `easyvrui/control/label.h`

静态文本标签。

#### `label`

声明：`class label : public text_control`。

标签继承`text_control`，用于显示文本，默认文字为空。

继承`text_control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_text_changed`|文本变化时触发。|
|`explicit label(const u32string &name)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`virtual const u32string &get_text() const`|读取文本内容。|
|`virtual void set_text(const u32string &value)`|设置文本内容。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|使用context绘制控件正文。派生类可重载以实现自定义外观。|

### `easyvrui/control/button.h`

可聚焦和点击的文本按钮。

#### `button`

声明：`class button : public text_control`。

文本按钮，默认text为空，支持焦点和on_click；继承text_control。

继承`text_control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_text_changed`|文本变化时触发。|
|`explicit button(const u32string &name)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`bool is_focusable() const override`|查询控件类型是否可接收焦点；实际焦点还受visible、enabled和窗口模态状态影响。|
|`virtual const u32string &get_text() const`|读取文本内容。|
|`virtual void set_text(const u32string &value)`|设置文本内容。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`button(const u32string &name, const u32string &type)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`void render(render_context &context) const override`|使用context绘制控件正文。派生类可重载以实现自定义外观。|

### `easyvrui/control/textbox.h`

文本输入、选区、多行与滚动条控件。

#### `textbox`

声明：`class textbox : public text_control`。

文本输入控件，默认text为空、selectable=true，read_only=false，max_length=0，multiline=false，两条滚动条显示开关均为false，选区起点和长度均为0。multiline保留换行；单行模式移除换行。修改max_length会规范现有文本。字号和布局决定实际行高，文本索引以码点计数并对齐字素边界。

继承`text_control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_text_changed`|文本变化时触发。|
|`event_container<event_args_t> on_read_only_changed`|只读状态变化时触发。|
|`event_container<event_args_t> on_selectable_changed`|文本选择设置变化时触发。|
|`event_container<event_args_t> on_selection_changed`|选择状态变化时触发；文本编辑器使用start/length，项目与页签使用selected。|
|`event_container<event_args_t> on_max_length_changed`|文本长度上限变化时触发。|
|`event_container<event_args_t> on_multiline_changed`|多行开关变化时触发。|
|`event_container<event_args_t> on_horizontal_scrollbar_visible_changed`|横向滚动条显示设置变化时触发。|
|`event_container<event_args_t> on_vertical_scrollbar_visible_changed`|纵向滚动条显示设置变化时触发。|
|`explicit textbox(const u32string &name)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`bool is_focusable() const override`|查询控件类型是否可接收焦点；实际焦点还受visible、enabled和窗口模态状态影响。|
|`virtual const u32string &get_text() const`|读取文本内容。|
|`virtual void set_text(const u32string &value)`|设置文本内容。|
|`virtual bool get_read_only() const`|读取用户输入只读状态；程序仍可设置文本。|
|`virtual void set_read_only(bool value)`|设置用户输入只读状态；程序仍可设置文本。|
|`virtual bool get_selectable() const`|是否允许文本选择、显示光标和唤起输入界面；false时仍可接收控件焦点。|
|`virtual void set_selectable(bool value)`|设置文本可选择开关；false时隐藏光标、关闭输入界面并阻止用户编辑，程序set_text仍可使用。|
|`virtual bool get_multiline() const`|读取多行模式，默认false。|
|`virtual void set_multiline(bool value)`|设置多行模式，默认false。|
|`virtual bool get_horizontal_scrollbar_visible() const`|读取横向滚动条显示开关。|
|`virtual void set_horizontal_scrollbar_visible(bool value)`|设置横向滚动条显示开关。|
|`virtual bool get_vertical_scrollbar_visible() const`|读取纵向滚动条显示状态。|
|`virtual void set_vertical_scrollbar_visible(bool value)`|设置纵向滚动条显示状态。|
|`virtual uint64_t get_selection_start() const`|读取选区较小端的码点位置。|
|`virtual uint64_t get_selection_length() const`|读取选区包含的码点数。|
|`virtual void set_selection_start(uint64_t value)`|设置选区较小端的码点位置。|
|`virtual void set_selection_length(uint64_t value)`|设置选区包含的码点数。|
|`virtual u32string get_selected_text() const`|读取选区文本副本。|
|`virtual bool get_can_undo() const`|查询文本编辑能否撤销。|
|`virtual bool get_can_redo() const`|查询是否有可重做的文本编辑记录。|
|`virtual bool undo()`|撤销一次编辑，成功时返回true。|
|`virtual bool redo()`|重做一次编辑，成功时返回true。|
|`virtual void set_selected_text(const u32string &value)`|以value替换当前选区；作为程序修改入口，可用于read_only控件。|
|`virtual uint64_t get_max_length() const`|读取文本最大码点数，0表示不限；截断保留完整字素。|
|`virtual void set_max_length(uint64_t value)`|设置文本最大码点数，0表示不限；截断保留完整字素。|
|`virtual void select(uint64_t start, uint64_t length = 0u)`|选择从start起的length个码点；默认length为0，即放置插入点。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`virtual uint64_t get_selection_anchor() const`|读取选区锚点，保留选择方向。|
|`virtual uint64_t get_selection_active() const`|读取选区活动端，即当前插入端。|
|`virtual void set_selection(uint64_t anchor, uint64_t active)`|以anchor和active指定带方向的选择范围；位置限制在文本范围并对齐字素边界。|
|`void render(render_context &context) const override`|使用context绘制控件正文。派生类可重载以实现自定义外观。|
|`void render_overlay(render_context &context) const override`|绘制控件浮层，例如组合框弹出菜单。|

编辑器拥有焦点时，Ctrl+Z撤销文本修改，Ctrl+Y或Ctrl+Shift+Z恢复修改。这些按键优先于应用菜单快捷键。

### `easyvrui/control/item_control.h`

项目列表、选中项和行滚动的公共基类。

#### `item_control`

声明：`class item_control : public selection_control`。

项目控件基类，构造函数为protected，继承selection_control。默认项目为空、selected_index=-1、scroll_offset=0、row_height=32。selected_item为只读u32string，无选中项时返回空字符串。scroll_offset访问接口为protected。

继承`selection_control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`item_collection item_list`|文本项目容器，修改会通知所属项目控件。|
|`event_container<event_args_t> on_item_list_changed`|文本项目列表变化时触发。|
|`event_container<event_args_t> on_selection_changed`|选择状态变化时触发；文本编辑器使用start/length，项目与页签使用selected。|
|`event_container<event_args_t> on_selected_index_changed`|选中索引变化时触发。|
|`event_container<event_args_t> on_row_height_changed`|行高变化时触发。|
|`bool is_focusable() const override`|查询控件类型是否可接收焦点；实际焦点还受visible、enabled和窗口模态状态影响。|
|`const item_collection &get_item_list() const`|读取有序字符串集合。|
|`item_collection &get_item_list()`|取得可修改集合，通过`assign(value)`替换内容。|
|`virtual int64_t get_selected_index() const`|读取当前选中索引，-1表示未选择。|
|`virtual void set_selected_index(int64_t value)`|设置当前选中索引，-1表示未选择。|
|`void clear_selection() override`|清空选择，selected_index变为-1，selected_item返回空字符串。|
|`virtual u32string get_selected_item() const`|读取选中文字；无选中项时返回空字符串。|
|`virtual uint64_t get_row_height() const`|读取项目行高，逻辑单位且必须大于0。|
|`virtual void set_row_height(uint64_t value)`|设置项目行高，逻辑单位且必须大于0。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`int64_t selected_index = NO_SELECTION_INDEX`|派生类可访问的当前选中索引，-1表示未选择；常规赋值使用setter以产生变化通知。|
|`uint64_t scroll_offset = 0u`|派生类可访问的首个显示项目的索引偏移；常规赋值使用setter以产生变化通知。|
|`uint64_t row_height = render_style::DEFAULT_ROW_HEIGHT`|派生类可访问的项目行高，逻辑单位且必须大于0；常规赋值使用setter以产生变化通知。|
|`virtual bool get_vertical_scrollbar_visible() const`|派生类查询是否显示纵向滚动条，默认返回false。|
|`void refresh_layout() override`|刷新控件布局，派生类覆盖时保留必要的基类处理。|
|`virtual void refresh_item_list()`|项目内容变化后的派生刷新入口。|
|`virtual void notify_selection_changed(int64_t previous_index, const u32string &previous_item, int64_t next_index, const u32string &next_item)`|选择变化通知，提供原索引/文字及新索引/文字。|
|`virtual void notify_item_list_changed(const vector<u32string> &previous, int64_t previous_index, const u32string &previous_item, uint64_t previous_scroll)`|项目列表变化通知，提供原列表、原选择和原滚动位置。|
|`virtual uint64_t get_scroll_offset() const`|读取首个显示项目的索引偏移。|
|`virtual void set_scroll_offset(uint64_t value)`|设置首个显示项目的索引偏移。|
|`item_control(const u32string &name, const u32string &type)`|构造对象；参数、默认状态和约束见本类型说明。|
|`virtual uint64_t get_maximum_scroll_offset() const`|返回当前项目控件允许的最大首行偏移。|
|`virtual uint64_t get_visible_item_count() const`|返回当前视口的项目行容量。|
|`void reveal_item(uint64_t index)`|滚动到可显示指定项目的位置，并保留仍可显示该项目的现有位置。|
|`virtual void handle_item_list_changed(const vector<u32string> &previous)`|处理项目列表变化并调整当前选择和显示。|
|`virtual void render_item_list(render_context &context, const render_rectangle_t &rectangle) const`|在rectangle中绘制当前可见项目。|

### `easyvrui/control/item_collection.h`

有序文本项目容器。

#### `item_collection`

声明：`class item_collection`。

有序Unicode文字项目容器，允许相同文字重复。按文字get_index/remove操作第一个匹配项；不存在或位置越界时抛出异常。insert超出末尾时追加。修改列表会同步所属item_control的选择和绘制状态。

|声明|用途与调用语义|
|---|---|
|`explicit item_collection(item_control &owner)`|构造本类型实例；参数含义见本类型说明及签名。|
|`void add(const u32string &item)`|追加项目；对象引用方式由调用方保证存活，shared_ptr方式由容器保留共享所有权。|
|`void insert(size_t index, const u32string &item)`|在index位置插入；index不小于当前数量时追加。具体元素类型、所有权和重名约束见所属容器说明。|
|`u32string remove(size_t index)`|按参数指定的位置、对象或名称移除项目；返回被移除对象或是否成功，具体返回类型见签名。|
|`u32string remove(const u32string &item)`|按参数指定的位置、对象或名称移除项目；返回被移除对象或是否成功，具体返回类型见签名。|
|`void clear()`|从集合移除全部文字项目。|
|`void assign(const vector<u32string> &item_list)`|用item_list整体替换文本项目列表，并更新选择与显示状态。|
|`size_t get_size() const`|返回集合项数。|
|`bool is_empty() const`|查询文字项目集合是否为空。|
|`bool contains(const u32string &item) const`|查询集合中是否存在与`item`相同的文字。|
|`const u32string &get_item(size_t index) const`|按index返回项目文字只读引用；越界时抛出异常。|
|`const u32string &operator[](size_t index) const`|按0起始位置返回项目文字const引用；越界抛出异常。|
|`size_t get_index(const u32string &item) const`|返回对象或文字在集合中的0起始位置；不存在时抛出异常。|
|`const vector<u32string> &get_item_list() const`|返回当前集合的只读有序列表；该引用的有效性随所属容器生命周期和后续修改变化。|

### `easyvrui/control/combobox.h`

列表选择及可选文本编辑的组合框。

#### `combobox`

声明：`class combobox : public item_control`。

继承`item_control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_dropdown_style_changed`|下拉样式变化时触发。|
|`event_container<event_args_t> on_text_changed`|文本变化时触发。|
|`explicit combobox(const u32string &name)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`virtual const u32string &get_text() const`|读取文本内容。|
|`virtual void set_text(const u32string &value)`|设置文本内容。|
|`virtual combobox_dropdown_style_t get_dropdown_style() const`|读取下拉样式，默认dropdown_list。|
|`virtual void set_dropdown_style(combobox_dropdown_style_t value)`|设置dropdown允许自由输入，设置dropdown_list从列表选择。|
|`virtual bool get_dropped_down() const`|读取下拉列表是否展开。|
|`virtual void set_dropped_down(bool value)`|展开或收起下拉列表。|
|`void set_selected_index(int64_t value) override`|设置当前选中索引，-1表示未选择。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void refresh_item_list() override`|同步选中文字、下拉列表及布局。|
|`void handle_item_list_changed(const vector<u32string> &previous) override`|处理项目列表变化并调整当前选择和显示。|
|`void render(render_context &context) const override`|使用context绘制控件正文。派生类可重载以实现自定义外观。|
|`void render_overlay(render_context &context) const override`|绘制控件浮层，例如组合框弹出菜单。|

### `easyvrui/control/listbox.h`

可滚动的单选列表。

#### `listbox`

声明：`class listbox : public item_control`。

继承item_control，默认行高30；内容超出可见行数时提供纵向滚动条。get_vertical_scrollbar_visible()为只读计算状态。激光对应手柄的摇杆可滚动列表，滚动量随偏转程度变化。

继承`item_control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`explicit listbox(const u32string &name)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`bool is_blank_at(double local_left, double local_top) const override`|判断本地位置是否为列表内容区空白。|
|`virtual bool get_vertical_scrollbar_visible() const`|计算列表是否存在超出可见区域的纵向项目；内容不足时返回false。|
|`void set_visible(bool value) override`|设置可见状态；隐藏时清理本控件正在进行的交互。|
|`void set_enabled(bool value) override`|设置可操作状态；禁用时清理正在进行的交互。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void refresh_layout() override`|刷新控件布局，派生类覆盖时保留必要的基类处理。|
|`uint64_t get_maximum_scroll_offset() const override`|返回当前项目控件允许的最大首行偏移。|
|`void render(render_context &context) const override`|使用context绘制控件正文。派生类可重载以实现自定义外观。|

## 扩展控件

### `easyvrui/control/checkbox.h`

#### `checkbox`

声明：`class checkbox : public text_control`。

复选框，默认text为空、checked=false。点击或按Space/Enter切换checked；文字外观继承text_control。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_text_changed`|文本变化时触发。|
|`event_container<event_args_t> on_checked_changed`|勾选状态变化时触发。|
|`explicit checkbox(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`bool is_focusable() const override`|查询该控件是否具有焦点能力；实际焦点还受visible、enabled和模态关系限制。|
|`virtual const std::u32string &get_text() const`|读取显示文字。|
|`virtual void set_text(const std::u32string &value)`|设置显示文字。|
|`virtual bool get_checked() const`|读取当前勾选状态。|
|`virtual void set_checked(bool value)`|设置当前勾选状态。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|

### `easyvrui/control/radiobutton.h`

#### `radiobutton`

声明：`class radiobutton : public text_control`。

单选按钮，默认text为空、checked=false。同一直接容器内的radiobutton互斥；set_checked(true)会取消同级其他单选按钮。可用panel划分独立组。点击或按Space/Enter选中。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_text_changed`|文本变化时触发。|
|`event_container<event_args_t> on_checked_changed`|勾选状态变化时触发。|
|`explicit radiobutton(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`bool is_focusable() const override`|查询该控件是否具有焦点能力；实际焦点还受visible、enabled和模态关系限制。|
|`virtual const std::u32string &get_text() const`|读取显示文字。|
|`virtual void set_text(const std::u32string &value)`|设置显示文字。|
|`virtual bool get_checked() const`|读取当前勾选状态。|
|`virtual void set_checked(bool value)`|设置当前勾选状态。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|

### `easyvrui/control/numericupdown.h`

#### `numericupdown`

声明：`class numericupdown : public text_control`。

数值输入与上下调节按钮。value/minimum/maximum/step为double，默认分别为0.0/0.0/100.0/1.0；decimal_places为uint32_t，默认0，范围0至17，控制显示小数位数。边界须有限且minimum<maximum，step须为有限正数；value限制在边界内。上下按钮各有悬停和焦点，点击它们保持数值编辑区关闭。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_value_changed`|当前值变化时触发。|
|`event_container<event_args_t> on_minimum_changed`|下限变化时触发。|
|`event_container<event_args_t> on_maximum_changed`|上限变化时触发。|
|`event_container<event_args_t> on_step_changed`|步长变化时触发。|
|`event_container<event_args_t> on_decimal_places_changed`|小数位数变化时触发。|
|`explicit numericupdown(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`bool is_focusable() const override`|查询该控件是否具有焦点能力；实际焦点还受visible、enabled和模态关系限制。|
|`virtual double get_value() const`|读取当前数值；setter按本类型边界处理。|
|`virtual void set_value(double next)`|设置当前数值；setter按本类型边界处理。|
|`virtual double get_minimum() const`|读取数值区间下界。|
|`virtual void set_minimum(double next)`|设置数值区间下界。|
|`virtual double get_maximum() const`|读取数值区间上界。|
|`virtual void set_maximum(double next)`|设置数值区间上界。|
|`virtual double get_step() const`|读取上下按钮每次调整的有限正步长。|
|`virtual void set_step(double next)`|设置上下按钮每次调整的有限正步长。|
|`virtual uint32_t get_decimal_places() const`|读取显示的小数位数，范围0至17。|
|`virtual void set_decimal_places(uint32_t next)`|设置显示的小数位数，范围0至17。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`size_t get_focus_target_count() const override`|返回内部可聚焦区域数量，供复合控件焦点导航使用。|
|`virtual size_t get_focus_target_at(double left, double top) const`|根据控件本地坐标取得内部焦点区域索引。|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|
|`void render_overlay(render_context &context) const override`|派生绘制入口；使用context绘制浮层。|

### `easyvrui/control/slider.h`

#### `slider`

声明：`class slider : public control`。

可拖动滑块。minimum、maximum、value均为int64_t，默认0、100、0，要求minimum<maximum；set_value将输入限制在区间内，修改边界同时收敛当前值。方向由`orientation_t`指定，默认`orientation_t::horizontal`，也可设为`orientation_t::vertical`。方向键以整数1增减数值，纵向上端对应maximum。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_minimum_changed`|下限变化时触发。|
|`event_container<event_args_t> on_maximum_changed`|上限变化时触发。|
|`event_container<event_args_t> on_value_changed`|当前值变化时触发。|
|`event_container<event_args_t> on_orientation_changed`|方向变化时触发。|
|`event_container<event_args_t> on_drag_start`|开始拖动时触发。|
|`event_container<interaction_end_event_args_t> on_drag_end`|结束或取消拖动时触发。|
|`explicit slider(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`bool is_focusable() const override`|查询该控件是否具有焦点能力；实际焦点还受visible、enabled和模态关系限制。|
|`virtual int64_t get_minimum() const`|读取数值区间下界。|
|`virtual void set_minimum(int64_t next)`|设置数值区间下界。|
|`virtual int64_t get_maximum() const`|读取数值区间上界。|
|`virtual void set_maximum(int64_t next)`|设置数值区间上界。|
|`virtual int64_t get_value() const`|读取当前数值；setter按本类型边界处理。|
|`virtual void set_value(int64_t next)`|设置当前数值；setter按本类型边界处理。|
|`virtual orientation_t get_orientation() const`|读取布局方向，允许值及含义见本类型说明。|
|`virtual void set_orientation(orientation_t next)`|设置布局方向，允许值及含义见本类型说明。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|

### `easyvrui/control/progressbar.h`

#### `progressbar`

声明：`class progressbar : public control`。

整数进度显示。minimum、maximum、value均为int64_t，默认0、100、0。minimum<maximum；set_value将输入限制到区间内，修改边界同时调整当前值。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_minimum_changed`|下限变化时触发。|
|`event_container<event_args_t> on_maximum_changed`|上限变化时触发。|
|`event_container<event_args_t> on_value_changed`|当前值变化时触发。|
|`explicit progressbar(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`virtual int64_t get_minimum() const`|读取数值区间下界。|
|`virtual void set_minimum(int64_t next)`|设置数值区间下界。|
|`virtual int64_t get_maximum() const`|读取数值区间上界。|
|`virtual void set_maximum(int64_t next)`|设置数值区间上界。|
|`virtual int64_t get_value() const`|读取当前数值；setter按本类型边界处理。|
|`virtual void set_value(int64_t next)`|设置当前数值；setter按本类型边界处理。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|

### `easyvrui/control/image.h`

#### `image`

声明：`class image : public control`。

图像控件。source保存`shared_ptr<const drawing_image>`，默认空。`stretch_mode`使用`image_stretch_mode_t`，默认`contain`。`fill`、`contain`、`cover`和`none`分别表示拉伸填满、等比完整显示、等比覆盖并裁切、保持原图像素尺寸。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_source_changed`|图像源变化时触发。|
|`event_container<event_args_t> on_stretch_mode_changed`|拉伸方式变化时触发。|
|`event_container<event_args_t> on_source_unavailable`|图像资源不可用时触发。|
|`explicit image(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`virtual const std::shared_ptr<const drawing_image> &get_source() const`|读取图像资源的共享引用，nullptr表示清除。|
|`virtual void set_source(std::shared_ptr<const drawing_image> value)`|设置图像资源的共享引用，nullptr表示清除。|
|`virtual image_stretch_mode_t get_stretch_mode() const`|读取图像拉伸模式：fill、contain、cover或none。|
|`virtual void set_stretch_mode(image_stretch_mode_t value)`|设置图像拉伸模式：fill、contain、cover或none。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|

### `easyvrui/control/screen.h`

#### `screen`

声明：`class screen : public control`。

实时显示器画面控件。screen_id为uint64_t，默认0；编号按当前引擎提供的显示器枚举对应，切屏使用set_screen_id。控件矩形决定逻辑显示尺寸，设为屏幕像素尺寸可按相同逻辑尺寸显示；实际空间大小仍受所属窗口physical_scale影响。get_screen_available提供可用状态。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_screen_id_changed`|显示器变化时触发。|
|`event_container<event_args_t> on_screen_unavailable`|显示器捕获不可用时触发。|
|`event_container<event_args_t> on_screen_restored`|显示器捕获恢复时触发。|
|`explicit screen(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`virtual uint64_t get_screen_id() const`|读取显示器编号。|
|`virtual void set_screen_id(uint64_t value)`|设置显示器编号。|
|`virtual bool get_screen_available() const`|读取当前显示器捕获是否可用。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|

### `easyvrui/control/scrollpanel.h`

#### `scrollpanel`

声明：`class scrollpanel : public container_control`。

可滚动容器，内容通过get_control_list()添加。horizontal_scrollbar_visible和vertical_scrollbar_visible默认true；滚动条及视口依据内容范围布局。滚动偏移访问接口为protected，应用通过控件布局及滚动输入操作。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_horizontal_scrollbar_visible_changed`|横向滚动条显示设置变化时触发。|
|`event_container<event_args_t> on_vertical_scrollbar_visible_changed`|纵向滚动条显示设置变化时触发。|
|`explicit scrollpanel(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`virtual bool get_horizontal_scrollbar_visible() const`|读取是否显示横向滚动条。|
|`virtual void set_horizontal_scrollbar_visible(bool value)`|设置是否显示横向滚动条。|
|`virtual bool get_vertical_scrollbar_visible() const`|读取是否显示纵向滚动条。|
|`virtual void set_vertical_scrollbar_visible(bool value)`|设置是否显示纵向滚动条。|
|`void set_visible(bool value) override`|设置可见状态；隐藏时清理本控件正在进行的交互。|
|`void set_enabled(bool value) override`|设置是否可操作。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void refresh_layout() override`|刷新控件布局，派生类覆盖时保留必要的基类处理。|
|`void notify_control_added(control &child, size_t index) override`|插入后的容器通知，index是元素的真实集合索引。|
|`void notify_control_removed(control &child, size_t index) override`|移除后的容器通知，index是移除前的真实集合索引。|
|`virtual uint64_t get_horizontal_scroll_offset() const`|派生类读取横向逻辑滚动偏移。|
|`virtual void set_horizontal_scroll_offset(uint64_t value)`|派生类设置横向逻辑滚动偏移，限制在内容范围内。|
|`virtual uint64_t get_vertical_scroll_offset() const`|派生类读取纵向逻辑滚动偏移。|
|`virtual void set_vertical_scroll_offset(uint64_t value)`|派生类设置纵向逻辑滚动偏移，限制在内容范围内。|
|`virtual uint64_t get_maximum_vertical_scroll_offset() const`|派生类读取纵向逻辑滚动上限。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|为元素提供容器管理的矩形；nullopt表示沿用其自身矩形。|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|
|`void render_overlay(render_context &context) const override`|派生绘制入口；使用context绘制浮层。|

### `easyvrui/control/splitter.h`

#### `splitter`

声明：`class splitter : public container_control`。

双区域分隔容器，按get_control_list()顺序安排至多两个控件。方向默认`orientation_t::vertical`，以竖直分隔条划分左右区域。`orientation_t::horizontal`以水平分隔条划分上下区域。split_position为有限double，范围0.0至1.0，默认0.5。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_orientation_changed`|方向变化时触发。|
|`event_container<event_args_t> on_split_position_changed`|分隔位置变化时触发。|
|`event_container<event_args_t> on_split_start`|开始拖动分隔条时触发。|
|`event_container<interaction_end_event_args_t> on_split_end`|结束拖动分隔条时触发。|
|`explicit splitter(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`virtual orientation_t get_orientation() const`|读取布局方向，允许值及含义见本类型说明。|
|`virtual void set_orientation(orientation_t value)`|设置布局方向，允许值及含义见本类型说明。|
|`virtual double get_split_position() const`|读取首区域占可用空间的比例，范围0.0至1.0。|
|`virtual void set_split_position(double value)`|设置首区域占可用空间的比例，范围0.0至1.0。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void validate_control(const control &child) const override`|验证普通容器条件，并限制最多两个区域控件。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|为元素提供容器管理的矩形；nullopt表示沿用其自身矩形。|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|

## 多列与树形控件

### `easyvrui/control/grid.h`

#### `grid_column_t`

声明：`struct grid_column_t`。

表格列定义：text为标题，width默认100，editable默认true。列加入grid或修改列宽时须为正；总宽度须能由int64_t表示，失败保留原列和原宽度。

|声明|用途与调用语义|
|---|---|
|`static constexpr uint64_t DEFAULT_WIDTH = 100u`|默认列宽100逻辑像素。|
|`std::u32string text`|表头文字。|
|`uint64_t width = DEFAULT_WIDTH`|正整数列宽，默认DEFAULT_WIDTH。|
|`bool editable = true`|本列是否允许用户编辑，默认true。|

#### `grid_cell_t`

声明：`struct grid_cell_t`。

以uint64_t记录row和column，均从0开始；相等比较按两个字段进行。

|声明|用途与调用语义|
|---|---|
|`uint64_t row = 0u`|0起始行索引。|
|`uint64_t column = 0u`|0起始列索引。|
|`bool operator==(const grid_cell_t &) const = default`|逐字段比较行列位置。|

#### `grid_selection_mode_t`

声明：`enum class grid_selection_mode_t`。

cell表示单元格选择，row表示整行选择。

|声明|用途与调用语义|
|---|---|
|`cell`|逐单元格选择。|
|`row`|整行选择。|

#### `grid_cell_render_t`

声明：`struct grid_cell_render_t`。

传给单元格绘制回调的数据记录，包含单元格位置、绘制矩形、值和选择/悬停/编辑状态。

|声明|用途与调用语义|
|---|---|
|`grid_cell_t cell`|当前行列位置。|
|`render_rectangle_t rectangle`|当前单元格的绘制矩形。|
|`grid_value_t value`|单元格值。|
|`bool selected = false`|是否已选中。|
|`bool hovered = false`|是否被指向。|
|`bool editing = false`|是否正在编辑。|

#### `grid`

声明：`class grid : public selection_control`。

可编辑二维表格。默认列为空、行数0、selection_mode=cell、multi_select=false、selected_index=-1、row_height=30、header_height=32、read_only=false。header_height=0隐藏表头。列宽默认100；插入或修改时width=0以及总宽度溢出均抛出异常，原数据与变更事件保持不变。public接口通过单元格、外部数据回调和编辑校验操作表格；滚动偏移属于protected扩展接口。

表头背景覆盖整个可见宽度，长标题末尾显示省略号。实体键盘捕获模式中，Ctrl点击切换单项、Shift扩展选择；显式select_cell的extend/toggle参数可由应用控制选择。begin_edit和commit_edit返回是否成功，失败说明可从get_edit_error读取；结束编辑时IME/layout对应当前单元格的可见矩形。

grid_value_t为variant<u32string, int64_t, double, bool>。value_provider_t读取指定行列；value_writer_t尝试写入并通过error返回失败说明；cell_renderer_t接收render_context与grid_cell_render_t；edit_validator_t在提交前检查单元格和值。

|声明|用途与调用语义|
|---|---|
|`using value_provider_t = std::function<grid_value_t(uint64_t, uint64_t)>`|外部数据读取回调，参数为行和列，返回grid_value_t。|
|`using value_writer_t = std::function<bool(uint64_t, uint64_t, const grid_value_t &, std::u32string &)>`|外部写入回调，参数为行、列、待写值及错误文字引用，返回bool。|
|`using cell_renderer_t = std::function<void(render_context &, const grid_cell_render_t &)>`|可见单元格绘制回调，接收render_context和单元格绘制记录。|
|`using edit_validator_t = std::function<bool(grid_cell_t, const grid_value_t &, std::u32string &)>`|编辑提交校验，参数为单元格位置、值和错误文字引用，返回bool。|
|`event_container<event_args_t> on_column_list_changed`|列定义变化时触发。|
|`event_container<grid_column_event_args_t> on_column_width_changed`|列宽变化时触发。|
|`event_container<grid_column_event_args_t> on_column_click`|点击列标题时触发。|
|`event_container<event_args_t> on_selection_changed`|选择状态变化时触发。|
|`event_container<grid_cell_event_args_t> on_cell_double_click`|双击单元格时触发。|
|`event_container<grid_cell_event_args_t> on_cell_value_changed`|单元格值变化时触发。|
|`event_container<event_args_t> on_row_height_changed`|行高变化时触发。|
|`event_container<event_args_t> on_header_height_changed`|表头高度变化时触发。|
|`event_container<grid_cell_event_args_t> on_edit_started`|开始编辑单元格时触发。|
|`event_container<grid_cell_event_args_t> on_edit_committed`|单元格编辑提交成功时触发。|
|`event_container<grid_cell_event_args_t> on_edit_cancelled`|取消单元格编辑时触发。|
|`event_container<grid_cell_event_args_t> on_edit_failed`|提交单元格编辑失败时触发。|
|`explicit grid(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`~grid() override`|析构实例，释放该对象持有的资源和引用。|
|`bool is_focusable() const override`|查询该控件是否具有焦点能力；实际焦点还受visible、enabled和模态关系限制。|
|`virtual const std::vector<grid_column_t> &get_column_list() const`|返回当前列定义的只读引用。|
|`virtual void set_column_list(std::vector<grid_column_t> value)`|整体替换列定义；宽度须为正且总宽度可由int64_t表示，校验失败保留原列。|
|`virtual uint64_t get_row_count() const`|读取总行数，初始0。|
|`virtual void set_row_count(uint64_t value)`|设置行数，并将选择与视口收敛到有效范围。|
|`virtual grid_value_t get_cell_value(uint64_t row, uint64_t column) const`|读取指定行列的值，索引越界时抛出异常。|
|`virtual void set_cell_value(uint64_t row, uint64_t column, grid_value_t value)`|调用当前数据写入入口更新指定单元格，失败抛出携带错误说明的异常。|
|`virtual void set_data_provider(uint64_t row_count, value_provider_t reader, value_writer_t writer = {})`|关联外部数据源；reader须有效，writer为空表示数据源只读，row_count为当前总行数。|
|`virtual void set_cell_renderer(cell_renderer_t renderer)`|配置可见单元格绘制回调；空回调恢复默认绘制。|
|`virtual void set_edit_validator(edit_validator_t validator)`|配置用户编辑提交校验；返回false时保留编辑状态并提供error。|
|`virtual void refresh_data()`|外部数据改变后刷新缓存、布局和显示。|
|`static std::u32string get_value_text(const grid_value_t &value)`|将grid_value_t转换为单元格显示文字。|
|`virtual std::optional<grid_cell_t> get_cell_at(double local_left, double local_top) const`|将控件本地坐标映射为单元格；表头、滚动条和空白处返回nullopt。|
|`virtual render_rectangle_t get_cell_rectangle(uint64_t row, uint64_t column) const`|读取指定单元格的逻辑绘制矩形。|
|`virtual grid_selection_mode_t get_selection_mode() const`|读取单元格或整行选择模式。|
|`virtual void set_selection_mode(grid_selection_mode_t value)`|设置cell或row选择模式。|
|`virtual bool get_multi_select() const`|读取多选开关，默认false。|
|`virtual void set_multi_select(bool value)`|启用或关闭多选。|
|`virtual const std::vector<grid_cell_t> &get_selected_cell_list() const`|返回当前选中单元格的有序只读列表。|
|`virtual bool get_cell_selected(uint64_t row, uint64_t column) const`|判断指定行列是否属于当前选择。|
|`virtual void select_cell(uint64_t row, uint64_t column, bool extend = false, bool toggle = false)`|选择指定行列；extend扩展范围，toggle切换该项选择，默认均为false。|
|`void clear_selection() override`|清空当前单元格或整行选择。|
|`bool is_blank_at(double local_left, double local_top) const override`|判断本地坐标是否属于项目区空白，供空白点击选择规则使用。|
|`virtual int64_t get_selected_index() const`|返回当前行索引，-1表示未选择。|
|`virtual void set_selected_index(int64_t value)`|选择指定有效行，-1清空选择。|
|`virtual uint64_t get_row_height() const`|读取正整数行高，默认30。|
|`virtual void set_row_height(uint64_t value)`|设置正整数行高。|
|`virtual uint64_t get_header_height() const`|读取表头高度，默认32。|
|`virtual void set_header_height(uint64_t value)`|设置表头高度；0隐藏表头。|
|`virtual uint64_t get_visible_row_count() const`|返回当前视口可显示的行数。|
|`virtual bool get_vertical_scrollbar_visible() const`|查询按内容范围计算出的纵向滚动条可见性。|
|`virtual bool get_horizontal_scrollbar_visible() const`|查询按内容范围计算出的横向滚动条可见性。|
|`virtual void set_column_width(uint64_t column, uint64_t value)`|设置已有列的正宽度；索引、宽度或总宽度非法时抛出异常，原值与事件状态保持不变。|
|`virtual bool get_read_only() const`|读取全表用户编辑只读开关，默认false。|
|`virtual void set_read_only(bool value)`|控制用户编辑；true时结束编辑并保持单元格显示。|
|`virtual bool get_editing() const`|是否存在正在编辑的单元格。|
|`virtual std::optional<grid_cell_t> get_edit_cell() const`|返回当前编辑单元格；未编辑时为nullopt。|
|`virtual const std::u32string &get_edit_text() const`|读取当前编辑区文字。|
|`virtual void set_edit_text(const std::u32string &value)`|更新当前编辑区文字，提交时再执行类型和业务校验。|
|`virtual const std::u32string &get_edit_error() const`|读取最近一次编辑失败说明。|
|`virtual bool begin_edit(uint64_t row, uint64_t column)`|开始编辑指定单元格，受控件及列只读条件限制；成功返回true。|
|`virtual bool commit_edit()`|提交当前编辑文字或指定grid_value_t，成功返回true，失败可读取get_edit_error。|
|`virtual bool commit_edit(const grid_value_t &value)`|提交当前编辑文字或指定grid_value_t，成功返回true，失败可读取get_edit_error。|
|`virtual void cancel_edit()`|取消当前编辑并收起相应输入界面。|
|`void set_visible(bool value) override`|设置可见状态；隐藏时清理本控件正在进行的交互。|
|`void set_enabled(bool value) override`|设置可操作状态；禁用时清理正在进行的交互。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void refresh_layout() override`|刷新控件布局，派生类覆盖时保留必要的基类处理。|
|`virtual void notify_selection_changed(const vector<grid_cell_t> &previous, int64_t previous_index)`|选择更新后的派生通知，提供原单元格列表及原行索引。|
|`virtual uint64_t get_scroll_offset() const`|派生类读取纵向滚动行偏移。|
|`virtual void set_scroll_offset(uint64_t value)`|派生类设置纵向滚动行偏移，限制在内容范围内。|
|`virtual uint64_t get_horizontal_scroll_offset() const`|派生类读取横向逻辑滚动偏移。|
|`virtual void set_horizontal_scroll_offset(uint64_t value)`|派生类设置横向逻辑滚动偏移，限制在内容范围内。|
|`virtual uint64_t get_maximum_scroll_offset() const`|派生类查询最大纵向行偏移。|
|`virtual uint64_t get_maximum_horizontal_scroll_offset() const`|派生类查询最大横向逻辑偏移。|
|`grid(const std::u32string &name, const std::u32string &type)`|构造实例；参数和约束见本类型说明。|
|`virtual void set_horizontal_scrollbar_enabled(bool value)`|派生类控制横向滚动条是否参与布局。|
|`virtual void remap_row_selection(uint64_t row_count, const std::function<std::optional<uint64_t>(uint64_t)> &mapper)`|数据重排后按mapper重映射原选择；返回nullopt表示原行已移除。|
|`virtual grid_value_t read_cell_value(uint64_t row, uint64_t column) const`|派生数据读取入口，返回指定行列的grid_value_t。|
|`virtual bool write_cell_value(uint64_t row, uint64_t column, const grid_value_t &value, std::u32string &error)`|派生数据写入入口；失败返回false并填写error。|
|`virtual bool get_cell_value_choice_list(uint64_t row, uint64_t column, std::vector<grid_value_t> &choice_list) const`|为单元格提供可选值；返回true时通过choice_list交付选项。|
|`virtual std::shared_ptr<const drawing_image> get_row_icon(uint64_t row) const`|读取该行的图像资源；空指针表示无图标。|
|`virtual void render_cell(render_context &context, const grid_cell_render_t &cell) const`|绘制单个可见单元格，可由派生类定制。|
|`rectangle_t get_input_rectangle() const override`|返回当前单元格实际可见的本地编辑区域，用于输入界面定位。|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|
|`void render_overlay(render_context &context) const override`|派生绘制入口；使用context绘制浮层。|

### `easyvrui/control/listview.h`

`listview`继承`selection_control`，按整行显示和选择多列文本。首列可显示项目图标。点击表头触发`on_column_click`，拖动分隔线调整列宽。用户可通过激光、滚动条和键盘浏览各行。

|成员|用途|
|---|---|
|`explicit listview(const std::u32string &name)`|创建列表视图。|
|`get_column_list()`|返回活的`listview_column_collection`引用，提供const重载。|
|`get_item_list()`|返回活的`listview_item_collection`引用，提供const重载。|
|`get_selected_index() / set_selected_index(value)`|读取或设置主选中项的位置，`-1`表示空选区。|
|`get_selected_item() / set_selected_item(item)`|读取或选择集合中的行对象，`nullptr`表示空选区。|
|`select_item(index, extend = false, toggle = false)`|按行下标选择。在多选模式下可扩展到锚点或切换当前行。|
|`get_selected_item_list()`|读取当前选区的行对象。|
|`get_multi_select() / set_multi_select(value)`|切换单选或多选。|
|`get_row_height() / set_row_height(value)`|设置正的行高，默认30逻辑像素。|
|`get_header_height() / set_header_height(value)`|设置表头高度，默认32，0隐藏表头。|
|`get_visible_row_count()`|读取一屏可容纳的逻辑行数。|
|`get_vertical_scrollbar_visible() / get_horizontal_scrollbar_visible()`|读取滚动条的显示状态。|
|`on_item_list_changed`、`on_column_list_changed`|项目或列集合变化时触发。|
|`on_column_width_changed`、`on_column_click`|列宽变化或点击表头时触发。参数为`listview_column_event_args_t`，提供列对象`column`及其索引`index`。|
|`on_selection_changed`、`on_row_double_click`|选区变化或激活一行时触发。行双击参数为`listview_item_event_args_t`，提供行对象`item`及其索引`index`。|
|`on_row_height_changed`、`on_header_height_changed`|行高或表头高度变化时触发。|

排序可将原有行对象以新顺序传入`get_item_list().assign(...)`。集合按对象身份维护选择。

### `easyvrui/control/listview_column.h`

`listview_column(text, width)`保存表头文字和逻辑宽度。默认文字为空，宽度为`DEFAULT_WIDTH`（100）。通过`get_text()/set_text()`和`get_width()/set_width()`访问。列宽须大于0，同一列表的列宽合计须落在`int64_t`正数范围内。已挂载列的修改会刷新视图。

### `easyvrui/control/listview_item.h`

`listview_item(cell_list, icon, tag)`保存一行文本、可选图标和应用标签。默认各项为空，可通过`get_icon()/set_icon()`和`get_tag()/set_tag()`访问。读写`get_cell_list()`返回的集合即可更新行文本。

### `easyvrui/control/listview_column_collection.h`

`listview_column_collection`由列表视图持有。使用`get_size()`读取数量，`contains(item)`和`get_index(item)`按列对象查询，`operator[]`返回共享引用。`add/insert`插入列，`remove`按对象或位置移出并返回共享指针，`assign`替换全部内容，`clear`清空集合。插入前校验所有权和宽度。

### `easyvrui/control/listview_item_collection.h`

`listview_item_collection`使用与列集合相同的成员名，元素为`std::shared_ptr<listview_item>`。每个行对象同时归属一个列表，移出后可以加入另一列表。

### `easyvrui/control/listview_cell_collection.h`

`listview_cell_collection`按列位置保存UTF-32单元格文字。`operator[]`读取文字，`set_cell(index, text)`修改已有位置。`add/insert/remove/assign/clear`调整集合，`get_size/contains/get_index`执行查询。已挂载项目的更新自动重绘。

### `easyvrui/control/treeview.h`

`treeview`继承`selection_control`。通过`get_node_list()`访问根节点集合，提供const重载。`get_selected_node()/set_selected_node(tree_node *)`按对象访问选择，`nullptr`清除选择。`get_row_height()`和`get_vertical_scrollbar_visible()`读取布局状态。

`on_node_list_changed`在增删节点时触发，`on_selection_changed`在选区变化时触发，`on_node_expanded/on_node_collapsed`对应展开和折叠，`on_node_activated`对应双击或Enter。`tree_node_event_args_t::node`指向事件涉及的节点。

### `easyvrui/control/tree_node.h`

`tree_node(text, expanded, tag)`创建节点，默认文字和标签为空，节点折叠。`get_text/set_text`、`get_tag/set_tag`和`get_expanded/set_expanded`访问各属性。`expand()`和`collapse()`切换展开状态。`get_parent()`返回父节点指针，根节点和脱离父节点的节点返回`nullptr`。`get_node_list()`返回子节点的可直接操作的集合并提供const重载。

### `easyvrui/control/tree_node_collection.h`

根节点与子节点集合使用`get_size/contains/get_index`查询，通过`operator[]`取得共享引用。`add/insert/assign`配置对象，`remove`按对象或位置移出，`clear`清空。节点按对象身份区分，每个节点同时归属一个集合。移动节点时先从原集合移出，再加入目标集合。

### `easyvrui/control/menu_container.h`

#### `menu_container`

声明：`class menu_container : public container_control`。

菜单容器的共同基类，构造函数为protected。get_control_list()返回普通control_collection，元素须为menuitem，名称在本层唯一。get_menubar()找到所属菜单栏；on_control_added/on_control_removed与菜单专有on_item_added/on_item_removed均可订阅。

|声明|用途与调用语义|
|---|---|
|`event_container<menu_item_event_args_t> on_item_added`|菜单项加入集合时触发，包含项目ID和实际索引。|
|`event_container<menu_item_event_args_t> on_item_removed`|菜单项移出集合时触发，包含项目ID和移除前的索引。|
|`virtual menubar *get_menubar() const`|返回所属menubar，尚未关联菜单栏时返回nullptr。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`menu_container(const std::u32string &name, const std::u32string &type)`|构造实例；参数和约束见本类型说明。|
|`void validate_control(const control &child) const override`|在插入前检查元素是否满足该容器约束，失败时抛出异常。|
|`void notify_control_added(control &child, size_t index) override`|插入后的容器通知，index是元素的真实集合索引。|
|`void notify_control_removed(control &child, size_t index) override`|移除后的容器通知，index是移除前的真实集合索引。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|为元素提供容器管理的矩形；nullopt表示沿用其自身矩形。|
|`std::vector<control *> get_active_control_list() const override`|返回当前参与显示和交互的直接元素。|
|`bool is_control_active(const control &item) const override`|判断指定元素是否参与当前显示和交互。|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|
|`void render_overlay(render_context &context) const override`|派生绘制入口；使用context绘制浮层。|

窗口菜单属于真实control_list。set_menu会完成添加；直接从control_list添加menubar也会同步get_menu。移除或clear同步解除关联，on_control_added/on_control_removed中的index就是该元素的真实集合索引。每个窗口同时关联一个menubar，新菜单可以使用被替换菜单的同名name。

```cpp
auto menubar_main = make_shared<easyvrui::menubar>(U"menubar_main");
auto menuitem_file = make_shared<easyvrui::menuitem>(U"menuitem_file");
menuitem_file->set_text(U"文件(&F)");
auto menuitem_open = make_shared<easyvrui::menuitem>(U"menuitem_open");
menuitem_open->set_text(U"打开(&O)");
menuitem_open->set_shortcut(U"Ctrl+O");
menuitem_file->get_control_list().add(menuitem_open);
menubar_main->get_control_list().add(menuitem_file);
window_main->set_menu(menubar_main);
```

### `easyvrui/control/menuitem.h`

#### `menuitem`

声明：`class menuitem : public menu_container`。

菜单项与子菜单容器。默认text/shortcut为空，icon为空，checkable/checked/separator均为false。子项通过get_control_list().add()加入，可按层级继续嵌套。separator=true绘制分隔线；文本中的&A或(&A)指定助记键。shortcut保存Ctrl+C等组合键文字；可选中项执行时触发继承的on_click。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_text_changed`|文本变化时触发。|
|`event_container<event_args_t> on_icon_changed`|图标变化时触发。|
|`event_container<event_args_t> on_shortcut_changed`|快捷键变化时触发。|
|`event_container<event_args_t> on_checkable_changed`|可勾选设置变化时触发。|
|`event_container<event_args_t> on_checked_changed`|勾选状态变化时触发。|
|`event_container<event_args_t> on_separator_changed`|分隔线设置变化时触发。|
|`event_container<event_args_t> on_opening`|准备展开子菜单时触发。|
|`event_container<event_args_t> on_closed`|子菜单收起时触发。|
|`explicit menuitem(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`virtual const std::u32string &get_text() const`|读取显示文字。|
|`virtual void set_text(const std::u32string &value)`|设置显示文字。|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|读取可选图像资源的共享引用，nullptr表示清除。|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|设置可选图像资源的共享引用，nullptr表示清除。|
|`virtual const std::u32string &get_shortcut() const`|读取菜单快捷键组合文字。|
|`virtual void set_shortcut(const std::u32string &value)`|设置菜单快捷键组合文字。|
|`virtual bool get_checkable() const`|读取是否允许勾选。|
|`virtual void set_checkable(bool value)`|设置是否允许勾选。|
|`virtual bool get_checked() const`|读取当前勾选状态。|
|`virtual void set_checked(bool value)`|设置当前勾选状态。|
|`virtual bool get_separator() const`|读取是否作为分隔线显示。|
|`virtual void set_separator(bool value)`|设置是否作为分隔线显示。|

### `easyvrui/control/menubar.h`

#### `menubar`

声明：`class menubar : public menu_container`。

菜单栏，默认font为font_t{}、row_height=32。主菜单及各层子菜单均通过get_control_list()维护。open/close管理菜单交互，重复点击展开的主菜单会收起；激光展开时初始无子项高亮，指向具体项后高亮。窗口通过set_menu关联菜单，也可将menubar作为实际元素加入窗口control_list。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_font_changed`|字体变化时触发。|
|`event_container<event_args_t> on_row_height_changed`|行高变化时触发。|
|`event_container<event_args_t> on_opening`|准备展开菜单栏时触发。|
|`event_container<event_args_t> on_closed`|菜单栏收起时触发。|
|`explicit menubar(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`bool is_focusable() const override`|查询该控件是否具有焦点能力；实际焦点还受visible、enabled和模态关系限制。|
|`virtual const font_t &get_font() const`|读取菜单字体，默认font_t{}。|
|`virtual void set_font(const font_t &value)`|设置菜单字体，字体名称非空、字号为正。|
|`virtual uint64_t get_row_height() const`|读取逻辑行高。|
|`virtual void set_row_height(uint64_t value)`|设置逻辑行高。|
|`virtual bool get_is_open() const`|查询当前是否处于菜单交互模式。|
|`virtual bool get_is_submenu_open(const menuitem &item) const`|查询指定菜单项的下一层弹出列表是否展开。|
|`virtual void open()`|进入菜单交互模式。|
|`virtual void close(bool restore_focus = true)`|收起全部子菜单；restore_focus默认true，用于恢复进入菜单前的焦点。|
|`void set_visible(bool value) override`|设置可见状态；隐藏时清理本控件正在进行的交互。|
|`void set_enabled(bool value) override`|设置可操作状态；禁用时清理正在进行的交互。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|
|`void render_overlay(render_context &context) const override`|派生绘制入口；使用context绘制浮层。|

### `easyvrui/control/toolbar.h`

#### `toolbar`

声明：`class toolbar : public container_control`。

图标工具栏。tool_size默认40且须大于0，spacing默认6.0且须有限非负。通过`get_button_list()`配置按钮、图标、提示和分隔线。按钮格按顺序横排，栏本身提供背景。超出可用区域的完整按钮格退出绘制和命中。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_spacing_changed`|工具格间距变化时触发。|
|`event_container<event_args_t> on_tool_size_changed`|工具格边长变化时触发。|
|`toolbar_button_collection &get_button_list()`及const重载|访问按钮及分隔线集合。|
|`explicit toolbar(const u32string &name)`|构造实例；参数和约束见本类型说明。|
|`void dispose() override`|清空button_list并释放该工具栏。|
|`virtual size_t get_tool_size() const`|读取工具按钮的正整数格边长。|
|`virtual void set_tool_size(size_t value)`|设置工具按钮的正整数格边长。|
|`virtual double get_spacing() const`|读取工具格间的有限非负逻辑间距。|
|`virtual void set_spacing(double value)`|设置工具格间的有限非负逻辑间距。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|派生绘制入口；使用context绘制正文。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|按工具格大小、间距及当前次序安排按钮显示矩形。|
|`bool is_control_active(const control &item) const override`|判断指定元素是否参与当前显示和交互。|
|`std::vector<control *> get_active_control_list() const override`|返回当前参与显示和交互的直接元素。|

应用通过`get_button_list()`配置按钮与分隔线：

```cpp
auto toolbar_main = make_shared<easyvrui::toolbar>(U"toolbar_main");
auto &button_save = toolbar_main->get_button_list().add(U"save");
button_save.set_tooltip_text(U"保存");
auto &separator_main = toolbar_main->get_button_list().add(U"separator");
separator_main.set_separator(true);
window_main->get_control_list().add(toolbar_main);
```

### `easyvrui/control/toolbar_button.h`

#### `toolbar_button`

声明：`class toolbar_button : public button`。

工具栏按钮继承`button`，构造后名称只读。icon默认空，separator=false，enabled=true，tooltip_text为空。图标保持比例，指向时显示提示；separator=true显示窄分隔线。加入toolbar.get_button_list()后get_parent返回所属toolbar。普通按钮接收on_click。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_click`|执行工具栏按钮操作时触发。|
|`event_container<event_args_t> on_icon_changed`|图标变化时触发。|
|`explicit toolbar_button(const std::u32string &name)`|构造实例；参数和约束见本类型说明。|
|`control_base *get_parent() const override`|返回所属toolbar；未加入任何工具栏时返回nullptr。|
|`void dispose() override`|从所属按钮集合移除并释放该按钮。|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|读取可选图像资源的共享引用，nullptr表示清除。|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|设置可选图像资源的共享引用，nullptr表示清除。|
|`virtual bool get_separator() const`|读取是否作为分隔线显示。|
|`virtual void set_separator(bool value)`|设置是否作为分隔线显示。|
|`virtual bool get_enabled() const`|读取是否可操作。|
|`virtual void set_enabled(bool value)`|设置是否可操作。|

### `easyvrui/control/toolbar_button_collection.h`

#### `toolbar_button_collection`

声明：`class toolbar_button_collection`。

属于toolbar的按钮容器，构造函数为private，由toolbar.get_button_list()提供。按索引或名称查询，名称在栏内唯一。add/insert既可接受shared_ptr<toolbar_button>，也可根据name创建并返回按钮引用。insert越过末尾时追加；remove返回shared_ptr<toolbar_button>；get_item_list返回指针列表的副本。

|声明|用途与调用语义|
|---|---|
|`toolbar_button_collection(const toolbar_button_collection &) = delete`|禁止复制构造。|
|`~toolbar_button_collection()`|析构实例，释放该对象持有的资源和引用。|
|`toolbar_button_collection &operator=(const toolbar_button_collection &) = delete`|禁止此复制或赋值操作。|
|`size_t get_size() const`|返回按钮及分隔线的总数量。|
|`bool is_empty() const`|查询集合是否为空。|
|`bool contains(const toolbar_button &item) const`|查询指定实例或名称是否属于本集合。|
|`bool contains(const std::u32string &name) const`|查询指定实例或名称是否属于本集合。|
|`toolbar_button &get_item(size_t index) const`|按索引或名称取得toolbar_button引用；缺失时抛出异常。|
|`toolbar_button &get_item(const std::u32string &name) const`|按索引或名称取得toolbar_button引用；缺失时抛出异常。|
|`size_t get_index(const toolbar_button &item) const`|取得按钮在集合中的0起始位置；未加入时抛出异常。|
|`std::vector<toolbar_button *> get_item_list() const`|返回按显示顺序排列的toolbar_button指针列表副本。|
|`void insert(size_t index, std::shared_ptr<toolbar_button> item)`|在index插入共享按钮，或根据name创建新按钮；越过末尾时追加。|
|`toolbar_button &insert(size_t index, const std::u32string &name)`|在index插入共享按钮，或根据name创建新按钮；越过末尾时追加。|
|`void add(std::shared_ptr<toolbar_button> item)`|追加共享按钮，或根据name创建并返回新按钮引用。|
|`toolbar_button &add(const std::u32string &name)`|追加共享按钮，或根据name创建并返回新按钮引用。|
|`std::shared_ptr<toolbar_button> remove(size_t index)`|移除并返回对应按钮的shared_ptr；可重新加入另一工具栏。|
|`std::shared_ptr<toolbar_button> remove(toolbar_button &item)`|移除并返回对应按钮的shared_ptr；可重新加入另一工具栏。|
|`std::shared_ptr<toolbar_button> remove(const std::u32string &name)`|移除并返回对应按钮的shared_ptr；可重新加入另一工具栏。|
|`void clear()`|移除全部按钮和分隔线，解除所属关系。|
|`toolbar_button &operator[](size_t index) const`|按索引或名称取得按钮引用。|
|`toolbar_button &operator[](const std::u32string &name) const`|按索引或名称取得按钮引用。|

### `easyvrui/control/tabpage.h`

页签内容容器。

#### `tabpage`

声明：`class tabpage : public panel`。

`tabpage`通过继承的控件集合容纳页面内容。页签标题由`tabpage`自身保存，页面的有效显示区域由所属`tabcontrol`管理。

继承`panel`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

|声明|用途与调用语义|
|---|---|
|`explicit tabpage(const u32string &name)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`~tabpage() override`|析构对象，结束其资源或引用的生命周期。|
|`virtual const u32string &get_text() const`|读取页签标题，默认为空。|
|`virtual void set_text(const u32string &value)`|修改标题并刷新所属`tabcontrol`的页签。|
|`event_container<event_args_t> on_text_changed`|页签标题变化时触发。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void render(render_context &context) const override`|使用context绘制控件正文。派生类可重载以实现自定义外观。|

### `easyvrui/control/tabpage_collection.h`

支持按位置或名称查找的页面集合。

#### `tabpage_collection`

声明：`class tabpage_collection : public control_collection`。

页面集合的索引、名称唯一性和生命周期规则与`control_collection`一致。`get_page()`和`operator[]`返回页面引用。`insert()`越过末尾时追加，移除页面时自动调整当前选择。

|声明|用途与调用语义|
|---|---|
|`explicit tabpage_collection(tabcontrol &owner)`|构造本类型实例；参数含义见本类型说明及签名。|
|`~tabpage_collection() override`|析构对象，结束其资源或引用的生命周期。|
|`tabpage &get_page(size_t index) const`|按index或name返回页面引用；不存在时抛出异常。|
|`tabpage &get_page(const u32string &name) const`|按index或name返回页面引用；不存在时抛出异常。|
|`void insert(size_t index, control &page) override`|在index位置插入；index不小于当前数量时追加。具体元素类型、所有权和重名约束见所属容器说明。|
|`void insert(size_t index, std::shared_ptr<control> page) override`|在index位置插入；index不小于当前数量时追加。具体元素类型、所有权和重名约束见所属容器说明。|
|`using control_collection::add`|追加项目；对象引用方式由调用方保证存活，shared_ptr方式由容器保留共享所有权。|
|`using control_collection::remove`|移除页面并返回`shared_ptr<control>`，可直接加入其它合适的集合。|
|`std::shared_ptr<control> remove(size_t index) override`|移除页面并返回`shared_ptr<control>`，可直接加入其它合适的集合。|
|`void clear() override`|移除全部页面。|
|`tabpage &operator[](size_t index) const`|按0起始位置或名称取得对象引用，行为与get_control/get_page一致。|
|`tabpage &operator[](const u32string &name) const`|按0起始位置或名称取得对象引用，行为与get_control/get_page一致。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`void notify_control_added(control &item, size_t index) override`|页面加入后同步页面选择和on_page_added事件。|
|`void notify_control_removed(control &item, size_t index, bool clearing) override`|页面移除后触发`on_page_removed`。|

`page_list`继承`control_collection`，沿用其页面存储、名称索引和所有权规则。通过`tabpage::set_text()`设置标题，标题随页面保留。

```cpp
auto tabcontrol_main = make_shared<easyvrui::tabcontrol>(U"tabcontrol_main");
auto tabpage_general = make_shared<easyvrui::tabpage>(U"tabpage_general");
auto textbox_value = make_shared<easyvrui::textbox>(U"textbox_value");
textbox_value->set_text(U"配置");
tabpage_general->get_control_list().add(textbox_value);
tabpage_general->set_text(U"常规");
tabcontrol_main->get_page_list().add(tabpage_general);
window_main->get_control_list().add(tabcontrol_main);
```

### `easyvrui/control/tabcontrol.h`

页签选择、标题外观和页面布局。

#### `tab_position_t`

声明：`enum class tab_position_t`。

|声明|用途与调用语义|
|---|---|
|`top`|页签在上方。|
|`bottom`|页签在下方。|
|`left`|页签在左侧。|
|`right`|页签在右侧。|

#### `tabcontrol`

声明：`class tabcontrol : public container_control`。

继承container_control。page_list管理页面及标题。默认页签在top，tab_size=36，未添加页面时selected_index=-1；添加首个页面后选择有效页面。只显示当前页面内容，悬停强调作用于页签选择区域。tab_font默认Segoe UI、18。窗口正文和tabpage保持各自背景。

应用通过`get_page_list()`管理页面。其余public成员按继承规则使用。

|声明|用途与调用语义|
|---|---|
|`tabpage_collection &get_page_list()`及const重载|访问页签集合，元素为`tabpage`。|
|`event_container<event_args_t> on_selected_index_changed`|选中索引变化时触发。|
|`event_container<event_args_t> on_tab_position_changed`|页签位置变化时触发。|
|`event_container<event_args_t> on_tab_size_changed`|页签栏厚度变化时触发。|
|`event_container<event_args_t> on_tab_font_changed`|页签字体变化时触发。|
|`event_container<event_args_t> on_tab_foreground_color_changed`|普通页签前景色变化时触发。|
|`event_container<event_args_t> on_tab_background_color_changed`|普通页签背景色变化时触发。|
|`event_container<event_args_t> on_selected_tab_foreground_color_changed`|选中页签前景色变化时触发。|
|`event_container<event_args_t> on_selected_tab_background_color_changed`|选中页签背景色变化时触发。|
|`event_container<tabpage_event_args_t> on_page_added`|添加页面时触发，包含页签`page`和索引`index`。|
|`event_container<tabpage_event_args_t> on_page_removed`|移除页面时触发，包含页签`page`和索引`index`。|
|`event_container<tabpage_event_args_t> on_page_text_changed`|页签标题变化时触发，通过`event.page->get_text()`读取页签标题。|
|`event_container<tabpage_event_args_t> on_page_close`|点击关闭图标或在页签聚焦时按Delete触发。应用确认保存后从`page_list`移除`event.page`。|
|`event_container<event_args_t> on_page_close_button_visible_changed`|页签关闭按钮显示设置变化时触发。|
|`event_container<event_args_t> on_selection_changed`|选择状态变化时触发；文本编辑器使用start/length，项目与页签使用selected。|
|`explicit tabcontrol(const u32string &name)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`bool is_focusable() const override`|查询该控件是否具有焦点能力；实际焦点还受visible、enabled和模态关系限制。|
|`virtual int64_t get_selected_index() const`|读取当前选中索引，-1表示未选择。|
|`virtual void set_selected_index(int64_t value)`|设置当前选中索引，-1表示未选择。|
|`virtual tabpage *get_selected_page() const`|读取当前tabpage指针；未选择时为nullptr。|
|`virtual tab_position_t get_tab_position() const`|读取页签位于top、bottom、left或right。|
|`virtual void set_tab_position(tab_position_t value)`|设置页签位于top、bottom、left或right。|
|`virtual uint64_t get_tab_size() const`|读取页签条厚度，必须大于0。|
|`virtual void set_tab_size(uint64_t value)`|设置页签条厚度，必须大于0。|
|`virtual bool get_page_close_button_visible() const`|读取页签关闭按钮是否显示，默认false。|
|`virtual void set_page_close_button_visible(bool value)`|设置页签关闭按钮；点击只发出on_page_close请求，由应用决定是否移除页面。|
|`virtual const font_t &get_tab_font() const`|读取页签字体。|
|`virtual void set_tab_font(const font_t &value)`|设置页签字体。|
|`virtual uint32_t get_tab_foreground_color() const`|读取未选中页签前景色。|
|`virtual void set_tab_foreground_color(uint32_t value)`|设置未选中页签前景色。|
|`virtual uint32_t get_tab_background_color() const`|读取未选中页签背景色。|
|`virtual void set_tab_background_color(uint32_t value)`|设置未选中页签背景色。|
|`virtual uint32_t get_selected_tab_foreground_color() const`|读取选中页签前景色。|
|`virtual void set_selected_tab_foreground_color(uint32_t value)`|设置选中页签前景色。|
|`virtual uint32_t get_selected_tab_background_color() const`|读取选中页签背景色。|
|`virtual void set_selected_tab_background_color(uint32_t value)`|设置选中页签背景色。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`tabpage_collection &get_control_list() override`|受保护的协变覆盖，返回page_list；应用通过`get_page_list()`访问。|
|`const tabpage_collection &get_control_list() const override`|受保护的协变覆盖，返回page_list；应用通过`get_page_list()`访问。|
|`void validate_control(const control &item) const override`|验证元素为tabpage；其它control类型不能加入页面集合。|
|`vector<control *> get_active_control_list() const override`|返回当前选中的页面，未选中时返回空列表。|
|`bool is_control_active(const control &item) const override`|判断元素是否为当前选中的页面。|
|`virtual void notify_selected_index(int64_t previous)`|当前页面索引变化的派生通知。|
|`void refresh_layout() override`|刷新控件布局，派生类覆盖时保留必要的基类处理。|
|`size_t get_focus_target_count() const override`|返回内部可聚焦区域数量，供复合控件焦点导航使用。|
|`virtual size_t get_focus_target_at(double left, double top) const`|根据控件本地坐标取得内部焦点区域索引。|
|`optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|为元素提供容器管理的矩形；nullopt表示沿用其自身矩形。|
|`optional<int64_t> get_selection_index_at(double left, double top, const rectangle_t &rectangle) const override`|查询给定逻辑坐标对应的可选子项索引；未命中时为nullopt。|
|`void render(render_context &context) const override`|使用context绘制控件正文。派生类可重载以实现自定义外观。|

### `easyvrui/control/window.h`

VR顶层容器、空间参考、显示、模态及窗口交互。

#### `startup_position_t`

声明：`enum class startup_position_t`，成员为`none`和`center`。

`none`使用配置的初始位置和姿态；`center`首次显示时优先与来源窗口平面平行、中心对齐，并沿头显所在一侧的法线前移。模态窗口严格使用直接父窗口。SDK提供的同session来源优先；来源省略时，Engine采用当前选中的可见普通表面，可跨session用于Desktop启动其它App。没有有效来源时按当前头显姿态居中，初始距离取`max(1.2, max(physical_width, physical_height))`米。Engine结合各会话窗口安排初始深度，并在present完成回调中同步最终position/rotation。启动定位只应用一次，随后隐藏、显示及来源窗口移动均保留该窗口已确定的位姿；辅助输入窗口由Engine关联输入区定位。

在`startup_position_t::none`且position和rotation均为零时，world窗口左上角使用初始正前方参考中心。默认center遵循上述来源优先与头显回退规则。

#### `window`

声明：`class window : public container_control`。

继承container_control。默认rect={0,0,640,360}、visible=false、title=name、标题字体Segoe UI/20、physical_scale=1.0倍、position和rotation全0、reference_object为world；标题栏、关闭按钮、移动和缩放均开启，跟踪菜单默认包含world/body/left/right/head。顶层窗口的空间位置由`position`和参考对象确定。窗口展开宽度为`rect.width * physical_scale / 1000`米，高度为`rect.height * physical_scale / 1000`米。可移动且尺寸足够时，正文外侧预留控制环；派生窗口可通过受保护的get_content_top()安排正文。普通单手侧握执行远距离移动与旋转，双手分别抓住两个控制环块执行受约束旋转。通过`get_closed()`查询窗口是否已关闭。

首次显示仅在未显式调用`set_physical_scale()`时继承SDK确定的同会话来源窗口缩放。显式设置优先，包括1.0。模态窗口采用world参考对象，可独立拖动。

`show_dialog(owner_window)`要求所有者是同一UI运行时内可交互的其他窗口，对话框须隐藏、尚未关闭且未进入模态。调用期间直接所有者暂时失去交互资格。可在按钮或菜单事件中同步打开对话框，并以当前可交互对话框作为下一层的所有者。渲染提交期间调用会报错。详见[会话与嵌套模态循环](/advanced/04_session_and_context)。

进入模态时将结果重置为`dialog_result_t::none`。设置非`none`的结果会请求关闭。处理器取消关闭时，对话框保持活动，结果恢复到设置前的值。结果仍为`none`时通过标题栏关闭按钮或`close()`成功关闭，返回`dialog_result_t::cancel`。调用方可保留窗口对象，在返回后读取控件值。

继承`container_control`的全部public属性访问、方法和事件；下表列出本类型自身声明或覆盖的成员。

曲率k为有限非负数，单位m⁻¹。k=0表示平面，非零时总弧度θ=k×get_physical_width()，属性和Engine校验均要求θ<2π。get_physical_width()是展开弧长，按rect.width×physical_scale/1000计算。窗口左下角交互柄和对应摇杆的安全调节上限为160°；该上限属于UI操作规则，set_curvature()仍使用前述合法域。改变rect或physical_scale也须保持曲率合法。

左下角曲率柄与右下角缩放柄使用trigger，按住期间保持选中并锁定激光末端；曲率使用摇杆左右调整，缩放使用上下调整。左下角双击恢复平面。curvature_adjustable和resizable分别控制两种调节入口。

|声明|用途与调用语义|
|---|---|
|`event_container<event_args_t> on_menu_changed`|菜单栏关联变化时触发。|
|`event_container<event_args_t> on_title_changed`|标题变化时触发。|
|`event_container<event_args_t> on_title_foreground_color_changed`|标题文字前景色变化时触发。|
|`event_container<event_args_t> on_title_background_color_changed`|标题栏背景色变化时触发。|
|`event_container<event_args_t> on_title_font_changed`|标题字体变化时触发。|
|`event_container<event_args_t> on_icon_changed`|标题图标对象改变或清空时触发。|
|`event_container<event_args_t> on_rotation_changed`|窗口旋转角度变化时触发。|
|`event_container<event_args_t> on_curvature_changed`|曲率变化时触发。|
|`event_container<event_args_t> on_startup_position_changed`|启动定位方式改变时触发。|
|`event_container<event_args_t> on_curvature_adjustable_changed`|曲率交互调整开关改变时触发。|
|`event_container<event_args_t> on_reference_object_changed`|空间参考对象变化时触发。|
|`event_container<event_args_t> on_show_title_bar_changed`|标题栏显示设置变化时触发。|
|`event_container<event_args_t> on_tracking_mode_set_changed`|跟踪模式选项变化时触发。|
|`event_container<event_args_t> on_show_close_button_changed`|关闭按钮显示设置变化时触发。|
|`event_container<event_args_t> on_movable_changed`|移动开关变化时触发。|
|`event_container<event_args_t> on_resizable_changed`|缩放开关变化时触发。|
|`event_container<event_args_t> on_load`|窗口首次显示加载时触发一次。|
|`event_container<event_args_t> on_shown`|窗口显示时触发。|
|`event_container<event_args_t> on_hidden`|窗口隐藏时触发。|
|`event_container<cancel_event_args_t> on_closing`|普通关闭前触发。`event.cancel = true`可中止此次关闭。|
|`event_container<event_args_t> on_closed`|窗口关闭完成时触发。|
|`event_container<render_error_event_args_t> on_render_failed`|窗口提交或渲染失败时触发，附带错误数据。|
|`event_container<event_args_t> on_tracking_lost`|窗口空间参考跟踪丢失时触发。|
|`event_container<event_args_t> on_tracking_restored`|窗口空间参考跟踪恢复时触发。|
|`event_container<event_args_t> on_activated`|窗口成为当前活动窗口时触发。|
|`event_container<event_args_t> on_deactivated`|窗口失去活动状态时触发。|
|`event_container<event_args_t> on_move_start`|窗口交互移动或旋转开始时触发。|
|`event_container<interaction_end_event_args_t> on_move_end`|窗口交互移动或旋转结束时触发，cancelled说明结束原因。|
|`event_container<event_args_t> on_resize_start`|窗口交互缩放开始时触发。|
|`event_container<interaction_end_event_args_t> on_resize_end`|窗口交互缩放结束时触发。|
|`event_container<event_args_t> on_curvature_adjust_start`|开始调整窗口曲率时触发。|
|`event_container<interaction_end_event_args_t> on_curvature_adjust_end`|结束窗口曲率调整时触发。|
|`explicit window(const u32string &name)`|按不可变Unicode名称name创建实例；其他属性使用各自setter配置。|
|`virtual const std::shared_ptr<menubar> &get_menu() const`|返回当前菜单的`const shared_ptr<menubar> &`；空引用表示未配置菜单。|
|`virtual void set_menu(std::shared_ptr<menubar> value)`|设置或清除固有菜单；菜单是control_list中的真实元素。替换先移除原菜单，再将新菜单追加到集合，支持使用原菜单同名的新实例。|
|`void set_visible(bool value) override`|设置可见状态。|
|`virtual const u32string &get_title() const`|读取窗口标题文字，默认等于name。|
|`virtual void set_title(const u32string &value)`|设置窗口标题文字，默认等于name。|
|`virtual uint32_t get_title_foreground_color() const`|读取窗口标题文字前景色。|
|`virtual void set_title_foreground_color(uint32_t value)`|设置窗口标题文字前景色。|
|`virtual uint32_t get_title_background_color() const`|读取窗口标题栏背景色。|
|`virtual void set_title_background_color(uint32_t value)`|设置窗口标题栏背景色。|
|`virtual const font_t &get_title_font() const`|读取窗口标题字体。|
|`virtual void set_title_font(const font_t &value)`|设置窗口标题字体。|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|读取标题栏左侧的图标对象，默认使用原生图标。|
|`static std::shared_ptr<const drawing_image> get_default_icon()`|读取原生默认图标；传给set_icon恢复默认值。|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|设置图标；图像等比缩放并垂直居中，为标题文字保留其后的区域；传入nullptr清空图标并恢复标题左侧布局。|
|`virtual double get_physical_scale() const`|读取缩放倍数，必须为有限正数。|
|`virtual void set_physical_scale(double value)`|设置有限正缩放倍数；新物理宽度仍须满足曲率合法域。|
|`virtual double get_curvature() const`|读取柱面曲率k，单位m⁻¹；0表示平面。|
|`virtual void set_curvature(double value)`|设置有限曲率k，要求k>=0且k×get_physical_width()<2π；160°仅为交互手柄的安全调节上限。|
|`virtual startup_position_t get_startup_position() const`|读取启动定位方式，默认center。|
|`virtual void set_startup_position(startup_position_t value)`|设置启动定位方式，接受none或center。|
|`virtual const vec3_t &get_position() const`|读取相对reference_object的位置偏移，单位米。|
|`virtual void set_position(const vec3_t &value)`|设置相对reference_object的位置偏移，单位米。|
|`virtual const vec3_t &get_rotation() const`|读取相对reference_object的XYZ欧拉旋转，单位度。|
|`virtual void set_rotation(const vec3_t &value)`|设置相对reference_object的XYZ欧拉旋转，单位度。|
|`virtual const reference_object_t &get_reference_object() const`|读取空间参考目标。|
|`virtual void set_reference_object(const reference_object_t &value)`|设置空间参考目标。|
|`virtual bool get_show_title_bar() const`|读取是否显示窗口标题栏。|
|`virtual void set_show_title_bar(bool value)`|设置是否显示窗口标题栏。|
|`virtual const std::set<reference_object_type_t> &get_tracking_mode_set() const`|读取标题栏跟踪菜单的模式集合；空集合隐藏切换按钮。|
|`virtual void set_tracking_mode_set(const std::set<reference_object_type_t> &value)`|设置标题栏跟踪菜单的模式集合；空集合隐藏切换按钮。|
|`virtual bool get_show_close_button() const`|读取是否显示标题栏关闭按钮。|
|`virtual void set_show_close_button(bool value)`|设置是否显示标题栏关闭按钮。|
|`virtual bool get_movable() const`|读取是否允许交互移动和控制环旋转。|
|`virtual void set_movable(bool value)`|设置是否允许交互移动和控制环旋转。|
|`virtual bool get_resizable() const`|读取是否允许交互改变逻辑尺寸。|
|`virtual void set_resizable(bool value)`|设置是否允许交互改变逻辑尺寸。|
|`virtual bool get_curvature_adjustable() const`|读取曲率交互开关，默认true。|
|`virtual void set_curvature_adjustable(bool value)`|设置左下角曲率按钮的显示与交互；关闭时立即取消当前曲率拖动和摇杆调整，重新开启后松开trigger再按可开始调整。|
|`virtual double get_physical_width() const`|返回展开宽度，单位米：rect.width×physical_scale/1000。|
|`virtual double get_physical_height() const`|返回高度，单位米：rect.height×physical_scale/1000。|
|`~window() override`|析构对象，结束其资源或引用的生命周期。|
|`virtual void show()`|显示窗口；首次显示触发load，显示状态变化触发shown。|
|`virtual void hide()`|隐藏窗口并释放相关捕获、焦点和输入界面；保留控件对象供再次显示。|
|`virtual bool close(bool force = false)`|请求关闭。成功时返回true。force=true时跳过关闭取消回调。|
|`virtual void activate()`|激活本对象所属窗口；窗口重载激活自身。|
|`virtual dialog_result_t show_dialog(window &owner_window)`|阻塞显示模态窗口，禁用直接所有者并继续分发UI事件。关闭后返回结果枚举，调用方仍可读取窗口属性。|
|`virtual bool get_loaded() const`|读取窗口是否完成首次加载。|
|`virtual bool get_closed() const`|读取窗口是否已关闭。|
|`virtual dialog_result_t get_dialog_result() const`|读取当前模态结果，进入模态时重置为none。|
|`virtual void set_dialog_result(dialog_result_t value)`|设置模态结果。模态期间，非`none`值请求关闭。关闭被取消时恢复原值。|
|`void set_rect(const rectangle_t &value) override`|设置逻辑矩形；宽高须为正，设置后的物理宽度仍须满足曲率合法域。|
|`virtual void set_size(uint64_t width, uint64_t height)`|设置窗口rect.width和rect.height，单位为逻辑单位且均须大于0。|
|`virtual void reparent(const reference_object_t &reference, bool keep_world = false)`|更换为world、body、head、left或right参考目标；传入keep_world=true时保持世界位姿。|
|`bool get_is_tracking_available(reference_object_type_t mode) const`|查询指定参考模式当前是否可以跟踪。|
|`virtual std::optional<pose_t> get_world_transform() const`|返回窗口中心的世界位姿；参考姿态不可用时为nullopt。position属性定义的锚点位于左上角，两者相差半宽和半高。|
|`virtual bool center_at_view(double distance)`|在视线前方指定米数处居中窗口。跟踪可用且定位成功时返回true。|
|`virtual bool get_auxiliary() const`|查询该窗口是否为关联输入区的辅助表面。|
|`virtual void set_auxiliary(bool value)`|标记应用辅助输入表面；实际定位及缩放由Engine根据当前输入区维护。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`u32string title`|派生类可访问的窗口标题文字，默认等于name；常规赋值使用setter以产生变化通知。|
|`uint32_t title_foreground_color = render_style::SELECTED_TEXT_FOREGROUND_COLOR`|派生类可访问的窗口标题文字前景色；常规赋值使用setter以产生变化通知。|
|`uint32_t title_background_color = render_style::WINDOW_TITLE_BACKGROUND_COLOR`|派生类可访问的窗口标题栏背景色；常规赋值使用setter以产生变化通知。|
|`font_t title_font`|派生类可访问的窗口标题字体；常规赋值使用setter以产生变化通知。|
|`std::shared_ptr<const drawing_image> icon`|标题图标，默认使用原生图标；派生类通过set_icon赋值以更新绘制并触发事件。|
|`double physical_scale = render_style::DEFAULT_PHYSICAL_SCALE`|派生类可访问的缩放倍数；必须为有限正数；常规赋值使用setter以产生变化通知。|
|`double curvature = 0.0`|柱面曲率，默认0.0，表示平面。|
|`startup_position_t startup_position = startup_position_t::center`|首次显示的位置策略，默认center。|
|`vec3_t position`|派生类可访问的相对reference_object的位置偏移，单位米；常规赋值使用setter以产生变化通知。|
|`vec3_t rotation`|派生类可访问的相对reference_object的XYZ欧拉旋转，单位度；常规赋值使用setter以产生变化通知。|
|`reference_object_t reference_object`|派生类可访问的空间参考目标；常规赋值使用setter以产生变化通知。|
|`bool show_title_bar = true`|派生类可访问的是否显示窗口标题栏；常规赋值使用setter以产生变化通知。|
|`std::set<reference_object_type_t> tracking_mode_set{reference_object_type_t::world, reference_object_type_t::body, reference_object_type_t::left, reference_object_type_t::right, reference_object_type_t::head}`|派生类可访问的标题栏跟踪菜单的模式集合；空集合隐藏切换按钮；常规赋值使用setter以产生变化通知。|
|`bool show_close_button = true`|派生类可访问的是否显示标题栏关闭按钮；常规赋值使用setter以产生变化通知。|
|`bool movable = true`|派生类可访问的是否允许交互移动和控制环旋转；常规赋值使用setter以产生变化通知。|
|`bool resizable = true`|派生类可访问的是否允许交互改变逻辑尺寸；常规赋值使用setter以产生变化通知。|
|`bool curvature_adjustable = true`|曲率交互开关；派生类通过set_curvature_adjustable赋值以同步取消捕获并触发事件。|
|`void refresh_layout() override`|刷新控件布局，派生类覆盖时保留必要的基类处理。|
|`void validate_control(const control &item) const override`|校验窗口可接收的元素；同一窗口同时只关联一个menubar。|
|`void notify_control_added(control &item, size_t index) override`|元素实际加入后同步menu关联，并按真实index发出容器事件。|
|`void notify_control_removed(control &item, size_t index) override`|元素实际移除后同步menu关联，并按原真实index发出容器事件。|
|`void notify_control_list_cleared() override`|集合清空后同步窗口的menu关联。|
|`virtual render_rectangle_t get_menu_rectangle() const`|读取当前窗口内菜单栏的实际逻辑矩形。|
|`virtual void render_window_frame(render_context &context, bool spatial_handle) const`|绘制窗口边框、标题及按spatial_handle控制的空间操作柄。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|为菜单安排标题栏下方的矩形；普通控件沿用自身矩形。|
|`double get_content_top() const override`|读取正文起始的逻辑top偏移。|
|`void render(render_context &context) const override`|使用context绘制控件正文。派生类可重载以实现自定义外观。|

参考目标为world、body、head、left、right五种；tracking_mode_set配置标题栏可选目标。world/body下可执行普通窗口抓取。派生窗口布局可通过受保护的get_content_top()适配标题栏、菜单和控制环。

### `easyvrui/dialog/dialog_result.h`

`dialog_result_t`是模态窗口和标准消息框共用的结果枚举。成员`none/ok/cancel/abort/retry/ignore/yes/no`依次对应`0`至`7`。

## 自定义绘图

### `easyvrui/render/render_context.h`

自定义控件使用的绘图和交互状态查询接口。

#### `render_rectangle_t`

声明：`struct render_rectangle_t`。

浮点逻辑矩形，left/top/width/height均为double，默认0。供绘图和裁剪使用。

|声明|用途与调用语义|
|---|---|
|`double left = 0.0`|矩形左边的横坐标。|
|`double top = 0.0`|矩形上边的纵坐标。|
|`double width = 0.0`|矩形宽度，单位为逻辑像素。|
|`double height = 0.0`|矩形高度，单位为逻辑像素。|

#### `render_context`

声明：`class render_context`。

自定义控件render/render_overlay收到的抽象绘图上下文。矩形、坐标、半径和线宽使用逻辑单位；颜色为0xRRGGBBAA。纯虚函数由具体上下文提供，普通控件直接调用。通过静态类型调用时，默认参数以该类型的声明为准。

|声明|用途与调用语义|
|---|---|
|`virtual ~render_context() = default`|析构对象，结束其资源或引用的生命周期。|
|`virtual render_rectangle_t get_rectangle(const control &item) const = 0`|取得控件在当前窗口中的逻辑绘制矩形。|
|`virtual render_rectangle_t get_popup_rectangle(const item_control &item) const = 0`|取得项目控件弹出区域矩形。|
|`virtual bool is_hovered(const control &item) const = 0`|查询激光是否悬停在控件或其指定矩形内。|
|`virtual bool is_hovered(const control &item, const render_rectangle_t &rectangle) const = 0`|查询激光是否悬停在控件或其指定矩形内。|
|`virtual bool is_focused(const control &item) const = 0`|查询控件的视觉焦点；输入排空等待期间可为false，此时逻辑焦点仍可能保留。|
|`virtual bool is_blinking() const = 0`|查询本帧插入点是否处于显示周期。|
|`virtual bool is_active(const window &item) const = 0`|查询窗口是否为当前激活窗口。|
|`virtual bool is_blocked(const window &item) const = 0`|查询窗口是否受模态关系阻挡。|
|`virtual bool is_close_button_hovered(const window &item) const = 0`|查询窗口关闭按钮是否处于悬停状态。|
|`virtual int64_t get_hovered_item(const item_control &item) const = 0`|取得激光指向项目的索引；未命中时为-1。|
|`virtual double measure(const u32string &text, const font_t &font) = 0`|测量Unicode文本在指定字体下的逻辑宽度。|
|`virtual void fill(const render_rectangle_t &rectangle, uint32_t color) = 0`|以color填充矩形；坐标为逻辑单位。|
|`virtual void outline(const render_rectangle_t &rectangle, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|绘制矩形轮廓，thickness为正线宽。|
|`virtual void draw_line(double x1, double y1, double x2, double y2, uint32_t color, double thickness = render_style::FOCUSED_OUTLINE_THICKNESS) = 0`|绘制(x1,y1)到(x2,y2)的线段，使用color和正线宽thickness。|
|`virtual void draw_text(const u32string &value, const font_t &font, const render_rectangle_t &rectangle, uint32_t color, bool center = false) = 0`|在给定矩形中绘制文本；center为true时居中，字体、字号和样式由对应参数指定。|
|`virtual void push_clip(const render_rectangle_t &rectangle) = 0`|压入矩形裁剪范围；后续绘图受当前裁剪范围约束。|
|`virtual void pop_clip() = 0`|弹出最近压入的裁剪范围；须与push_clip成对使用。|
|`virtual void render_control_list(const window &item) = 0`|按窗口当前集合顺序绘制控件。|
|`virtual void render_overlay_list(const window &item) = 0`|绘制窗口内控件浮层。|
|`virtual void fill_ellipse(double center_x, double center_y, double radius_x, double radius_y, uint32_t color) = 0`|填充以(center_x,center_y)为中心、半径为radius_x/radius_y的椭圆。|
|`virtual void outline_ellipse(double center_x, double center_y, double radius_x, double radius_y, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|绘制椭圆轮廓；半径与线宽均需满足绘图参数约束。|
|`virtual void fill_rounded_rectangle(const render_rectangle_t &rectangle, double radius_x, double radius_y, uint32_t color) = 0`|填充矩形，radius_x/radius_y指定圆角半径。|
|`virtual void outline_rounded_rectangle(const render_rectangle_t &rectangle, double radius_x, double radius_y, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|绘制圆角矩形轮廓。|
|`virtual void draw_image(const drawing_image &image, const render_rectangle_t &rectangle, double opacity = 1.0) = 0`|将RGBA图像缩放绘制到目标矩形，opacity范围为0至1。|
|`virtual void draw_screen(uint64_t screen_id, const render_rectangle_t &rectangle) = 0`|绘制screen_id指定的实时显示器画面。|
|`virtual void fill_path(const drawing_path &path, uint32_t color) = 0`|按路径的填充规则填充路径。|
|`virtual void outline_path(const drawing_path &path, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|按thickness绘制路径轮廓。|
|`virtual void render_control(const control &item)`|调用指定控件的受保护正文绘制入口，供自定义组合绘制使用。|
|`virtual void render_control_overlay(const control &item)`|调用指定控件的受保护浮层绘制入口。|
|`void fill_circle(double center_x, double center_y, double radius, uint32_t color)`|填充圆；radius为半径。|
|`void draw_circle(double center_x, double center_y, double radius, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS)`|绘制圆轮廓；radius为半径，thickness为线宽。|
|`static render_rectangle_t get_inset_rectangle(render_rectangle_t rectangle, double left_padding, double right_padding, double top_padding = 0.0, double bottom_padding = 0.0)`|按给定四边内边距或控件及左右边距返回内缩矩形。|
|`render_rectangle_t get_inset_rectangle(const control &item, double left_padding, double right_padding) const`|按给定四边内边距或控件及左右边距返回内缩矩形。|
|`void draw_control(const control &item, bool highlight = true)`|绘制控件背景和边框；highlight控制是否显示交互强调。|
|`uint32_t get_foreground(const text_control &item) const`|返回文字控件当前状态适用的前景色。|

### `drawing_image.h`

不可变的RGBA图像值。

#### `drawing_image`

声明：`class drawing_image`。

全局命名空间中的不可变图像。构造接收width、height和RGBA字节数组，每像素4字节，按行排列；字节数必须与宽高一致。通过getter读取各字段。

|声明|用途与调用语义|
|---|---|
|`drawing_image(uint64_t width, uint64_t height, std::vector<uint8_t> pixel_data)`|构造对象；参数、默认状态和约束见本类型说明。|
|`static std::shared_ptr<drawing_image> load_file(const std::filesystem::path &path)`|加载系统支持的图像文件，ICO选取最大图像帧。|
|`static std::shared_ptr<drawing_image> load_memory(std::span<const uint8_t> data)`|从完整编码图像字节加载。|
|`static std::shared_ptr<drawing_image> load_ico(std::span<const uint8_t> data)`|检查ICO文件头并从内存加载图标。|
|`std::vector<uint8_t> encode_ico() const`|无损编码PNG并封入单图ICO，保留RGBA像素；宽高各为1～256像素。|
|`uint64_t get_width() const`|读取图像像素宽度。|
|`uint64_t get_height() const`|读取图像像素高度。|
|`const std::vector<uint8_t> &get_pixel_data() const`|读取RGBA像素字节数组。|

### `drawing_path.h`

路径片段、填充规则和可链式构建的二维路径。

#### `drawing_path_operation_t`

声明：`enum class drawing_path_operation_t : uint8_t`。

|声明|用途与调用语义|
|---|---|
|`move = 0u`|移动到起点，value_list[0..1]为x/y。|
|`line = 1u`|直线到终点，value_list[0..1]为x/y。|
|`quadratic = 2u`|二次曲线，value_list[0..3]为控制点和终点。|
|`cubic = 3u`|三次曲线，value_list[0..5]为两个控制点和终点。|
|`arc = 4u`|椭圆弧，value_list[0..4]为终点x/y、半径x/y、旋转度数，另用clockwise/large_arc。|
|`close = 5u`|闭合当前子路径。|

#### `drawing_fill_rule_t`

声明：`enum class drawing_fill_rule_t : uint8_t`。

|声明|用途与调用语义|
|---|---|
|`even_odd = 0u`|奇偶填充规则。|
|`non_zero = 1u`|非零绕数填充规则。|

#### `drawing_path_segment_t`

声明：`struct drawing_path_segment_t`。

|声明|用途与调用语义|
|---|---|
|`drawing_path_operation_t operation = drawing_path_operation_t::move`|本路径片段的操作类型。|
|`std::array<double, 6u> value_list{}`|路径片段的坐标与参数数组，容量为6。|
|`bool clockwise = true`|圆弧是否顺时针。|
|`bool large_arc = false`|圆弧是否采用大于半圈的路径。|

value_list的实际使用位置由operation确定；move/line使用前2项，quadratic使用前4项，cubic使用6项，arc使用前5项。未使用项保持默认值即可。

#### `drawing_path`

声明：`class drawing_path`。

全局命名空间中的路径构建器。move_to/line_to/曲线/arc_to/close均返回drawing_path &，可链式调用。默认填充规则even_odd；clear清空片段。坐标需有限，半径非负，路径应从有效起点开始。

|声明|用途与调用语义|
|---|---|
|`drawing_path()`|构造本类型实例；参数含义见本类型说明及签名。|
|`const std::vector<drawing_path_segment_t> &get_segment_list() const`|读取路径片段只读列表。|
|`drawing_fill_rule_t get_fill_rule() const`|读取路径填充规则。|
|`void set_fill_rule(drawing_fill_rule_t value)`|设置路径填充规则。|
|`void clear()`|清空路径片段，保留当前填充规则。|
|`drawing_path &move_to(double x, double y)`|开始或移动到(x,y)的新路径起点，返回当前路径引用以链式调用。|
|`drawing_path &line_to(double x, double y)`|从当前点连接直线到(x,y)，返回当前路径引用。|
|`drawing_path &quadratic_to(double control_x, double control_y, double end_x, double end_y)`|追加二次贝塞尔曲线，control为控制点、end为终点，返回当前路径引用。|
|`drawing_path &cubic_to(double control1_x, double control1_y, double control2_x, double control2_y, double end_x, double end_y)`|追加三次贝塞尔曲线，control1/control2为控制点、end为终点，返回当前路径引用。|
|`drawing_path &arc_to(double end_x, double end_y, double radius_x, double radius_y, double rotation_degree = 0.0, bool clockwise = true, bool large_arc = false)`|追加到(end_x,end_y)的椭圆弧；radius为半径，rotation_degree为角度，clockwise和large_arc选择弧方向与大小。|
|`drawing_path &close()`|将当前子路径闭合，返回当前drawing_path引用。|

### `easyvrui/render/render_style.h`

默认颜色、尺寸、线宽和布局常量。

#### `render_style`

声明：`class render_style`。

|声明|用途与调用语义|
|---|---|
|`static constexpr uint32_t CONTROL_BACKGROUND_COLOR = 0x162738ffu`|普通控件默认背景色。|
|`static constexpr uint32_t TEXT_FOREGROUND_COLOR = 0xd1def0ffu`|默认文字前景色。|
|`static constexpr uint32_t SELECTED_TEXT_FOREGROUND_COLOR = 0xffffffffu`|选中内容文字色。|
|`static constexpr uint32_t WINDOW_BACKGROUND_COLOR = 0x0d1624ffu`|窗口默认背景色。|
|`static constexpr uint32_t WINDOW_TITLE_BACKGROUND_COLOR = 0x244565ffu`|窗口标题栏默认背景色。|
|`static constexpr uint32_t HOVER_OVERLAY_COLOR = 0x469eff55u`|悬停叠加色。|
|`static constexpr uint32_t FOCUSED_OUTLINE_COLOR = 0x7bc9ffffu`|焦点边框色。|
|`static constexpr uint32_t HOVERED_OUTLINE_COLOR = 0x63b4ffffu`|悬停边框色。|
|`static constexpr uint32_t NORMAL_OUTLINE_COLOR = 0x45617dffu`|普通边框色。|
|`static constexpr uint32_t SELECTED_ITEM_BACKGROUND_COLOR = 0x316b9affu`|选中项目背景色。|
|`static constexpr uint32_t HOVERED_ITEM_BACKGROUND_COLOR = 0x5eacff66u`|悬停项目背景色。|
|`static constexpr uint32_t ITEM_LIST_OUTLINE_COLOR = 0x567a9cffu`|项目列表轮廓色。|
|`static constexpr uint32_t TEXT_SELECTION_BACKGROUND_COLOR = 0x3679bcddu`|文本选区背景色。|
|`static constexpr uint32_t CLOSE_BUTTON_HOVER_COLOR = 0xc84e64ffu`|关闭按钮悬停色。|
|`static constexpr uint32_t WINDOW_OUTLINE_COLOR = 0x5f87a9ffu`|窗口轮廓色。|
|`static constexpr uint32_t BLOCKED_WINDOW_OVERLAY_COLOR = 0x00000088u`|模态阻挡遮罩色。|
|`static constexpr uint32_t COLOR_RGB_MASK = 0xffffff00u`|提取高24位RGB的位掩码。|
|`static constexpr uint32_t COLOR_ALPHA_MASK = 0x000000ffu`|提取低8位Alpha的位掩码。|
|`static constexpr uint32_t DISABLED_ALPHA_DIVISOR = 2u`|禁用状态透明度分母。|
|`static constexpr uint64_t DEFAULT_TAB_SIZE = 36u`|默认页签条厚度。|
|`static constexpr uint64_t DEFAULT_ROW_HEIGHT = 32u`|默认项目行高。|
|`static constexpr uint64_t DEFAULT_WINDOW_WIDTH = 640u`|默认窗口逻辑宽度。|
|`static constexpr uint64_t DEFAULT_WINDOW_HEIGHT = 360u`|默认窗口逻辑高度。|
|`static constexpr uint64_t WINDOW_TITLE_FONT_SIZE = uint64_t{20u}`|默认标题逻辑字号。|
|`static constexpr double LOGICAL_PIXELS_PER_METER = 1000.0`|1倍缩放下每米对应的逻辑像素数。|
|`static constexpr double DEFAULT_PHYSICAL_SCALE = 1.0`|默认窗口物理缩放倍数。|
|`static constexpr double NORMAL_OUTLINE_THICKNESS = 1.0`|普通轮廓线宽。|
|`static constexpr double FOCUSED_OUTLINE_THICKNESS = 2.0`|焦点轮廓线宽。|
|`static constexpr double TEXT_HORIZONTAL_PADDING = 10.0`|文字水平内边距。|
|`static constexpr double BUTTON_HORIZONTAL_PADDING = 6.0`|按钮文字水平内边距。|
|`static constexpr double COMBOBOX_BUTTON_WIDTH = 48.0`|组合框下拉按钮宽度。|
|`static constexpr uint64_t INPUT_BAR_HEIGHT = 48u`|辅助输入条高度。|
|`static constexpr uint64_t INPUT_BAR_MINIMUM_WIDTH = 480u`|辅助输入条最小宽度。|
|`static constexpr uint64_t INPUT_BAR_PADDING = 8u`|辅助输入条内边距。|
|`static constexpr uint64_t INPUT_BAR_COLUMN_GAP = 12u`|辅助输入条列间距。|
|`static constexpr uint64_t INPUT_BAR_FONT_SIZE = 20u`|辅助输入条字号。|
|`static constexpr uint64_t INPUT_BAR_SWITCH_MINIMUM_WIDTH = 144u`|输入法切换按钮最小宽度。|
|`static constexpr double COMBOBOX_ARROW_CENTER_OFFSET = 24.0`|下拉箭头中心偏移。|
|`static constexpr double COMBOBOX_ARROW_HORIZONTAL_RADIUS = 8.0`|下拉箭头水平半径。|
|`static constexpr double COMBOBOX_ARROW_VERTICAL_RADIUS = 4.0`|下拉箭头垂直半径。|
|`static constexpr double COMBOBOX_ARROW_THICKNESS = 3.0`|下拉箭头线宽。|
|`static constexpr double TEXTBOX_SCROLL_PADDING = 4.0`|文本框滚动内边距。|
|`static constexpr double TEXTBOX_SELECTION_VERTICAL_PADDING = 5.0`|文本选区垂直留白。|
|`static constexpr double TEXTBOX_TEXT_TRAILING_PADDING = 2.0`|文本行尾留白。|
|`static constexpr double TEXTBOX_CARET_VERTICAL_PADDING = 7.0`|插入点垂直留白。|
|`static constexpr double TEXTBOX_CARET_THICKNESS = 2.0`|插入点线宽。|
|`static constexpr double TEXTBOX_LINE_HEIGHT_RATIO = 1.4`|文本行高相对字号的比例。|
|`static constexpr double SCROLLBAR_WIDTH = 12.0`|文本编辑滚动条宽度。|
|`static constexpr double SCROLLBAR_MINIMUM_THUMB_SIZE = 18.0`|滚动条滑块最小长度。|
|`static constexpr uint32_t SCROLLBAR_TRACK_COLOR = 0x0d1624ffu`|滚动条轨道色。|
|`static constexpr uint32_t SCROLLBAR_THUMB_COLOR = 0x5f87a9ffu`|滚动条滑块色。|
|`static constexpr double WINDOW_TITLE_HEIGHT = 48.0`|标题栏逻辑高度。|
|`static constexpr double WINDOW_TITLE_LEFT_PADDING = 16.0`|标题文字左侧留白。|
|`static constexpr double WINDOW_TITLE_ICON_SIZE = 28.0`|标题栏图标边长。|
|`static constexpr double WINDOW_TITLE_ICON_GAP = 10.0`|标题图标与文字的间距。|
|`static constexpr double WINDOW_TITLE_RIGHT_PADDING = 56.0`|标题文字右侧留白。|
|`static constexpr double WINDOW_CLOSE_BUTTON_WIDTH = 48.0`|关闭按钮宽度。|
|`static constexpr double WINDOW_TRACKING_BUTTON_WIDTH = 48.0`|跟踪切换按钮宽度。|
|`static constexpr double WINDOW_TRACKING_POPUP_WIDTH = 160.0`|跟踪选择菜单宽度。|
|`static constexpr double WINDOW_TRACKING_ROW_HEIGHT = 32.0`|跟踪选择菜单行高。|
|`static constexpr double WINDOW_CLOSE_ICON_NEAR_OFFSET = 15.0`|关闭图标近侧端点偏移。|
|`static constexpr double WINDOW_CLOSE_ICON_FAR_OFFSET = 33.0`|关闭图标远侧端点偏移。|
|`static constexpr double WINDOW_CLOSE_ICON_THICKNESS = 3.0`|关闭图标线宽。|
|`static constexpr double WINDOW_RESIZE_OUTER_OFFSET = 6.0`|缩放图标外侧偏移。|
|`static constexpr double WINDOW_RESIZE_LONG_INNER_OFFSET = 22.0`|缩放图标长线内侧偏移。|
|`static constexpr double WINDOW_RESIZE_SHORT_INNER_OFFSET = 14.0`|缩放图标短线内侧偏移。|
|`static constexpr double WINDOW_OUTLINE_INSET = 1.0`|窗口轮廓内缩距离。|
|`static constexpr double WINDOW_OUTLINE_THICKNESS = 2.0`|窗口轮廓线宽。|
|`static constexpr uint64_t POPUP_BOTTOM_MARGIN = 24u`|弹出菜单底部留白。|
|`static constexpr uint64_t POPUP_MAXIMUM_VISIBLE_ITEM_COUNT = 8u`|弹出菜单单次最多显示的项目行数。|
|`static constexpr double WINDOW_RESIZE_HIT_SIZE = 30.0`|窗口缩放入口命中区域尺寸。|
|`static uint32_t get_disabled_color(uint32_t color)`|返回降低透明度的禁用颜色。|

## 输入组件

### `easyvrui/input/input_provider.h`

独立layout和IME应用的注册、输入、状态和排空接口。

#### `input_role_t`

声明：`enum class input_role_t`。

|声明|用途与调用语义|
|---|---|
|`layout`|产生虚拟键盘按键的布局程序。|
|`ime`|处理按键、转发未使用事件并提交最终文字的输入法程序。|

#### `input_provider_state_t`

声明：`enum class input_provider_state_t`。

|声明|用途与调用语义|
|---|---|
|`stopped`|当前未运行。|
|`starting`|已发起启动，等待注册。|
|`running`|已注册并处于运行状态。|

#### `provider_info_t`

声明：`struct provider_info_t`。

|声明|用途与调用语义|
|---|---|
|`uint64_t id = 0u`|输入组件编号。|
|`std::u32string name`|组件显示名称，使用UTF-32。|
|`std::u32string language = U"en"`|IME语言代码，常用zh/en/ja；支持其它非空代码。layout沿用记录默认值，协议中的layout项省略language。|
|`input_role_t role = input_role_t::ime`|layout或IME角色。|
|`input_provider_state_t state = input_provider_state_t::stopped`|组件stopped、starting或running状态。|
|`bool configured = false`|是否来自引擎固定配置。|
|`bool active = false`|组件是否为查询会话相应角色当前选择的活动项；输入路径是否启用由input_ui_state_t::active表示。|
|`bool default_provider = false`|该IME是否为持久默认项。|
|`uint32_t process_id = 0u`|组件进程编号。|
|`std::string error`|组件最近的错误说明。|
|`bool operator==(const provider_info_t &other) const = default`|按对应成员值比较是否相等，返回bool。|

#### `input_ui_state_t`

声明：`struct input_ui_state_t`。

|声明|用途与调用语义|
|---|---|
|`bool active = false`|组件是否被当前选择，或输入区是否处于活动状态。|
|`bool physical = false`|当前是否为实体键盘模式。|
|`std::optional<render_rectangle_t> rectangle`|输入区在窗口中的逻辑矩形；没有关联输入区时为nullopt。|

#### `input_event_type_t`

|枚举值|含义|
|---|---|
|`unknown`|未识别的事件。|
|`key_down`|按键按下或重复。|
|`key_up`|按键释放。|
|`ime_submit`|IME提交最终文字。|

#### `input_event_t`

声明：`struct input_event_t`。

|声明|用途与调用语义|
|---|---|
|`std::string event_type`|事件名称，例如key_down或key_up。|
|`std::u32string key`|逻辑按键名称。|
|`std::u32string text`|显示文字或IME提交文字，使用UTF-32。|
|`bool shift = false`|Shift是否按下。|
|`bool ctrl = false`|Ctrl是否按下。|
|`bool alt = false`|Alt是否按下。|
|`bool meta = false`|Windows/Meta是否按下。|
|`bool handled = false`|组件是否已消费当前按键；IME可将未消费按键继续转发。|
|`input_event_type_t get_type() const`|将`event_type`解释为事件枚举，无法识别时返回`unknown`。|

#### `input_provider`

声明：`class input_provider`。

供独立layout/IME应用使用。注册后会话固定为组件角色，组件通过辅助表面呈现界面。IME处理按键并调用`commit_text`提交文字。layout发送虚拟按键。普通应用可在输入法切换对话框中将选中的IME设为默认项。输入区状态由get_state和on_state_changed提供。异步任务必须成对begin_input_task/finish_input_task，排空包括这些任务和待发输出。

on_input的回调签名为void(input_provider &source, input_event_t &event)。process_input及on_input执行后，event.handled仍为false的按键会自动转发；消费按键时把handled设为true。若自行调用send_event转发同一按键，也应设置handled=true以避免重复。IME提交文字后通常消费对应按键。注册是异步过程，通过run或消息循环继续处理注册响应；同一线程只允许一个当前输入组件，注册后角色保持固定。

|声明|用途与调用语义|
|---|---|
|`event_signal<input_provider, input_ui_state_t> on_state_changed`|输入组件的活动输入区、模式或矩形状态变化时触发。|
|`event_signal<input_provider, input_event_t> on_input`|输入组件收到按键或文字事件时触发；可消费或转发。|
|`input_provider()`|创建输入组件实例。|
|`virtual ~input_provider()`|析构对象，结束其资源或引用的生命周期。|
|`input_provider(const input_provider &) = delete`|禁止复制或赋值；对象由其原始实例及生命周期管理。|
|`input_provider &operator=(const input_provider &) = delete`|禁止复制或赋值；对象由其原始实例及生命周期管理。|
|`const input_ui_state_t &get_state() const`|读取输入界面状态。|
|`input_role_t get_role() const`|读取输入组件角色。|
|`bool get_draining() const`|读取组件是否正在排空输入。|
|`bool get_connected() const`|读取当前输入组件连接状态。|
|`uint64_t get_session_id() const`|读取当前输入组件会话编号，未连接时返回0。|
|`const std::vector<provider_info_t> &get_provider_list() const`|读取已知输入组件列表。|
|`void register_provider(input_role_t role = input_role_t::ime, bool default_provider = false, const std::u32string &name = U"", const std::u32string &language = U"en")`|注册当前独立程序为layout或IME；default_provider表示默认选择意向，name为显示名称。language仅用于IME，须为非空代码，省略时为en。一个会话角色固定且互斥。|
|`void begin_input_task()`|登记尚未完成的异步输入任务；用于延迟排空完成确认。|
|`void finish_input_task()`|完成一次begin_input_task登记；每个登记应对应一次完成。|
|`void send_event(const input_event_t &event)`|发送组件输出的按键事件。|
|`void commit_text(const std::u32string &text)`|作为IME提交最终文字，由引擎转发至当前输入窗口。|
|`void run()`|运行输入组件事件循环；未注册时先按默认IME角色发起注册，注册未成功或组件注销后返回。|

##### 派生扩展成员（protected）

以下成员供派生类使用；普通应用通过上表的public接口操作对象。

|声明|用途与调用语义|
|---|---|
|`virtual void process_state(input_ui_state_t &state)`|处理组件输入区状态，供派生类扩展。|
|`virtual void process_input(input_event_t &event)`|处理IME收到的按键；派生类可修改事件或设置handled，随后调用on_input事件链。|
|`virtual void process_drain()`|准备排空输入，派生实现需完成异步任务并停止旧路径输出。|

## 文字与环境工具

### `easyvrui/common/u32string_hash.h`

支持u32string_view查询的透明散列器。

#### `u32string_hash`

声明：`class u32string_hash`。

|声明|用途与调用语义|
|---|---|
|`using is_transparent = void`|透明散列标记，使哈希容器支持不同字符串视图类型查询。|
|`size_t operator()(u32string_view value) const noexcept`|计算Unicode字符串视图的size_t散列值，保证不抛出异常。|

## 错误与语言

### `easyvrui/common/error_diagnostic.h`

源码位置、条件表达式和单行错误诊断。

#### 自由函数与类型别名

|声明|用途与返回值|
|---|---|
|`error_diagnostic get_error_diagnostic(const std::exception &error, const std::source_location &location = std::source_location::current())`|从异常取得已有诊断；异常没有诊断时使用调用位置构造。|
|`std::string get_error_message(const std::exception &error, const std::source_location &location = std::source_location::current())`|返回单行、带源码位置的异常诊断文字。|

#### `error_diagnostic`

声明：`class error_diagnostic`。

诊断值记录文件、行列、函数和条件；source_location默认捕获接口调用位置。get_message输出单行VSCode可识别诊断格式。

|声明|用途与调用语义|
|---|---|
|`explicit error_diagnostic(const std::source_location &location = std::source_location::current(), std::string_view condition = {})`|构造本类型实例；参数含义见本类型说明及签名。|
|`error_diagnostic(std::string file, uint64_t line, uint64_t column, std::string function, std::string condition)`|构造本类型实例；参数含义见本类型说明及签名。|
|`virtual ~error_diagnostic()`|析构对象，结束其资源或引用的生命周期。|
|`const std::string &get_file() const`|读取诊断源文件名。|
|`uint64_t get_line() const`|读取诊断行号。|
|`uint64_t get_column() const`|读取诊断列号。|
|`const std::string &get_function() const`|读取诊断函数名。|
|`const std::string &get_condition() const`|读取失败的条件表达式。|
|`std::string get_message(std::string_view key = {}, std::string_view detail = {}) const`|返回file:line:column: error: condition [key] detail格式的单行文字。|

### `easyvrui/common/error.h`

控件与绘图错误键、结构化异常和断言式条件检查。

#### 自由函数与类型别名

|声明|用途与返回值|
|---|---|
|`string_view get_language_key(error_key_t key)`|将错误枚举转换为语言键。|

#### `error_key_t`

声明：`enum class error_key_t`。

|声明|用途与调用语义|
|---|---|
|`unknown`|未知错误。|
|`owning_thread_required`|请使用begin_invoke()从工作线程访问控件。|
|`callable_required`|字段需要可调用对象。|
|`candidate_string_sequence`|候选项必须是字符串序列。|
|`candidate_index_invalid`|候选索引必须是整数。|
|`operation_failed`|UI服务操作失败。|
|`service_disconnected`|UI服务连接已断开。|
|`service_request_timeout`|UI服务请求超时。|
|`number_required`|字段必须是数值。|
|`finite_number_required`|字段必须是有限数值。|
|`unsigned_integer_required`|字段必须是无符号整数。|
|`three_component_required`|字段需要三个分量。|
|`name_invalid`|名称必须是非空字符串。|
|`duplicate_property`|属性重复：指定值。|
|`unknown_property`|未知属性：指定值。|
|`property_type_mismatch`|属性类型不匹配：指定值。|
|`duplicate_control_name`|控件名称重复：指定值。|
|`duplicate_tabpage_name`|选项卡页面名称重复：指定值。|
|`event_data_object_required`|事件数据必须是对象。|
|`object_disposed`|对象已被释放。|
|`window_activation_failed`|窗口无法激活。|
|`control_focus_failed`|控件无法获得焦点。|
|`client_mismatch`|控件属于不同的UI运行环境。|
|`control_has_parent`|控件已属于某个容器。|
|`cyclic_control_hierarchy`|控件不能包含自身或其祖先控件。|
|`cyclic_reference_object`|窗口参考对象不能形成循环。|
|`cyclic_json_container`|JSON容器不能包含自身或其祖先。|
|`control_not_in_container`|控件不属于此容器。|
|`item_not_in_collection`|选项不属于此集合。|
|`item_index_out_of_range`|选项索引超出范围。|
|`selected_item_index_out_of_range`|选中选项的索引超出范围。|
|`selected_tab_index_out_of_range`|选中标签页的索引超出范围。|
|`positive_rect_required`|控件宽度和高度必须为正数。|
|`positive_row_height_required`|行高必须大于零。|
|`positive_tab_size_required`|标签尺寸必须大于零。|
|`font_family_invalid`|字体名称不能为空或包含NUL。|
|`font_size_invalid`|字体大小必须是正整数。|
|`title_font_family_invalid`|标题字体名称无效。|
|`title_font_size_invalid`|标题字号必须大于零。|
|`tab_font_family_invalid`|标签字体名称无效。|
|`tab_font_size_invalid`|标签字号必须大于零。|
|`physical_scale_invalid`|physical_scale必须是有限的正数倍率。|
|`curvature_invalid`|曲率必须为非负数，窗口的总弧度必须小于一整圈。|
|`position_invalid`|位置必须由有限数值组成。|
|`rotation_invalid`|旋转必须由有限数值组成。|
|`combobox_item_required`|文本必须匹配组合框中的可用选项。|
|`invalid_dialog_owner`|对话框所有者必须是可交互的窗口。|
|`invalid_reference_object_type`|参考对象类型无效。|
|`reference_not_tracked`|窗口参考对象当前未被追踪。|
|`unknown_reference_object`|未知窗口参考对象。|
|`invalid_reference_owner`|引用必须指向当前UI运行环境中未关闭的窗口。|
|`control_required`|需要control实例。|
|`tabpage_required`|需要tabpage实例。|
|`page_list_required`|请通过get_page_list()管理页签。|
|`invalid_rotation`|旋转值无效。|
|`zero_direction`|方向向量不能为零。|
|`invalid_utf8_leading_byte`|UTF-8起始字节无效。|
|`invalid_utf8_continuation_byte`|UTF-8后续字节无效。|
|`truncated_utf8`|UTF-8序列不完整。|
|`overlong_utf8`|UTF-8序列存在超长编码。|
|`invalid_utf8_scalar`|UTF-8字符值超出范围。|
|`invalid_utf32_scalar`|UTF-32字符值超出范围。|
|`truncated_utf16_surrogate`|UTF-16代理对不完整。|
|`invalid_utf16_surrogate`|UTF-16代理对无效。|
|`invalid_utf16_low_surrogate`|UTF-16低位代理项无效。|
|`event_handler_null`|事件处理函数不能为空。|
|`window_render_failed`|窗口渲染失败。|
|`service_stopped`|服务已停止。|
|`window_closing`|窗口正在关闭。|
|`window_closed`|窗口已关闭。|
|`invalid_drawing_coordinate`|绘图坐标必须为有限数值。|
|`invalid_drawing_radius`|绘图半径必须为有限的非负数值。|
|`invalid_drawing_thickness`|描边宽度必须为有限的正数值。|
|`invalid_drawing_opacity`|绘图透明度必须为零到一之间的有限数值。|
|`invalid_drawing_rectangle`|绘图矩形宽高必须为非负数值。|
|`invalid_drawing_image`|绘图图片尺寸必须为正且与RGBA8字节数一致。|
|`drawing_image_size_overflow`|绘图图片字节数超出整数或可寻址尺寸范围。|
|`invalid_drawing_path`|绘图路径填充规则、线段数值或图形顺序无效。|
|`invalid_input_provider_role`|输入提供者角色必须是layout或ime。|
|`language_pack_unavailable`|语言包不可用：指定值。|
|`language_pack_object_required`|语言包必须是对象：指定值。|
|`language_value_text_required`|语言值必须是文本：指定值。|
|`language_key_unavailable`|语言键不可用：指定值。|
|`invalid_base64`|无效的标准Base64编码。|
|`base64_size_overflow`|Base64数据超过容器可寻址大小。|
|`desktop_open_failed`|无法唤出桌面应用：指定值。|
|`grid_value_required`|单元格值不能为空。|
|`grid_boolean_required`|单元格值必须为true或false。|
|`grid_integer_required`|单元格值必须为64位有符号整数。|
|`grid_finite_number_required`|单元格值必须为有限浮点数。|
|`grid_cell_type_mismatch`|单元格值必须保持原有类型。|
|`grid_provider_read_only`|单元格数据提供器为只读。|
|`grid_value_rejected`|单元格值被拒绝。|
|`grid_value_type_required`|单元格值必须为文本、64位有符号整数、有限浮点数或布尔值。|
|`grid_write_result_invalid`|单元格写入回调必须返回bool、None、错误文本或(bool, 错误文本)。|
|`process_launch_failed`|启动应用失败，诊断信息包含Windows错误码。|

#### `engine_error`

声明：`class engine_error : public error_diagnostic, public runtime_error`。

控件与绘图异常，同时继承error_diagnostic和std::runtime_error；get_key返回error_key_t，what()返回单行诊断。

|声明|用途与调用语义|
|---|---|
|`engine_error(error_key_t key, vector<string> argument_list = {}, const source_location &location = source_location::current(), string_view condition = {})`|按key生成异常，argument_list代入本地化说明；location默认捕获调用位置，condition保存失败条件。|
|`error_key_t get_key() const`|读取结构化错误键。|
|`const vector<string> &get_argument_list() const`|读取错误格式化参数。|

### `easyvrui/localization/error.h`

连接层错误键及本地化异常。

#### 自由函数与类型别名

|声明|用途与返回值|
|---|---|
|`using localized_invalid_argument = localized_exception<invalid_argument>`|localized_exception<invalid_argument>别名。|
|`using localized_runtime_error = localized_exception<runtime_error>`|localized_exception<runtime_error>别名。|
|`string_view get_language_key(language_key_t key)`|将错误枚举转换为语言键。|
|`string get_localized_error(language_key_t key, const vector<string> &argument_list = {})`|按language_key_t和argument_list生成本地化错误文字。|
|`void select_error_language(const string &language)`|选择连接错误语言。|
|`string get_error_language()`|返回当前连接错误语言代码。|

#### `language_key_t`

声明：`enum class language_key_t`。

|声明|用途与调用语义|
|---|---|
|`unknown`|未分类错误。|
|`service_disconnected`|服务连接已断开。|
|`operation_failed`|操作失败。|
|`invalid_utf32_scalar`|UTF-32包含非法Unicode标量。|
|`winsock_initialization_failed`|网络运行环境初始化失败。|
|`service_connection_failed`|连接服务失败。|
|`invalid_frame_length`|接收帧长度无效。|
|`json_object_required`|消息必须为JSON对象。|
|`invalid_outgoing_frame_size`|发送帧大小无效。|
|`socket_wait_failed`|套接字等待失败。|
|`accepted_connection_configuration_failed`|连接配置失败。|
|`service_connection_cancelled`|连接操作已取消。|
|`service_identity_mismatch`|服务身份或启动参数不匹配。|
|`tls_operation_failed`|TLS操作失败。|
|`authentication_failed`|接入鉴权失败。|
|`invalid_session`|会话无效。|
|`heartbeat_timeout`|心跳超时。|
|`remote_service_unavailable`|远程服务不可用。|
|`service_startup_timeout`|服务启动超时。|
|`executable_location_failed`|可执行文件位置查询失败。|
|`native_service_required`|需要原生服务程序。|
|`native_service_start_failed`|原生服务启动失败。|

#### `localized_exception<base_type>`

声明：`class localized_exception : public error_diagnostic, public base_type`。

模板异常，同时继承error_diagnostic和base_type。localized_invalid_argument与localized_runtime_error分别对应invalid_argument和runtime_error。get_language_key()成员返回language_key_t枚举。

|声明|用途与调用语义|
|---|---|
|`localized_exception(language_key_t key, vector<string> argument_list = {}, const source_location &location = source_location::current(), string_view expression = {})`|按连接错误key和argument_list生成本地化异常，location记录调用位置，expression保存失败条件。|
|`language_key_t get_language_key() const`|返回此异常的错误键枚举。|
|`const vector<string> &get_argument_list() const`|读取错误格式化参数。|

### `easyvrui/localization/request_error.h`

远端请求失败的异常类型。

#### `request_error`

声明：`class request_error : public error_diagnostic, public std::runtime_error`。

请求失败异常，同时提供std::runtime_error::what()和error_diagnostic的源位置接口；language_key与argument_list保留服务给出的错误信息。

|声明|用途与调用语义|
|---|---|
|`request_error(std::string language_key, std::string message, std::vector<std::string> argument_list, error_diagnostic diagnostic)`|由UTF-8语言键、服务错误说明、格式化参数及已有源码诊断构造请求异常。|
|`const std::string &get_language_key() const`|返回此异常的错误键字符串。|
|`const std::vector<std::string> &get_argument_list() const`|读取错误格式化参数。|

### `easyvrui/localization/language_pack.h`

界面语言选择和语言文本查询。

#### `language_pack`

声明：`class language_pack`。

`get_current()`取得SDK当前语言包。内置文字编入静态库及DLL，默认根据系统语言选择。`load_directory(path)`可显式从指定目录加载自定义语言包，以`en.json`提供基础文字。

|声明|用途与调用语义|
|---|---|
|`static language_pack &get_current()`|返回由SDK管理的当前语言包。|
|`void select_language(const std::u32string &language)`|选择界面语言，支持zh、ja、en及其地区形式归一化。|
|`std::string get_code() const`|读取当前语言代码。|
|`static std::unique_ptr<language_pack> load_directory(const std::filesystem::path &path)`|载入指定目录的语言包。|
|`std::vector<std::u32string> get_available_locale_list() const`|读取目录中的语言代码。|
|`std::vector<std::u32string> get_key_list() const`|列出当前语言包的键。|
|`size_t get_size() const`|读取语言键的数量。|
|`std::optional<std::u32string> find_text(const std::u32string &key) const`|按键查找翻译文字，缺失时返回空值。|
|`std::u32string get_text(const std::u32string &key) const`|按Unicode语言键返回翻译文字；键不存在时返回键本身。|
|`std::string get_message(const std::string &key, const std::vector<std::string> &argument_list) const`|读取UTF-8语言键，按{0}、{1}等占位项代入UTF-8参数，返回UTF-8说明。|

## 通用输入与校验

### `easyvrui/common/keyboard_key.h`

特殊按键枚举及文本键名解析。`keyboard_key_t`包含`unknown`、`backquote`、`backspace`、`tab`、`enter`、`escape`、`space`、方向键`left/right/up/down`、`home/end/page_up/page_down/insert/delete_key`、`caps_lock/num_lock/scroll_lock/menu/pause`、`f1`至`f24`，以及`control/shift/alt/meta`各自的通用、左侧和右侧枚举项，例如`control/left_control/right_control`。

|声明|用途与返回值|
|---|---|
|`keyboard_key_t parse_keyboard_key(std::string_view text)`|解析UTF-8特殊键名，未识别时返回unknown。|
|`keyboard_key_t parse_keyboard_key(std::u32string_view text)`|解析UTF-32特殊键名，未识别时返回unknown。|

键名按大小写匹配，支持`Ctrl/Control`、`Enter/Return`、`Meta/Win`及相应左右修饰键别名。普通字符通过事件的key/text读取；unknown仅表示未匹配特殊键。

#### `keyboard_modifier_t`

声明：`struct keyboard_modifier_t`。

按键修饰状态，ctrl、shift、alt、meta默认false。

|声明|用途与调用语义|
|---|---|
|`bool ctrl = false`|Control修饰键状态，默认false。|
|`bool shift = false`|Shift修饰键状态，默认false。|
|`bool alt = false`|Alt修饰键状态，默认false。|
|`bool meta = false`|Windows/Meta修饰键状态，默认false。|

#### `keyboard_key_t`

声明：`enum class keyboard_key_t`。

命名特殊键枚举，parse_keyboard_key接受UTF-8或UTF-32名称；无法识别的名称返回unknown。

|声明|用途与调用语义|
|---|---|
|`unknown`|未识别的特殊键。|
|`backquote`|`backquote`特殊键；字符串名称由parse_keyboard_key解析。|
|`backspace`|`backspace`特殊键；字符串名称由parse_keyboard_key解析。|
|`tab`|`tab`特殊键；字符串名称由parse_keyboard_key解析。|
|`enter`|`enter`特殊键；字符串名称由parse_keyboard_key解析。|
|`control`|`control`特殊键；字符串名称由parse_keyboard_key解析。|
|`left_control`|`left_control`特殊键；字符串名称由parse_keyboard_key解析。|
|`right_control`|`right_control`特殊键；字符串名称由parse_keyboard_key解析。|
|`shift`|`shift`特殊键；字符串名称由parse_keyboard_key解析。|
|`left_shift`|`left_shift`特殊键；字符串名称由parse_keyboard_key解析。|
|`right_shift`|`right_shift`特殊键；字符串名称由parse_keyboard_key解析。|
|`alt`|`alt`特殊键；字符串名称由parse_keyboard_key解析。|
|`left_alt`|`left_alt`特殊键；字符串名称由parse_keyboard_key解析。|
|`right_alt`|`right_alt`特殊键；字符串名称由parse_keyboard_key解析。|
|`meta`|`meta`特殊键；字符串名称由parse_keyboard_key解析。|
|`left_meta`|`left_meta`特殊键；字符串名称由parse_keyboard_key解析。|
|`right_meta`|`right_meta`特殊键；字符串名称由parse_keyboard_key解析。|
|`pause`|`pause`特殊键；字符串名称由parse_keyboard_key解析。|
|`escape`|`escape`特殊键；字符串名称由parse_keyboard_key解析。|
|`space`|`space`特殊键；字符串名称由parse_keyboard_key解析。|
|`left`|`left`特殊键；字符串名称由parse_keyboard_key解析。|
|`right`|`right`特殊键；字符串名称由parse_keyboard_key解析。|
|`up`|`up`特殊键；字符串名称由parse_keyboard_key解析。|
|`down`|`down`特殊键；字符串名称由parse_keyboard_key解析。|
|`home`|`home`特殊键；字符串名称由parse_keyboard_key解析。|
|`end`|`end`特殊键；字符串名称由parse_keyboard_key解析。|
|`page_up`|`page_up`特殊键；字符串名称由parse_keyboard_key解析。|
|`page_down`|`page_down`特殊键；字符串名称由parse_keyboard_key解析。|
|`insert`|`insert`特殊键；字符串名称由parse_keyboard_key解析。|
|`delete_key`|`delete_key`特殊键；字符串名称由parse_keyboard_key解析。|
|`caps_lock`|`caps_lock`特殊键；字符串名称由parse_keyboard_key解析。|
|`num_lock`|`num_lock`特殊键；字符串名称由parse_keyboard_key解析。|
|`scroll_lock`|`scroll_lock`特殊键；字符串名称由parse_keyboard_key解析。|
|`menu`|`menu`特殊键；字符串名称由parse_keyboard_key解析。|
|`f1`|`f1`特殊键；字符串名称由parse_keyboard_key解析。|
|`f2`|`f2`特殊键；字符串名称由parse_keyboard_key解析。|
|`f3`|`f3`特殊键；字符串名称由parse_keyboard_key解析。|
|`f4`|`f4`特殊键；字符串名称由parse_keyboard_key解析。|
|`f5`|`f5`特殊键；字符串名称由parse_keyboard_key解析。|
|`f6`|`f6`特殊键；字符串名称由parse_keyboard_key解析。|
|`f7`|`f7`特殊键；字符串名称由parse_keyboard_key解析。|
|`f8`|`f8`特殊键；字符串名称由parse_keyboard_key解析。|
|`f9`|`f9`特殊键；字符串名称由parse_keyboard_key解析。|
|`f10`|`f10`特殊键；字符串名称由parse_keyboard_key解析。|
|`f11`|`f11`特殊键；字符串名称由parse_keyboard_key解析。|
|`f12`|`f12`特殊键；字符串名称由parse_keyboard_key解析。|
|`f13`|`f13`特殊键；字符串名称由parse_keyboard_key解析。|
|`f14`|`f14`特殊键；字符串名称由parse_keyboard_key解析。|
|`f15`|`f15`特殊键；字符串名称由parse_keyboard_key解析。|
|`f16`|`f16`特殊键；字符串名称由parse_keyboard_key解析。|
|`f17`|`f17`特殊键；字符串名称由parse_keyboard_key解析。|
|`f18`|`f18`特殊键；字符串名称由parse_keyboard_key解析。|
|`f19`|`f19`特殊键；字符串名称由parse_keyboard_key解析。|
|`f20`|`f20`特殊键；字符串名称由parse_keyboard_key解析。|
|`f21`|`f21`特殊键；字符串名称由parse_keyboard_key解析。|
|`f22`|`f22`特殊键；字符串名称由parse_keyboard_key解析。|
|`f23`|`f23`特殊键；字符串名称由parse_keyboard_key解析。|
|`f24`|`f24`特殊键；字符串名称由parse_keyboard_key解析。|

## 链接宏

### `engine_interface_api.h`

静态库与DLL的声明宏，由构建配置按链接形式设置。

|宏或编译定义|用途|
|---|---|
|`ENGINE_INTERFACE_BUILD`|构建DLL时使ENGINE_INTERFACE_API展开为__declspec(dllexport)|
|`ENGINE_INTERFACE_STATIC`|静态库和其调用方使用，ENGINE_INTERFACE_API展开为空|
|`ENGINE_INTERFACE_API`|未定义前述构建宏时展开为__declspec(dllimport)，声明DLL导入接口|

## 标准对话框

以下函数在调用完成时返回结果，等待期间持续处理界面活动。owner指定直接父窗口；模态期间禁用该父窗口，其它窗口继续交互。对话框采用World与center定位，并继承父窗口的physical_scale。

### 颜色与字体

|头文件|函数|结果|
|---|---|---|
|`easyvrui/dialog/color_dialog.h`|`std::optional<uint32_t> color_dialog(uint32_t color = 0x000000ffu, const std::u32string &title = U"", uint32_t default_color = 0x000000ffu, window *owner = nullptr)`|确定返回`0xRRGGBBAA`，取消返回`std::nullopt`|
|`easyvrui/dialog/font_dialog.h`|`std::optional<font_t> font_dialog(const font_t &font = font_t{}, const std::u32string &title = U"", const font_t &default_font = font_t{}, window *owner = nullptr)`|确定返回系统字体，取消返回`std::nullopt`|

颜色界面包含色域、色相、透明度和RGB／HSV输入。字体界面提供系统字体、数字字号、粗体、斜体及预览。default_color和default_font指定默认值按钮的恢复目标。

### 消息框与输入框

`easyvrui/dialog/messagebox.h`提供两个重载：

```cpp
dialog_result_t messagebox(const std::u32string &message, const std::u32string &title = U"", messagebox_button_set_t button_set = messagebox_button_set_t::ok, messagebox_icon_t icon = messagebox_icon_t::none, dialog_result_t default_button = dialog_result_t::none, window *owner = nullptr);
std::u32string messagebox(const std::u32string &message, const std::u32string &title, const std::vector<messagebox_button_t> &button_list, messagebox_icon_t icon = messagebox_icon_t::none, const std::u32string &default_button_name = U"", window *owner = nullptr);
```

`messagebox_button_t`保存name与text。标准重载返回`dialog_result_t`；自定义按钮重载返回所选按钮的name。

|枚举|成员及数值|
|---|---|
|`messagebox_icon_t`|`none=0`、`error=0x10`、`question=0x20`、`warning=0x30`、`information=0x40`|
|`messagebox_button_set_t`|`ok=0`、`ok_cancel=1`、`abort_retry_ignore=2`、`yes_no_cancel=3`、`yes_no=4`、`retry_cancel=5`|
|`dialog_result_t`|`none=0`、`ok=1`、`cancel=2`、`abort=3`、`retry=4`、`ignore=5`、`yes=6`、`no=7`|

`easyvrui/dialog/inputbox.h`声明：

```cpp
std::optional<std::u32string> inputbox(const std::u32string &prompt, const std::u32string &title = U"", const std::u32string &default_text = U"", uint64_t max_length = 0u, window *owner = nullptr);
```

确定返回输入文字，允许空字符串及字面文字cancel；取消返回`std::nullopt`。max_length为0时不限制长度。

### 文件打开与保存

`easyvrui/dialog/file_open_dialog.h`声明筛选器`file_filter_t`和打开函数。`easyvrui/dialog/file_save_dialog.h`声明保存函数。

```cpp
std::vector<std::filesystem::path> file_open_dialog(const std::u32string &title = U"", const std::filesystem::path &initial_directory = {}, const std::u32string &initial_filename = U"", const std::vector<file_filter_t> &filter_list = {}, std::size_t filter_index = 0u, bool multi_select = false, const std::u32string &confirm_text = U"", window *owner = nullptr, std::function<void(const std::filesystem::path &)> directory_changed = {}, std::function<void(std::size_t)> filter_changed = {});
std::optional<std::filesystem::path> file_save_dialog(const std::u32string &title = U"", const std::filesystem::path &initial_directory = {}, const std::u32string &initial_filename = U"", const std::vector<file_filter_t> &filter_list = {}, std::size_t filter_index = 0u, const std::u32string &default_extension = U"", bool confirm_overwrite = true, const std::u32string &confirm_text = U"", window *owner = nullptr, std::function<void(const std::filesystem::path &)> directory_changed = {}, std::function<void(std::size_t)> filter_changed = {});
```

`initial_directory`为空时使用记忆目录。`initial_filename`用于预填文件名。筛选列表为空时采用默认筛选，`filter_index`从0开始。`file_filter_t`的`pattern_list`支持`*`和`?`。`confirm_text`为空时使用本地化确认按钮。目录和筛选回调在UI线程收到初始值及后续变化。

打开返回所选路径列表，取消返回空列表。启用`multi_select`可以选择多个文件。保存返回目标路径，取消返回`std::nullopt`。`default_extension`为空时按当前筛选推导，`confirm_overwrite`控制覆盖确认。

## 常见调用组合

|场景|调用入口|
|---|---|
|创建普通窗口|构造window→配置属性→get_control_list().add→show→easyvrui::run|
|配置字体|复制get_font()返回的font_t→修改字段→set_font|
|从后台更新界面|begin_invoke(callback)→在callback中调用setter|
|打开模态窗口|构造独立window→show_dialog(owner)→结果枚举。事件处理函数通过set_dialog_result设置结果|
|自定义控件|派生control或text_control→重载render/render_overlay→状态改变后invalidate|
|创建页签|构造`tabcontrol`与`tabpage`→调用`tabpage::set_text()`设置标题→`page_list.add(page)`→向页面添加子控件|
|修改文本选区|select(start,length)→get_selected_text/set_selected_text|
|移除事件回调|保存on_click.add(callback)返回的token→on_click.remove(token)|
|自定义IME|register_provider(input_role_t::ime)→run分派on_input→消费并commit_text，或保持handled=false自动转发|
|自定义layout|input_provider.register_provider(input_role_t::layout)→根据state显示辅助窗口→send_event发送按键→run|
|手动集成应用循环|周期调用easyvrui::pump；宿主负责安排调用时机与其他工作|

示例应用目录为`repo/app/demo/cpp`；应用负责把API头文件和已编译的engine_interface库组合为可执行程序。Python示例位于`repo/app/demo/python`。

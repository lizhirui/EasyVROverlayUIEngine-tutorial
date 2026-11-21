# C++ API Reference

For control usage and complete examples, see the [control catalog](/en/guide/). Window interface examples are found in [window](/en/guide/controls/window-and-text/window), while standard dialog box usage is described in [built-in dialog](/en/guide/09_builtin_dialogs).

The name of regular controls uses `type_用途`, such as `button_ok`. Public control members exported by the designer have the same name as their corresponding names, which can be accessed directly through `button_ok`; the form class name corresponds to the design file name.

This document refers to the public header files in `repo/sdk/api/cpp/include`. After installation, use the public headers under `sdk/api/cpp/include/`, and all public interfaces can be introduced through `#include <easyvrui.h>`. Library and CMake exports are located in `sdk/engine_interface/`.

## Usage Conventions

### Namespace and Linking

Windows, controls, events, geometric, and application interfaces are located in the `easyvrui` namespace, including `get_preferred_ui_language()`. `drawing_image` and `drawing_path` are located in the global namespace.

Use C++20, and match API headers with libraries of the same build version. Built-in C++ applications default to linking with `sdk/engine_interface/lib/engine_interface_static.lib` and use static CRT. Static library callers define `ENGINE_INTERFACE_STATIC`. When selecting a DLL, use `lib/engine_interface.lib` to import the library, and deploy `bin/engine_interface.dll` from the same SDK; consumers must use compatible dynamic CRT. CMake-assisted configuration is located in `sdk/engine_interface/lib/cmake/EngineInterface/`. C++ interfaces use standard library strings, containers, and callbacks, and the calling program must match the compiler, standard library, build configuration, and ABI.

The `ENGINE_INTERFACE_API` in declarations is an export marker; the following signatures omit this marker. `using std::...` introduced in header files is understood according to the standard library's original meaning for convenience.

### Types, Units, and Return Values

|Conventions|Meanings|
|---|---|
|`u32string`、`std::u32string`、`U"..."`|Unicode code point sequences, used for control names, interface text, and font names|
|`string`、`std::string`|UTF-8 is used when text is explicitly specified in this API; protocol keys, diagnostics, and Base64 are explained according to the corresponding interfaces.|
|`uint32_t color`|Arranged according to `0xRRGGBBAA`; Alpha=0 is completely transparent, Alpha=255 is opaque|
|`rectangle_t`|Unsigned integer logical coordinates, with field order being `left`, `top`, `width`, `height`|
|`render_rectangle_t`|double logical coordinates, allowing floating-point positions for drawing|
|`window.position`|Offset relative to a reference target, measured in meters|
|`window.rotation` and Euler angles interface|XYZ rotation, measured in degrees; the combination order is Rz×Ry×Rx|
|`physical_scale`|Scaling factor for the physical size of logical pixels; when it is 1, each logical pixel corresponds to 1 millimeter|
|`index`、`start`|Typically starting from 0, see the corresponding interface for specifics|
|Text selection position|UTF-32 code point offset; actual selection, movement, and deletion will align the character boundaries|
|`optional<T>`|Provide T when there is a value; otherwise, use `nullopt`.|
|Object pointer|Situations where `nullptr` may occur are listed in the interface description.|
|`const T &`|Borrowing of read-only references, whose validity period depends on the original object and subsequent modifications.|
|`void`|Delivering effects through object state, events, or completion callbacks.|

An element in `std::u32string` is a character point. A visible character may consist of multiple character points; the length of a text selection is still counted in character points.

### Threads, lifecycle, and events

Controls are assigned to the current UI thread when created. Window, container, text, and message loop operations are executed on the associated thread. After background work is completed, updates are delivered through `control_base::begin_invoke(callback)`. Regular events are dispatched by the application message loop, while `show_dialog()` continues to be dispatched through nested loops in the same thread. Internal synchronization requests only wait for their own responses; events that arrive during this time remain in the queue and are processed by subsequent message loops.

Control construction only requires `name`. The name must be non-empty and not contain U+0000. The text should consist of valid Unicode scalars; the name becomes read-only after construction. Names within the same control container are unique; different containers can use the same name. Containers allow obtaining objects by name. An object can have only one parent, and the control hierarchy must not form a loop.

References like `add(control &)` have overloads, and the caller ensures the object's survival; references like `add(shared_ptr<control>)` have shared ownership retained by the container. `remove` and `clear` indicate removing from the container, while `dispose` indicates releasing the object. `hide` retains the window for redisplaying, and `close` goes through closing and modal completion processes.

Control events use `event_container<参数类型>`, and the callback signature is `void(control_base &source, 参数类型 &event)`. Using `add`, you can obtain a token to unsubscribe; using `+=`, you can register directly.

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

Subsequent code snippets follow the example of the header file and using namespace std, and are executed within the corresponding application functions; window_main indicates `shared_ptr<window>` held by the caller, while owner indicates a valid window reference.

During window display, the SDK treats Ctrl+C in this process as a shortcut key on the interface. After the last displayed window closes, the console resumes processing. Ctrl+Break follows the console behavior.

### Inheritance relationships and property reading/writing

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

Derived classes inherit all public members of their ancestors; each type listed below specifies its declared public members and overloads. Protected members are listed separately, and inherited methods with the same name are used according to C++ rules of overriding and name hiding. `text_control` provides the text foreground color and font; regular `control` and containers provide the background color. Window titles and tab titles have independent text appearance properties.

Properties are read and modified through `get_xxx()` and `set_xxx(value)`. Each setter verifies and sets the property, and triggering the corresponding event occurs when the value changes.

Tab navigation targets controls within the current window that are focusable, visible, enabled, and active. Positive numbers for tab_index are sorted in ascending order first; 0 follows. Within the same group, they are sorted in ascending order by window absolute top, then in ascending order by left. Controls with the same position retain the traversal order. Tab moves forward, Shift+Tab moves backward, cycling between start and end. Pause switches the physical keyboard interception mode; text focus is controlled by IME/layout, while other focusable controls can still receive key presses.

After activating the editing control, the auxiliary input bar below the input area displays the language, IME name, and "Input Method Switch" button. Clicking the button first empties and hides the input interface, then opens a modal dialog box; the layout is independently selected, and the language list determines the filtering range of the IME list. Each language is applied after clicking "OK"; it is discarded when canceled. After closing, return to the original editing control. In physical keyboard mode and with a valid current window, Alt+Shift switches languages and restores the last used IME for that language; Ctrl+Shift switches the IME within the current language.

### Strongly typed events

The control provides the event source through the first parameter, and the type of the second parameter is determined by the event member declaration. Ordinary events use `event_args_t`, and the parameters for the other 18 control events inherit from this base class. Events with cancellation or consumption markers allow callbacks to update `cancel` or `handled`, with the distribution process reading the updated values. Container events provide the actual object, with indices starting from 0.

### Remote connection startup parameters

The connection entry reads the current process startup parameters. All remote options are in the form of `--name=value`:

|Parameter|Purpose and default values|
|---|---|
|`--easyvrui-host=地址`|Remote hostname, IPv4 or raw IPv6 address, such as `::1`; required when using the remote mode|
|`--easyvrui-port=端口`|Decimal port, default 49537, valid range 1 to 65535|
|`--easyvrui-access-credential=凭据`|Remote access credentials, required|
|`--easyvrui-public-key-fingerprint=指纹`|Service public key SHA-256 hexadecimal fingerprint, required|

The application can provide its own startup parameters on the same command line. Local programs use automatic discovery; ordinary controls create and `run(application_name)` entries use the current connection configuration. For protocol message definitions, see the [Engine protocol reference](./engine_protocol).

### Export layout of design files

The generated C++ layout class inherits from the SDK type corresponding to the design root. All non-root controls reference are public members, and their names are exactly the same as their respective control.name. Controls in nested containers, tabs, and menus share the member namespace of this generated class. Therefore, the names must be unique throughout the design, following C++ and Python identifier rules, and avoiding root SDK public entries.

The generated class itself only defines a constructor. Ordinary exports will have declarations and implementations written separately in the same-name `.h` and `.cpp`. The constructor creates the control, adds it to the corresponding collection, and initializes properties. The default name parameter uses the name of the design root node, such as `const std::u32string &name = U"sample_form"`. The business class holds a generated form instance and binds events through members with the same name, reading and modifying control properties.

Images and icons reuse the SDK's `drawing_image::load_file()` and other drawing resource loading interfaces; value records are constructed directly through the SDK type, and resource files are deployed with the export results.

## Public header file index

|Modules|Header files|
|---|---|
|Drawing|`drawing_image.h`、`drawing_path.h`、`easyvrui/render/render_context.h`、`easyvrui/render/render_style.h`|
|Application entry|`easyvrui/application.h`、`easyvrui/application_management.h`|
|Modal window results|`easyvrui/dialog/dialog_result.h`|
|Basic values and text tools|`easyvrui/common/color.h`、`easyvrui/common/error.h`、`easyvrui/common/error_diagnostic.h`、`easyvrui/common/keyboard_key.h`、`easyvrui/common/u32string_hash.h`、`easyvrui/common/value.h`|
|Standard dialogs|`easyvrui/dialog/color_dialog.h`、`easyvrui/dialog/file_open_dialog.h`、`easyvrui/dialog/file_save_dialog.h`、`easyvrui/dialog/font_dialog.h`、`easyvrui/dialog/inputbox.h`、`easyvrui/dialog/messagebox.h`|
|Active rows and columns and tree nodes|`easyvrui/control/listview_column.h`、`easyvrui/control/listview_column_collection.h`、`easyvrui/control/listview_item.h`、`easyvrui/control/listview_item_collection.h`、`easyvrui/control/listview_cell_collection.h`、`easyvrui/control/tree_node.h`、`easyvrui/control/tree_node_collection.h`|
|Event|`easyvrui/event/event_args.h`、`easyvrui/event/event_container.h`、`easyvrui/event/event_signal.h`|
|Spatial geometry|`easyvrui/geometry/pose.h`、`easyvrui/geometry/quat.h`、`easyvrui/geometry/vec3.h`|
|Input components|`easyvrui/input/input_provider.h`|
|Errors and Languages|`easyvrui/localization/error.h`、`easyvrui/localization/language_pack.h`、`easyvrui/localization/request_error.h`|
|Aggregation Entrance|`easyvrui.h`|
|Export Configuration|`engine_interface_api.h`|

Ordinary applications use the public interface of controls, while derived controls use the protected extension points listed in each section of this document.

## Application entry

### `easyvrui.h`

Aggregation entrances for common controls, applications, events, and drawing interfaces. Ordinary window applications usually start from this header file.

The public include directory contains 76 header files, including the aggregation entrance `easyvrui.h`. The declaration locations of each interface are shown below.

### `easyvrui/application.h`

Event loop, resource query, and input area control entrances for window applications.

#### Free Functions and Type Aliases

|Declaration|Purpose and Return Values|
|---|---|
|`void show_input_ui(window &item, const rectangle_t &rectangle, std::function<void(bool)> completion = {})`|For the logical input area of the item window, “rectangle”, set it to IME/layout. The completion function receives a boolean value indicating whether the operation was successful or not.|
|`void hide_input_ui(std::function<void(bool)> completion = {})`|Hide the current input area and associated IME/layout; completion receives a boolean value indicating whether the operation was successful.|
|`void set_application_name(const std::u32string &application_name)`|Set a non-empty session name. Registered names can be re-set after the connection is established.|
|`void run(const std::u32string &application_name)`|Register a session with a required non-empty name and run the event loop of the window application. Return when the window is completely closed or the running environment stops.|
|`bool pump(uint64_t timeout_millisecond = 0u)`|Dispatch messages and callbacks, submit the window to be updated, and wait for the specified milliseconds as needed. Return false to indicate the loop ends.|
|`std::filesystem::path get_application_directory()`|Return to the application directory, which can be used to locate resources.|
|`double measure_text(const std::u32string &text, const font_t &font)`|Measure the text width in logical pixels using the specified font.|

The application message loop dispatches server events on the UI thread, asynchronously notifies completion, and locally delivers callbacks, then advances the timing state and submits the window to be updated. The connection saves asynchronous responses and server events separately, and the message pump maintains the order of receipt when merging the two queues. For example, the old input text is dispatched first, followed by the completion callback for closing the input area. Internal synchronous responses are delivered separately by request ID. See [, IPC, TLS, and connection queue](/en/advanced/03_ipc_tls_protocol) for implementation.

### `easyvrui/application_management.h`

`application_entry_t.name` saves the matched name, `icon_path` saves the icon path, `icon_data` saves the original file bytes of the embedded image. When `language` is empty, it matches the system language and reverts to `en`. See [for application list and](./application_manifest) for list fields.

Entrance for reading application lists, local startup, querying application snapshots, and ending.

#### Free Functions and Type Aliases

|Declaration|Purpose and Return Values|
|---|---|
|`application_entry_t read_application_entry(const std::filesystem::path &manifest_path, const std::u32string &language = {})`|Read the `.easyvrui` list and parse it into a startup description. Throw an exception if the list is missing or the fields are invalid.|
|`uint32_t launch_application(const std::filesystem::path &manifest_path, const std::vector<std::u32string> &extra_argument_list = {})`|Read the list on the machine where the calling process is located and start the application, returning the new process PID; extra_argument_list is appended to the parameters declared in the list. Python entries execute the script specified by the list through python.exe in the PATH. Throw an exception if the startup fails.|
|`std::vector<application_snapshot_t> get_application_snapshot_list()`|The query engine returns a list of locally verified application snapshots, including session names and window lists.|
|`bool terminate_application(uint64_t session_id)`|End the process corresponding to the target session, returning the operation result given by the engine.|
|`bool close_application_window(uint64_t session_id, uint64_t window_id)`|Request the target session to properly close the specified window, returning whether the event was delivered.|
|`void request_application_snapshot_list(std::function<void(std::vector<application_snapshot_t>, std::exception_ptr)> completion)`|Asynchronous query of application snapshots.|
|`void request_terminate_application(uint64_t session_id, std::function<void(bool, std::exception_ptr)> completion)`|Asynchronous request ends the target application.|
|`void request_close_application_window(uint64_t session_id, uint64_t window_id, std::function<void(bool, std::exception_ptr)> completion)`|Asynchronous request normally closes the target window.|

Both inventory parsing and startup are completed locally on the SDK, so the program and engine can be on different machines. The single instance is implemented by the application itself. Instance coordination is performed by the target app using mechanisms such as process instance locks. The application list and termination operations require a verified engine local session; the list includes Desktops, with input components being filtered. Desktops and input components are protected by termination operations.

Asynchronous callbacks are executed on the application UI thread. Snapshot callbacks receive the snapshot list and `exception_ptr`, while operation callbacks receive boolean results and `exception_ptr`. When successful, the exception pointer is empty; in case of failure, it can be re-thrown for diagnosis.

#### `application_type_t`

Declaration: `enum class application_type_t`.

`application` represents a regular application, while `ime` and `layout` represent input components, and `desktop` represents a desktop.

|Declaration|Purpose and calling semantics|
|---|---|
|`application`|Regular application.|
|`ime`|Independent input method.|
|`layout`|Independent keyboard layout.|
|`desktop`|Desktop application.|

#### `application_runtime_t`

Declaration: `enum class application_runtime_t`.

Native uses the local executable file, Python uses the Python main script.

|Declaration|Purpose and calling semantics|
|---|---|
|`native`|Launch the local executable file.|
|`python`|Launch the Python main script.|

#### `application_entry_t`

Declaration: `struct application_entry_t`.

The parsed application inventory, with paths resolved according to the directory where the inventory is located; names have been matched according to specified or system languages. If a missing match occurs, en is used as a fallback.

|Declaration|Purpose and calling semantics|
|---|---|
|`std::u32string id`|Application ID in the inventory.|
|`std::u32string name`|Application display name after language matching.|
|`std::filesystem::path icon_path`|External icon path.|
|`std::vector<uint8_t> icon_data`|Original bytes of the embedded image file.|
|`std::filesystem::path executable`|Path to the local program or Python interpreter.|
|`application_runtime_t runtime = application_runtime_t::native`|By default, native when starting the runtime.|
|`std::filesystem::path script`|Path to the Python main script.|
|`std::vector<std::u32string> argument_list`|Parameter list added to the target program.|
|`application_type_t type = application_type_t::application`|Application type, default is `application`.|

#### `application_window_t`

Declaration: `struct application_window_t`.

Window records in the application snapshot, with id being the global window ID, name being the fixed internal name, title being the actual window title, and visible indicating the display status.

|Declaration|Purpose and calling semantics|
|---|---|
|`uint64_t id = 0u`|Global window ID.|
|`std::u32string name`|Fixed name when the window is constructed.|
|`std::u32string title`|Actual window title seen by the user.|
|`bool visible = false`|Whether the window is currently displayed.|

#### `application_snapshot_t`

Declaration: `struct application_snapshot_t`.

Local application session snapshot verified by Engine, including session ID, process ID, name, window list, memory bytes, and percentage of CPU/GPU.

|Declaration|Purpose and calling semantics|
|---|---|
|`uint64_t session_id = 0u`|Engine session ID.|
|`uint32_t process_id = 0u`|Local process ID.|
|`std::u32string name`|Session registration name.|
|`std::vector<application_window_t> window_list`|Window list for this session.|
|`uint64_t memory_bytes = 0u`|Process memory usage, in bytes.|
|`double cpu_percent = 0.0`|Percentage of process CPU usage.|
|`double gpu_percent = 0.0`|Percentage of process GPU usage.|

## Basic values and spatial geometry

### `easyvrui/common/value.h`

Enumerations of fonts, control rectangles, and directions.

#### Free Functions and Type Aliases

|Declaration|Purpose and Return Values|
|---|---|

#### `font_t`

Declaration: `struct font_t`.

Pure data font values, with family being the system font name, size being the logical font size of uint64_t and must be greater than 0; default is Segoe UI, 18, bold=false, italic=false. operator== compares field by field.

|Declaration|Purpose and calling semantics|
|---|---|
|`static constexpr uint64_t DEFAULT_SIZE = uint64_t{18u}`|Default logical font size of font_t.|
|`u32string family = U"Segoe UI"`|System font family name.|
|`uint64_t size = DEFAULT_SIZE`|Logical font size of the font.|
|`bool bold = false`|Whether to bold the text.|
|`bool italic = false`|Whether to italic the text.|
|`bool operator==(const font_t &other) const = default`|Returns a bool indicating whether the corresponding member values are equal, by comparing field by field.|

#### `rectangle_t`

Declaration: `struct rectangle_t`.

Pure data control rectangle, with all fields being uint64_t. The default values are left=0, top=60, width=160, height=40; control setters require both width and height to be positive. operator== compares field by field.

|Declaration|Purpose and calling semantics|
|---|---|
|`uint64_t left = 0u`|The horizontal coordinate on the left side of the rectangle.|
|`uint64_t top = 60u`|The vertical coordinate on the top side of the rectangle.|
|`uint64_t width = 160u`|The width of the rectangle, in logical pixels.|
|`uint64_t height = 40u`|The height of the rectangle, in logical pixels.|
|`bool operator==(const rectangle_t &other) const = default`|Returns a bool indicating whether the corresponding member values are equal, by comparing field by field.|

### `easyvrui/common/color.h`

RRGGBBAA color value and components, hexadecimal, and transparency operations.

#### `color_t`

Declaration: `struct color_t`.

Default value=0, which is completely transparent black; for 32-bit arrangement, it is RRGGBBAA, with the lowest 8 bits being transparency, 0 for complete transparency, and 255 for opacity.

|Declaration|Purpose and calling semantics|
|---|---|
|`uint32_t value = 0u`|32-bit RRGGBBAA color value.|
|`color_t() = default`|Construct this type of instance; see the type description and signature for parameter meanings.|
|`explicit color_t(uint32_t value)`|Construct this type of instance; see the type description and signature for parameter meanings.|
|`std::array<uint8_t, 4u> get_rgba() const`|Return 4 8-bit components in order of R, G, B, A.|
|`std::string get_hex() const`|Return a RRGGBBAA hexadecimal color string starting with 0x.|
|`color_t create_with_alpha(uint8_t alpha) const`|Keep RGB and replace alpha to return the new color value.|
|`bool operator==(const color_t &other) const = default`|Returns a bool indicating whether the corresponding member values are equal, by comparing field by field.|

### `easyvrui/geometry/vec3.h`

Three-dimensional vector.

#### `vec3_t`

Declaration: `struct vec3_t`.

Default zero vector. operator== performs approximate comparison by scaling each component to double precision, returning false for non-finite values.

|Declaration|Purpose and calling semantics|
|---|---|
|`double x = 0.0`|The X component of the vector.|
|`double y = 0.0`|The Y component of the vector.|
|`double z = 0.0`|The Z component of the vector.|
|`static bool is_equal(double left, double right)`|Compare finite floating-point numbers with a double precision threshold and numerical scale; return false for non-finite values.|
|`bool operator==(const vec3_t &other) const`|Perform approximate comparison based on three double components, using is_equal rules.|
|`vec3_t operator+(vec3_t b) const`|Add each component to get the new vec3_t.|
|`vec3_t operator-(vec3_t b) const`|Subtract each component to get the new vec3_t.|
|`vec3_t operator*(double scalar) const`|Multiply all components by a scalar to get the new vector.|
|`double calculate_dot_product(vec3_t b) const`|Return the dot product with b.|
|`vec3_t calculate_cross_product(vec3_t b) const`|Return the cross product with b.|
|`double get_length() const`|Return the length of the three-dimensional vector.|
|`vec3_t get_normalized() const`|Return the vector per unit length; throw exceptions for zero, too small values, and non-finite inputs.|

### `easyvrui/geometry/quat.h`

Quaternion rotation.

#### `quat_t`

Declaration: `struct quat_t`.

Default unit rotation {x=0, y=0, z=0, w=1}. Angular and Euler angles use degrees; create_from_euler is combined as Rz×Ry×Rx. get_inverse/rotate interprets the current value as a normalized rotation.

|Declaration|Purpose and calling semantics|
|---|---|
|`double x = 0.0`|The X component of the quaternion.|
|`double y = 0.0`|The Y component of the quaternion.|
|`double z = 0.0`|The Z component of the quaternion.|
|`double w = 1.0`|The real part of the quaternion; unit rotation is 1.|
|`quat_t operator*(quat_t b) const`|Combine the current quaternion with b, with b's rotation applying first.|
|`quat_t get_normalized() const`|Return the unit quaternion; throw exceptions for zero, too small values, and non-finite inputs.|
|`quat_t get_inverse() const`|Return the quaternion representing the inverse rotation.|
|`vec3_t rotate(vec3_t v) const`|Use the current quaternion to rotate the vector v, and return the resulting rotation.|
|`static quat_t get_axis(vec3_t v, double angle)`|Create an angular-quaternion based on the unit axis v and angle degrees; the caller provides the unit axis.|
|`static quat_t create_from_euler(vec3_t v)`|Create a rotation based on XYZ angles, combined as Rz×Ry×Rx.|
|`vec3_t get_euler_angle_vector() const`|Return the equivalent XYZ Euler angles, in units of degrees; different angle combinations may represent the same pose.|
|`static quat_t create_from_axis_basis(vec3_t a, vec3_t b, vec3_t c)`|Create and normalize the rotation using the three axis base vectors a/b/c.|
|`static quat_t blend(quat_t a, quat_t b, double t)`|Perform the shortest parallel normalization linear interpolation on a/b, with t typically ranging from 0 to 1.|

### `easyvrui/geometry/pose.h`

The combined pose of position and quaternion rotation.

#### `pose_t`

Declaration: `struct pose_t`.

Default: position is zero, rotation is the unit quaternion. a*b indicates combining b's local pose into a; transform_point performs rotation followed by translation.

|Declaration|Purpose and calling semantics|
|---|---|
|`vec3_t position`|Three-dimensional translation.|
|`quat_t rotation`|Represent the pose rotation in quaternions.|
|`pose_t operator*(const pose_t &b) const`|Combine the current pose with b, with b applying first, then transform using the current pose.|
|`pose_t get_inverse() const`|Return the inverse pose.|
|`vec3_t transform_point(vec3_t v) const`|Transform the local point v to the parent reference frame of the current pose.|

### `easyvrui/control/reference_object.h`

Optional window reference targets: `world`, `body`, `head`, `left`, and `right`. The Engine locates the auxiliary surface of IME/layout based on the associated input area.

#### Free Functions and Type Aliases

|Declaration|Purpose and Return Values|
|---|---|
|`u32string get_reference_object_type_name(reference_object_type_t value)`|Convert the reference target enumeration to Unicode names.|
|`reference_object_type_t parse_reference_object_type(const u32string &value)`|Parse the Unicode names into reference targets; invalid names throw an exception.|

#### `reference_object_type_t`

Declaration: `enum class reference_object_type_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`world`|World spatial reference.|
|`body`|A reference that follows the body's position and maintains the calibrated orientation, which can be recalibrated using reset_body_center.|
|`head`|Headset reference, with follow position and rotation.|
|`left`|Left handle reference.|
|`right`|Right handle reference.|

#### `reference_object_t`

Declaration: `struct reference_object_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`reference_object_type_t type = reference_object_type_t::world`|Reference target category.|
|`bool operator==(const reference_object_t &other) const = default`|Returns a bool indicating whether the corresponding member values are equal, by comparing field by field.|

## Event and value container.

### `easyvrui/event/event_signal.h`

A generic event chain called in registration order.

#### `event_signal<source_type, argument_type_list...>`

Declaration: `class event_signal`.

Template parameters are source_type and argument_type_list..., and the function handler signature is void(source_type &, argument_type_list &...). add returns the registered token; remove and operator-= use the token, and operator+= returns a reference to the event chain. call calls in registration order; the current call uses a snapshot of the function handler list, with additions and deletions reflected in the next call. Callback exceptions are propagated to the caller. The event chain is used by the thread of the associated object.

|Declaration|Purpose and calling semantics|
|---|---|
|`uint64_t add(std::function<void(source_type &, argument_type_list &...)> callback)`|Register a non-empty callback and return the uint64_t token for subsequent use with remove or operator-=.|
|`event_signal &operator+=(std::function<void(source_type &, argument_type_list &...)> callback)`|Register a callback and return a reference to the event chain, suitable for C#-style append syntax; when cancellation is needed, prioritize calling add to retain the token.|
|`bool remove(uint64_t token)`|Delete the function handler specified by the token; return true if found, otherwise false.|
|`event_signal &operator-=(uint64_t token)`|Remove the function handler corresponding to the token and return a reference to the event chain.|
|`void clear()`|Remove all function handlers.|
|`bool is_empty() const`|Query whether the event chain has zero subscriptions.|
|`void call(source_type &source, argument_type_list &...argument_list) const`|Call the current event chain in registration order with source and reference parameters; the callback returns void.|

### `easyvrui/event/event_container.h`

An alias for the type of event chain with control_base as the event source.

#### Free Functions and Type Aliases

|Declaration|Purpose and Return Values|
|---|---|
|`using event_container = event_signal<control_base, argument_type_list...>`|An alias for template <typename... argument_type_list>, with the event source fixed as control_base.|

### `easyvrui/event/event_args.h`

`event_args_t` is an empty base class. The other 18 structures in the table publicly inherit from `event_args_t`. Each event is called by its specific parameter type in the declaration.

|Parameter types|Field|Purpose|
|---|---|---|
|`event_args_t`|None|Changes in click, focus, window lifecycle, and specific properties.|
|`cancel_event_args_t`|`bool cancel = false`|Setting `cancel` before closing the window can cancel a normal close. Forced close always executes.|
|`key_event_args_t`|`std::u32string key`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`、`bool handled = false`|Key names, modifier keys, and consumption status.|
|`text_input_event_args_t`|`std::u32string text`、`bool handled = false`|Submitted text and consumption status.|
|`pointer_event_args_t`|`std::u32string hand`、`double left = 0.0`、`double top = 0.0`、`double x = 0.0`、`double y = 0.0`、`bool captured = false`、`bool cancelled = false`、`bool handled = false`、`bool has_position = false`、`bool has_local_position = false`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`|Include hand position, window coordinates `left/top`, control local coordinates `x/y`, and modifier keys. Use `has_position` and `has_local_position` to determine whether the corresponding coordinates are valid.|
|`scroll_event_args_t`|`std::u32string hand`、`double delta_x = 0.0`、`double delta_y = 0.0`、`bool handled = false`|Hand position, horizontal and vertical scroll amounts, and consumption status.|
|`interaction_end_event_args_t`|`bool cancelled = false`|Movement, zoom, curvature adjustment, or drag completion. `cancelled` indicates the operation was canceled.|
|`property_changed_event_args_t`|`std::u32string property_name`|`property_name` is the name of the changing property. Read the current value through `source`.|
|`control_collection_event_args_t`|`control *item = nullptr`、`size_t index = 0u`|Controls in the collection and their indices. `item` for overall table notification is empty.|
|`menu_item_event_args_t`|`menuitem *item = nullptr`、`size_t index = 0u`|Menu items and indices.|
|`tabpage_event_args_t`|`tabpage *page = nullptr`、`size_t index = 0u`|Tab objects and indices.|
|`listview_column_event_args_t`|`std::shared_ptr<listview_column> column`、`size_t index = 0u`|ListView column objects and indices. `column` for overall table notification is empty.|
|`listview_item_event_args_t`|`std::shared_ptr<listview_item> item`、`size_t index = 0u`|ListView item objects and indices. `item` for overall table notification is empty.|
|`grid_column_event_args_t`|`size_t index = 0u`、`uint64_t width = 0u`|Grid column indices and widths. Read column indices through `index` when clicking on the header.|
|`grid_cell_event_args_t`|`uint64_t row = 0u`、`uint64_t column = 0u`、`std::u32string error`|Grid cell row and column indices. `error` contains error descriptions when editing fails.|
|`tree_node_event_args_t`|`tree_node *node = nullptr`|Tree nodes of operations. `node` is empty when selection is canceled.|
|`render_error_event_args_t`|`std::string message`|Messages of rendering exceptions.|
|`controller_event_args_t`|`std::u32string hand`、`bool trigger = false`、`bool grip = false`、`uint8_t joystick_x = 128u`、`uint8_t joystick_y = 128u`、`bool joystick_pressed = false`、`bool primary = false`、`bool secondary = false`|Handle button presses and joystick status. The joystick axis range is 0 to 255, with `primary` representing left-hand X or right-hand A, and `secondary` representing left-hand Y or right-hand B.|
|`control_input_event_args_t`|`control_input_type_t type = control_input_type_t::none`、`std::u32string hand`、`std::u32string key`、`std::u32string text`、`double left = 0.0`、`double top = 0.0`、`double x = 0.0`、`double y = 0.0`、`int64_t steps = 0`、`bool horizontal = false`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`、`bool captured = false`、`bool cancelled = false`、`bool handled = false`、`bool has_position = false`、`bool has_local_position = false`|Input assignment parameters for derived controls. Distinguish inputs through `type`, read fields by type, and set `handled` to indicate consumption.|

The values of `control_input_type_t` are `none`, `click`, `focus_in`, `focus_out`, `pointer_enter`, `pointer_leave`, `pointer_move`, `pointer_down`, `pointer_up`, `scroll`, `key_down`, `key_up`, `text_input`, `controller_input`.

## Control base class and container

### `easyvrui/control/control_base.h`

Control identification, parent, lifecycle, property access, and basic events.

#### `control_base`

Declaration: `class control_base: public std::enable_shared_from_this<control_base>`.

Identity and lifecycle base class, inherited from `std::enable_shared_from_this<control_base>`. The constructor is protected and called by derived classes. name and type are read-only after construction; get_id() is a runtime number. Controls cannot be copied. Object operations follow the constraints of the underlying UI thread, and cross-thread updates use begin_invoke. Inherited shared_from_this() and weak_from_this() follow the standard library's shared ownership rules; controls managed by reference methods are typically accessed through containers and control interfaces.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_disposed`|Triggered when objects are released.|
|`event_container<property_changed_event_args_t> on_property_changed`|Triggered when property values change. property_name is the name of the changing property.|
|`virtual ~control_base()`|Destructs objects, ending their resources or referenced lifetimes.|
|`virtual uint64_t get_id() const`|Read the object number allocated at runtime.|
|`virtual control_base *get_parent() const`|Read the parent object pointer; the top-level object is nullptr.|
|`virtual bool get_disposed() const`|Read whether the object has been released.|
|`virtual void invalidate()`|Request a repaint of the associated window; used for refreshing the screen after custom state changes.|
|`virtual void dispose()`|Release the control and related runtime resources; stop using the object after release.|
|`virtual void begin_invoke(std::function<void()> callback)`|Queue the callback in the UI thread of the object; skip the callback if the object is released before execution.|
|`virtual const u32string &get_name() const`|Read the name determined during construction.|
|`virtual const u32string &get_type() const`|Read the object type name.|
|`virtual const u32string &get_tag() const`|Read the string marker saved by the application, defaulting to an empty string.|
|`virtual void set_tag(const u32string &value)`|Set the marker. Trigger `on_tag_changed` when the value changes.|
|`event_container<event_args_t> on_tag_changed`|The change is triggered when the marker changes. The callback receives the source control and the `event_args_t` without any additional data.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`virtual std::shared_ptr<control_base> get_retained_owner()`|Return the shared reference required to retain the object's lifetime during operations.|
|`virtual bool notify_property_changed(std::u32string_view name, bool changed, event_container<event_args_t> *specific = nullptr, bool redraw = true)`|Trigger notification when the property changes and return true. The redraw control determines whether to request a repaint.|
|`control_base(const u32string &name, const u32string &type)`|Construct the object; see the type description for parameters, default states, and constraints.|
|`virtual void process_input(control_input_event_args_t &event)`|Virtual function for handling control input events; can be extended and distinguished by input type through event.type.|

### `easyvrui/control/control.h`

Public properties and input events of visual controls.

#### `control`

Declaration: `class control: public control_base`.

A visual base class that can be constructed directly. The default rect is {0,60,160,40}, visible=true, enabled=true, tab_index = 0; it does not accept focus by default. The background color is 0x162738FF by default. Container coordinates use relative to the parent level’s logical units.

Inherit all public property access, methods, and events of `control_base`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_background_color_changed`|Trigger when the background color changes.|
|`event_container<event_args_t> on_visible_changed`|Trigger when the visible state changes.|
|`event_container<event_args_t> on_enabled_changed`|Trigger when the available state changes.|
|`event_container<event_args_t> on_tab_index_changed`|Trigger when the Tab focus order changes.|
|`event_container<event_args_t> on_moved`|Triggered when the logical position or window space position changes; based on the current properties of the source object.|
|`event_container<event_args_t> on_size_changed`|Triggered when the width and height of the rect change.|
|`event_container<pointer_event_args_t> on_pointer_enter`|Triggered when the laser enters the control.|
|`event_container<pointer_event_args_t> on_pointer_leave`|Triggered when the laser leaves the control.|
|`event_container<pointer_event_args_t> on_pointer_move`|Triggered when the laser's pointing on the control changes.|
|`event_container<pointer_event_args_t> on_pointer_down`|Triggered when the laser trigger is pressed.|
|`event_container<pointer_event_args_t> on_pointer_up`|Triggered when the laser trigger is released or a cancellation occurs; "cancelled" indicates whether it was canceled.|
|`event_container<event_args_t> on_click`|Triggered when the control is clicked or activated by default.|
|`event_container<scroll_event_args_t> on_scroll`|Triggered when scrolling input reaches the control.|
|`event_container<event_args_t> on_viewport_changed`|Triggered when the scrolling viewport changes.|
|`event_container<event_args_t> on_focus_in`|Triggered when the control gains keyboard focus.|
|`event_container<event_args_t> on_focus_out`|Triggered when the control loses keyboard focus.|
|`event_container<key_event_args_t> on_key_down`|Triggered when a key is pressed; the parameter includes the key name, modifier key, and consumption state.|
|`event_container<key_event_args_t> on_key_up`|Triggered when a key is released.|
|`explicit control(const u32string &name)`|Construct the object; see the type description for parameters, default states, and constraints.|
|`virtual bool is_focusable() const`|Checks whether the control type can receive focus; actual focus is also affected by visible, enabled, and window modal states.|
|`virtual const rectangle_t &get_rect() const`|Reads the relative logical rectangle of the parent level.|
|`virtual void set_rect(const rectangle_t &value)`|Sets the relative logical rectangle of the parent level.|
|`virtual uint32_t get_background_color() const`|Reads the background color in the format 0xRRGGBBAA.|
|`virtual void set_background_color(uint32_t value)`|Sets the background color in the format 0xRRGGBBAA.|
|`virtual const u32string &get_tooltip_text() const`|Reads the hover prompt; default is an empty string.|
|`virtual void set_tooltip_text(const u32string &value)`|Sets the hover prompt.|
|`event_container<event_args_t> on_tooltip_text_changed`|Triggered when the prompt text changes.|
|`virtual bool get_visible() const`|Reads the visible state.|
|`virtual void set_visible(bool value)`|Sets the visible state.|
|`virtual bool get_enabled() const`|Read interactive status.|
|`virtual void set_enabled(bool value)`|Set interactive status.|
|`virtual uint64_t get_tab_index() const`|Read Tab focus order, default 0.|
|`virtual void set_tab_index(uint64_t value)`|Set Tab focus order, default 0.|
|`~control() override`|Destructs objects, ending their resources or referenced lifetimes.|
|`virtual void show()`|Display controls or windows and trigger corresponding visibility and window lifecycle behaviors.|
|`virtual void hide()`|Hide controls or windows. Related focus, capture, and input areas are released according to window status.|
|`virtual void focus()`|Request to move keyboard focus to this control.|
|`virtual void activate()`|Activate the window to which this object belongs; the window reloading activates itself.|
|`virtual rectangle_t get_absolute_rectangle() const`|Return to the logical rectangle of the control within the window.|
|`virtual bool get_focused() const`|Query whether the control has focus.|
|`virtual std::shared_ptr<window> get_owning_window() const`|Return the window to which the control belongs; return a null pointer if it does not belong to a window.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`rectangle_t rect`|The logical rectangle of the accessible relative parent; use setter for regular assignment to notify changes.|
|`uint32_t background_color = render_style::CONTROL_BACKGROUND_COLOR`|The background color accessible to the derived class, format 0xRRGGBBAA; use setter for regular assignment to notify changes.|
|`bool visible = true`|The visible status accessible to the derived class; use setter for regular assignment to notify changes.|
|`bool enabled = true`|The interactive status accessible to the derived class; use setter for regular assignment to notify changes.|
|`uint64_t tab_index = 0u`|The Tab focus order accessible to the derived class, default 0; use setter for regular assignment to notify changes.|
|`size_t focus_target_index = 0u`|Current internal focus area index, initial 0.|
|`virtual size_t get_focus_target_count() const`|Return the number of internal focusable areas of the control, for composite controls such as numeric buttons and tab arrows to cover.|
|`virtual size_t get_focus_target_index() const`|Read the current internal focus area index.|
|`virtual void set_focus_target_index(size_t value)`|Set the current internal focus area index.|
|`control(const u32string &name, const u32string &type)`|Construct the object; see the type description for parameters, default states, and constraints.|
|`virtual void refresh_layout()`|Refresh the control layout; the base class handling is retained when overridden by derived classes.|
|`virtual rectangle_t get_input_rectangle() const`|Return the input area in the control's local coordinates; by default, the entire control is covered, and derived editing controls can be scaled down to the actual editing area.|
|`virtual double get_content_top() const`|Read the logical top offset of the text start.|
|`void notify_viewport_changed()`|Request a repaint and trigger the `on_viewport_changed` event.|
|`virtual void render(render_context &context) const`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|
|`virtual void render_overlay(render_context &context) const`|Draw the control overlay, such as the combo box pop-up menu.|

### `easyvrui/control/blank.h`

#### `blank`

Declaration: `class blank: public control`.

Name the rectangular placeholder objects. The basic configuration includes a read-only name and a modifiable rect; geometric change events, property change notifications, and object lifecycle interfaces follow the base class. Add to a regular container through get_control_list().add().

|Declaration|Purpose and calling semantics|
|---|---|
|`explicit blank(const u32string &name)`|Construct placeholder objects with unique names, where the name remains fixed during the instance's lifetime.|
|`~blank() override`|End the object's lifecycle.|
|`const u32string &get_name() const`|Inherited name reading interface.|
|`const rectangle_t &get_rect() const`、`void set_rect(const rectangle_t &value)`|Inherited rectangular reading and setting interfaces.|
|`on_moved`、`on_size_changed`|Notify left/top and width/height of changes respectively.|
|`on_property_changed`|Property change notification. Read the name through `event.property_name`, and read the current value from the source control.|
|`on_disposed`、`get_disposed()`、`dispose()`|Object release notification, status, and release entry points.|
|`invalidate()`、`begin_invoke(callback)`|Inherited refresh request and creation thread scheduling interfaces.|

Direct access to visible, enabled, background_color, tab_index, and their corresponding accessors, visibility, focus, activation, and interaction events is restricted to private access. Drawing and input processing are handled by the framework's internal hooks.

Containers and frameworks can still hold references to the regular control base class. When virtual functions are called through the control reference, get_visible(), get_enabled(), and is_focusable() always return false, and the setters for visible and enabled remain in this state. Name, rectangular, geometric events, and lifecycle interfaces remain available.

### `easyvrui/control/text_control.h`

Font and foreground color of text controls.

#### `text_control`

Declaration: `class text_control: public control`.

Base class for font and foreground color, with a protected constructor. The default foreground color is 0xD1DEF0FF, and the font is Segoe UI, size 18, normal font weight, and non-italic. The text content is defined by the specific control.

Inherit all public property access, methods, and events of `control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_foreground_color_changed`|Triggered when the text foreground color changes.|
|`event_container<event_args_t> on_font_changed`|Triggered when the font changes.|
|`virtual uint32_t get_foreground_color() const`|Read the text foreground color in the format 0xRRGGBBAA.|
|`virtual void set_foreground_color(uint32_t value)`|Set the text foreground color in the format 0xRRGGBBAA.|
|`virtual const font_t &get_font() const`|Read the text font.|
|`virtual void set_font(const font_t &value)`|Set the text font.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`uint32_t foreground_color = render_style::TEXT_FOREGROUND_COLOR`|Derivable classes can access the text foreground color in the format 0xRRGGBBAA; regular assignments use setters to generate change notifications.|
|`font_t font`|Derivable classes can access the text font; regular assignments use setters to generate change notifications.|
|`text_control(const u32string &name, const u32string &type)`|Construct the object; see the type description for parameters, default states, and constraints.|

### `easyvrui/control/container_control.h`

Base class for accommodating sub-controls and unified container access interfaces.

#### `container_control`

Declaration: `class container_control: public control`.

Container base class, with a protected constructor. get_control_list() returns a live control_collection, managing elements, name indices, and ownership. Ordinary containers operate through this collection; tabcontrol exposes an independent page_list for application management pages.

Inherit all public property access, methods, and events of `control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<control_collection_event_args_t> on_control_added`|Triggered when adding a child control, including the control object `item` and index `index`.|
|`event_container<control_collection_event_args_t> on_control_removed`|Triggered when removing a child control, including the control object `item` and index `index`.|
|`virtual control_collection &get_control_list()`|Returns a directly operable collection belonging to the container; can be queried, indexed, added, inserted, removed, and cleared. const overload provides read-only access to the collection.|
|`virtual const control_collection &get_control_list() const`|Returns a directly operable collection belonging to the container; can be queried, indexed, added, inserted, removed, and cleared. const overload provides read-only access to the collection.|
|`virtual std::vector<control *> get_active_item_list() const`|Returns a list of direct controls currently involved in display and interaction.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`container_control(const std::u32string &name, const std::u32string &type)`|Construct the object; see the type description for parameters, default states, and constraints.|
|`virtual void validate_control(const control &item) const`|Checks the element type and additional constraints of the container before insertion; throws an exception if failed, keeping the collection unchanged.|
|`virtual void notify_control_added(control &item, size_t index)`|Notifies the container when an element is added, with index being the actual collection index.|
|`virtual void notify_control_removed(control &item, size_t index)`|Notifies the container when an element is removed, with index being the actual index before removal.|
|`virtual void notify_control_list_cleared()`|Notifies the container when the collection is completely cleared.|
|`virtual std::vector<control *> get_active_control_list() const`|Returns the element currently involved in display and interaction; derived containers can filter out inactive pages.|
|`virtual bool is_control_active(const control &item) const`|Determines whether a specified element is involved in the current display and interaction of the container.|
|`virtual std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const`|Returns the rectangular area arranged by the container; nullopt indicates using the element's own rectangular area.|
|`virtual std::optional<int64_t> get_selection_index_at(double left, double top, const rectangle_t &rectangle) const`|Determines the selection index based on the local position and container's rectangular area; returns nullopt if not found.|

### `easyvrui/control/control_collection.h`

A control container with ordered and named indices.

#### `control_collection`

Declaration: `class control_collection`.

It holds ordered child controls, with unique names within the current container. The index starts at 0; inserts are added at the end of the list. Querying by name takes an average of O(1), while getting elements by position also takes O(1). Inserting and removing elements requires moving the ordered items. Reference overloading does not take over when the object is destroyed; the caller ensures that the object lasts longer than the reference in the container. shared_ptr overloading retains shared ownership. The remove method terminates the parent relationship and returns the object. When adding a reference, the return value may not actually own the object. Sharing pointers will fail if they are empty, have the same name, already have a parent, or form a cycle.

|Declaration|Purpose and calling semantics|
|---|---|
|`explicit control_collection(container_control &owner)`|Construct this type of instance; see the type description and signature for parameter meanings.|
|`virtual ~control_collection()`|Destructs objects, ending their resources or referenced lifetimes.|
|`size_t get_size() const`|Returns the number of items in the collection.|
|`bool is_empty() const`|Queries whether the control collection is empty.|
|`bool contains(const control &item) const`|Searches for a specified control by instance.|
|`bool contains(const u32string &name) const`|Searches for a control by name.|
|`control &get_control(size_t index) const`|Returns a control reference by index or name; throws an exception if not found.|
|`control &get_control(const u32string &name) const`|Returns a control reference by index or name; throws an exception if not found.|
|`size_t get_index(const control &item) const`|Returns the 0-based position of an object or text in the collection; throws an exception if not found.|
|`const vector<control *> &get_item_list() const`|Returns a read-only ordered list of the current collection; the validity of this reference changes with the lifecycle of the container and subsequent modifications.|
|`virtual void insert(size_t index, control &item)`|Inserts at the index position; appends if the index is not less than the current quantity. See the container's description for specific element types, ownership, and duplicate name constraints.|
|`virtual void insert(size_t index, std::shared_ptr<control> item)`|Inserts at the index position; appends if the index is not less than the current quantity. See the container's description for specific element types, ownership, and duplicate name constraints.|
|`void add(control &item)`|Append items; the caller ensures the object reference survives, while shared_ptr retains shared ownership.|
|`void add(std::shared_ptr<control> item)`|Append items; the caller ensures the object reference survives, while shared_ptr retains shared ownership.|
|`virtual std::shared_ptr<control> remove(size_t index)`|Remove the specified element and return its shared_ptr; share the reference when added, and return the reference without taking over or destroying it when added.|
|`std::shared_ptr<control> remove(control &item)`|Remove the specified element and return its shared_ptr; share the reference when added, and return the reference without taking over or destroying it when added.|
|`std::shared_ptr<control> remove(const u32string &name)`|Remove the specified element and return its shared_ptr; share the reference when added, and return the reference without taking over or destroying it when added.|
|`virtual void clear()`|Remove all controls from the collection.|
|`control &operator[](size_t index) const`|Obtain an object reference starting from position 0 or by name, with behavior consistent with get_control/get_page.|
|`control &operator[](const u32string &name) const`|Obtain an object reference starting from position 0 or by name, with behavior consistent with get_control/get_page.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`container_control &get_owner() const`|Return the reference to the container where the collection belongs.|
|`void release_control_list() noexcept`|Release the references held by the collection for use during the destructor phase of derived collections.|
|`virtual void notify_control_added(control &item, size_t index)`|Addition notification for derived collections: the item has been added, with index being the actual index.|
|`virtual void notify_control_removed(control &item, size_t index, bool clearing)`|Removal notification for derived collections; clearing indicates this operation comes from clear.|

### `easyvrui/control/panel.h`

Ordinary sub-control panel.

#### `panel`

Declaration: `class panel: public container_control`.

Ordinary content panel, only adding a name construction method, inheriting all public interfaces of container_control.

Inherit all public property access, methods, and events of `container_control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`explicit panel(const u32string &name)`|Construct the object; see the type description for parameters, default states, and constraints.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`panel(const u32string &name, const u32string &type)`|Construct the object; see the type description for parameters, default states, and constraints.|

### `easyvrui/control/selection_control.h`

#### `selection_control`

Declaration: `class selection_control: public text_control`.

Abstract base class for selecting controls in collections, inheriting fonts and foreground colors. Derived classes define item area blank hit and clearing selection. Listbox, TreeView, Grid, and ListView's item blank areas exit text editing, collapse IME/layout, and retain keyboard navigation focus. Clear item selection simultaneously when `clear_selection_on_blank_click` is enabled. Headers, column width adjustment areas, scroll bars, and pop-up options handle clicks separately.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_clear_selection_on_blank_click_changed`|Triggered when the rule for blank click selection changes.|
|`virtual bool get_clear_selection_on_blank_click() const`|Read whether to clear item selection when clicking on the item area blank, default false.|
|`virtual void set_clear_selection_on_blank_click(bool value)`|Set whether to clear item selection when clicking on the item area blank, default false.|
|`virtual bool is_blank_at(double local_left, double local_top) const`|Determine whether the control's local position is blank; the specific item area is determined by the derived class.|
|`virtual void clear_selection() = 0`|Pure virtual function, implemented by the specific collection control to clear selection.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`selection_control(const std::u32string &name, const std::u32string &type)`|Construct an instance; see this type's description for parameters and constraints.|

## Text and item controls

### `easyvrui/control/label.h`

Static text labels.

#### `label`

Declaration: `class label: public text_control`.

Labels inherit from `text_control`, used to display text, with default text being empty.

Inherit all public property access, methods, and events of `text_control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_text_changed`|Triggered when text changes.|
|`explicit label(const u32string &name)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`virtual const u32string &get_text() const`|Read text content.|
|`virtual void set_text(const u32string &value)`|Set text content.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|

### `easyvrui/control/button.h`

Focusable and clickable text buttons.

#### `button`

Declaration: `class button: public text_control`.

Text button, default text is empty, supports focus and on_click; inherits from text_control.

Inherit all public property access, methods, and events of `text_control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_text_changed`|Triggered when text changes.|
|`explicit button(const u32string &name)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`bool is_focusable() const override`|Checks whether the control type can receive focus; actual focus is also affected by visible, enabled, and window modal states.|
|`virtual const u32string &get_text() const`|Read text content.|
|`virtual void set_text(const u32string &value)`|Set text content.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`button(const u32string &name, const u32string &type)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`void render(render_context &context) const override`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|

### `easyvrui/control/textbox.h`

Text input, selection, multi-line, and scroll bar controls.

#### `textbox`

Declaration: `class textbox: public text_control`.

Text input control, default text is empty, selectable=true, read_only = false, max_length = 0, multiline=false, both scroll bars display switches are false, selection start and length are 0. Multiline is retained; single-line mode removes line breaks. Changing max_length will standardize existing text. Font size and layout determine the actual line height, text indexing counts by code points and aligns to character boundaries.

Inherit all public property access, methods, and events of `text_control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_text_changed`|Triggered when text changes.|
|`event_container<event_args_t> on_read_only_changed`|Triggered when read-only state changes.|
|`event_container<event_args_t> on_selectable_changed`|Triggered when text selection settings change.|
|`event_container<event_args_t> on_selection_changed`|Triggered when selection state changes; text editor uses start/length, items and tabs use selected.|
|`event_container<event_args_t> on_max_length_changed`|Triggered when text length limit changes.|
|`event_container<event_args_t> on_multiline_changed`|Triggered when multi-line switch changes.|
|`event_container<event_args_t> on_horizontal_scrollbar_visible_changed`|Triggered when horizontal scroll bar display settings change.|
|`event_container<event_args_t> on_vertical_scrollbar_visible_changed`|Triggered when vertical scroll bar display settings change.|
|`explicit textbox(const u32string &name)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`bool is_focusable() const override`|Checks whether the control type can receive focus; actual focus is also affected by visible, enabled, and window modal states.|
|`virtual const u32string &get_text() const`|Read text content.|
|`virtual void set_text(const u32string &value)`|Set text content.|
|`virtual bool get_read_only() const`|Read-only state for user input; program can still set text.|
|`virtual void set_read_only(bool value)`|Set read-only state for user input; program can still set text.|
|`virtual bool get_selectable() const`|Whether to allow text selection, display cursor, and trigger input interface; if false, still receive control focus.|
|`virtual void set_selectable(bool value)`|Set whether text can be selected; if false, hides cursor, closes input interface, and prevents user editing, but program set_text can still be used.|
|`virtual bool get_multiline() const`|Read multi-line mode, default false.|
|`virtual void set_multiline(bool value)`|Set multi-line mode, default false.|
|`virtual bool get_horizontal_scrollbar_visible() const`|Read horizontal scroll bar display switch.|
|`virtual void set_horizontal_scrollbar_visible(bool value)`|Set horizontal scroll bar display switch.|
|`virtual bool get_vertical_scrollbar_visible() const`|Read vertical scroll bar display status.|
|`virtual void set_vertical_scrollbar_visible(bool value)`|Set vertical scroll bar display status.|
|`virtual uint64_t get_selection_start() const`|Read the code point position of the smaller end of the selection.|
|`virtual uint64_t get_selection_length() const`|Read the number of code points contained in the selection.|
|`virtual void set_selection_start(uint64_t value)`|Set the code point position of the smaller end of the selection.|
|`virtual void set_selection_length(uint64_t value)`|Set the number of code points contained in the selection.|
|`virtual u32string get_selected_text() const`|Read the text copy of the selected area.|
|`virtual bool get_can_undo() const`|Check whether text editing can be undone.|
|`virtual bool get_can_redo() const`|Check if there are any text editing records that can be redone.|
|`virtual bool undo()`|Undo an edit; return true if successful.|
|`virtual bool redo()`|Redo an edit; return true if successful.|
|`virtual void set_selected_text(const u32string &value)`|Replace the current selected area with the value; used as a program modification entry, applicable to the read_only control.|
|`virtual uint64_t get_max_length() const`|Read the maximum number of code points for text; 0 means unlimited; truncate to retain complete characters.|
|`virtual void set_max_length(uint64_t value)`|Set the maximum number of code points for text; 0 means unlimited; truncate to retain complete characters.|
|`virtual void select(uint64_t start, uint64_t length = 0u)`|Select length code points starting from start; default length is 0, meaning place the insertion point.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`virtual uint64_t get_selection_anchor() const`|Read the anchor point of the selected area, retaining the selection direction.|
|`virtual uint64_t get_selection_active() const`|Read the active end of the selected area, i.e., the current insertion point.|
|`virtual void set_selection(uint64_t anchor, uint64_t active)`|Specify the selection range with anchor and active; position is limited to within the text range and aligns character boundaries.|
|`void render(render_context &context) const override`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|
|`void render_overlay(render_context &context) const override`|Draw the control overlay, such as the combo box pop-up menu.|

When the editor has focus, Ctrl+Z undoes text modifications; Ctrl+Y or Ctrl+Shift+Z restores modifications. These keys take precedence over application menu shortcuts.

### `easyvrui/control/item_control.h`

Common base class for item lists, selected items, and line scrolling.

#### `item_control`

Declaration: `class item_control: public selection_control`.

Base class for item controls, with a protected constructor, inheriting from selection_control. Default values: items are empty, selected_index = -1, scroll_offset = 0, row_height = 32. selected_item is a read-only u32string; returns an empty string if no selected items. The access interface for scroll_offset is protected.

Inherit all public property access, methods, and events of `selection_control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`item_collection item_list`|Text item container; modifications are notified to the associated item control.|
|`event_container<event_args_t> on_item_list_changed`|Triggered when the text item list changes.|
|`event_container<event_args_t> on_selection_changed`|Triggered when selection state changes; text editor uses start/length, items and tabs use selected.|
|`event_container<event_args_t> on_selected_index_changed`|Triggered when the selected index changes.|
|`event_container<event_args_t> on_row_height_changed`|Triggered when the line height changes.|
|`bool is_focusable() const override`|Checks whether the control type can receive focus; actual focus is also affected by visible, enabled, and window modal states.|
|`const item_collection &get_item_list() const`|Read an ordered string collection.|
|`item_collection &get_item_list()`|Obtain a modifiable collection and replace content through `assign(value)`.|
|`virtual int64_t get_selected_index() const`|Read the current selected index; -1 indicates no selection.|
|`virtual void set_selected_index(int64_t value)`|Set the current selected index; -1 indicates no selection.|
|`void clear_selection() override`|Clear the selection; selected_index becomes -1, and selected_item returns an empty string.|
|`virtual u32string get_selected_item() const`|Read the selected text; return an empty string if no items are selected.|
|`virtual uint64_t get_row_height() const`|Read the row height of an item, in logical units and must be greater than 0.|
|`virtual void set_row_height(uint64_t value)`|Set the row height of an item, in logical units and must be greater than 0.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`int64_t selected_index = NO_SELECTION_INDEX`|The index of the currently selected item that is accessible to the derived class; -1 indicates no selection. For regular assignments, use a setter to notify of changes.|
|`uint64_t scroll_offset = 0u`|The index offset of the first displayed item that is accessible to the derived class; for regular assignments, use a setter to notify of changes.|
|`uint64_t row_height = render_style::DEFAULT_ROW_HEIGHT`|The row height of an item that is accessible to the derived class, in logical units and must be greater than 0; for regular assignments, use a setter to notify of changes.|
|`virtual bool get_vertical_scrollbar_visible() const`|The derived class queries whether a vertical scroll bar is displayed, returning false by default.|
|`void refresh_layout() override`|Refresh the control layout; the base class handling is retained when overridden by derived classes.|
|`virtual void refresh_item_list()`|The refresh entry for the derived class after the item content changes.|
|`virtual void notify_selection_changed(int64_t previous_index, const u32string &previous_item, int64_t next_index, const u32string &next_item)`|Notifies of changes in selection, providing the original index/text and the new index/text.|
|`virtual void notify_item_list_changed(const vector<u32string> &previous, int64_t previous_index, const u32string &previous_item, uint64_t previous_scroll)`|Notifies of changes in the item list, providing the original list, original selection, and original scroll position.|
|`virtual uint64_t get_scroll_offset() const`|Read the index offset of the first displayed item.|
|`virtual void set_scroll_offset(uint64_t value)`|Set the index offset of the first displayed item.|
|`item_control(const u32string &name, const u32string &type)`|Construct the object; see the type description for parameters, default states, and constraints.|
|`virtual uint64_t get_maximum_scroll_offset() const`|Return the maximum first-line offset allowed by the current item control.|
|`virtual uint64_t get_visible_item_count() const`|Return the row capacity of the current viewport for items.|
|`void reveal_item(uint64_t index)`|Scroll to the position where the specified item can be displayed, while retaining the existing positions where the item can still be displayed.|
|`virtual void handle_item_list_changed(const vector<u32string> &previous)`|Process changes in the item list and adjust the current selection and display.|
|`virtual void render_item_list(render_context &context, const render_rectangle_t &rectangle) const`|Draw the currently visible item within a rectangle.|

### `easyvrui/control/item_collection.h`

An ordered text item container.

#### `item_collection`

Declaration: `class item_collection`.

An ordered Unicode text item container that allows duplicate text. Operate on the first matching item by text get_index/remove; throw an exception if it does not exist or the position is out of bounds. Append when inserting goes beyond the end. Modifications to the list will synchronize the selection and drawing state of the associated item_control.

|Declaration|Purpose and calling semantics|
|---|---|
|`explicit item_collection(item_control &owner)`|Construct this type of instance; see the type description and signature for parameter meanings.|
|`void add(const u32string &item)`|Append items; the caller ensures the object reference survives, while shared_ptr retains shared ownership.|
|`void insert(size_t index, const u32string &item)`|Inserts at the index position; appends if the index is not less than the current quantity. See the container's description for specific element types, ownership, and duplicate name constraints.|
|`u32string remove(size_t index)`|Remove an item at the position, object, or name specified by a parameter; return the removed object or whether it was successful. See the signature for the specific return type.|
|`u32string remove(const u32string &item)`|Remove an item at the position, object, or name specified by a parameter; return the removed object or whether it was successful. See the signature for the specific return type.|
|`void clear()`|Remove all text items from the collection.|
|`void assign(const vector<u32string> &item_list)`|Replace the text item list entirely with item_list and update the selection and display state.|
|`size_t get_size() const`|Returns the number of items in the collection.|
|`bool is_empty() const`|Query whether the text item collection is empty.|
|`bool contains(const u32string &item) const`|Query whether there is a text in the collection that matches `item`.|
|`const u32string &get_item(size_t index) const`|Read-only reference to item text by index; throws an exception when out of bounds.|
|`const u32string &operator[](size_t index) const`|Const reference to item text starting at position 0; throws an exception when out of bounds.|
|`size_t get_index(const u32string &item) const`|Returns the 0-based position of an object or text in the collection; throws an exception if not found.|
|`const vector<u32string> &get_item_list() const`|Returns a read-only ordered list of the current collection; the validity of this reference changes with the lifecycle of the container and subsequent modifications.|

### `easyvrui/control/combobox.h`

Combo box for list selection and optional text editing.

#### `combobox`

Declaration: `class combobox: public item_control`.

Inherit all public property access, methods, and events of `item_control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_dropdown_style_changed`|Triggered when dropdown style changes.|
|`event_container<event_args_t> on_text_changed`|Triggered when text changes.|
|`explicit combobox(const u32string &name)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`virtual const u32string &get_text() const`|Read text content.|
|`virtual void set_text(const u32string &value)`|Set text content.|
|`virtual combobox_dropdown_style_t get_dropdown_style() const`|Reads the dropdown style, defaulting to dropdown_list.|
|`virtual void set_dropdown_style(combobox_dropdown_style_t value)`|Sets dropdown to allow free input, setting it to dropdown_list for list selection.|
|`virtual bool get_dropped_down() const`|Reads whether the dropdown list is expanded.|
|`virtual void set_dropped_down(bool value)`|Expands or collapses the dropdown list.|
|`void set_selected_index(int64_t value) override`|Set the current selected index; -1 indicates no selection.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void refresh_item_list() override`|Synchronizes selected text, dropdown list, and layout.|
|`void handle_item_list_changed(const vector<u32string> &previous) override`|Process changes in the item list and adjust the current selection and display.|
|`void render(render_context &context) const override`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|
|`void render_overlay(render_context &context) const override`|Draw the control overlay, such as the combo box pop-up menu.|

### `easyvrui/control/listbox.h`

Scrollable single-choice list.

#### `listbox`

Declaration: `class listbox: public item_control`.

Inherits from item_control, with a default line height of 30; provides vertical scroll bars when content exceeds the visible lines. get_vertical_scrollbar_visible() is a read-only calculation state. The joystick of the corresponding laser controller allows scrolling of the list, with the amount of scrolling varying with the degree of deflection.

Inherit all public property access, methods, and events of `item_control`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`explicit listbox(const u32string &name)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`bool is_blank_at(double local_left, double local_top) const override`|Determines whether the local position is blank in the list content area.|
|`virtual bool get_vertical_scrollbar_visible() const`|Calculates whether there are vertical items beyond the visible area; returns false if insufficient content.|
|`void set_visible(bool value) override`|Sets the visible state; clears ongoing interactions when hidden.|
|`void set_enabled(bool value) override`|Sets the operable state; clears ongoing interactions when disabled.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void refresh_layout() override`|Refresh the control layout; the base class handling is retained when overridden by derived classes.|
|`uint64_t get_maximum_scroll_offset() const override`|Return the maximum first-line offset allowed by the current item control.|
|`void render(render_context &context) const override`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|

## Extended control

### `easyvrui/control/checkbox.h`

#### `checkbox`

Declaration: `class checkbox: public text_control`.

Checkbox, with default text empty and checked=false. Click or press Space/Enter to toggle checked; text appearance inherits from text_control.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_text_changed`|Triggered when text changes.|
|`event_container<event_args_t> on_checked_changed`|Triggered when the checked state changes.|
|`explicit checkbox(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`bool is_focusable() const override`|Checks whether the control has focus capability; actual focus is also limited by visible, enabled, and modal relationships.|
|`virtual const std::u32string &get_text() const`|Reads the displayed text.|
|`virtual void set_text(const std::u32string &value)`|Sets the displayed text.|
|`virtual bool get_checked() const`|Reads the current checked state.|
|`virtual void set_checked(bool value)`|Sets the current checked state.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|

### `easyvrui/control/radiobutton.h`

#### `radiobutton`

Declaration: `class radiobutton: public text_control`.

Radio buttons have a default value where text is empty and checked is false. Radio buttons within the same container are mutually exclusive. set_checked (true) will disable any other radio buttons of the same level. Independent groups can be created using panels. Click or press Space/Enter to select an option.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_text_changed`|Triggered when text changes.|
|`event_container<event_args_t> on_checked_changed`|Triggered when the checked state changes.|
|`explicit radiobutton(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`bool is_focusable() const override`|Checks whether the control has focus capability; actual focus is also limited by visible, enabled, and modal relationships.|
|`virtual const std::u32string &get_text() const`|Reads the displayed text.|
|`virtual void set_text(const std::u32string &value)`|Sets the displayed text.|
|`virtual bool get_checked() const`|Reads the current checked state.|
|`virtual void set_checked(bool value)`|Sets the current checked state.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|

### `easyvrui/control/numericupdown.h`

#### `numericupdown`

Declaration: `class numericupdown: public text_control`.

Numerical input and up/down adjustment buttons. value/minimum/maximum/step is double, with default values 0.0/0.0/100.0/1.0; decimal_places is uint32_t, with default value 0, range 0 to 17, controlling the number of decimal places. The boundaries must be finite, with minimum<maximum, and step must be a finite positive number; values are limited within the boundaries. The up and down buttons have hover and focus states, and clicking on them keeps the value editing area closed.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_value_changed`|Triggered when the current value changes.|
|`event_container<event_args_t> on_minimum_changed`|Triggered when the lower limit changes.|
|`event_container<event_args_t> on_maximum_changed`|Triggered when the upper limit changes.|
|`event_container<event_args_t> on_step_changed`|Triggered when the step size changes.|
|`event_container<event_args_t> on_decimal_places_changed`|Triggered when the number of decimal places changes.|
|`explicit numericupdown(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`bool is_focusable() const override`|Checks whether the control has focus capability; actual focus is also limited by visible, enabled, and modal relationships.|
|`virtual double get_value() const`|Reads the current value; setter handles according to the type's boundaries.|
|`virtual void set_value(double next)`|Sets the current value; setter handles according to the type's boundaries.|
|`virtual double get_minimum() const`|Reads the lower boundary of the value range.|
|`virtual void set_minimum(double next)`|Sets the lower boundary of the value range.|
|`virtual double get_maximum() const`|Reads the upper boundary of the value range.|
|`virtual void set_maximum(double next)`|Sets the upper boundary of the value range.|
|`virtual double get_step() const`|Reads the finite positive step size for each adjustment of the up/down buttons.|
|`virtual void set_step(double next)`|Sets the finite positive step size for each adjustment of the up/down buttons.|
|`virtual uint32_t get_decimal_places() const`|Reads the number of decimal places for display, with range 0 to 17.|
|`virtual void set_decimal_places(uint32_t next)`|Sets the number of decimal places for display, with range 0 to 17.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`size_t get_focus_target_count() const override`|Returns the number of internally focusable areas for focus navigation in composite controls.|
|`virtual size_t get_focus_target_at(double left, double top) const`|Gets the index of the internal focus area based on the control's local coordinates.|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|
|`void render_overlay(render_context &context) const override`|Derives the drawing entry; uses context to draw the floating layer.|

### `easyvrui/control/slider.h`

#### `slider`

Declaration: `class slider: public control`.

Slider can be dragged. Minimum, maximum, and value are all int64_t, with default values 0, 100, 0, requiring minimum<maximum; set_value limits input within the range, and modifying the boundaries also converges the current value. The direction is specified by `orientation_t`, with default `orientation_t::horizontal`, or can be set to `orientation_t::vertical`. The direction keys increase or decrease values by integers 1, with the top corresponding to maximum.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_minimum_changed`|Triggered when the lower limit changes.|
|`event_container<event_args_t> on_maximum_changed`|Triggered when the upper limit changes.|
|`event_container<event_args_t> on_value_changed`|Triggered when the current value changes.|
|`event_container<event_args_t> on_orientation_changed`|Triggered when the direction changes.|
|`event_container<event_args_t> on_drag_start`|Triggered when dragging starts.|
|`event_container<interaction_end_event_args_t> on_drag_end`|Triggered when dragging ends or is canceled.|
|`explicit slider(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`bool is_focusable() const override`|Checks whether the control has focus capability; actual focus is also limited by visible, enabled, and modal relationships.|
|`virtual int64_t get_minimum() const`|Reads the lower boundary of the value range.|
|`virtual void set_minimum(int64_t next)`|Sets the lower boundary of the value range.|
|`virtual int64_t get_maximum() const`|Reads the upper boundary of the value range.|
|`virtual void set_maximum(int64_t next)`|Sets the upper boundary of the value range.|
|`virtual int64_t get_value() const`|Reads the current value; setter handles according to the type's boundaries.|
|`virtual void set_value(int64_t next)`|Sets the current value; setter handles according to the type's boundaries.|
|`virtual orientation_t get_orientation() const`|Read the layout direction. Allowable values and meanings are described in this type's documentation.|
|`virtual void set_orientation(orientation_t next)`|Set the layout direction. Allowable values and meanings are described in this type's documentation.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|

### `easyvrui/control/progressbar.h`

#### `progressbar`

Declaration: `class progressbar: public control`.

Integer progress display. minimum, maximum, and value are all set to int64_t, with default values being 0, 100, and 0 respectively. If minimum < maximum, set_value will limit the input within the range, adjusting the current value when boundaries are modified.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_minimum_changed`|Triggered when the lower limit changes.|
|`event_container<event_args_t> on_maximum_changed`|Triggered when the upper limit changes.|
|`event_container<event_args_t> on_value_changed`|Triggered when the current value changes.|
|`explicit progressbar(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`virtual int64_t get_minimum() const`|Reads the lower boundary of the value range.|
|`virtual void set_minimum(int64_t next)`|Sets the lower boundary of the value range.|
|`virtual int64_t get_maximum() const`|Reads the upper boundary of the value range.|
|`virtual void set_maximum(int64_t next)`|Sets the upper boundary of the value range.|
|`virtual int64_t get_value() const`|Reads the current value; setter handles according to the type's boundaries.|
|`virtual void set_value(int64_t next)`|Sets the current value; setter handles according to the type's boundaries.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|

### `easyvrui/control/image.h`

#### `image`

Declaration: `class image: public control`.

Image control. source is set to `shared_ptr<const drawing_image>`, with a default value of empty. When set to `stretch_mode`, it uses `image_stretch_mode_t`, with a default value of `contain`. `fill`, `contain`, `cover`, and `none` represent filling, full proportion display, covering and cutting, and maintaining the original pixel size, respectively.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_source_changed`|Triggered when the image source changes.|
|`event_container<event_args_t> on_stretch_mode_changed`|Triggered when the stretching method changes.|
|`event_container<event_args_t> on_source_unavailable`|Triggered when image resources are unavailable.|
|`explicit image(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`virtual const std::shared_ptr<const drawing_image> &get_source() const`|Read the shared reference of image resources. nullptr indicates clearing.|
|`virtual void set_source(std::shared_ptr<const drawing_image> value)`|Set the shared reference of image resources. nullptr indicates clearing.|
|`virtual image_stretch_mode_t get_stretch_mode() const`|Read the image stretching mode: fill, contain, cover, or none.|
|`virtual void set_stretch_mode(image_stretch_mode_t value)`|Set the image stretching mode: fill, contain, cover, or none.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|

### `easyvrui/control/screen.h`

#### `screen`

Declaration: `class screen: public control`.

Real-time monitor screen control. screen_id is equivalent to uint64_t, with a default value of 0. Numbers correspond to the monitor enumeration provided by the current engine. For split-screen, use set_screen_id. The control's rectangle determines the logical display size; setting it to the screen pixel size will display according to the same logical size. The actual space size is still affected by the window physical_scale. get_screen_available provides available status.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_screen_id_changed`|Triggered when the monitor changes.|
|`event_container<event_args_t> on_screen_unavailable`|Triggered when monitor capture becomes unavailable.|
|`event_container<event_args_t> on_screen_restored`|Triggered when monitor capture is restored.|
|`explicit screen(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`virtual uint64_t get_screen_id() const`|Read the monitor number.|
|`virtual void set_screen_id(uint64_t value)`|Set the monitor number.|
|`virtual bool get_screen_available() const`|Read whether the current monitor capture is available.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|

### `easyvrui/control/scrollpanel.h`

#### `scrollpanel`

Declaration: `class scrollpanel: public container_control`.

Scrollable container, with content added through get_control_list(). horizontal_scrollbar_visible and vertical_scrollbar_visible are set to true by default. The scroll bar and viewport are arranged based on the content range. The scroll offset access interface is protected, and applications operate through control layout and scroll input.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_horizontal_scrollbar_visible_changed`|Triggered when horizontal scroll bar display settings change.|
|`event_container<event_args_t> on_vertical_scrollbar_visible_changed`|Triggered when vertical scroll bar display settings change.|
|`explicit scrollpanel(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`virtual bool get_horizontal_scrollbar_visible() const`|Read whether to display a horizontal scroll bar.|
|`virtual void set_horizontal_scrollbar_visible(bool value)`|Set whether to display a horizontal scroll bar.|
|`virtual bool get_vertical_scrollbar_visible() const`|Read whether to display a vertical scroll bar.|
|`virtual void set_vertical_scrollbar_visible(bool value)`|Set whether to display a vertical scroll bar.|
|`void set_visible(bool value) override`|Sets the visible state; clears ongoing interactions when hidden.|
|`void set_enabled(bool value) override`|Set whether it can be operated.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void refresh_layout() override`|Refresh the control layout; the base class handling is retained when overridden by derived classes.|
|`void notify_control_added(control &child, size_t index) override`|Container notification after insertion, where the index is the actual collection index of the element.|
|`void notify_control_removed(control &child, size_t index) override`|Container notification after removal, where the index is the actual collection index before removal.|
|`virtual uint64_t get_horizontal_scroll_offset() const`|Reading the horizontal logical scroll offset for derived classes.|
|`virtual void set_horizontal_scroll_offset(uint64_t value)`|Setting the horizontal logical scroll offset for derived classes, limited within the content range.|
|`virtual uint64_t get_vertical_scroll_offset() const`|Reading the vertical logical scroll offset for derived classes.|
|`virtual void set_vertical_scroll_offset(uint64_t value)`|Setting the vertical logical scroll offset for derived classes, limited within the content range.|
|`virtual uint64_t get_maximum_vertical_scroll_offset() const`|Reading the upper limit of vertical logical scroll for derived classes.|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|Providing a rectangular container management for elements; nullopt indicates using its own rectangular area.|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|
|`void render_overlay(render_context &context) const override`|Derives the drawing entry; uses context to draw the floating layer.|

### `easyvrui/control/splitter.h`

#### `splitter`

Declaration: `class splitter: public container_control`.

Dual-zone container division, arranging up to two controls in the order of get_control_list(). The default direction is `orientation_t::vertical`, dividing the left and right regions with a vertical separator. `orientation_t::horizontal` divides the upper and lower regions with a horizontal separator. split_position is a limited double, ranging from 0.0 to 1.0, with a default value of 0.5.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_orientation_changed`|Triggered when the direction changes.|
|`event_container<event_args_t> on_split_position_changed`|Trigger when the separation position changes.|
|`event_container<event_args_t> on_split_start`|Trigger when starting to drag the separator bar.|
|`event_container<interaction_end_event_args_t> on_split_end`|Trigger when ending to drag the separator bar.|
|`explicit splitter(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`virtual orientation_t get_orientation() const`|Read the layout direction. Allowable values and meanings are described in this type's documentation.|
|`virtual void set_orientation(orientation_t value)`|Set the layout direction. Allowable values and meanings are described in this type's documentation.|
|`virtual double get_split_position() const`|Reading the proportion of available space occupied by the first region, ranging from 0.0 to 1.0.|
|`virtual void set_split_position(double value)`|Setting the proportion of available space occupied by the first region, ranging from 0.0 to 1.0.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void validate_control(const control &child) const override`|Verifying conditions for ordinary containers and limiting up to two region controls.|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|Providing a rectangular container management for elements; nullopt indicates using its own rectangular area.|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|

## Multiple columns and tree controls

### `easyvrui/control/grid.h`

#### `grid_column_t`

Declaration: `struct grid_column_t`.

Table column definition: text as the title, width defaulting to 100, editable defaulting to true. When adding columns to the grid or modifying column width, it must be positive; the total width must be represented by int64_t. If failed, the original column and width will be retained.

|Declaration|Purpose and calling semantics|
|---|---|
|`static constexpr uint64_t DEFAULT_WIDTH = 100u`|Default column width is 100 logical pixels.|
|`std::u32string text`|Header text.|
|`uint64_t width = DEFAULT_WIDTH`|Positive integer column width, defaulting to DEFAULT_WIDTH.|
|`bool editable = true`|Whether this column allows user editing, defaulting to true.|

#### `grid_cell_t`

Declaration: `struct grid_cell_t`.

Recording rows and columns with uint64_t, both starting from 0; equality comparison is performed based on two fields.

|Declaration|Purpose and calling semantics|
|---|---|
|`uint64_t row = 0u`|0 starting row index.|
|`uint64_t column = 0u`|0 starting column index.|
|`bool operator==(const grid_cell_t &) const = default`|Compare row and column positions field by field.|

#### `grid_selection_mode_t`

Declaration: `enum class grid_selection_mode_t`.

"cell" indicates cell selection, "row" indicates selection of the entire row.

|Declaration|Purpose and calling semantics|
|---|---|
|`cell`|Select cell by cell.|
|`row`|Select the entire row.|

#### `grid_cell_render_t`

Declaration: `struct grid_cell_render_t`.

Data record passed to the cell drawing callback, including cell position, drawn rectangle, value, and selection/hover/editing status.

|Declaration|Purpose and calling semantics|
|---|---|
|`grid_cell_t cell`|Current row and column position.|
|`render_rectangle_t rectangle`|Drawn rectangle of the current cell.|
|`grid_value_t value`|Cell value.|
|`bool selected = false`|Whether selected.|
|`bool hovered = false`|Whether pointed to.|
|`bool editing = false`|Whether being edited.|

#### `grid`

Declaration: `class grid: public selection_control`.

Editable two-dimensional table. Default: columns empty, number of rows 0, selection_mode = cell, multi_select = false, selected_index = -1, row_height = 30, header_height = 32, read_only = false. header_height = 0 hides the header. Column width defaults to 100; exceptions occur when width=0 is set during insertion or modification, and when the total width exceeds limits. Original data remains unchanged during changes. The public interface manages the table through cell, external data callbacks, and editing validation; scroll offset is handled by the protected extension interface.

Header background covers the entire visible width, ellipsis are displayed at the end of long titles. In entity keyboard capture mode, Ctrl-click switches items, Shift-extends selection; the extend/toggle parameter of explicit select_cell can be controlled by the application for selection. begin_edit and commit_edit return success or failure, failure details can be read from get_edit_error; when editing ends, IME/layout corresponds to the visible rectangle of the current cell.

grid_value_t is a variant of <u32string, int64_t, double, bool>. value_provider_t reads the specified row and column; value_writer_t attempts to write and returns failure details via error; cell_renderer_t receives render_context and grid_cell_render_t; edit_validator_t checks cells and values before submission.

|Declaration|Purpose and calling semantics|
|---|---|
|`using value_provider_t = std::function<grid_value_t(uint64_t, uint64_t)>`|External data reading callback, with parameters being row and column, returning grid_value_t.|
|`using value_writer_t = std::function<bool(uint64_t, uint64_t, const grid_value_t &, std::u32string &)>`|External writing callback, with parameters being row, column, value to write, and error message, returning bool.|
|`using cell_renderer_t = std::function<void(render_context &, const grid_cell_render_t &)>`|Visible cell drawing callback, receiving render_context and cell drawing records.|
|`using edit_validator_t = std::function<bool(grid_cell_t, const grid_value_t &, std::u32string &)>`|Editing submission validation, with parameters being cell position, value, and error message, returning bool.|
|`event_container<event_args_t> on_column_list_changed`|Triggered when column definition changes.|
|`event_container<grid_column_event_args_t> on_column_width_changed`|Triggered when column width changes.|
|`event_container<grid_column_event_args_t> on_column_click`|Triggered when clicking on column header.|
|`event_container<event_args_t> on_selection_changed`|Triggered when selection status changes.|
|`event_container<grid_cell_event_args_t> on_cell_double_click`|Triggered when double-clicking on a cell.|
|`event_container<grid_cell_event_args_t> on_cell_value_changed`|Triggered when cell value changes.|
|`event_container<event_args_t> on_row_height_changed`|Triggered when the line height changes.|
|`event_container<event_args_t> on_header_height_changed`|Triggered when the header height changes.|
|`event_container<grid_cell_event_args_t> on_edit_started`|Triggered when cell editing starts.|
|`event_container<grid_cell_event_args_t> on_edit_committed`|Triggered when cell editing is successfully submitted.|
|`event_container<grid_cell_event_args_t> on_edit_cancelled`|Triggered when cell editing is cancelled.|
|`event_container<grid_cell_event_args_t> on_edit_failed`|Triggered when submitting cell edits fails.|
|`explicit grid(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`~grid() override`|Destructor instance is called, releasing resources and references held by the object.|
|`bool is_focusable() const override`|Checks whether the control has focus capability; actual focus is also limited by visible, enabled, and modal relationships.|
|`virtual const std::vector<grid_column_t> &get_column_list() const`|Returns the read-only reference defined by the current column.|
|`virtual void set_column_list(std::vector<grid_column_t> value)`|Replace the column definition entirely; the width must be positive and the total width can be represented by int64_t. If the verification fails, keep the original column.|
|`virtual uint64_t get_row_count() const`|Reads the total number of rows, initially 0.|
|`virtual void set_row_count(uint64_t value)`|Sets the number of rows and adjusts the selection to a valid range based on the viewport.|
|`virtual grid_value_t get_cell_value(uint64_t row, uint64_t column) const`|Reads the values of the specified row and column. Throws an exception if the index is out of range.|
|`virtual void set_cell_value(uint64_t row, uint64_t column, grid_value_t value)`|Calls the current data writing interface to update the specified cell. Throws an exception with an error message if it fails.|
|`virtual void set_data_provider(uint64_t row_count, value_provider_t reader, value_writer_t writer = {})`|Associate with an external data source; the reader must be valid. If the writer is empty, it indicates the data source is read-only. row_count is the current total number of rows.|
|`virtual void set_cell_renderer(cell_renderer_t renderer)`|Configure the drawing callback for visible cells; an empty callback reverts to the default drawing.|
|`virtual void set_edit_validator(edit_validator_t validator)`|Configure user editing submission verification; if false is returned, preserve the editing state and provide an error.|
|`virtual void refresh_data()`|Refresh the cache, layout, and display after external data changes.|
|`static std::u32string get_value_text(const grid_value_t &value)`|Convert grid_value_t to text for cell display.|
|`virtual std::optional<grid_cell_t> get_cell_at(double local_left, double local_top) const`|Map the control's local coordinates to cells; return nullopt for headers, scroll bars, and empty areas.|
|`virtual render_rectangle_t get_cell_rectangle(uint64_t row, uint64_t column) const`|Reads the logical drawing rectangle of the specified cell.|
|`virtual grid_selection_mode_t get_selection_mode() const`|Reads the cell or whole row selection mode.|
|`virtual void set_selection_mode(grid_selection_mode_t value)`|Sets the cell or row selection mode.|
|`virtual bool get_multi_select() const`|Reads the multi-selection switch, defaulting to false.|
|`virtual void set_multi_select(bool value)`|Enable or disable multi-selection.|
|`virtual const std::vector<grid_cell_t> &get_selected_cell_list() const`|Returns an ordered read-only list of the currently selected cells.|
|`virtual bool get_cell_selected(uint64_t row, uint64_t column) const`|Determine whether the specified row and column belong to the current selection.|
|`virtual void select_cell(uint64_t row, uint64_t column, bool extend = false, bool toggle = false)`|Select the specified row and column; extend the scope, toggle the selection, default is false for both.|
|`void clear_selection() override`|Clear the current cell or entire row selection.|
|`bool is_blank_at(double local_left, double local_top) const override`|Determine whether the local coordinates belong to the blank area of the project, used for click selection rules in blank areas.|
|`virtual int64_t get_selected_index() const`|Return the current row index, -1 indicates no selection.|
|`virtual void set_selected_index(int64_t value)`|Select the specified valid row, -1 clears the selection.|
|`virtual uint64_t get_row_height() const`|Read the positive integer row height, default is 30.|
|`virtual void set_row_height(uint64_t value)`|Set the positive integer row height.|
|`virtual uint64_t get_header_height() const`|Read the table header height, default is 32.|
|`virtual void set_header_height(uint64_t value)`|Set the table header height; 0 hides the table header.|
|`virtual uint64_t get_visible_row_count() const`|Return the number of rows visible in the current viewport.|
|`virtual bool get_vertical_scrollbar_visible() const`|Query the visibility of the vertical scroll bar calculated based on content range.|
|`virtual bool get_horizontal_scrollbar_visible() const`|Query the visibility of the horizontal scroll bar calculated based on content range.|
|`virtual void set_column_width(uint64_t column, uint64_t value)`|Set the positive width of an existing column; throw an exception if the index, width, or total width is invalid, the original value and event state remain unchanged.|
|`virtual bool get_read_only() const`|Read the read-only switch for all table users, default is false.|
|`virtual void set_read_only(bool value)`|Control user editing; true ends editing and keeps the cell visible.|
|`virtual bool get_editing() const`|Whether there is a cell being edited.|
|`virtual std::optional<grid_cell_t> get_edit_cell() const`|Return the current editing cell; nullopt when not edited.|
|`virtual const std::u32string &get_edit_text() const`|Read the text in the current editing area.|
|`virtual void set_edit_text(const std::u32string &value)`|Update the text in the current editing area, perform type and business verification again when submitting.|
|`virtual const std::u32string &get_edit_error() const`|Read the last failed editing description.|
|`virtual bool begin_edit(uint64_t row, uint64_t column)`|Start editing the specified cell, limited by control and column read-only conditions; true if successful.|
|`virtual bool commit_edit()`|Submit the current editing text or specify grid_value_t, true if successful, fail to read get_edit_error.|
|`virtual bool commit_edit(const grid_value_t &value)`|Submit the current editing text or specify grid_value_t, true if successful, fail to read get_edit_error.|
|`virtual void cancel_edit()`|Cancel the current editing and hide the corresponding input interface.|
|`void set_visible(bool value) override`|Sets the visible state; clears ongoing interactions when hidden.|
|`void set_enabled(bool value) override`|Sets the operable state; clears ongoing interactions when disabled.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void refresh_layout() override`|Refresh the control layout; the base class handling is retained when overridden by derived classes.|
|`virtual void notify_selection_changed(const vector<grid_cell_t> &previous, int64_t previous_index)`|Select the updated derived notification, providing the original cell list and original row index.|
|`virtual uint64_t get_scroll_offset() const`|The derived class reads the vertical scroll row offset.|
|`virtual void set_scroll_offset(uint64_t value)`|The derived class sets the vertical scroll row offset, limited within the content range.|
|`virtual uint64_t get_horizontal_scroll_offset() const`|Reading the horizontal logical scroll offset for derived classes.|
|`virtual void set_horizontal_scroll_offset(uint64_t value)`|Setting the horizontal logical scroll offset for derived classes, limited within the content range.|
|`virtual uint64_t get_maximum_scroll_offset() const`|The derived class queries the maximum vertical row offset.|
|`virtual uint64_t get_maximum_horizontal_scroll_offset() const`|The derived class queries the maximum horizontal logical offset.|
|`grid(const std::u32string &name, const std::u32string &type)`|Construct an instance; see this type's description for parameters and constraints.|
|`virtual void set_horizontal_scrollbar_enabled(bool value)`|The derived class controls whether the horizontal scroll bar participates in layout.|
|`virtual void remap_row_selection(uint64_t row_count, const std::function<std::optional<uint64_t>(uint64_t)> &mapper)`|After data rearrangement, remap the original selection according to the mapper; returning nullopt indicates the original row has been removed.|
|`virtual grid_value_t read_cell_value(uint64_t row, uint64_t column) const`|The derived data reading entry returns grid_value_t for the specified row and column.|
|`virtual bool write_cell_value(uint64_t row, uint64_t column, const grid_value_t &value, std::u32string &error)`|The derived data writing entry; failing to return false and provide an error.|
|`virtual bool get_cell_value_choice_list(uint64_t row, uint64_t column, std::vector<grid_value_t> &choice_list) const`|Provide an optional value for the cell; returning true delivers the option through choice_list.|
|`virtual std::shared_ptr<const drawing_image> get_row_icon(uint64_t row) const`|Read the image resources of the row; null pointer indicates no icon.|
|`virtual void render_cell(render_context &context, const grid_cell_render_t &cell) const`|Draw a single visible cell, which can be customized by the derived class.|
|`rectangle_t get_input_rectangle() const override`|Return the actual visible local editing area of the current cell for input interface positioning.|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|
|`void render_overlay(render_context &context) const override`|Derives the drawing entry; uses context to draw the floating layer.|

### `easyvrui/control/listview.h`

`listview` inherits from `selection_control`, displaying an entire row and selecting multiple column texts. The first column can display item icons. Clicking the header triggers `on_column_click`, and dragging the separator line adjusts column width. Users can browse each row using a laser, scroll bar, and keyboard.

|Member|Purpose|
|---|---|
|`explicit listview(const std::u32string &name)`|Create a list view.|
|`get_column_list()`|Return a live `listview_column_collection` reference, providing a const overload.|
|`get_item_list()`|Return a live `listview_item_collection` reference, providing a const overload.|
|`get_selected_index() / set_selected_index(value)`|Read or set the position of the main selected item, with `-1` indicating an empty selection.|
|`get_selected_item() / set_selected_item(item)`|Read or select row objects in the collection, with `nullptr` indicating an empty selection.|
|`select_item(index, extend = false, toggle = false)`|Select by row subscript. In multiple selection mode, it can be extended to anchors or switch to the current row.|
|`get_selected_item_list()`|Read the row objects of the current selection.|
|`get_multi_select() / set_multi_select(value)`|Switch between single or multiple selections.|
|`get_row_height() / set_row_height(value)`|Set the positive row height, defaulting to 30 logical pixels.|
|`get_header_height() / set_header_height(value)`|Set the header height, defaulting to 32; 0 hides the header.|
|`get_visible_row_count()`|Read the number of logical rows that can fit on one screen.|
|`get_vertical_scrollbar_visible() / get_horizontal_scrollbar_visible()`|Read the display status of the scroll bar.|
|`on_item_list_changed`、`on_column_list_changed`|Triggered when an item or column set changes.|
|`on_column_width_changed`、`on_column_click`|Triggered when column width changes or when clicking on a header. The parameter is `listview_column_event_args_t`, providing the column object `column` and its index `index`.|
|`on_selection_changed`、`on_row_double_click`|Triggered when a selection changes or a row is activated. For double-clicking a row, the parameter is `listview_item_event_args_t`, providing the row object `item` and its index `index`.|
|`on_row_height_changed`、`on_header_height_changed`|Triggered when row height or header height changes.|

Sorting can pass the original row object in a new order via `get_item_list().assign(...)`. The set is maintained by object identity.

### `easyvrui/control/listview_column.h`

`listview_column(text, width)` saves the header text and logical width. The default text is empty, with a width of `DEFAULT_WIDTH` (100). Access is provided through `get_text()/set_text()` and `get_width()/set_width()`. Column width must be greater than 0, and the total column width of the same list must fall within the positive range of `int64_t`. Modifications to mounted columns will refresh the view.

### `easyvrui/control/listview_item.h`

`listview_item(cell_list, icon, tag)` saves a row text, optional icons, and application tags. By default, all items are empty, and access can be done through `get_icon()/set_icon()` and `get_tag()/set_tag()`. The row text can be updated by reading and writing `get_cell_list()`, which returns the updated set.

### `easyvrui/control/listview_column_collection.h`

`listview_column_collection` is held by the list view. Use `get_size()` to read the quantity, `contains(item)` and `get_index(item)` to query by column object, and `operator[]` returns a shared reference. `add/insert` inserts a column, `remove` removes it by object or position and returns a shared pointer, `assign` replaces all content, and `clear` clears the set. Ownership and width are verified before insertion.

### `easyvrui/control/listview_item_collection.h`

`listview_item_collection` uses the same member names as the column set, with elements being `std::shared_ptr<listview_item>`. Each row object belongs to one list at a time; it can be moved to another list after removal.

### `easyvrui/control/listview_cell_collection.h`

`listview_cell_collection` saves UTF-32 cell text by column position. `operator[]` reads the text, `set_cell(index, text)` modifies the existing position. `add/insert/remove/assign/clear` adjusts the set, and `get_size/contains/get_index` performs queries. Updates to mounted items are automatically redrawn.

### `easyvrui/control/treeview.h`

`treeview` inherits from `selection_control`. Access to the root node set is provided through `get_node_list()`, with a const overload. `get_selected_node()/set_selected_node(tree_node *)` accesses selection by object, and `nullptr` clears the selection. `get_row_height()` and `get_vertical_scrollbar_visible()` read the layout status.

`on_node_list_changed` is triggered when nodes are added or removed. `on_selection_changed` is triggered when the selection changes. `on_node_expanded/on_node_collapsed` corresponds to expanding and collapsing nodes. `on_node_activated` corresponds to double-clicking or pressing Enter. `tree_node_event_args_t::node` points to the node involved in the event.

### `easyvrui/control/tree_node.h`

`tree_node(text, expanded, tag)` creates nodes with default text and tags empty, and the nodes are collapsed. `get_text/set_text`, `get_tag/set_tag`, and `get_expanded/set_expanded` access their respective properties. `expand()` and `collapse()` switch the expansion state. `get_parent()` returns the parent node pointer, while nodes that are detached from the parent node return `nullptr`. `get_node_list()` returns the directly operable set of child nodes with a const overload.

### `easyvrui/control/tree_node_collection.h`

The root node and child node sets are queried using `get_size/contains/get_index`, and shared references are obtained through `operator[]`. `add/insert/assign` configures the object, `remove` removes it by object or position, and `clear` clears it. Nodes are distinguished by object identity, and each node belongs to one set at a time. When moving a node, it is first removed from the original set and then added to the target set.

### `easyvrui/control/menu_container.h`

#### `menu_container`

Declaration: `class menu_container: public container_control`.

The common base class for menu containers, with a protected constructor. get_control_list() returns a regular control_collection, with elements being menuitem, and the name must be unique at this level. get_menubar() finds the corresponding menu bar; both on_control_added/on_control_removed and the menu-specific on_item_added/on_item_removed can subscribe.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<menu_item_event_args_t> on_item_added`|Triggered when a menu item is added to the set, including the item ID and actual index.|
|`event_container<menu_item_event_args_t> on_item_removed`|Triggered when a menu item is removed from the set, including the item ID and the index before removal.|
|`virtual menubar *get_menubar() const`|Return to the parent menubar; return nullptr if no menu bar is associated.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`menu_container(const std::u32string &name, const std::u32string &type)`|Construct an instance; see this type's description for parameters and constraints.|
|`void validate_control(const control &child) const override`|Check if the element meets the container constraints before insertion; throw an exception if not.|
|`void notify_control_added(control &child, size_t index) override`|Container notification after insertion, where the index is the actual collection index of the element.|
|`void notify_control_removed(control &child, size_t index) override`|Container notification after removal, where the index is the actual collection index before removal.|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|Providing a rectangular container management for elements; nullopt indicates using its own rectangular area.|
|`std::vector<control *> get_active_control_list() const override`|Return the directly involved elements for display and interaction.|
|`bool is_control_active(const control &item) const override`|Determine whether the specified element participates in the current display and interaction.|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|
|`void render_overlay(render_context &context) const override`|Derives the drawing entry; uses context to draw the floating layer.|

The window menu belongs to the actual control_list. set_menu will complete the addition; adding a menubar directly from control_list will also synchronize with get_menu. Removal or clearing disassociates the connection; the index in on_control_added/on_control_removed is the actual collection index of the element. Each window is associated with one menubar, and the new menu can use the same name as the replaced menu.

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

Declaration: `class menuitem: public menu_container`.

Menu items and submenu containers. By default, text/shortcut is empty, icons are empty, and checkable/checked/separator is false. Sub-items are added through get_control_list().add() and can be nested hierarchically. separator=true draws a separator line; &A or (&A) in the text specifies a mnemonic key. shortcut saves text for combination keys like Ctrl+C; optional items trigger the inherited on_click when executed.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_text_changed`|Triggered when text changes.|
|`event_container<event_args_t> on_icon_changed`|Triggered when the icon changes.|
|`event_container<event_args_t> on_shortcut_changed`|Triggered when the shortcut key changes.|
|`event_container<event_args_t> on_checkable_changed`|Triggered when the setting changes is selected.|
|`event_container<event_args_t> on_checked_changed`|Triggered when the checked state changes.|
|`event_container<event_args_t> on_separator_changed`|Triggered when the separator line setting changes.|
|`event_container<event_args_t> on_opening`|Triggered when preparing to expand the submenu.|
|`event_container<event_args_t> on_closed`|Triggered when the submenu is collapsed.|
|`explicit menuitem(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`virtual const std::u32string &get_text() const`|Reads the displayed text.|
|`virtual void set_text(const std::u32string &value)`|Sets the displayed text.|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|Read the shared reference of the optional image resource; nullptr indicates clearing.|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|Set the shared reference of the optional image resource; nullptr indicates clearing.|
|`virtual const std::u32string &get_shortcut() const`|Read the menu shortcut combination text.|
|`virtual void set_shortcut(const std::u32string &value)`|Set the menu shortcut combination text.|
|`virtual bool get_checkable() const`|Read whether selection is allowed.|
|`virtual void set_checkable(bool value)`|Set whether selection is allowed.|
|`virtual bool get_checked() const`|Reads the current checked state.|
|`virtual void set_checked(bool value)`|Sets the current checked state.|
|`virtual bool get_separator() const`|Read whether it is displayed as a separator line.|
|`virtual void set_separator(bool value)`|Set whether it is displayed as a separator line.|

### `easyvrui/control/menubar.h`

#### `menubar`

Declaration: `class menubar: public menu_container`.

Menu bar, with default font being font_t {} and row_height =32. The main menu and each level of submenus are maintained through get_control_list(). open/close manages menu interactions; the main menu expanded by repeated clicks will collapse; no sub-items are highlighted initially during laser expansion, but they become highlighted when a specific item is pointed to. Windows associate menus with set_menu, and menubars can also be added as actual elements in the window control_list.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_font_changed`|Triggered when the font changes.|
|`event_container<event_args_t> on_row_height_changed`|Triggered when the line height changes.|
|`event_container<event_args_t> on_opening`|Triggered when preparing to expand the menu bar.|
|`event_container<event_args_t> on_closed`|Triggered when the menu bar is collapsed.|
|`explicit menubar(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`bool is_focusable() const override`|Checks whether the control has focus capability; actual focus is also limited by visible, enabled, and modal relationships.|
|`virtual const font_t &get_font() const`|Read the menu font, defaulting to font_t {}.|
|`virtual void set_font(const font_t &value)`|Set the menu font. The font name must not be empty, and the font size must be correct.|
|`virtual uint64_t get_row_height() const`|Read the logical line height.|
|`virtual void set_row_height(uint64_t value)`|Set the logical line height.|
|`virtual bool get_is_open() const`|Check whether the current is in menu interaction mode.|
|`virtual bool get_is_submenu_open(const menuitem &item) const`|Check whether the next-level pop-up list of the specified menu item is expanded.|
|`virtual void open()`|Enter menu interaction mode.|
|`virtual void close(bool restore_focus = true)`|Collapse all sub-menus; restore_focus defaults to true, used to restore the focus before entering the menu.|
|`void set_visible(bool value) override`|Sets the visible state; clears ongoing interactions when hidden.|
|`void set_enabled(bool value) override`|Sets the operable state; clears ongoing interactions when disabled.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|
|`void render_overlay(render_context &context) const override`|Derives the drawing entry; uses context to draw the floating layer.|

### `easyvrui/control/toolbar.h`

#### `toolbar`

Declaration: `class toolbar: public container_control`.

Icon toolbar. tool_size defaults to 40 and must be greater than 0. The spacing defaults to 6.0 and must be finite and non-negative. Configure buttons, icons, prompts, and separators using `get_button_list()`. The button grid is arranged horizontally in order, and the bar itself provides a background. Complete button grids that exceed the available area are exited from drawing and hit detection.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_spacing_changed`|Trigger when the tool grid spacing changes.|
|`event_container<event_args_t> on_tool_size_changed`|Trigger when the tool grid side length changes.|
|`toolbar_button_collection &get_button_list()` and const overload|Access the set of buttons and separators.|
|`explicit toolbar(const u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`void dispose() override`|Clear button_list and release the toolbar.|
|`virtual size_t get_tool_size() const`|Read the positive integer side length of the tool button.|
|`virtual void set_tool_size(size_t value)`|Set the positive integer side length of the tool button.|
|`virtual double get_spacing() const`|Read the finite and non-negative logical spacing between tool grids.|
|`virtual void set_spacing(double value)`|Set the finite and non-negative logical spacing between tool grids.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Derives the drawing entry; uses context to draw the text.|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|Arrange button display rectangles according to the size of the tool grid, spacing, and current order.|
|`bool is_control_active(const control &item) const override`|Determine whether the specified element participates in the current display and interaction.|
|`std::vector<control *> get_active_control_list() const override`|Return the directly involved elements for display and interaction.|

Apply configuration of buttons and separators through `get_button_list()`:

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

Declaration: `class toolbar_button: public button`.

Toolbar buttons inherit from `button`, and the constructed name is read-only. The icon defaults to empty, separator=false, enabled=true, and tooltip_text is empty. The icon maintains proportion, and a prompt is displayed when pointed at; separator=true displays a narrow separator. After adding toolbar.get_button_list (), get_parent returns to its corresponding toolbar. Ordinary buttons receive on_click.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_click`|Trigger when the toolbar button operation is executed.|
|`event_container<event_args_t> on_icon_changed`|Triggered when the icon changes.|
|`explicit toolbar_button(const std::u32string &name)`|Construct an instance; see this type's description for parameters and constraints.|
|`control_base *get_parent() const override`|Return to the corresponding toolbar; return nullptr if not added to any toolbar.|
|`void dispose() override`|Remove from the corresponding button set and release the button.|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|Read the shared reference of the optional image resource; nullptr indicates clearing.|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|Set the shared reference of the optional image resource; nullptr indicates clearing.|
|`virtual bool get_separator() const`|Read whether it is displayed as a separator line.|
|`virtual void set_separator(bool value)`|Set whether it is displayed as a separator line.|
|`virtual bool get_enabled() const`|Read whether it is operable.|
|`virtual void set_enabled(bool value)`|Set whether it can be operated.|

### `easyvrui/control/toolbar_button_collection.h`

#### `toolbar_button_collection`

Declaration: `class toolbar_button_collection`.

Is a button container belonging to the toolbar. The constructor is private and provided by toolbar.get_button_list(). It can be queried by index or name, with unique names within the container. add/insert can accept either shared_ptr or <toolbar_button>, and can also create and return a button reference based on the name. insert is used to append when reaching the end; remove returns shared_ptr or <toolbar_button>; get_item_list returns a copy of the pointer list.

|Declaration|Purpose and calling semantics|
|---|---|
|`toolbar_button_collection(const toolbar_button_collection &) = delete`|Copying is prohibited.|
|`~toolbar_button_collection()`|Destructor instance is called, releasing resources and references held by the object.|
|`toolbar_button_collection &operator=(const toolbar_button_collection &) = delete`|This copying or assignment operation is prohibited.|
|`size_t get_size() const`|Returns the total number of buttons and separator lines.|
|`bool is_empty() const`|Queries whether the collection is empty.|
|`bool contains(const toolbar_button &item) const`|Checks whether a specified instance or name belongs to this collection.|
|`bool contains(const std::u32string &name) const`|Checks whether a specified instance or name belongs to this collection.|
|`toolbar_button &get_item(size_t index) const`|Retrieves a toolbar_button reference by index or name; throws an exception if not found.|
|`toolbar_button &get_item(const std::u32string &name) const`|Retrieves a toolbar_button reference by index or name; throws an exception if not found.|
|`size_t get_index(const toolbar_button &item) const`|Gets the starting position of the button in the collection; throws an exception if not added.|
|`std::vector<toolbar_button *> get_item_list() const`|Returns a copy of the toolbar_button pointer list arranged in display order.|
|`void insert(size_t index, std::shared_ptr<toolbar_button> item)`|Inserts a shared button at the index, or creates a new button based on the name; appends when reaching the end.|
|`toolbar_button &insert(size_t index, const std::u32string &name)`|Inserts a shared button at the index, or creates a new button based on the name; appends when reaching the end.|
|`void add(std::shared_ptr<toolbar_button> item)`|Append a shared button, or create and return a new button reference based on the name.|
|`toolbar_button &add(const std::u32string &name)`|Append a shared button, or create and return a new button reference based on the name.|
|`std::shared_ptr<toolbar_button> remove(size_t index)`|Removes and returns the corresponding shared_ptr button; can be re-added to another toolbar.|
|`std::shared_ptr<toolbar_button> remove(toolbar_button &item)`|Removes and returns the corresponding shared_ptr button; can be re-added to another toolbar.|
|`std::shared_ptr<toolbar_button> remove(const std::u32string &name)`|Removes and returns the corresponding shared_ptr button; can be re-added to another toolbar.|
|`void clear()`|Removes all buttons and separators, releasing the ownership relationship.|
|`toolbar_button &operator[](size_t index) const`|Retrieves a button reference by index or name.|
|`toolbar_button &operator[](const std::u32string &name) const`|Retrieves a button reference by index or name.|

### `easyvrui/control/tabpage.h`

Tab content container.

#### `tabpage`

Declaration: `class tabpage: public panel`.

`tabpage` contains page content through an inherited control collection. The tab title is stored by `tabpage` itself, and the effective display area of the page is managed by the associated `tabcontrol`.

Inherit all public property access, methods, and events of `panel`; the table below lists members declared by this type or overridden.

|Declaration|Purpose and calling semantics|
|---|---|
|`explicit tabpage(const u32string &name)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`~tabpage() override`|Destructs objects, ending their resources or referenced lifetimes.|
|`virtual const u32string &get_text() const`|Reads the tab title, defaulting to empty.|
|`virtual void set_text(const u32string &value)`|Modifies the title and refreshes the tab associated with `tabcontrol`.|
|`event_container<event_args_t> on_text_changed`|Triggered when the tab title changes.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void render(render_context &context) const override`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|

### `easyvrui/control/tabpage_collection.h`

Supports searching for page collections by position or name.

#### `tabpage_collection`

Declaration: `class tabpage_collection: public control_collection`.

The indexing, name uniqueness, and lifecycle rules of the page collection are consistent with `control_collection`. `get_page()` and `operator[]` return page references. `insert()` is appended when reaching the end, and automatically adjusts the current selection when pages are removed.

|Declaration|Purpose and calling semantics|
|---|---|
|`explicit tabpage_collection(tabcontrol &owner)`|Construct this type of instance; see the type description and signature for parameter meanings.|
|`~tabpage_collection() override`|Destructs objects, ending their resources or referenced lifetimes.|
|`tabpage &get_page(size_t index) const`|Returns a page reference by index or name; throws an exception if not found.|
|`tabpage &get_page(const u32string &name) const`|Returns a page reference by index or name; throws an exception if not found.|
|`void insert(size_t index, control &page) override`|Inserts at the index position; appends if the index is not less than the current quantity. See the container's description for specific element types, ownership, and duplicate name constraints.|
|`void insert(size_t index, std::shared_ptr<control> page) override`|Inserts at the index position; appends if the index is not less than the current quantity. See the container's description for specific element types, ownership, and duplicate name constraints.|
|`using control_collection::add`|Append items; the caller ensures the object reference survives, while shared_ptr retains shared ownership.|
|`using control_collection::remove`|Removes the page and returns `shared_ptr<control>`, which can be directly added to other appropriate collections.|
|`std::shared_ptr<control> remove(size_t index) override`|Removes the page and returns `shared_ptr<control>`, which can be directly added to other appropriate collections.|
|`void clear() override`|Removes all pages.|
|`tabpage &operator[](size_t index) const`|Obtain an object reference starting from position 0 or by name, with behavior consistent with get_control/get_page.|
|`tabpage &operator[](const u32string &name) const`|Obtain an object reference starting from position 0 or by name, with behavior consistent with get_control/get_page.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`void notify_control_added(control &item, size_t index) override`|After the page is added, synchronize the page selection with on_page_added events.|
|`void notify_control_removed(control &item, size_t index, bool clearing) override`|When the page is removed, trigger `on_page_removed`.|

`page_list` inherits from `control_collection`, continuing its page storage, name indexing, and ownership rules. The title is set through `tabpage::set_text()`, and the title is retained with the page.

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

Tab selection, title appearance, and page layout.

#### `tab_position_t`

Declaration: `enum class tab_position_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`top`|Tabs are above.|
|`bottom`|Tabs are below.|
|`left`|Tabs are on the left.|
|`right`|Tabs are on the right.|

#### `tabcontrol`

Declaration: `class tabcontrol: public container_control`.

Inherit from container_control. page_list manages the page and title. The default tab is at the top, tab_size = 36, selected_index = -1 when no page is added; select a valid page after adding the first page. Only display the content of the current page, with hover highlighting applied to the tab selection area. tab_font defaults to Segoe UI, 18. The window text and tabpage maintain their respective backgrounds.

The application is managed through the `get_page_list()` page. Other public members are used according to inheritance rules.

|Declaration|Purpose and calling semantics|
|---|---|
|`tabpage_collection &get_page_list()` and const overload|Access the set of tabs, with elements being `tabpage`.|
|`event_container<event_args_t> on_selected_index_changed`|Triggered when the selected index changes.|
|`event_container<event_args_t> on_tab_position_changed`|Triggered when the tab position changes.|
|`event_container<event_args_t> on_tab_size_changed`|Triggered when the tabbar thickness changes.|
|`event_container<event_args_t> on_tab_font_changed`|Triggered when the tab font changes.|
|`event_container<event_args_t> on_tab_foreground_color_changed`|Triggered when the foreground color of a regular tab changes.|
|`event_container<event_args_t> on_tab_background_color_changed`|Triggered when the background color of a regular tab changes.|
|`event_container<event_args_t> on_selected_tab_foreground_color_changed`|Triggered when the foreground color of a selected tab changes.|
|`event_container<event_args_t> on_selected_tab_background_color_changed`|Triggered when the background color of a selected tab changes.|
|`event_container<tabpage_event_args_t> on_page_added`|Triggered when a page is added, including the tab `page` and index `index`.|
|`event_container<tabpage_event_args_t> on_page_removed`|Triggered when a page is removed, including the tab `page` and index `index`.|
|`event_container<tabpage_event_args_t> on_page_text_changed`|Triggered when the tab title changes, by reading the tab title through `event.page->get_text()`.|
|`event_container<tabpage_event_args_t> on_page_close`|Triggered by clicking the close icon or pressing Delete when the tab is focused. After confirmation of save, `event.page` is removed from `page_list`.|
|`event_container<event_args_t> on_page_close_button_visible_changed`|Triggered when the tab close button display settings change.|
|`event_container<event_args_t> on_selection_changed`|Triggered when selection state changes; text editor uses start/length, items and tabs use selected.|
|`explicit tabcontrol(const u32string &name)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`bool is_focusable() const override`|Checks whether the control has focus capability; actual focus is also limited by visible, enabled, and modal relationships.|
|`virtual int64_t get_selected_index() const`|Read the current selected index; -1 indicates no selection.|
|`virtual void set_selected_index(int64_t value)`|Set the current selected index; -1 indicates no selection.|
|`virtual tabpage *get_selected_page() const`|Read the current tabpage pointer; it is nullptr if no tab is selected.|
|`virtual tab_position_t get_tab_position() const`|The read tab is located at top, bottom, left, or right.|
|`virtual void set_tab_position(tab_position_t value)`|The set tab is located at top, bottom, left, or right.|
|`virtual uint64_t get_tab_size() const`|The thickness of the read tab bar must be greater than 0.|
|`virtual void set_tab_size(uint64_t value)`|The thickness of the set tab bar must be greater than 0.|
|`virtual bool get_page_close_button_visible() const`|Whether the close tab button is displayed, default is false.|
|`virtual void set_page_close_button_visible(bool value)`|Set the close tab button; clicking only sends a on_page_close request, and the application decides whether to remove the page.|
|`virtual const font_t &get_tab_font() const`|Read the bold font of the tab.|
|`virtual void set_tab_font(const font_t &value)`|Set the bold font of the tab.|
|`virtual uint32_t get_tab_foreground_color() const`|Read the foreground color of the unselected tab.|
|`virtual void set_tab_foreground_color(uint32_t value)`|Set the foreground color of the unselected tab.|
|`virtual uint32_t get_tab_background_color() const`|Read the background color of the unselected tab.|
|`virtual void set_tab_background_color(uint32_t value)`|Set the background color of the unselected tab.|
|`virtual uint32_t get_selected_tab_foreground_color() const`|Read the foreground color of the selected tab.|
|`virtual void set_selected_tab_foreground_color(uint32_t value)`|Set the foreground color of the selected tab.|
|`virtual uint32_t get_selected_tab_background_color() const`|Read the background color of the selected tab.|
|`virtual void set_selected_tab_background_color(uint32_t value)`|Set the background color of the selected tab.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`tabpage_collection &get_control_list() override`|Protected covariant override, returns page_list; the application accesses through `get_page_list()`.|
|`const tabpage_collection &get_control_list() const override`|Protected covariant override, returns page_list; the application accesses through `get_page_list()`.|
|`void validate_control(const control &item) const override`|Verify that the element is tabpage; other control types cannot be added to the page collection.|
|`vector<control *> get_active_control_list() const override`|Return the currently selected page, and an empty list if not selected.|
|`bool is_control_active(const control &item) const override`|Determine whether the element is the currently selected page.|
|`virtual void notify_selected_index(int64_t previous)`|Notification of changes in the current page index.|
|`void refresh_layout() override`|Refresh the control layout; the base class handling is retained when overridden by derived classes.|
|`size_t get_focus_target_count() const override`|Returns the number of internally focusable areas for focus navigation in composite controls.|
|`virtual size_t get_focus_target_at(double left, double top) const`|Gets the index of the internal focus area based on the control's local coordinates.|
|`optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|Providing a rectangular container management for elements; nullopt indicates using its own rectangular area.|
|`optional<int64_t> get_selection_index_at(double left, double top, const rectangle_t &rectangle) const override`|Query the index of the optional sub-item corresponding to a given logical coordinate; return nullopt if not found.|
|`void render(render_context &context) const override`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|

### `easyvrui/control/window.h`

VR top-level container, spatial reference, display, modal, and window interactions.

#### `startup_position_t`

Declaration: `enum class startup_position_t`, with members `none` and `center`.

`none` uses the initial position and orientation configured for it. `center` is displayed with its center aligned parallel to the source window plane at the first display. It also moves forward along the normal direction of the side where the headset is located. The modal window strictly follows the direct parent window’s orientation. The SDK provides priority to the same session’s sources. When no source is specified, the Engine uses the currently selected visible surface as the source. This can be used across sessions to launch other apps on the Desktop. When there is no valid source, the window is centered based on its current orientation, with an initial distance of `max(1.2, max(physical_width, physical_height))` meters. The Engine determines the initial depth based on each session’s window, and synchronizes the final position with position/rotation during the present callback. The positioning is applied only once during startup. After that, the hidden/visible state and the movement of the source window remain unchanged. The auxiliary input window is positioned based on the input area associated with the Engine.

When `startup_position_t::none` has both position and rotation set to zero, the upper left corner of the world window uses the initial front-facing reference center. The default center follows the above rule of priority to the headset when using the source.

#### `window`

Declaration: `class window: public container_control`.

Inherits from container_control. The default rect={0,0,640,360}, visible=false, title=name, title font Segoe UI/20, physical_scale =1.0 times, position and rotation all zero, with reference_object as the world; the title bar, close button, move, and zoom are all enabled, and the tracking menu defaults to include world/body/left/right/head. The spatial position of the top-level window is determined by `position` and the reference object. The window's expansion width is `rect.width * physical_scale / 1000` meters, and the height is `rect.height * physical_scale / 1000` meters. When it is movable and large enough, a control ring is reserved outside the text; derived windows can arrange the text through the protected get_content_top(). Ordinary single-handed side grip performs long-distance movement and rotation, while both hands grasp two control ring blocks to perform constrained rotation. `get_closed()` checks whether the window is closed.

When first displayed, it inherits the scaling of the same session source window determined by the SDK, unless `set_physical_scale()` is explicitly called. Explicit settings take precedence, including 1.0. The modal window uses the world reference object and can be dragged independently.

`show_dialog(owner_window)` requires the owner to be another interactive window within the same UI runtime. Dialog boxes must be hidden, not closed, and not in a modal state. During the call, the direct owner temporarily loses interactivity. Dialog boxes can be opened synchronously in button or menu events, with the currently interactive dialog box serving as the owner of the next layer. Calling during rendering submission will result in an error. See [session and nested modal loop](/en/advanced/04_session_and_context) for details.

When entering a modal state, the result is reset to `dialog_result_t::none`. Setting a result other than `none` will request a close. When the processor cancels the close, the dialog box remains active, and the result returns to the value before setting. When the result is still `none`, it can be closed through the title bar close button or `close()`, returning to `dialog_result_t::cancel`. The caller can retain the window object and read the control values after returning.

Inherit all public property access, methods, and events of `container_control`; the table below lists members declared by this type or overridden.

Curvature k is a finite non-negative number, with units of m⁻¹. k=0 represents a plane; when non-zero, the total arc angle θ=k×get_physical_width(), and both attributes and Engine verification require θ<2π. get_physical_width() is the unfolded arc length, calculated as rect.width×physical_scale/1000. The safe adjustment limit for the interactive handle at the bottom left of the window and the corresponding joystick is 160°; this limit is part of UI operation rules, and set_curvature() still uses the aforementioned legal domain. Changing rect or physical_scale must also maintain valid curvature.

The bottom left curvature handle and the bottom right zoom handle use trigger; holding them keeps them selected and locks the laser end during use. Curvature is adjusted with the joystick left and right, while zoom is adjusted up and down. Double-clicking at the bottom left restores the plane. curvature_adjustable and resizable control the two adjustment methods respectively.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_container<event_args_t> on_menu_changed`|The menu bar is triggered when it changes.|
|`event_container<event_args_t> on_title_changed`|The title changes are triggered.|
|`event_container<event_args_t> on_title_foreground_color_changed`|The foreground color of the title text changes are triggered.|
|`event_container<event_args_t> on_title_background_color_changed`|The background color of the title bar changes are triggered.|
|`event_container<event_args_t> on_title_font_changed`|The title font changes are triggered.|
|`event_container<event_args_t> on_icon_changed`|The title icon object changes or is cleared are triggered.|
|`event_container<event_args_t> on_rotation_changed`|The window rotation angle changes are triggered.|
|`event_container<event_args_t> on_curvature_changed`|The curvature changes are triggered.|
|`event_container<event_args_t> on_startup_position_changed`|Triggered when the startup positioning mode changes.|
|`event_container<event_args_t> on_curvature_adjustable_changed`|Triggered when the curvature interaction adjustment switch changes.|
|`event_container<event_args_t> on_reference_object_changed`|Triggered when the spatial reference object changes.|
|`event_container<event_args_t> on_show_title_bar_changed`|Triggered when the title bar display settings change.|
|`event_container<event_args_t> on_tracking_mode_set_changed`|Triggered when the tracking mode options change.|
|`event_container<event_args_t> on_show_close_button_changed`|Triggered when the close button display settings change.|
|`event_container<event_args_t> on_movable_changed`|Triggered when the move switch changes.|
|`event_container<event_args_t> on_resizable_changed`|Triggered when the zoom switch changes.|
|`event_container<event_args_t> on_load`|Triggered once when the window is first displayed.|
|`event_container<event_args_t> on_shown`|Triggered when the window is displayed.|
|`event_container<event_args_t> on_hidden`|Triggered when the window is hidden.|
|`event_container<cancel_event_args_t> on_closing`|Triggered before normal closing. `event.cancel = true` can abort this closing process.|
|`event_container<event_args_t> on_closed`|Triggered when the window closing is completed.|
|`event_container<render_error_event_args_t> on_render_failed`|Triggered when window submission or rendering fails, along with error data.|
|`event_container<event_args_t> on_tracking_lost`|Triggered when window spatial reference tracking is lost.|
|`event_container<event_args_t> on_tracking_restored`|Triggered when window spatial reference tracking is restored.|
|`event_container<event_args_t> on_activated`|Triggered when the window becomes the current active window.|
|`event_container<event_args_t> on_deactivated`|Triggered when the window loses its active state.|
|`event_container<event_args_t> on_move_start`|Triggered when window interaction movement or rotation begins.|
|`event_container<interaction_end_event_args_t> on_move_end`|Triggered when window interaction movement or rotation ends, with "cancelled" indicating the reason for ending.|
|`event_container<event_args_t> on_resize_start`|Triggered when window interaction zooming begins.|
|`event_container<interaction_end_event_args_t> on_resize_end`|Triggered when window interaction zooming ends.|
|`event_container<event_args_t> on_curvature_adjust_start`|Triggered when starting to adjust the window curvature.|
|`event_container<interaction_end_event_args_t> on_curvature_adjust_end`|Triggered when ending the window curvature adjustment.|
|`explicit window(const u32string &name)`|Create an instance by immutable Unicode name name; other properties are configured using their respective setters.|
|`virtual const std::shared_ptr<menubar> &get_menu() const`|Return to the current menu's `const shared_ptr<menubar> &`; empty reference indicates no menu is configured.|
|`virtual void set_menu(std::shared_ptr<menubar> value)`|Set or clear an inherent menu; the menu is a real element in control_list. To replace, first remove the original menu and then add the new menu to the collection. Support using a new instance with the same name as the original menu.|
|`void set_visible(bool value) override`|Sets the visible state.|
|`virtual const u32string &get_title() const`|Read the window title text, defaulting to name.|
|`virtual void set_title(const u32string &value)`|Set the window title text, defaulting to name.|
|`virtual uint32_t get_title_foreground_color() const`|Read the foreground color of the window title.|
|`virtual void set_title_foreground_color(uint32_t value)`|Set the foreground color of the window title.|
|`virtual uint32_t get_title_background_color() const`|Read the background color of the window title bar.|
|`virtual void set_title_background_color(uint32_t value)`|Set the background color of the window title bar.|
|`virtual const font_t &get_title_font() const`|Read the window title font.|
|`virtual void set_title_font(const font_t &value)`|Set the window title font.|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|Read the icon object on the left side of the title bar, defaulting to native icons.|
|`static std::shared_ptr<const drawing_image> get_default_icon()`|Read the default native icon; pass to set_icon to restore default values.|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|Set the icon; scale the image proportionally and center vertically, leaving space behind the title text; pass nullptr to clear the icon and restore the layout on the left side of the title.|
|`virtual double get_physical_scale() const`|Read the scaling factor, which must be a positive finite number.|
|`virtual void set_physical_scale(double value)`|Set a positive finite scaling factor; the new physical width must still fit within the valid curvature range.|
|`virtual double get_curvature() const`|Read the cylindrical curvature k, in meters⁻¹; 0 represents a plane.|
|`virtual void set_curvature(double value)`|Set the finite curvature k, requiring k >= 0 and k × get_physical_width() < 2π; 160° is the safe adjustment limit for interactive controls.|
|`virtual startup_position_t get_startup_position() const`|Read the startup positioning method, defaulting to center.|
|`virtual void set_startup_position(startup_position_t value)`|Set the startup positioning method, accepting none or center.|
|`virtual const vec3_t &get_position() const`|Read the relative position offset from reference_object, in meters.|
|`virtual void set_position(const vec3_t &value)`|Set the relative position offset from reference_object, in meters.|
|`virtual const vec3_t &get_rotation() const`|Read the XYZ Euler rotation of the relative position from reference_object, in degrees.|
|`virtual void set_rotation(const vec3_t &value)`|Set the XYZ Euler rotation of the relative position from reference_object, in degrees.|
|`virtual const reference_object_t &get_reference_object() const`|Read the spatial reference target.|
|`virtual void set_reference_object(const reference_object_t &value)`|Set spatial reference target.|
|`virtual bool get_show_title_bar() const`|Read whether to display the window title bar.|
|`virtual void set_show_title_bar(bool value)`|Set whether to display the window title bar.|
|`virtual const std::set<reference_object_type_t> &get_tracking_mode_set() const`|Read the mode collection for the title bar tracking menu; an empty collection hides the toggle button.|
|`virtual void set_tracking_mode_set(const std::set<reference_object_type_t> &value)`|Set the mode collection for the title bar tracking menu; an empty collection hides the toggle button.|
|`virtual bool get_show_close_button() const`|Read whether to display the title bar close button.|
|`virtual void set_show_close_button(bool value)`|Set whether to display the title bar close button.|
|`virtual bool get_movable() const`|Read whether interactive movement and control ring rotation are allowed.|
|`virtual void set_movable(bool value)`|Set whether interactive movement and control ring rotation are allowed.|
|`virtual bool get_resizable() const`|Read whether interactive changes to logical size are allowed.|
|`virtual void set_resizable(bool value)`|Set whether interactive changes to logical size are allowed.|
|`virtual bool get_curvature_adjustable() const`|Read the curvature interaction switch, default is true.|
|`virtual void set_curvature_adjustable(bool value)`|Set the display and interaction of the lower-left curvature button; when turned off, immediately cancel the current curvature dragging and joystick adjustment. After re-enabling, release the trigger before continuing the adjustment.|
|`virtual double get_physical_width() const`|Return the expansion width, in meters: rect.width × physical_scale /1000.|
|`virtual double get_physical_height() const`|Return the height, in meters: rect.height × physical_scale /1000.|
|`~window() override`|Destructs objects, ending their resources or referenced lifetimes.|
|`virtual void show()`|Display the window; the first display triggers load, and changes in display status trigger shown.|
|`virtual void hide()`|Hide the window and release related capture, focus, and input interfaces; retain the control object for future display.|
|`virtual bool close(bool force = false)`|Request close. Return true if successful. Skip the close cancellation callback when force=true.|
|`virtual void activate()`|Activate the window to which this object belongs; the window reloading activates itself.|
|`virtual dialog_result_t show_dialog(window &owner_window)`|Block the display of modal windows, disable the direct owner, and continue distributing UI events. After closing, return a result enumeration; the caller can still read window properties.|
|`virtual bool get_loaded() const`|Read whether the window has completed its first load.|
|`virtual bool get_closed() const`|Read whether the window has been closed.|
|`virtual dialog_result_t get_dialog_result() const`|Read the current modal result, reset to none when entering the modal.|
|`virtual void set_dialog_result(dialog_result_t value)`|Set the modal result. During the modal period, requests to close with values other than `none` will be canceled. The original value will be restored when the close is cancelled.|
|`void set_rect(const rectangle_t &value) override`|Set the logical rectangle; width and height must be positive. The physical width after setting must still satisfy the valid curvature domain.|
|`virtual void set_size(uint64_t width, uint64_t height)`|Set the window rect.width and rect.height, with units in logical units and both must be greater than 0.|
|`virtual void reparent(const reference_object_t &reference, bool keep_world = false)`|Change to a reference target of world, body, head, left, or right; maintain the world pose when keep_world is set to true.|
|`bool get_is_tracking_available(reference_object_type_t mode) const`|Query whether the specified reference mode can currently be tracked.|
|`virtual std::optional<pose_t> get_world_transform() const`|Return the world pose at the window center; if the reference pose is not available, return nullopt. The anchor point defined by the position attribute is located at the upper left corner, with a difference of half the width and height.|
|`virtual bool center_at_view(double distance)`|Center the window at a specified distance in meters ahead of the line of sight. Return true when tracking is available and positioning is successful.|
|`virtual bool get_auxiliary() const`|Query whether the window is an auxiliary surface associated with the input area.|
|`virtual void set_auxiliary(bool value)`|Mark the applied auxiliary input surface; actual positioning and scaling are maintained by the Engine based on the current input area.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`u32string title`|The accessible window title text for derived classes, defaulting to name; regular assignment uses setter to produce changes.|
|`uint32_t title_foreground_color = render_style::SELECTED_TEXT_FOREGROUND_COLOR`|The foreground color of the window title text for derived classes; regular assignment uses setter to produce changes.|
|`uint32_t title_background_color = render_style::WINDOW_TITLE_BACKGROUND_COLOR`|The background color of the window title bar for derived classes; regular assignment uses setter to produce changes.|
|`font_t title_font`|The font of the window title for derived classes; regular assignment uses setter to produce changes.|
|`std::shared_ptr<const drawing_image> icon`|Title icon, defaulting to the native icon; derived classes update drawing and trigger events through set_icon assignment.|
|`double physical_scale = render_style::DEFAULT_PHYSICAL_SCALE`|The scaling factor accessible for derived classes; must be a positive finite number; regular assignment uses setter to produce changes.|
|`double curvature = 0.0`|Cylindrical curvature, defaulting to 0.0, indicating a plane.|
|`startup_position_t startup_position = startup_position_t::center`|The initial display position strategy, defaulting to center.|
|`vec3_t position`|The relative position offset of reference_object accessible for derived classes, in meters; regular assignment uses setter to produce changes.|
|`vec3_t rotation`|The XYZ Euler rotation of reference_object accessible for derived classes, in degrees; regular assignment uses setter to produce changes.|
|`reference_object_t reference_object`|The spatial reference target accessible for derived classes; regular assignment uses setter to produce changes.|
|`bool show_title_bar = true`|Whether the window title bar is visible for derived classes; regular assignment uses setter to produce changes.|
|`std::set<reference_object_type_t> tracking_mode_set{reference_object_type_t::world, reference_object_type_t::body, reference_object_type_t::left, reference_object_type_t::right, reference_object_type_t::head}`|The mode set for the title bar tracking menu accessible for derived classes; an empty set hides the switch button; regular assignment uses setter to produce changes.|
|`bool show_close_button = true`|Whether the title bar close button is visible for derived classes; regular assignment uses setter to produce changes.|
|`bool movable = true`|Whether interactive movement and control ring rotation are allowed for derived classes; regular assignment uses setter to produce changes.|
|`bool resizable = true`|Whether interactive changes to logical dimensions are allowed for derived classes; regular assignment uses setter to produce changes.|
|`bool curvature_adjustable = true`|Curvature interaction switch; derived classes assign values through set_curvature_adjustable to synchronize cancellation and trigger events.|
|`void refresh_layout() override`|Refresh the control layout; the base class handling is retained when overridden by derived classes.|
|`void validate_control(const control &item) const override`|Elements that can be received by the validation window; only one menubar is associated with the same window at a time.|
|`void notify_control_added(control &item, size_t index) override`|After the element is actually added, the menu association is synchronized, and container events are issued according to the actual index.|
|`void notify_control_removed(control &item, size_t index) override`|After the element is actually removed, the menu association is synchronized, and container events are issued according to the original actual index.|
|`void notify_control_list_cleared() override`|After the collection is cleared, the menu association of the window is synchronized.|
|`virtual render_rectangle_t get_menu_rectangle() const`|Read the actual logical rectangle of the menu bar in the current window.|
|`virtual void render_window_frame(render_context &context, bool spatial_handle) const`|Draw the window border, title, and space manipulators controlled by spatial_handle.|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|Arrange the rectangle below the title bar for the menu; ordinary controls use their own rectangles.|
|`double get_content_top() const override`|Read the logical top offset of the text start.|
|`void render(render_context &context) const override`|Use context to draw the control text. Derivable classes can override this to implement custom appearances.|

The reference targets include five types: world, body, head, left, and right; tracking_mode_set can configure the optional target for the title bar. world/body can perform ordinary window capture. The layout of derived windows can be adapted to the title bar, menu, and control ring through the protected get_content_top().

### `easyvrui/dialog/dialog_result.h`

`dialog_result_t` is a common result enumeration used by modal windows and standard message boxes. Members `none/ok/cancel/abort/retry/ignore/yes/no` correspond to `0` to `7` in sequence.

## Custom drawing

### `easyvrui/render/render_context.h`

The drawing and interaction state query interface used by custom controls.

#### `render_rectangle_t`

Declaration: `struct render_rectangle_t`.

Floating point logical rectangles; left/top/width/height is all double, default 0. Used for drawing and clipping.

|Declaration|Purpose and calling semantics|
|---|---|
|`double left = 0.0`|The horizontal coordinate on the left side of the rectangle.|
|`double top = 0.0`|The vertical coordinate on the top side of the rectangle.|
|`double width = 0.0`|The width of the rectangle, in logical pixels.|
|`double height = 0.0`|The height of the rectangle, in logical pixels.|

#### `render_context`

Declaration: `class render_context`.

The abstract drawing context received by the custom control render/render_overlay. Rectangles, coordinates, radii, and line widths use logical units; color is 0xRRGGBBAA. Pure virtual functions are provided by the specific context, and ordinary controls call them directly. When called through a static type, the default parameters are based on the declaration of that type.

|Declaration|Purpose and calling semantics|
|---|---|
|`virtual ~render_context() = default`|Destructs objects, ending their resources or referenced lifetimes.|
|`virtual render_rectangle_t get_rectangle(const control &item) const = 0`|Obtain the logical drawing rectangle of the control in the current window.|
|`virtual render_rectangle_t get_popup_rectangle(const item_control &item) const = 0`|Obtain the rectangle of the pop-up area of the item control.|
|`virtual bool is_hovered(const control &item) const = 0`|Query whether the laser is hovering over the control or its specified rectangle.|
|`virtual bool is_hovered(const control &item, const render_rectangle_t &rectangle) const = 0`|Query whether the laser is hovering over the control or its specified rectangle.|
|`virtual bool is_focused(const control &item) const = 0`|Query the visual focus of the control; it can be false during input emptying waiting, and the logical focus may still be retained at this time.|
|`virtual bool is_blinking() const = 0`|Query whether the insertion point in this frame is in the display cycle.|
|`virtual bool is_active(const window &item) const = 0`|Query whether the window is the currently active window.|
|`virtual bool is_blocked(const window &item) const = 0`|Query whether the window is blocked by a modal relationship.|
|`virtual bool is_close_button_hovered(const window &item) const = 0`|Query whether the window close button is in a hovered state.|
|`virtual int64_t get_hovered_item(const item_control &item) const = 0`|Obtain the index of the item pointed by the laser; -1 when not hit.|
|`virtual double measure(const u32string &text, const font_t &font) = 0`|Measure the logical width of Unicode text in the specified font.|
|`virtual void fill(const render_rectangle_t &rectangle, uint32_t color) = 0`|Fill the rectangle with color; the coordinates use logical units.|
|`virtual void outline(const render_rectangle_t &rectangle, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|Draw the rectangular contour with thickness equal to the line width.|
|`virtual void draw_line(double x1, double y1, double x2, double y2, uint32_t color, double thickness = render_style::FOCUSED_OUTLINE_THICKNESS) = 0`|Draw the line segment from (x1,y1) to (x2,y2) using color and line width.|
|`virtual void draw_text(const u32string &value, const font_t &font, const render_rectangle_t &rectangle, uint32_t color, bool center = false) = 0`|Draw text within the given rectangle; center the text if set to true, with font, size, and style specified by corresponding parameters.|
|`virtual void push_clip(const render_rectangle_t &rectangle) = 0`|Push into the rectangular clipping area; subsequent drawings are constrained by the current clipping area.|
|`virtual void pop_clip() = 0`|Pop up the nearest pushed clipping area; must be used in pairs with push_clip.|
|`virtual void render_control_list(const window &item) = 0`|Draw controls in the current order of window collection.|
|`virtual void render_overlay_list(const window &item) = 0`|Draw the floating layer of controls within the window.|
|`virtual void fill_ellipse(double center_x, double center_y, double radius_x, double radius_y, uint32_t color) = 0`|Fill an ellipse centered at (center_x, center_y) with radius radius_x/radius_y.|
|`virtual void outline_ellipse(double center_x, double center_y, double radius_x, double radius_y, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|Draw the contour of the ellipse; both radius and line width must meet drawing parameter constraints.|
|`virtual void fill_rounded_rectangle(const render_rectangle_t &rectangle, double radius_x, double radius_y, uint32_t color) = 0`|Fill the rectangle with a rounded corner radius specified by radius_x/radius_y.|
|`virtual void outline_rounded_rectangle(const render_rectangle_t &rectangle, double radius_x, double radius_y, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|Draw the contour of the rounded rectangle.|
|`virtual void draw_image(const drawing_image &image, const render_rectangle_t &rectangle, double opacity = 1.0) = 0`|Scale and draw an RGBA image onto the target rectangle, with opacity ranging from 0 to 1.|
|`virtual void draw_screen(uint64_t screen_id, const render_rectangle_t &rectangle) = 0`|Draw the real-time display screen specified by screen_id.|
|`virtual void fill_path(const drawing_path &path, uint32_t color) = 0`|Fill the path according to its filling rules.|
|`virtual void outline_path(const drawing_path &path, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|Draw the path contour based on thickness.|
|`virtual void render_control(const control &item)`|Call the protected text drawing entry of the specified control for custom combined drawing use.|
|`virtual void render_control_overlay(const control &item)`|Call the protected floating layer drawing entry of the specified control.|
|`void fill_circle(double center_x, double center_y, double radius, uint32_t color)`|Fill a circle with radius equal to radius.|
|`void draw_circle(double center_x, double center_y, double radius, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS)`|Draw the contour of a circle with radius equal to radius and line width equal to thickness.|
|`static render_rectangle_t get_inset_rectangle(render_rectangle_t rectangle, double left_padding, double right_padding, double top_padding = 0.0, double bottom_padding = 0.0)`|Return a reduced rectangle based on given inner margins of the four sides or margins of the control and its left and right sides.|
|`render_rectangle_t get_inset_rectangle(const control &item, double left_padding, double right_padding) const`|Return a reduced rectangle based on given inner margins of the four sides or margins of the control and its left and right sides.|
|`void draw_control(const control &item, bool highlight = true)`|Draw the background and border of the control; highlight controls to show interactive emphasis.|
|`uint32_t get_foreground(const text_control &item) const`|Return the foreground color applicable to the current state of text controls.|

### `drawing_image.h`

Invariant RGBA image values.

#### `drawing_image`

Declaration: `class drawing_image`.

Invariant images in the global namespace. Construct an array of width, height, and RGBA bytes, with 4 bytes per pixel arranged row by row; the number of bytes must match the width and height. Read each field through a getter.

|Declaration|Purpose and calling semantics|
|---|---|
|`drawing_image(uint64_t width, uint64_t height, std::vector<uint8_t> pixel_data)`|Construct the object; see the type description for parameters, default states, and constraints.|
|`static std::shared_ptr<drawing_image> load_file(const std::filesystem::path &path)`|Load the supported image files by the system. Select the largest image frame for ICO.|
|`static std::shared_ptr<drawing_image> load_memory(std::span<const uint8_t> data)`|Load from the fully encoded image bytes.|
|`static std::shared_ptr<drawing_image> load_ico(std::span<const uint8_t> data)`|Check the ICO file header and load the icon from memory.|
|`std::vector<uint8_t> encode_ico() const`|Losslessly encode PNG and encapsulate it into a single-image ICO, retaining RGBA pixels; width and height are each 1 to 256 pixels.|
|`uint64_t get_width() const`|Read the image pixel width.|
|`uint64_t get_height() const`|Read the image pixel height.|
|`const std::vector<uint8_t> &get_pixel_data() const`|Read the RGBA pixel byte array.|

### `drawing_path.h`

Path segment, filling rule, and chainable two-dimensional path.

#### `drawing_path_operation_t`

Declaration: `enum class drawing_path_operation_t: uint8_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`move = 0u`|Move to the starting point, value_list [0..1] becomes x/y.|
|`line = 1u`|Straight line to the end point, value_list [0..1] becomes x/y.|
|`quadratic = 2u`|Quadratic curve, value_list [0..3] are the control points and the end point.|
|`cubic = 3u`|Cubic curve, value_list [0..5] are two control points and the end point.|
|`arc = 4u`|Elliptical arc, value_list [0..4] are the end point x/y, radius x/y, rotation degree, and additionally clockwise/large_arc.|
|`close = 5u`|Close the current sub-path.|

#### `drawing_fill_rule_t`

Declaration: `enum class drawing_fill_rule_t: uint8_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`even_odd = 0u`|Odd-even filling rule.|
|`non_zero = 1u`|Non-zero wrap-around filling rule.|

#### `drawing_path_segment_t`

Declaration: `struct drawing_path_segment_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`drawing_path_operation_t operation = drawing_path_operation_t::move`|Operation type of this path segment.|
|`std::array<double, 6u> value_list{}`|Coordinate and parameter array of the path segment, with a capacity of 6.|
|`bool clockwise = true`|Whether the arc is clockwise.|
|`bool large_arc = false`|Whether the arc uses a path greater than half a circle.|

The actual usage position of value_list is determined by operation; move/line uses the first two items, quadratic uses the first four items, cubic uses the six items, and arc uses the first five items. Unused items can remain with default values.

#### `drawing_path`

Declaration: `class drawing_path`.

Path builder in the global namespace. move_to/line_to /curve/arc_ to/close both return drawing_path &, which can be called in a chain. Default filling rule is even_odd; clear clears the segment. Coordinates must be finite, radius must be non-negative, and the path should start from a valid starting point.

|Declaration|Purpose and calling semantics|
|---|---|
|`drawing_path()`|Construct this type of instance; see the type description and signature for parameter meanings.|
|`const std::vector<drawing_path_segment_t> &get_segment_list() const`|Read the read-only list of path segments.|
|`drawing_fill_rule_t get_fill_rule() const`|Read the path filling rule.|
|`void set_fill_rule(drawing_fill_rule_t value)`|Set path filling rules.|
|`void clear()`|Clear path segments, retaining the current filling rules.|
|`drawing_path &move_to(double x, double y)`|Start or move to the new starting point of the path at (x,y), return to the current path reference for chain calling.|
|`drawing_path &line_to(double x, double y)`|Connect a straight line from the current point to (x,y), return to the current path reference.|
|`drawing_path &quadratic_to(double control_x, double control_y, double end_x, double end_y)`|Add a quadratic Bézier curve, with control as the control point and end as the endpoint, return to the current path reference.|
|`drawing_path &cubic_to(double control1_x, double control1_y, double control2_x, double control2_y, double end_x, double end_y)`|Add a cubic Bézier curve, with control1/control2 as the control point and end as the endpoint, return to the current path reference.|
|`drawing_path &arc_to(double end_x, double end_y, double radius_x, double radius_y, double rotation_degree = 0.0, bool clockwise = true, bool large_arc = false)`|Add an elliptical arc to (end_x, end_y); radius is the radius, rotation_degree is the angle, and clockwise and large_arc determine the arc direction and size.|
|`drawing_path &close()`|Close the current sub-path, return to the current drawing_path reference.|

### `easyvrui/render/render_style.h`

Default color, size, line width, and layout constants.

#### `render_style`

Declaration: `class render_style`.

|Declaration|Purpose and calling semantics|
|---|---|
|`static constexpr uint32_t CONTROL_BACKGROUND_COLOR = 0x162738ffu`|Default background color for regular controls.|
|`static constexpr uint32_t TEXT_FOREGROUND_COLOR = 0xd1def0ffu`|Default text foreground color.|
|`static constexpr uint32_t SELECTED_TEXT_FOREGROUND_COLOR = 0xffffffffu`|Text color for selected content.|
|`static constexpr uint32_t WINDOW_BACKGROUND_COLOR = 0x0d1624ffu`|Default background color for the window.|
|`static constexpr uint32_t WINDOW_TITLE_BACKGROUND_COLOR = 0x244565ffu`|Default background color for the window title bar.|
|`static constexpr uint32_t HOVER_OVERLAY_COLOR = 0x469eff55u`|Hover overlay color.|
|`static constexpr uint32_t FOCUSED_OUTLINE_COLOR = 0x7bc9ffffu`|Focus border color.|
|`static constexpr uint32_t HOVERED_OUTLINE_COLOR = 0x63b4ffffu`|Hover border color.|
|`static constexpr uint32_t NORMAL_OUTLINE_COLOR = 0x45617dffu`|Regular border color.|
|`static constexpr uint32_t SELECTED_ITEM_BACKGROUND_COLOR = 0x316b9affu`|Background color for selected items.|
|`static constexpr uint32_t HOVERED_ITEM_BACKGROUND_COLOR = 0x5eacff66u`|Background color for hovered items.|
|`static constexpr uint32_t ITEM_LIST_OUTLINE_COLOR = 0x567a9cffu`|Outline color for item list.|
|`static constexpr uint32_t TEXT_SELECTION_BACKGROUND_COLOR = 0x3679bcddu`|Background color for text selection.|
|`static constexpr uint32_t CLOSE_BUTTON_HOVER_COLOR = 0xc84e64ffu`|Hover color for close button.|
|`static constexpr uint32_t WINDOW_OUTLINE_COLOR = 0x5f87a9ffu`|Window outline color.|
|`static constexpr uint32_t BLOCKED_WINDOW_OVERLAY_COLOR = 0x00000088u`|Modal blocking mask color.|
|`static constexpr uint32_t COLOR_RGB_MASK = 0xffffff00u`|Extract the bit mask of the high 24-bit RGB.|
|`static constexpr uint32_t COLOR_ALPHA_MASK = 0x000000ffu`|Extract the bit mask of the low 8-bit Alpha.|
|`static constexpr uint32_t DISABLED_ALPHA_DIVISOR = 2u`|Disable status transparency denominator.|
|`static constexpr uint64_t DEFAULT_TAB_SIZE = 36u`|Default tab bar thickness.|
|`static constexpr uint64_t DEFAULT_ROW_HEIGHT = 32u`|Default item line height.|
|`static constexpr uint64_t DEFAULT_WINDOW_WIDTH = 640u`|Default window logical width.|
|`static constexpr uint64_t DEFAULT_WINDOW_HEIGHT = 360u`|Default window logical height.|
|`static constexpr uint64_t WINDOW_TITLE_FONT_SIZE = uint64_t{20u}`|Default title logical font size.|
|`static constexpr double LOGICAL_PIXELS_PER_METER = 1000.0`|Logical pixels per meter for 1x zoom.|
|`static constexpr double DEFAULT_PHYSICAL_SCALE = 1.0`|Default window physical zoom factor.|
|`static constexpr double NORMAL_OUTLINE_THICKNESS = 1.0`|Normal outline width.|
|`static constexpr double FOCUSED_OUTLINE_THICKNESS = 2.0`|Focus outline width.|
|`static constexpr double TEXT_HORIZONTAL_PADDING = 10.0`|Text horizontal inner margin.|
|`static constexpr double BUTTON_HORIZONTAL_PADDING = 6.0`|Button text horizontal inner margin.|
|`static constexpr double COMBOBOX_BUTTON_WIDTH = 48.0`|Combo box drop-down button width.|
|`static constexpr uint64_t INPUT_BAR_HEIGHT = 48u`|Auxiliary input bar height.|
|`static constexpr uint64_t INPUT_BAR_MINIMUM_WIDTH = 480u`|Auxiliary input bar minimum width.|
|`static constexpr uint64_t INPUT_BAR_PADDING = 8u`|Auxiliary input bar inner margin.|
|`static constexpr uint64_t INPUT_BAR_COLUMN_GAP = 12u`|Auxiliary input bar column spacing.|
|`static constexpr uint64_t INPUT_BAR_FONT_SIZE = 20u`|Auxiliary input bar font size.|
|`static constexpr uint64_t INPUT_BAR_SWITCH_MINIMUM_WIDTH = 144u`|Minimum width of input method switch button.|
|`static constexpr double COMBOBOX_ARROW_CENTER_OFFSET = 24.0`|Center offset of drop-down arrow.|
|`static constexpr double COMBOBOX_ARROW_HORIZONTAL_RADIUS = 8.0`|Horizontal radius of drop-down arrow.|
|`static constexpr double COMBOBOX_ARROW_VERTICAL_RADIUS = 4.0`|Vertical radius of the drop-down arrow.|
|`static constexpr double COMBOBOX_ARROW_THICKNESS = 3.0`|Line width of the drop-down arrow.|
|`static constexpr double TEXTBOX_SCROLL_PADDING = 4.0`|Inner margin for text box scrolling.|
|`static constexpr double TEXTBOX_SELECTION_VERTICAL_PADDING = 5.0`|Vertical whitespace for text selection.|
|`static constexpr double TEXTBOX_TEXT_TRAILING_PADDING = 2.0`|Whitespace at the end of text lines.|
|`static constexpr double TEXTBOX_CARET_VERTICAL_PADDING = 7.0`|Vertical whitespace for the insertion point.|
|`static constexpr double TEXTBOX_CARET_THICKNESS = 2.0`|Line width of the insertion point.|
|`static constexpr double TEXTBOX_LINE_HEIGHT_RATIO = 1.4`|Ratio of text line height to font size.|
|`static constexpr double SCROLLBAR_WIDTH = 12.0`|Width of the text editing scroll bar.|
|`static constexpr double SCROLLBAR_MINIMUM_THUMB_SIZE = 18.0`|Minimum length of the scroll bar slider.|
|`static constexpr uint32_t SCROLLBAR_TRACK_COLOR = 0x0d1624ffu`|Color of the scroll bar track.|
|`static constexpr uint32_t SCROLLBAR_THUMB_COLOR = 0x5f87a9ffu`|Color of the scroll bar slider.|
|`static constexpr double WINDOW_TITLE_HEIGHT = 48.0`|Logical height of the title bar.|
|`static constexpr double WINDOW_TITLE_LEFT_PADDING = 16.0`|Whitespace on the left side of the title text.|
|`static constexpr double WINDOW_TITLE_ICON_SIZE = 28.0`|Side length of the title bar icon.|
|`static constexpr double WINDOW_TITLE_ICON_GAP = 10.0`|Distance between the title icon and the text.|
|`static constexpr double WINDOW_TITLE_RIGHT_PADDING = 56.0`|Whitespace on the right side of the title text.|
|`static constexpr double WINDOW_CLOSE_BUTTON_WIDTH = 48.0`|Width of the close button.|
|`static constexpr double WINDOW_TRACKING_BUTTON_WIDTH = 48.0`|Width of the tracking switch button.|
|`static constexpr double WINDOW_TRACKING_POPUP_WIDTH = 160.0`|Width of the tracking selection menu.|
|`static constexpr double WINDOW_TRACKING_ROW_HEIGHT = 32.0`|Line height of the tracking selection menu.|
|`static constexpr double WINDOW_CLOSE_ICON_NEAR_OFFSET = 15.0`|Offset of the close icon's near-side endpoint.|
|`static constexpr double WINDOW_CLOSE_ICON_FAR_OFFSET = 33.0`|Offset of the close icon's far-side endpoint.|
|`static constexpr double WINDOW_CLOSE_ICON_THICKNESS = 3.0`|Line width of the close icon.|
|`static constexpr double WINDOW_RESIZE_OUTER_OFFSET = 6.0`|Offset outside the zoom icon.|
|`static constexpr double WINDOW_RESIZE_LONG_INNER_OFFSET = 22.0`|Offset inside the long line of the zoom icon.|
|`static constexpr double WINDOW_RESIZE_SHORT_INNER_OFFSET = 14.0`|Offset inside the short line of the zoom icon.|
|`static constexpr double WINDOW_OUTLINE_INSET = 1.0`|Distance of window outline contraction.|
|`static constexpr double WINDOW_OUTLINE_THICKNESS = 2.0`|Width of window outline line.|
|`static constexpr uint64_t POPUP_BOTTOM_MARGIN = 24u`|White space at the bottom of the pop-up menu.|
|`static constexpr uint64_t POPUP_MAXIMUM_VISIBLE_ITEM_COUNT = 8u`|Maximum number of items displayed in a single pop-up menu.|
|`static constexpr double WINDOW_RESIZE_HIT_SIZE = 30.0`|Size of the window zoom hit area.|
|`static uint32_t get_disabled_color(uint32_t color)`|Disabled color for returning to reduced transparency.|

## Input components

### `easyvrui/input/input_provider.h`

Registration, input, status, and empty interface for independent layout and IME applications.

#### `input_role_t`

Declaration: `enum class input_role_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`layout`|Layout program that generates virtual keyboard keys.|
|`ime`|Input method program that processes keys, forwards unused events, and submits final text.|

#### `input_provider_state_t`

Declaration: `enum class input_provider_state_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`stopped`|Currently not running.|
|`starting`|Started, waiting for registration.|
|`running`|Registered and running.|

#### `provider_info_t`

Declaration: `struct provider_info_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`uint64_t id = 0u`|Input component number.|
|`std::u32string name`|Component display name, using UTF-32.|
|`std::u32string language = U"en"`|IME language code, commonly zh/en/ja; supports other non-empty codes. The layout follows the recorded default value, omitting the language in the protocol.|
|`input_role_t role = input_role_t::ime`|Layout or IME role.|
|`input_provider_state_t state = input_provider_state_t::stopped`|Component status: stopped, starting, or running.|
|`bool configured = false`|Whether from engine fixed configuration.|
|`bool active = false`|Whether the component is the active item selected for the query session; whether the input path is enabled is represented by input_ui_state_t::active.|
|`bool default_provider = false`|Whether this IME is the persistent default item.|
|`uint32_t process_id = 0u`|Component process number.|
|`std::string error`|Recent error descriptions of the component.|
|`bool operator==(const provider_info_t &other) const = default`|Returns a bool indicating whether the corresponding member values are equal, by comparing field by field.|

#### `input_ui_state_t`

Declaration: `struct input_ui_state_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`bool active = false`|Whether the component is currently selected, or whether the input area is active.|
|`bool physical = false`|Whether it is currently in entity keyboard mode.|
|`std::optional<render_rectangle_t> rectangle`|The logical rectangle of the input area in the window; nullopt when no associated input area exists.|

#### `input_event_type_t`

|Enumeration values|Meanings|
|---|---|
|`unknown`|Unrecognized events.|
|`key_down`|Key press or repetition.|
|`key_up`|Key release.|
|`ime_submit`|IME submits final text.|

#### `input_event_t`

Declaration: `struct input_event_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`std::string event_type`|Event name, such as key_down or key_up.|
|`std::u32string key`|Logical key name.|
|`std::u32string text`|Displayed text or IME submitted text, using UTF-32.|
|`bool shift = false`|Whether Shift is pressed.|
|`bool ctrl = false`|Whether Ctrl is pressed.|
|`bool alt = false`|Whether Alt is pressed.|
|`bool meta = false`|Whether Windows/Meta is pressed.|
|`bool handled = false`|Whether the component has consumed the current key; IME can continue to forward unconsumed keys.|
|`input_event_type_t get_type() const`|Interpret `event_type` as an event enumeration; return `unknown` if it cannot be recognized.|

#### `input_provider`

Declaration: `class input_provider`.

For use by independent layout/IME applications. After registration, the session is fixed as the component role, and the component presents the interface through an auxiliary surface. IME processes keys and calls `commit_text` to submit text. layout sends virtual keys. Ordinary applications can set the selected IME as the default item in the input method switching dialog box. The input area status is provided by get_state and on_state_changed. Asynchronous tasks must be paired with begin_input_task/finish_input_task, and the queue includes these tasks and pending outputs.

The callback signature for on_input is void(input_provider &source, input_event_t &event). After process_input and on_input are executed, keys where event.handled is still false will be automatically forwarded; set handled to true when consuming keys. If send_event is called to forward the same key, handle should also be set to true to avoid duplication. The corresponding key is usually consumed after IME submits text. Registration is an asynchronous process, and the registration response is continued to be processed through run or message loop; only one current input component is allowed in the same thread, and the registration role remains fixed.

|Declaration|Purpose and calling semantics|
|---|---|
|`event_signal<input_provider, input_ui_state_t> on_state_changed`|Triggered when the active input area, mode, or rectangular status of the input component changes.|
|`event_signal<input_provider, input_event_t> on_input`|Triggered when the input component receives a key or text event; can be consumed or forwarded.|
|`input_provider()`|Create an instance of the input component.|
|`virtual ~input_provider()`|Destructs objects, ending their resources or referenced lifetimes.|
|`input_provider(const input_provider &) = delete`|Disable copying or assignment; objects are managed by their original instance and lifecycle.|
|`input_provider &operator=(const input_provider &) = delete`|Disable copying or assignment; objects are managed by their original instance and lifecycle.|
|`const input_ui_state_t &get_state() const`|Read the status of the input interface.|
|`input_role_t get_role() const`|Read the roles of input components.|
|`bool get_draining() const`|Check if the component is currently draining input.|
|`bool get_connected() const`|Retrieve the current connection status of input components.|
|`uint64_t get_session_id() const`|Retrieve the current input component session number; return 0 if not connected.|
|`const std::vector<provider_info_t> &get_provider_list() const`|Retrieve the list of known input components.|
|`void register_provider(input_role_t role = input_role_t::ime, bool default_provider = false, const std::u32string &name = U"", const std::u32string &language = U"en")`|Register the current standalone program as layout or IME; default_provider indicates the default selection, and name is the display name. language is only used for IME and must be a non-empty code; if omitted, it defaults to en. A session role is fixed and mutually exclusive.|
|`void begin_input_task()`|Register unfinished asynchronous input tasks; used to delay confirmation of draining completion.|
|`void finish_input_task()`|Complete one registration of begin_input_task; each registration should correspond to one completion.|
|`void send_event(const input_event_t &event)`|Send key event output from components.|
|`void commit_text(const std::u32string &text)`|Submit the final text as IME, forwarded by the engine to the current input window.|
|`void run()`|Run the input component event loop; if not registered, initiate registration using the default IME role first. Return after unsuccessful registration or after the component is canceled.|

##### Derived extended members (protected)

The following members are for derived classes; ordinary applications operate on the object through the public interfaces listed above.

|Declaration|Purpose and calling semantics|
|---|---|
|`virtual void process_state(input_ui_state_t &state)`|Process the status of the component input area for extended by derived classes.|
|`virtual void process_input(input_event_t &event)`|Process keys received by IME; derived classes can modify events or set handled, then call the on_input event chain.|
|`virtual void process_drain()`|Prepare to drain input; derived implementations must complete asynchronous tasks and stop output from old paths.|

## Text and environment tools.

### `easyvrui/common/u32string_hash.h`

Support a transparent hash function for queries of type u32string_view.

#### `u32string_hash`

Declaration: `class u32string_hash`.

|Declaration|Purpose and calling semantics|
|---|---|
|`using is_transparent = void`|Transparent hash marker, enabling hash containers to support queries of different string view types.|
|`size_t operator()(u32string_view value) const noexcept`|Calculate the size_t hash value of Unicode string views, ensuring no exceptions are thrown.|

## Errors and Languages

### `easyvrui/common/error_diagnostic.h`

Source code location, conditional expressions, and single-line error diagnosis.

#### Free Functions and Type Aliases

|Declaration|Purpose and Return Values|
|---|---|
|`error_diagnostic get_error_diagnostic(const std::exception &error, const std::source_location &location = std::source_location::current())`|Obtain existing diagnostic information from exceptions; construct using the calling position if no diagnostic is available for the exception.|
|`std::string get_error_message(const std::exception &error, const std::source_location &location = std::source_location::current())`|Return a single-line exception diagnostic text with source code location.|

#### `error_diagnostic`

Declaration: `class error_diagnostic`.

Record diagnostic values in files, rows, columns, functions, and conditions; source_location defaults to capturing interface calling positions. get_message outputs a single-line VSCode recognizable diagnostic format.

|Declaration|Purpose and calling semantics|
|---|---|
|`explicit error_diagnostic(const std::source_location &location = std::source_location::current(), std::string_view condition = {})`|Construct this type of instance; see the type description and signature for parameter meanings.|
|`error_diagnostic(std::string file, uint64_t line, uint64_t column, std::string function, std::string condition)`|Construct this type of instance; see the type description and signature for parameter meanings.|
|`virtual ~error_diagnostic()`|Destructs objects, ending their resources or referenced lifetimes.|
|`const std::string &get_file() const`|Read the name of the diagnostic source file.|
|`uint64_t get_line() const`|Read the diagnostic line number.|
|`uint64_t get_column() const`|Read the diagnostic column number.|
|`const std::string &get_function() const`|Read the diagnostic function name.|
|`const std::string &get_condition() const`|Read the failed conditional expression.|
|`std::string get_message(std::string_view key = {}, std::string_view detail = {}) const`|Return a single line of text in the format of file:line:column:error:condition[key] detail.|

### `easyvrui/common/error.h`

Controls and drawing error keys, structured exceptions, and assertion condition checks.

#### Free Functions and Type Aliases

|Declaration|Purpose and Return Values|
|---|---|
|`string_view get_language_key(error_key_t key)`|Convert the error enumeration to language keys.|

#### `error_key_t`

Declaration: `enum class error_key_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`unknown`|Unknown errors.|
|`owning_thread_required`|Please use begin_invoke() to access the control from the worker thread.|
|`callable_required`|The field requires a callable object.|
|`candidate_string_sequence`|The candidate must be a string sequence.|
|`candidate_index_invalid`|The candidate index must be an integer.|
|`operation_failed`|UI service operation failed.|
|`service_disconnected`|UI service connection has been disconnected.|
|`service_request_timeout`|UI service request timed out.|
|`number_required`|The field must be a numerical value.|
|`finite_number_required`|The field must be a finite numerical value.|
|`unsigned_integer_required`|The field must be an unsigned integer.|
|`three_component_required`|The field requires three components.|
|`name_invalid`|The name must be a non-empty string.|
|`duplicate_property`|Property duplication: specified value.|
|`unknown_property`|Unknown property: specified value.|
|`property_type_mismatch`|Property type mismatch: specified value.|
|`duplicate_control_name`|Control name duplication: specified value.|
|`duplicate_tabpage_name`|Tab page name duplication: Specified value.|
|`event_data_object_required`|Event data must be an object.|
|`object_disposed`|The object has been released.|
|`window_activation_failed`|The window cannot be activated.|
|`control_focus_failed`|The control cannot gain focus.|
|`client_mismatch`|The control belongs to a different UI runtime environment.|
|`control_has_parent`|The control already belongs to a container.|
|`cyclic_control_hierarchy`|A control cannot contain itself or its ancestor controls.|
|`cyclic_reference_object`|Window reference objects cannot form a loop.|
|`cyclic_json_container`|JSON containers cannot contain themselves or their ancestors.|
|`control_not_in_container`|The control does not belong to this container.|
|`item_not_in_collection`|The option does not belong to this collection.|
|`item_index_out_of_range`|The option index is out of range.|
|`selected_item_index_out_of_range`|The index of the selected option is out of range.|
|`selected_tab_index_out_of_range`|The index of the selected tab is out of range.|
|`positive_rect_required`|The width and height of the control must be positive numbers.|
|`positive_row_height_required`|The line height must be greater than zero.|
|`positive_tab_size_required`|The tag size must be greater than zero.|
|`font_family_invalid`|The font name cannot be empty or contain NUL.|
|`font_size_invalid`|The font size must be a positive integer.|
|`title_font_family_invalid`|The title font name is invalid.|
|`title_font_size_invalid`|The title font size must be greater than zero.|
|`tab_font_family_invalid`|The tag font name is invalid.|
|`tab_font_size_invalid`|The tag font size must be greater than zero.|
|`physical_scale_invalid`|physical_scale must be a finite positive multiple.|
|`curvature_invalid`|The curvature must be non-negative, and the total arc of the window must be less than one full circle.|
|`position_invalid`|The position must be composed of finite values.|
|`rotation_invalid`|The rotation must be composed of finite values.|
|`combobox_item_required`|The text must match the available options in the combo box.|
|`invalid_dialog_owner`|The dialog owner must be an interactive window.|
|`invalid_reference_object_type`|The reference object type is invalid.|
|`reference_not_tracked`|The window reference object is currently not tracked.|
|`unknown_reference_object`|Unknown window reference object.|
|`invalid_reference_owner`|The reference must point to a window that is not closed in the current UI runtime environment.|
|`control_required`|A control instance is required.|
|`tabpage_required`|A tabpage instance is required.|
|`page_list_required`|Please manage through the get_page_list () tab.|
|`invalid_rotation`|The rotation value is invalid.|
|`zero_direction`|The direction vector cannot be zero.|
|`invalid_utf8_leading_byte`|The initial UTF-8 byte is invalid.|
|`invalid_utf8_continuation_byte`|The subsequent UTF-8 bytes are invalid.|
|`truncated_utf8`|The UTF-8 sequence is incomplete.|
|`overlong_utf8`|The UTF-8 sequence has an oversized encoding.|
|`invalid_utf8_scalar`|The UTF-8 character value is out of range.|
|`invalid_utf32_scalar`|The UTF-32 character value is out of range.|
|`truncated_utf16_surrogate`|The UTF-16 surrogate pair is incomplete.|
|`invalid_utf16_surrogate`|The UTF-16 surrogate pair is invalid.|
|`invalid_utf16_low_surrogate`|The low-order UTF-16 surrogate item is invalid.|
|`event_handler_null`|The event handling function cannot be empty.|
|`window_render_failed`|Window rendering failed.|
|`service_stopped`|Service has stopped.|
|`window_closing`|Window is closing.|
|`window_closed`|Window has been closed.|
|`invalid_drawing_coordinate`|The drawing coordinates must be finite values.|
|`invalid_drawing_radius`|The drawing radius must be a non-negative finite value.|
|`invalid_drawing_thickness`|The stroke width must be a positive finite value.|
|`invalid_drawing_opacity`|The drawing transparency must be a finite value between zero and one.|
|`invalid_drawing_rectangle`|The width and height of the drawing rectangle must be non-negative values.|
|`invalid_drawing_image`|The size of the drawing image must be positive and consistent with the RGBA8 byte count.|
|`drawing_image_size_overflow`|The byte count of the drawing image exceeds the integer or addressable size range.|
|`invalid_drawing_path`|The drawing path filling rules, line segment values, or graphic order are invalid.|
|`invalid_input_provider_role`|The input provider role must be layout or ime.|
|`language_pack_unavailable`|The language pack is not available: specified value.|
|`language_pack_object_required`|The language pack must be an object: specified value.|
|`language_value_text_required`|The language value must be text: specified value.|
|`language_key_unavailable`|The language key is not available: specified value.|
|`invalid_base64`|Invalid standard Base64 encoding.|
|`base64_size_overflow`|The Base64 data exceeds the container's addressable size.|
|`desktop_open_failed`|Unable to invoke the desktop application: specified value.|
|`grid_value_required`|The cell value cannot be empty.|
|`grid_boolean_required`|The cell value must be true or false.|
|`grid_integer_required`|The cell value must be a 64-bit signed integer.|
|`grid_finite_number_required`|Cell values must be finite floating-point numbers.|
|`grid_cell_type_mismatch`|Cell values must maintain their original type.|
|`grid_provider_read_only`|The cell data provider is read-only.|
|`grid_value_rejected`|Cell values are rejected.|
|`grid_value_type_required`|Cell values must be text, 64-bit signed integers, finite floating-point numbers, or boolean values.|
|`grid_write_result_invalid`|The cell write callback must return bool, None, error text, or a bool, error text.|
|`process_launch_failed`|Application startup failed; diagnostic information includes a Windows error code.|

#### `engine_error`

Declaration: `class engine_error: public error_diagnostic, public runtime_error`.

Control and drawing exceptions, inheriting from error_diagnostic and std::runtime_error; get_key returns error_key_t, and what() returns a single-line diagnostic.

|Declaration|Purpose and calling semantics|
|---|---|
|`engine_error(error_key_t key, vector<string> argument_list = {}, const source_location &location = source_location::current(), string_view condition = {})`|Abnormalities due to key presses; argument_list is replaced with localized descriptions; location defaults to the call location, and condition saves failed conditions.|
|`error_key_t get_key() const`|Read the structured error key.|
|`const vector<string> &get_argument_list() const`|Read the error formatting parameters.|

### `easyvrui/localization/error.h`

Connect to the layer error key and localize exceptions.

#### Free Functions and Type Aliases

|Declaration|Purpose and Return Values|
|---|---|
|`using localized_invalid_argument = localized_exception<invalid_argument>`|Aliases for localized_exception and <invalid_argument>.|
|`using localized_runtime_error = localized_exception<runtime_error>`|Aliases for localized_exception and <runtime_error>.|
|`string_view get_language_key(language_key_t key)`|Convert the error enumeration to language keys.|
|`string get_localized_error(language_key_t key, const vector<string> &argument_list = {})`|Generate localized error text based on language_key_t and argument_list.|
|`void select_error_language(const string &language)`|Select the connection error language.|
|`string get_error_language()`|Return the current connection error language code.|

#### `language_key_t`

Declaration: `enum class language_key_t`.

|Declaration|Purpose and calling semantics|
|---|---|
|`unknown`|Unclassified errors.|
|`service_disconnected`|Service connection has been disconnected.|
|`operation_failed`|Operation failed.|
|`invalid_utf32_scalar`|UTF-32 contains illegal Unicode scalars.|
|`winsock_initialization_failed`|Network runtime environment initialization failed.|
|`service_connection_failed`|Connection to the service failed.|
|`invalid_frame_length`|The received frame length is invalid.|
|`json_object_required`|The message must be a JSON object.|
|`invalid_outgoing_frame_size`|Invalid frame size for sending.|
|`socket_wait_failed`|Socket waiting failed.|
|`accepted_connection_configuration_failed`|Connection configuration failed.|
|`service_connection_cancelled`|Connection operation was cancelled.|
|`service_identity_mismatch`|Service identity or startup parameters do not match.|
|`tls_operation_failed`|TLS operation failed.|
|`authentication_failed`|Access authentication failed.|
|`invalid_session`|Session is invalid.|
|`heartbeat_timeout`|Heartbeat timeout.|
|`remote_service_unavailable`|Remote service is unavailable.|
|`service_startup_timeout`|Service startup timeout.|
|`executable_location_failed`|Failed to query the location of the executable file.|
|`native_service_required`|Native service program is required.|
|`native_service_start_failed`|Native service startup failed.|

#### `localized_exception<base_type>`

Declaration: `class localized_exception: public error_diagnostic, public base_type`.

Template exception, inheriting from error_diagnostic and base_type simultaneously. localized_invalid_argument corresponds to invalid_argument, and localized_runtime_error corresponds to runtime_error. Members of get_language_key () return language_key_t enumeration.

|Declaration|Purpose and calling semantics|
|---|---|
|`localized_exception(language_key_t key, vector<string> argument_list = {}, const source_location &location = source_location::current(), string_view expression = {})`|Generate localized exception based on the connection error key and argument_list. The location records the calling position, and the expression saves the failure conditions.|
|`language_key_t get_language_key() const`|Enumeration of error keys that return this exception.|
|`const vector<string> &get_argument_list() const`|Read the error formatting parameters.|

### `easyvrui/localization/request_error.h`

Exception types for remote request failures.

#### `request_error`

Declaration: `class request_error: public error_diagnostic, public std::runtime_error`.

Request failure exception, providing the source location interfaces for std::runtime_error::what () and error_diagnostic; language_key and argument_list retain the error messages given by the service.

|Declaration|Purpose and calling semantics|
|---|---|
|`request_error(std::string language_key, std::string message, std::vector<std::string> argument_list, error_diagnostic diagnostic)`|Request exception constructed from UTF-8 language key, service error description, formatted parameters, and existing source code diagnosis.|
|`const std::string &get_language_key() const`|Return the error key string for this exception.|
|`const std::vector<std::string> &get_argument_list() const`|Read the error formatting parameters.|

### `easyvrui/localization/language_pack.h`

Interface language selection and language text query.

#### `language_pack`

Declaration: `class language_pack`.

`get_current()` obtains the current SDK language pack. Built-in texts are included in the static library and DLL, and are selected based on the system language by default. `load_directory(path)` can explicitly load custom language packs from a specified directory, with `en.json` providing the basic texts.

|Declaration|Purpose and calling semantics|
|---|---|
|`static language_pack &get_current()`|Return the current language pack managed by the SDK.|
|`void select_language(const std::u32string &language)`|Select the interface language, supporting zh, ja, en, and their regional forms normalization.|
|`std::string get_code() const`|Read the current language code.|
|`static std::unique_ptr<language_pack> load_directory(const std::filesystem::path &path)`|Load the language package from the specified directory.|
|`std::vector<std::u32string> get_available_locale_list() const`|Read the language codes in the directory.|
|`std::vector<std::u32string> get_key_list() const`|List the keys of the current language package.|
|`size_t get_size() const`|Read the number of language keys.|
|`std::optional<std::u32string> find_text(const std::u32string &key) const`|Search for the translation text by key; return null value if missing.|
|`std::u32string get_text(const std::u32string &key) const`|Return the translation text by Unicode language key; return the key itself if the key does not exist.|
|`std::string get_message(const std::string &key, const std::vector<std::string> &argument_list) const`|Read the UTF-8 language key, substitute UTF-8 parameters with placeholders such as {0}, {1}, etc., and return the UTF-8 description.|

## General input and verification

### `easyvrui/common/keyboard_key.h`

Enumeration of special keys and parsing of text key names. `keyboard_key_t` includes `unknown`, `backquote`, `backspace`, `tab`, `enter`, `escape`, `space`, direction keys `left/right/up/down`, `home/end/page_up/page_down/insert/delete_key`, `caps_lock/num_lock/scroll_lock/menu/pause`, `f1` to `f24`, as well as the respective general, left, and right enumeration items of `control/shift/alt/meta`, such as `control/left_control/right_control`.

|Declaration|Purpose and Return Values|
|---|---|
|`keyboard_key_t parse_keyboard_key(std::string_view text)`|Parse UTF-8 special key names; return unknown if not recognized.|
|`keyboard_key_t parse_keyboard_key(std::u32string_view text)`|Parse UTF-32 special key names; return unknown if not recognized.|

Key names are matched case-insensitive, supporting `Ctrl/Control`, `Enter/Return`, `Meta/Win`, and corresponding left and right modifier key aliases. Ordinary characters are read through event key/text; unknown only indicates that no special key is matched.

#### `keyboard_modifier_t`

Declaration: `struct keyboard_modifier_t`.

Key modifier states, ctrl, shift, alt, meta are false by default.

|Declaration|Purpose and calling semantics|
|---|---|
|`bool ctrl = false`|Control modifier state, false by default.|
|`bool shift = false`|Shift modifier state, false by default.|
|`bool alt = false`|Alt modifier state, false by default.|
|`bool meta = false`|Windows/Meta modifier state, false by default.|

#### `keyboard_key_t`

Declaration: `enum class keyboard_key_t`.

Enumeration of named special keys, parse_keyboard_key accepts UTF-8 or UTF-32 names; return unknown for unrecognized names.

|Declaration|Purpose and calling semantics|
|---|---|
|`unknown`|Unrecognized special keys.|
|`backquote`|Special key `backquote`; string names are parsed by parse_keyboard_key.|
|`backspace`|Special key `backspace`; string names are parsed by parse_keyboard_key.|
|`tab`|Special key `tab`; string names are parsed by parse_keyboard_key.|
|`enter`|Special key `enter`; string names are parsed by parse_keyboard_key.|
|`control`|Special key `control`; string names are parsed by parse_keyboard_key.|
|`left_control`|Special key `left_control`; string names are parsed by parse_keyboard_key.|
|`right_control`|Special key `right_control`; string names are parsed by parse_keyboard_key.|
|`shift`|Special key `shift`; string names are parsed by parse_keyboard_key.|
|`left_shift`|Special key `left_shift`; string names are parsed by parse_keyboard_key.|
|`right_shift`|Special key `right_shift`; string names are parsed by parse_keyboard_key.|
|`alt`|Special key `alt`; string names are parsed by parse_keyboard_key.|
|`left_alt`|Special key `left_alt`; string names are parsed by parse_keyboard_key.|
|`right_alt`|Special key `right_alt`; string names are parsed by parse_keyboard_key.|
|`meta`|Special key `meta`; string names are parsed by parse_keyboard_key.|
|`left_meta`|Special key `left_meta`; string names are parsed by parse_keyboard_key.|
|`right_meta`|Special key `right_meta`; string names are parsed by parse_keyboard_key.|
|`pause`|Special key `pause`; string names are parsed by parse_keyboard_key.|
|`escape`|Special key `escape`; string names are parsed by parse_keyboard_key.|
|`space`|Special key `space`; string names are parsed by parse_keyboard_key.|
|`left`|Special key `left`; string names are parsed by parse_keyboard_key.|
|`right`|Special key `right`; string names are parsed by parse_keyboard_key.|
|`up`|Special key `up`; string names are parsed by parse_keyboard_key.|
|`down`|Special key `down`; string names are parsed by parse_keyboard_key.|
|`home`|Special key `home`; string names are parsed by parse_keyboard_key.|
|`end`|Special key `end`; string names are parsed by parse_keyboard_key.|
|`page_up`|Special key `page_up`; string names are parsed by parse_keyboard_key.|
|`page_down`|Special key `page_down`; string names are parsed by parse_keyboard_key.|
|`insert`|Special key `insert`; string names are parsed by parse_keyboard_key.|
|`delete_key`|Special key `delete_key`; string names are parsed by parse_keyboard_key.|
|`caps_lock`|Special key `caps_lock`; string names are parsed by parse_keyboard_key.|
|`num_lock`|Special key `num_lock`; string names are parsed by parse_keyboard_key.|
|`scroll_lock`|Special key `scroll_lock`; string names are parsed by parse_keyboard_key.|
|`menu`|Special key `menu`; string names are parsed by parse_keyboard_key.|
|`f1`|Special key `f1`; string names are parsed by parse_keyboard_key.|
|`f2`|Special key `f2`; string names are parsed by parse_keyboard_key.|
|`f3`|Special key `f3`; string names are parsed by parse_keyboard_key.|
|`f4`|Special key `f4`; string names are parsed by parse_keyboard_key.|
|`f5`|Special key `f5`; string names are parsed by parse_keyboard_key.|
|`f6`|Special key `f6`; string names are parsed by parse_keyboard_key.|
|`f7`|Special key `f7`; string names are parsed by parse_keyboard_key.|
|`f8`|Special key `f8`; string names are parsed by parse_keyboard_key.|
|`f9`|Special key `f9`; string names are parsed by parse_keyboard_key.|
|`f10`|Special key `f10`; string names are parsed by parse_keyboard_key.|
|`f11`|Special key `f11`; string names are parsed by parse_keyboard_key.|
|`f12`|Special key `f12`; string names are parsed by parse_keyboard_key.|
|`f13`|Special key `f13`; string names are parsed by parse_keyboard_key.|
|`f14`|Special key `f14`; string names are parsed by parse_keyboard_key.|
|`f15`|Special key `f15`; string names are parsed by parse_keyboard_key.|
|`f16`|Special key `f16`; string names are parsed by parse_keyboard_key.|
|`f17`|Special key `f17`; string names are parsed by parse_keyboard_key.|
|`f18`|Special key `f18`; string names are parsed by parse_keyboard_key.|
|`f19`|Special key `f19`; string names are parsed by parse_keyboard_key.|
|`f20`|Special key `f20`; string names are parsed by parse_keyboard_key.|
|`f21`|Special key `f21`; string names are parsed by parse_keyboard_key.|
|`f22`|Special key `f22`; string names are parsed by parse_keyboard_key.|
|`f23`|Special key `f23`; string names are parsed by parse_keyboard_key.|
|`f24`|Special key `f24`; string names are parsed by parse_keyboard_key.|

## Link macros

### `engine_interface_api.h`

Declaration macros for static libraries and DLLs, set by the build configuration in link form.

|Macro or Compilation Definitions|Purpose|
|---|---|
|`ENGINE_INTERFACE_BUILD`|When building DLLs, expand ENGINE_INTERFACE_API to __declspec(dllexport)|
|`ENGINE_INTERFACE_STATIC`|Used by static libraries and their callers; ENGINE_INTERFACE_API expands to nothing|
|`ENGINE_INTERFACE_API`|When the aforementioned build macro is not defined, expand to __declspec(dllimport, declaring that the DLL imports interfaces)|

## Standard dialogs

The following functions return results upon completion of the call, continuously processing interface activities during waiting periods. owner specifies the direct parent window; the parent window is disabled during modal periods, while other windows continue to interact. Dialog boxes use World and center positioning and inherit physical_scale from the parent window.

### Colors and Fonts

|Header files|Functions|Results|
|---|---|---|
|`easyvrui/dialog/color_dialog.h`|`std::optional<uint32_t> color_dialog(uint32_t color = 0x000000ffu, const std::u32string &title = U"", uint32_t default_color = 0x000000ffu, window *owner = nullptr)`|Confirmation returns `0xRRGGBBAA`, cancellation returns `std::nullopt`|
|`easyvrui/dialog/font_dialog.h`|`std::optional<font_t> font_dialog(const font_t &font = font_t{}, const std::u32string &title = U"", const font_t &default_font = font_t{}, window *owner = nullptr)`|Confirmation returns the system font, cancellation returns `std::nullopt`|

Color interfaces include color gamut, hue, transparency, and RGB/HSV inputs. Font interfaces provide system fonts, numerical sizes, bold, italic, and preview. default_color and default_font specify the default values for button restoration.

### Message Boxes and Input Fields

`easyvrui/dialog/messagebox.h` provides two overloads:

```cpp
dialog_result_t messagebox(const std::u32string &message, const std::u32string &title = U"", messagebox_button_set_t button_set = messagebox_button_set_t::ok, messagebox_icon_t icon = messagebox_icon_t::none, dialog_result_t default_button = dialog_result_t::none, window *owner = nullptr);
std::u32string messagebox(const std::u32string &message, const std::u32string &title, const std::vector<messagebox_button_t> &button_list, messagebox_icon_t icon = messagebox_icon_t::none, const std::u32string &default_button_name = U"", window *owner = nullptr);
```

`messagebox_button_t` saves name and text. The standard overload returns `dialog_result_t`; the custom button overload returns the name of the selected button.

|Enumeration|Members and Values|
|---|---|
|`messagebox_icon_t`|`none=0`、`error=0x10`、`question=0x20`、`warning=0x30`、`information=0x40`|
|`messagebox_button_set_t`|`ok=0`、`ok_cancel=1`、`abort_retry_ignore=2`、`yes_no_cancel=3`、`yes_no=4`、`retry_cancel=5`|
|`dialog_result_t`|`none=0`、`ok=1`、`cancel=2`、`abort=3`、`retry=4`、`ignore=5`、`yes=6`、`no=7`|

`easyvrui/dialog/inputbox.h` declares:

```cpp
std::optional<std::u32string> inputbox(const std::u32string &prompt, const std::u32string &title = U"", const std::u32string &default_text = U"", uint64_t max_length = 0u, window *owner = nullptr);
```

Confirmation returns the input text, allowing empty strings and literal text cancel; cancellation returns `std::nullopt`. When max_length is 0, there is no length limit.

### Opening and Saving Files

`easyvrui/dialog/file_open_dialog.h` declares the filter `file_filter_t` and the opening function. `easyvrui/dialog/file_save_dialog.h` declares the saving function.

```cpp
std::vector<std::filesystem::path> file_open_dialog(const std::u32string &title = U"", const std::filesystem::path &initial_directory = {}, const std::u32string &initial_filename = U"", const std::vector<file_filter_t> &filter_list = {}, std::size_t filter_index = 0u, bool multi_select = false, const std::u32string &confirm_text = U"", window *owner = nullptr, std::function<void(const std::filesystem::path &)> directory_changed = {}, std::function<void(std::size_t)> filter_changed = {});
std::optional<std::filesystem::path> file_save_dialog(const std::u32string &title = U"", const std::filesystem::path &initial_directory = {}, const std::u32string &initial_filename = U"", const std::vector<file_filter_t> &filter_list = {}, std::size_t filter_index = 0u, const std::u32string &default_extension = U"", bool confirm_overwrite = true, const std::u32string &confirm_text = U"", window *owner = nullptr, std::function<void(const std::filesystem::path &)> directory_changed = {}, std::function<void(std::size_t)> filter_changed = {});
```

Use a memory directory when `initial_directory` is empty. `initial_filename` is used to prefill the file name. When the filter list is empty, the default filter is used; `filter_index` starts from 0. `file_filter_t`'s `pattern_list` supports `*` and `?`. `confirm_text` uses localizable confirmation buttons when empty. Directory and filter callbacks are received in the UI thread upon initial values and subsequent changes.

Opening returns the selected path list, cancellation returns an empty list. Enabling `multi_select` allows selecting multiple files. Saving returns the target path, cancellation returns `std::nullopt`. When `default_extension` is empty, it derives from the current filter; `confirm_overwrite` controls overwrite confirmation.

## Common Call Combinations

|Scenario|Call Entries|
|---|---|
|Create a regular window|Construct the window → Configure properties → get_control_list().add→show→easyvrui::run|
|Configure the font|Copy font_t returned by get_font() → Modify the field → set_font|
|Update the interface from the background|begin_invoke (callback) → Call the setter in the callback|
|Open a modal window|Construct an independent window → show_dialog (owner) → Enumerate the results. The event handler sets the results through set_dialog_result|
|Custom controls|Derive a control or text_control → Overload render/render_overlay → Invalidate after the state changes|
|Create a tab|Construct `tabcontrol` and `tabpage` → Call `tabpage::set_text()` to set the title → `page_list.add(page)` → Add child controls to the page|
|Modify the text selection|select(start,length)→get_selected_text/set_selected_text|
|Remove event callbacks|Save the token returned by on_click.add (callback) → on_click.remove (token)|
|Custom IME|register_provider (input_role_t::ime) → Dispatch on_input → Consume and commit_text, or keep handled=false for automatic forwarding|
|Custom layout|input_provider.register_provider (input_role_t::layout) → Display a auxiliary window based on the state → send_event sends key presses → Run|
|Manually integrate application loops|Periodically call easyvrui::pump; the host is responsible for arranging the calling timing and other tasks|

The example application directory is `repo/app/demo/cpp`; the application is responsible for combining the API header files and compiled engine_interface libraries into an executable program. Python examples are located at `repo/app/demo/python`.
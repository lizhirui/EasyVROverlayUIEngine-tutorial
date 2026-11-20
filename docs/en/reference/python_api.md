# Python API Reference

For control usage and complete examples, see the [control catalog](/en/guide/). Windows, events, and thread scheduling are covered in [window,](/en/guide/controls/window-and-text/window), and [strong-type events and multithreading scheduling](/en/guide/07_events_dialogs_threading).

The name of regular controls uses `type_用途`, such as `button_ok`. Public control members exported by the designer have the same name as their corresponding names, which can be accessed directly through `button_ok`; the form class name corresponds to the design file name.

This article introduces the public interfaces and calling rules of `easyvrui`. Method signatures are omitted in `self`.

## 1. Import and Running Conventions

### 1.1. Application Composition

After installation, the Python application uses `sdk/api/python/` in the root directory. This directory contains `easyvrui/`, statically linked `engine_interface_native*.pyd`, and `requirements.txt`. The interpreter must match the CPython version and x64 architecture specified in the installation record. When the list is initiated via Desktop or File Manager through SDK, the sub-process' `PYTHONPATH` will prepend this directory and retain the original value, and `EASYVRUI_NATIVE_DIR` also points to this directory. When running examples directly from CMD, this directory is prepended to `PYTHONPATH`.

During source code development, `repo/sdk/api/python/` can be added to the module search path, and the directory of the built extension can be specified using `EASYVRUI_NATIVE_DIR`. The loader also supports searching for extensions from the parent directory of the library files pointed to by `EASYVRUI_ENGINE_INTERFACE`. When building extensions using DLL linking, matching `engine_interface.dll` must be deployed. The extensions deployed by the installer already include native implementations.

The API part of Python uses standard libraries and pre-compiled extensions. Your own Python dependencies are recorded in the corresponding application directory's `requirements.txt`. Example applications are located in `repo/app/demo/python`, and their control derived classes belong to the application examples.

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

### 1.2. Modules and Namespaces

`import easyvrui` provides public entry points. Controls and value types in sub-modules reference the same native class.

|Import Location|Public Interfaces|
|---|---|
|`easyvrui`|Controls, value types, events, drawing, dialog boxes, application functions, and input components|
|`easyvrui.application`|`run`, `set_application_name`, `pump`, input interface, and application management functions|
|`easyvrui.application_manage`|Application list, startup, running snapshots, and session and window management|
|`easyvrui.control`|Controls and their collections|
|`easyvrui.common.color/rect/font`|Colors, rectangles, and fonts|
|`easyvrui.common.error`|Language selection and localization exceptions|
|`easyvrui.geometry`|`vec3`、`quat`、`pose`|
|`easyvrui.dialog`|Standard dialog functions, file filtering, and message box enumeration|
|`easyvrui.event`|`event_container` and strong-type event parameters|
|`easyvrui.render`|`render_context`、`drawing_path`、`drawing_image`、`drawing_fill_rule`|
|`easyvrui.input`|`input_provider`, roles, input events, and component states|

The following table lists the top-level application interfaces of `easyvrui`.

|Name|Name|Name|Name|
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

### 1.3. Export Layout of Design Files

The generated Python layout files use `import easyvrui`. All non-root controls are exposed via `self.<control.name>`, with property names exactly matching the control names; names are unique throughout the design, following C++ and Python identifier rules, and avoiding the root SDK public entry points.

Only the generation class itself has `__init__`. By default, the name uses the name of the design root node, such as `def __init__(self, name = "sample_form"):`. The constructor creates controls and establishes ownership relationships through `control_list` or `page_list`, then initializes attributes and value records.

Images and icons call SDK drawing resource interfaces such as `easyvrui.drawing_image.load_file()`. Business classes hold instances of form generators, and use properties with the same names to bind events and read/write control properties.

Form Designer is an independent app. Its design files have the extension `.easyvruifrm`, and it can export Python and C++ design code. The property panel propertygrid belongs to the internal derived controls of this app. Ordinary applications use the general grid. The generated Python design class creates controls, configures attributes, and assembles containers through public APIs.

### 1.4 Parameters, Return Values, and Data Types

The interface table is described using Python types. Parameters with names explicitly declared in binding can use keyword arguments; some directly mapped methods are only registered with position parameters. In the following signatures, `/` indicates that it should be called by position, based on the position parameters in the function signature.

|Type|Calling Convention|
|---|---|
|`str`|Unicode text; control names, displayed text, font families, etc., all use ordinary Python strings.|
|`int`|Unsigned 64-bit fields accept values from `0` to `2**64-1`; colors accept values from `0` to `2**32-1`; Signed 64-bit fields accept values from `-(2**63)` to `2**63-1`.|
|`float`|Corresponding double-precision values; spatial positions, rotation angles, scaling, and drawing coordinates are verified for limitedness and range according to interface requirements.|
|`bool`|Switches; application code should pass `True` or `False`.|
|`None`|No objects, no selected items, or missing optional values; see the corresponding interface for specific meanings.|
|`list`、`set`|Reading from attributes usually results in a snapshot; after modifying the snapshot, the attribute needs to be reassigned. See the collection section for specialized collection types.|

Text positions are counted by Unicode code points, consistent with Python's `len(text)` and slicing indices. Composite characters, variant selectors, and multi-code point emojis may occupy multiple positions; cursor movement and deletion in user interaction are processed according to text boundaries. When setting selections in the program, legal text positions should be used.

### 1.5 Objects, Threads, and Updates

Operate on controls and windows on the creation thread. Objects in containers belong to the same application running environment. `begin_invoke()` is used to arrange work on the creation thread from other threads. Actual execution depends on the application continuing to call `run()` or `pump()`. Callbacks should return as soon as possible; time-consuming tasks can be transferred to background threads and then updated through `begin_invoke()`.

The constructor for ordinary controls is uniformly `类型(name: str)`. `name` cannot be empty and cannot contain empty characters; it is read-only after construction. Names within the same collection are unique, and adding duplicate names will throw an exception. A control can only have one parent container at a time, and no circular parent-child relationships can be formed.

Control attributes can be read and written within the application. Changes to attributes that affect display will arrange for redrawing; after changes to ordinary Python members that depend on custom drawing, call `invalidate()`. Applications loop to handle inputs, events, and pending updates. After `render()` returns, the drawing is uniformly submitted by the framework; simply call the drawing interface in order in the drawing callback.

## 2. Basic Value Types

### 2.1.rect

Import: `from easyvrui import rect`.

Construction: `rect(left: int = 0, top: int = 60, width: int = 160, height: int = 40)`.

|Member|Reading and Writing|Purpose|
|---|---|---|
|`left: int`|Reading and Writing|Left position of the logical rectangle|
|`top: int`|Reading and Writing|Top position of the logical rectangle|
|`width: int`|Reading and Writing|Logical width|
|`height: int`|Reading and Writing|Logical Height|
|`a == b -> bool`|Operator|Field-by-field Comparison|

All four fields are unsigned 64-bit integers. Independent `rect` objects store their own values; the objects obtained from `control.rect` are views associated with the control, so `button_ok.rect.left = 80` will directly update the control. Values are written when an independent rectangle is assigned to `control.rect`. The control rectangle requires `width > 0` and `height > 0`.

The position of a regular sub-control relative to the parent container; the `rect.left/top` of the window does not participate in spatial positioning. The window position uses `position`.

### 2.2.color

Constructed as `color(value: int | color = 0)`. Color integers use `0xRRGGBBAA`, with a height of 24 bits for RGB and the lowest 8 bits for transparency. Transparency `0` is completely transparent, while `255` is completely opaque.

|Member|Purpose|
|---|---|
|`value: int`|Read and write complete color values, with a range of unsigned 32-bit integers.|
|`r: int`、`g: int`、`b: int`、`a: int`|Read and write red, green, blue, and transparency components, with a range of `0` to `255`.|
|`rgba: list[int]`|Read-only, returns red, green, blue, and transparency in order.|
|`hex_string: str`|Read-only, eight-digit hexadecimal color text with the prefix `0x`.|
|`color.create_from_rgba(r: int, g: int, b: int, a: int = 255) -> color`|Construct color based on four components.|
|`color.create_from_hex(text: str) -> color`|Parse eight-digit hexadecimal color text, supporting the prefix `0x`.|
|`create_with_alpha(alpha: int, /) -> color`|Return the new color after replacing transparency.|
|`int(value)`、`value.__index__()`|Obtain the complete color integer.|
|`str(value)`|Obtain the hexadecimal color text.|
|`a == b`|Compare complete color values.|

The control color property accepts color integers and `color` objects, returning `int` when reading. The color parameter in drawing methods uses integers, which can be converted using `int(color_object)`.

### 2.3.font

Constructed as `font(family: str = "Segoe UI", size: int = font.DEFAULT_SIZE, bold: bool = False, italic: bool = False)`. The class constant `font.DEFAULT_SIZE` is `18`.

|Member|Purpose|
|---|---|
|`family: str`|Read and write system font family names.|
|`size: int`|Read and write logical font sizes, as unsigned 64-bit integers.|
|`bold: bool`|Read and write bold status.|
|`italic: bool`|Read and write italic status.|
|`a == b`|Field-by-field Comparison|

When assigning a font to a control, `family` must not be empty and must not contain null characters. `size` must be greater than `0`. Reading the `font` property of the control will obtain the independent font value. When modifying the font size, first obtain `style = textbox_text.font`, then set `style.size = 22`, and assign `style` back to the control.

### 2.4.vec3

Constructed as `vec3(x: float = 0.0, y: float = 0.0, z: float = 0.0)`. `x/y/z` can be read and written.

|Member|Purpose|
|---|---|
|`a == b`|Per-component approximate comparison|
|`a + b -> vec3`、`a - b -> vec3`|Per-component addition and subtraction|
|`value * scalar -> vec3`、`scalar * value -> vec3`|Scalar multiplication|
|`calculate_dot_product(other: vec3, /) -> float`|Dot product|
|`calculate_cross_product(other: vec3, /) -> vec3`|Cross product|
|`length: float`|Read-only, vector length|
|`normalized: vec3`|Read-only, returns a unit vector in the same direction. Throws an exception if the direction is zero, too small, or contains non-finite values.|
|`vec3.is_equal(left: float, right: float) -> bool`|Approximate comparison of two scalars using double-precision epsilon and numerical scale|

Spatial position is in meters, window Euler angles are in degrees. When modifying window positions, perform an overall assignment, for example, `window_main.position = vec3(0.1, 0.0, 0.0)`.

### 2.5.quat

Constructed as `quat(x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0)`. `x/y/z/w` can be read and written; the default value represents a unit rotation.

|Member|Purpose|
|---|---|
|`a * b -> quat`|Combine rotations, apply `b` first, then `a`|
|`length: float`|Read-only, quaternion length|
|`normalized: quat`|Read-only, unit quaternions|
|`inverse: quat`|Read-only, inverse rotation|
|`euler: vec3`|Read-only, XYZ Euler angles in degrees|
|`rotate(value: vec3, /) -> vec3`|Rotation vector|
|`slerp(target: quat, amount: float) -> quat`|Interpolation along the shortest arc of the quaternions, with progress `0.0` corresponding to the current rotation, and `1.0` corresponding to the target rotation|
|`quat.create_from_axis_angle(axis: vec3, angle: float) -> quat`|Rotate around a specified unit axis, with the angle unit being degrees|
|`quat.create_from_axis_basis(a: vec3, b: vec3, c: vec3, /) -> quat`|Construct a rotation from three orthogonal base axes after rotation|
|`quat.create_from_euler(angles: vec3) -> quat`|Construct a rotation from XYZ Euler angles in degrees|

The combination of Euler angles satisfies `Rz * Ry * Rx`. Reading `euler` may result in equivalent angles.

### 2.6.pose

Constructed as `pose(position: vec3 = vec3(), rotation: quat = quat())`. `position/rotation` can be read and written.

|Member|Purpose|
|---|---|
|`a * b -> pose`、`a @ b -> pose`|Combine poses, apply `b` first, then `a`|
|`inverse: pose`|Read-only, inverse pose|
|`matrix: tuple[tuple[float, ...], ...]`|Read-only, returns a 4×4 homogeneous transformation matrix per row, with the last column containing translation components|
|`transform_point(value: vec3, /) -> vec3`|Convert local points to the reference frame of the pose|

The configurable position and rotation of the window are `position` and `rotation`, respectively.

## 3. Control inheritance tree and common conventions

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

Derived classes inherit properties, methods, and events exposed by the ancestor; see the corresponding sections for rules for blank instances. Ordinary controls are created through `类型(name: str)`. `control_base` provides `super().__init__(name: str, type: str)` for Python-derived classes; directly creating an instance of control_base will throw a TypeError. `menu_container(name: str, type: str)` provides a constructor entry for the menu container base class. See "Drawing and Custom Controls" for Python control derivation methods.

Python integration adaptation provides a constructor overload of `(name: str, type: str)` for `control/text_control/selection_control/item_control/container_control`, allowing custom derived types to specify type names; single-parameter constructors of these types still use their native type names.

### 3.1. Property access

Use the dot symbol to read properties, such as `textbox_entry.text`, and use assignment to modify writable properties, such as `textbox_entry.text = "Hello"`.

`control_list` and `page_list` are directly operable collection entries, and their attributes can be modified through collection methods; `item_list` is a collection of string items that can be directly operated on, and overall assignments can replace text lists. Other ordinary list or collection properties usually return snapshots, and reassignments are required after modification. Event members are subscribed through `+=/-=`.

### 3.2.control_base

Python-derived classes call `super().__init__(name, type)` in the constructor to complete the initialization of the native base class.

|Property|Reading and Writing|Purpose|
|---|---|---|
|`name: str`|Read-only|Object name determined at construction|
|`tag: str`|Reading and Writing|Apply the saved string marker, defaulting to an empty string. When the value changes, `on_tag_changed` is triggered, and the callback signature is `handler(source, event_args)`.|
|`type: str`|Read-only|The control type name of the object; Python-derived classes follow the corresponding native control type.|
|`disposed: bool`|Read-only|Whether it has been released, initially set to `False`.|
|`id: int`|Read-only|Object number|
|`parent: container_control \| None`|Read-only|Direct parent container|

|Signature|Purpose|
|---|---|
|`invalidate() -> None`|Request redrawing|
|`dispose() -> None`|Release the object and its related resources; the container will handle child objects accordingly.|
|`begin_invoke(callback: Callable[[], None], /) -> None`|Schedule callbacks to be executed in the object creation thread; calls that have not been executed after the object becomes invalid will be canceled.|
|`process_input(event: control_input_event_args, /) -> None`|Process inputs distributed to the object; can be overridden by derived classes.|

|Event|Purpose|
|---|---|
|`on_disposed`|Object release. Parameter is `event_args`.|
|`on_property_changed`|Triggered when a property changes, with `event.property_name` being the name of the changed property. Parameter is `property_changed_event_args`.|

### 3.3.control

General visual controls, adding rectangles, backgrounds, visibility, usability, and Tab order.

|Property|Type and initial values|Purpose|
|---|---|---|
|`rect`|`rect(0, 60, 160, 40)`|Control logic rectangle, with subfields that can be modified|
|`tooltip_text`|`str = ""`|Hover hint. Displays text when the window is directed by the laser pointer.|
|`background_color`|`int = 0x162738FF`|Background color|
|`visible`|`bool = True`|Whether to display|
|`enabled`|`bool = True`|Whether to accept interaction|
|`tab_index`|`int = 0`|Tab navigation sorting, using unsigned 64-bit integers|

|Signature|Purpose|
|---|---|
|`show() -> None`|Display controls|
|`hide() -> None`|Hide controls|
|`focus() -> None`|Request to focus to this control|
|`activate() -> None`|Execute programmatic activation actions for controls, such as triggering button clicks or item selections|
|`focusable: bool`|Query whether keyboard focus can be obtained; default for ordinary `control` is `False`, derived classes can override|
|`absolute_rectangle: rect`|Return to the logical rectangle of controls within the window.|
|`get_input_rectangle() -> rect`|Return to an independent rectangle, describing the local input area of controls, derived classes can override.|
|`focused: bool`|Query focus status.|
|`owning_window: window \| None`|Return to the parent window.|
|`get_content_top() -> float`|Obtain the top content offset; for ordinary controls, it is `0.0`, and the window includes the title bar and control ring.|
|`render(context: render_context, /) -> None`|Draw the main body of the control, can be overridden|
|`render_overlay(context: render_context, /) -> None`|Draw pop-up menus and other override content, can be overridden|

Tab navigation only selects controls that are visible, available, and focusable in the current window, `Tab` for forward, `Shift+Tab` for backward. `tab_index = 0` sorts by coordinates; positive values can be explicitly specified for control order. Specific sorting and loop rules are described in the focus section later.

|Event|Purpose|
|---|---|
|`on_background_color_changed`|Background color change. Parameter is `event_args`.|
|`on_visible_changed`|Visibility change. Parameter is `event_args`.|
|`on_enabled_changed`|Availability change. Parameter is `event_args`.|
|`on_tab_index_changed`|Tab order change. Parameter is `event_args`.|
|`on_moved`|Two-dimensional position change; also used to notify three-dimensional position changes in the window. Parameter is `event_args`.|
|`on_size_changed`|Logical size change; window physical scale changes also send size notifications. Parameter is `event_args`.|
|`on_pointer_enter`|Laser pointer enters. Parameter: `pointer_event_args`.|
|`on_pointer_leave`|Laser pointer exits. Parameter: `pointer_event_args`.|
|`on_pointer_move`|Laser pointer moves. Parameter: `pointer_event_args`.|
|`on_pointer_down`|Laser trigger is pressed. Parameter: `pointer_event_args`.|
|`on_pointer_up`|Laser trigger is released. Parameter: `pointer_event_args`.|
|`on_click`|Click completion. Parameter: `event_args`.|
|`on_scroll`|Scroll input. Parameter: `scroll_event_args`.|
|`on_viewport_changed`|Triggered when scroll viewport changes. Parameter: `event_args`.|
|`on_focus_in`|Focus is obtained. Parameter: `event_args`.|
|`on_focus_out`|Focus is lost. Parameter: `event_args`.|
|`on_key_down`|Keyboard is pressed. Parameter: `key_event_args`.|
|`on_key_up`|Keyboard is released. Parameter: `key_event_args`.|

#### blank

`blank(name: str)` can be imported from `easyvrui`, `easyvrui.control`, or `easyvrui.control.blank`, inheriting control, used for saving named rectangular placeholders.

|Basic properties|Call rules|
|---|---|
|`name: str`|Specified at construction, read-only|
|`rect: rect`|Readable and writable; can update rectangular subfields|

on_moved, on_size_changed, on_property_changed, and on_disposed remain available; `dispose()`, `disposed`, `invalidate()`, and `begin_invoke(callback)` follow the base class lifecycle and scheduling rules. Object identification and release status queries follow control_base conventions.

|Instance hiding entry|Behavior|
|---|---|
|`visible/enabled/background_color/tab_index`|Both reading and assignment throw AttributeError|
|`show/hide/focus/activate/focusable`|Instance access throws AttributeError|
|`render/render_overlay/process_input/get_input_rectangle/get_content_top`|Instance access throws AttributeError|
|Background color, visibility, usability, Tab order change events, as well as laser, click, scroll, focus, keyboard, and handle events|Instance access throws AttributeError|

Native objects can still be managed by the framework through the control base class interface; native layout treats `visible` and `enabled` as `False`. Python instances follow the hiding rules listed above through the access entry of the blank attribute.

```python
from easyvrui import blank, rect

blank_content = blank("blank_content")
blank_content.rect = rect(24, 80, 600, 320)
```

### 3.4.text_control

Provide styles for text display. This base class only adds styles; specific implementations like `text` are provided by types such as `label/button/textbox/combobox`.

|Property|Type and initial values|Purpose|
|---|---|---|
|`foreground_color`|`int = 0xD1DEF0FF`|Text foreground color|
|`font`|`font()`|Text font|

Event: `on_foreground_color_changed` is triggered when the foreground color changes; `on_font_changed` is triggered when the font changes.

### 3.5.selection_control

`selection_control` can be imported from `easyvrui`, `easyvrui.control`, or `easyvrui.control.selection_control`, and inherits from `text_control`. `item_control`, `grid`, `listview`, and `treeview` inherit this layer, while `listbox/combobox` inherits from `item_control`. Python custom derived classes can implement `clear_selection()` and override `is_blank_at(local_left, local_top)`; when derived from specific controls, the native implementation can be reused through `super()`.

|Member|Purpose|
|---|---|
|`clear_selection_on_blank_click: bool = False`|Whether to clear item selection when clicking blank space, used for selection strategies for blank space clicks|
|`on_clear_selection_on_blank_click_changed`|Triggered when the setting for clearing selection changes upon clicking blank space. Parameter is `event_args`.|
|`is_blank_at(local_left, local_top) -> bool`|Query whether the local coordinate is blank within the item area, can be overridden|
|`clear_selection() -> None`|Clear item selection; custom selection_control derived classes are responsible for implementation|

When the item area of listbox, treeview, grid, and listview is clicked in a blank space, it will exit text editing, close IME/layout, and retain the keyboard navigation focus of the collection control. Set to True to clear item selection; False to retain item selection. Headers, scroll bars, column width adjustment areas, and pop-up options are handled according to their functions. When switching to another text box, a single click completes the transfer of focus to the input interface; controls like buttons retain their respective focus and Tab behavior.

### 3.6.item_control

Base class with string items, single selection, and row-by-row scrolling, defaults to focusing.

|Property|Type and initial values|Read, write, and uses|
|---|---|---|
|`item_list`|`item_collection`, initially empty|Can modify collections; overall assignment accepts `list[str]`|
|`selected_index`|`int = -1`|Read, write; `-1` indicates no selection, other values must be existing item indices|
|`selected_item`|`str = ""`|Read-only; currently selected item, empty string if not selected|
|`row_height`|`int = 32`|Read, write; logical height of each row, must be greater than `0`|

Modifying the item collection may clear selected items outside the range and limit the scroll position to valid areas. Events are `on_item_list_changed`, `on_selected_index_changed`, `on_selection_changed`, `on_row_height_changed`, respectively notifying changes in items, indices, selections, scrolling, and row heights.

### 3.7. container_control, panel, and tabpage

`container_control` inherits from `control`. Ordinary child controls are uniformly managed by directly operable collections:

|Member|Purpose|
|---|---|
|`active_item_list: list[control]`|Query the currently displayed and interactive direct controls.|
|`control_list: control_collection`|Read-only collection entry|
|`on_control_added`|Triggered when a control is added. Read the control's `item` and its index `index` through `control_collection_event_args`.|
|`on_control_removed`|Triggered when a control is removed. Read the control's `item` and its index `index` before removal through `control_collection_event_args`.|

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

`panel(name)` is a regular container. `tabpage(name)` is the content container for tabs, and the page text is assembled through its own `control_list`. The page is managed by `tabcontrol.page_list`.

|Tab properties or events|Purpose|
|---|---|
|`text: str = ""`|Tab title; refresh the associated `tabcontrol` after modification|
|`on_text_changed`|Triggered when the tab title changes. Parameter is `event_args`.|

## 4. Specific controls

### 4.1.label

Inherits from `text_control`. Construction: `label(name: str)`.

|Member|Purpose|
|---|---|
|`text: str = ""`|Read and write text display|
|`on_text_changed`|Text changes. Parameter is `event_args`.|

Tags are used to display text; they do not participate in keyboard navigation by default.

### 4.2.button

Inherits from `text_control`. Construction: `button(name: str)`.

|Member|Purpose|
|---|---|
|`text: str = ""`|Read and write button text|
|`on_text_changed`|Text changes. Parameter is `event_args`.|
|Inherited from `on_click`|Execute button business logic|

The button can be focused. The button click handler can set the `dialog_result` property of the associated window to end the modal state.

### 4.3.textbox

Inherits from `text_control`. Construction: `textbox(name: str)`. Can be focused and provides text selection, editing, and scrolling.

|Property|Type and initial values|Read, write, and uses|
|---|---|---|
|`text`|`str = ""`|Read and write; text content|
|`read_only`|`bool = False`|Read and write; restricts interactive editing|
|`selectable`|`bool = True`|Read and write; whether cursor, selection, and interactive input are allowed|
|`multiline`|`bool = False`|Read and write; enables multi-line editing and Enter key for line break|
|`horizontal_scrollbar_visible`|`bool = False`|Read and write; switch for horizontal scroll bar display|
|`vertical_scrollbar_visible`|`bool = False`|Read and write; switch for vertical scroll bar display|
|`max_length`|`int = 0`|Read and write; upper limit of code points, `0` indicates no restriction|
|`selection_start`|`int = 0`|Read and write; smaller end position of the selection|
|`selection_length`|`int = 0`|Read and write; length of code points in the selection|
|`selected_text`|`str = ""`|Read and write, read the current selection text. The selection is replaced programmatically, including read-only text boxes|
|`can_undo`、`can_redo`|`bool = False`|Read-only; whether the current editing history supports undo or redo|

|Signature|Purpose|
|---|---|
|`select(start: int, length: int = 0) -> None`|Select by starting position and length; move the insertion position when the length is `0`|
|`undo() -> bool`|Undo an edit once. Return `True` if successful|
|`redo() -> bool`|Redo an edit. Return `True` if successful|

Text settings and replacements apply multi-line and length constraints; `\r\n` and `\r` are normalized to `\n`, and single-line mode removes line breaks. Filtration and truncation preserve complete text boundaries. Selection positions are limited to valid ranges, and non-boundary positions are adjusted according to the selection direction. The scroll bar switch controls display and line breaking capabilities separately with `multiline`

`read_only = True` allows retaining the cursor, selection, and copying, while interactive input and deletion keep the text unchanged. With `selectable = False`, the control still gains focus, but text cursor, selection, input editing, and the IME/layout interface are disabled; the application can still update the display content through `text` properties

|Event|Purpose|
|---|---|
|`on_text_changed`|Text content changes. Parameter is `event_args`|
|`on_read_only_changed`|Read-only switch changes. Parameter is `event_args`|
|`on_selectable_changed`|Selection and interactive input switch changes. Parameter is `event_args`|
|`on_selection_changed`|Selection or insertion position changes. Parameter is `event_args`|
|`on_max_length_changed`|Length limit changes. Parameter is `event_args`|
|`on_multiline_changed`|Multi-line switch changes. Parameter is `event_args`|
|`on_horizontal_scrollbar_visible_changed`|Horizontal scroll bar switch changes. Parameter is `event_args`|
|`on_vertical_scrollbar_visible_changed`|Vertical scroll bar switch changes. Parameter is `event_args`|
|`on_text_input`|Text editing input notification|

When the vertical content is scrollable, point the laser at the text box and use the corresponding joystick rudder to scroll up and down. The deflection amplitude determines the speed; you can also drag the scroll bar.

When the text editor has focus, Ctrl+Z undoes changes, and Ctrl+Y or Ctrl+Shift+Z restores changes. These keys take precedence over application menu shortcut keys.

### 4.4.combobox

Inherits from `item_control`. Construction: `combobox(name: str)`.

|Property|Type and initial values|Purpose|
|---|---|---|
|`dropdown_style`|`combobox_dropdown_style.dropdown_list`|`dropdown` is editable, `dropdown_list` is selected from a list|
|`dropped_down`|`bool = False`|Whether the dropdown list expands, readable and writable|
|`text`|`str = ""`|Text displayed or edited; when selecting an existing item, it is synchronized to that item|

Events are `on_dropdown_style_changed`, `on_text_changed`; items and selection events inherit from `item_control`

With `dropdown_list`, non-empty `text` must match existing items; setting it to an empty string clears the selection. With `dropdown`, new text can change `selected_index` to `-1`. Selected items are always read through `selected_index/selected_item`. The dropdown list expands by clicking; only the item currently pointed at by the laser shows a hover highlight.

### 4.5.listbox

Inherits from `item_control`. Construction: `listbox(name: str)`. This layer defaults `row_height` to `30`, and other public properties, methods, and events use inherited interfaces.

When the display limit is exceeded, a vertical scroll bar will be automatically provided. When the laser points to a list, you can scroll up and down using the corresponding joystick ruder or drag the scroll bar. `selected_index = -1` Deselect.

### 4.6.tabcontrol

Inherits from `container_control`. Construction: `tabcontrol(name: str)`.

|Property|Type and initial values|Read, write, and uses|
|---|---|---|
|`page_list`|`tabpage_collection`, initially empty|Read-only collection entrance, management page, and tab text|
|`selected_index`|`int = -1`|Read and write; current page index, `-1` indicates no selected page|
|`page_close_button_visible`|`bool = False`|Read and write; whether to display the tab close button|
|`selected_page`|`tabpage \| None`|Read-only; current page object|
|`tab_position`|`tab_position.top`|Read and write; accepts enumeration or `"top"/"bottom"/"left"/"right"` string|
|`tab_size`|`int = 36`|Read and write; tab bar thickness must be greater than `0`|
|`tab_font`|`font()`|Read and write; tab font|
|`tab_foreground_color`|`int = 0xD1DEF0FF`|Read and write; normal tab text color|
|`tab_background_color`|`int = 0x162738FF`|Read and write; normal tab background color|
|`selected_tab_foreground_color`|`int = 0xFFFFFFFF`|Read and write; selected tab text color|
|`selected_tab_background_color`|`int = 0x316B9AFF`|Read and write; selected tab background color|

The `tab_position` enumeration can be imported from `easyvrui`, with members being `top/bottom/left/right`.

Pages are added through `page_list.add(page)`, while tab appearance and active pages are managed by `tabcontrol`. The main content area follows the container background, with hover effects applied to specific tabs. `tabcontrol` is uniformly using `page_list`; accessing its `control_list`, including through base class entry calls, will throw a `RuntimeError` with diagnostic information containing `page_list_required`.

|Event|Purpose|
|---|---|
|`on_selected_index_changed`|Change in selected page index. Parameter is `event_args`.|
|`on_selection_changed`|Change in page selection. Parameter is `event_args`.|
|`on_tab_position_changed`|Change in tab bar position. Parameter is `event_args`.|
|`on_tab_size_changed`|Change in tab bar thickness. Parameter is `event_args`.|
|`on_tab_font_changed`|Change in tab font. Parameter is `event_args`.|
|`on_tab_foreground_color_changed`|Change in normal tab text color. Parameter is `event_args`.|
|`on_tab_background_color_changed`|Change in normal tab background color. Parameter is `event_args`.|
|`on_selected_tab_foreground_color_changed`|Change in selected tab text color. Parameter is `event_args`.|
|`on_selected_tab_background_color_changed`|Change in selected tab background color. Parameter is `event_args`.|
|`on_page_added`|Page addition; data contains `page/index/text`. Parameter is `tabpage_event_args`.|
|`on_page_removed`|Page removal; data contains `page/index`. Parameter is `tabpage_event_args`.|
|`on_page_text_changed`|Triggered when the tab title changes. Reads the current title through `tabpage_event_args.page.text`.|
|`on_page_close`|Triggered when the tab is closed. Reads the tab `page` and its index `index` through `tabpage_event_args`.|
|`on_page_close_button_visible_changed`|Changes in the display settings of the tab close button. The parameter is `event_args`.|

The event field `page` is the numerical identifier of the page object, with `index` starting from `0`. The page object is obtained through the collection.

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

Click the tab close icon or press Delete when the tab is focused to trigger `on_page_close`. After the application confirms the save, `event.page` will be removed from `page_list`.

### 4.7.window

Inherits from `container_control`. Construction: `window(name: str)`. The window is initially hidden, with `title` initially being `name`, `rect` initially being `rect(0, 0, 640, 360)`, and `background_color` initially being `0x0D1624FF`.

The enumeration of `startup_position` can be imported from `easyvrui`, `easyvrui.control`, or `easyvrui.control.window`, with members being `none/center`.

When the center is first positioned, it aligns with the source window and centers itself along the normal direction towards the headset; modal windows use the direct parent window. When there is no valid source, it centers on the headset, with the initial distance being `max(1.2, max(physical_width, physical_height))` meters. The Engine arranges the initial depth of the common windows visible in each session, responding to synchronization from the SDK event loop to position/rotation. The positioning is applied only once at startup, and subsequent hiding and showing retain the current pose. none uses the configured reference object and pose. The input component auxiliary window is positioned by the Engine associating with the input area.

|Property|Type and initial values|Read, write, and uses|
|---|---|---|
|`title`|`str = name`|Read and write; title text|
|`title_foreground_color`|`int = 0xFFFFFFFF`|Read and write; title text color|
|`title_background_color`|`int = 0x244565FF`|Read and write; title bar background color|
|`title_font`|`font("Segoe UI", 20)`|Read and write; title font|
|`icon`|`drawing_image \| None，默认原生图标`|Read and write; icon on the left side of the title bar, scaled proportionally and centered vertically; when set to None, the title uses the left-side space directly|
|`window.get_default_icon() -> drawing_image`|Static method, reads the native default icon; restores the default value by assigning an icon|
|`curvature`|`float = 0.0`|Read and write; curvature of the cylindrical surface, in meters' reciprocal, 0 represents a plane|
|`physical_scale`|`float = 1.0`|Read and write; scaling factor of the logical pixel physical size, must be a positive finite number; when it's 1, each logical pixel is 1 millimeter|
|`position`|`vec3()`|Read and write; position offset of the window's upper left corner relative to the reference object, in meters|
|`rotation`|`vec3()`|Read and write; XYZ Euler angles, in degrees|
|`reference_object`|`reference_object()`|Read and write; reference target record containing `type: reference_object_type`, default is world|
|`show_title_bar`|`bool = True`|Read and write; whether to display the title bar|
|`tracking_mode_set`|`set[reference_object_type]`|Read and write; mode collection in the title bar tracking selector, initially including `world/body/left/right/head`|
|`show_close_button`|`bool = True`|Read and write; title bar close button|
|`movable`|`bool = True`|Read and write; whether to allow movement and rotation via the controller|
|`resizable`|`bool = True`|Read and write; whether to allow interactive scaling|
|`startup_position`|`startup_position.center`|Read and write; accepts enumeration or `"none"/"center"` string. None uses initial position and orientation; center is centered parallel to the source window when displayed for the first time and moved forward towards the headset. When there is no valid source, it centers on the headset.|
|`curvature_adjustable`|`bool = True`|Read and write; controls the display and interaction of the lower-left curvature button. When turned off, it immediately cancels the current drag and joystick adjustment. After re-enabling, release the trigger before pressing again to start the adjustment.|

In `physical_scale = 1.0`, each logical pixel corresponds to 1 millimeter. `rect.width * physical_scale / 1000.0` is the surface expansion width, and in curved windows, it corresponds to the arc length of expansion. `curvature` is denoted as k, and the expansion width is denoted as W: the valid domain of attributes is finite, `k >= 0`, and `k * W < 2π`; this relationship must be satisfied when setting curvature and scaling. When interacting with the handle entry at the lower-left corner of the window, a safety arc angle limit of 160° is used; this interaction limit is handled separately from the valid domain of attributes. The left and lower-right entries are held down by the trigger until released to maintain selection and laser capture; curvature is adjusted left and right with the joystick, and size is adjusted up and down with the joystick. Double-clicking at the lower-left corner restores the plane.

The `reference_object_type` enumeration includes `world/body/head/left/right`. `reference_object()` constructs the default world record, and `reference_object(type)` receives this enumeration; the recorded `type` can be read and written. `get_reference_object_type_name(value: reference_object_type) -> str` returns the name, and `parse_reference_object_type(value: str) -> reference_object_type` parses the name. Two reference_object records are compared by type; `item.reference_object.type` is used for comparison with enumerations, and `get_reference_object_type_name(item.reference_object.type)` is used for comparison with names.

Python access adaptation allows `reference_object` to assign values and `reparent()` to use the reference_object record, reference_object_type enumeration, or five mode name strings; reading reference_object always returns the record. `tracking_mode_set` assignment accepts `set` or `frozenset`, and the elements can be enumerations, or mode strings from the access adaptation, or reference_object records; reading returns a snapshot of the enumeration set. An empty set hides the switch button; when a mode needs to be added, it is re-assigned as a whole.

|Other status attributes|Read, write, and uses|
|---|---|
|`closed: bool`|Read-only; whether it is closed, initially `False`|
|`loaded: bool`|Read-only; whether it has been displayed for the first time, initially `False`|
|`dialog_result: dialog_result`|Read and write; resets to `none` when entering a modal state. During the modal period, assigning a value other than `none` will close the window, and direct closing returns `cancel`.|
|`physical_width: float`|Read-only; expansion width, equal to `rect.width * physical_scale / 1000`|
|`physical_height: float`|Read-only; actual height, equal to `rect.height * physical_scale / 1000`|
|`auxiliary: bool`|Read and write; auxiliary input surface marker, initially `False`; the window of the IME/layout session automatically becomes the auxiliary surface, and the Engine maintains the scaling of the position, reference, and following input windows.|

|Signature|Purpose|
|---|---|
|`show() -> None`|Display a normal window; the first display triggers a loading event.|
|`hide() -> None`|Hide the window and cancel the corresponding interaction; end the active modal state of the window.|
|`activate() -> None`|Request to activate the window.|
|`show_dialog(owner_window: window) -> dialog_result`|Synchronize the modal window, disabling the direct owner and continuing to distribute UI events. After closing, return the result enumeration.|
|`close(force: bool = False) -> bool`|Request to close the window; return `True` if successful. When force is True, skip the close and cancel the callback.|
|`set_size(width: int, height: int, /) -> None`|Set the logical rectangle width and height, which must be greater than `0`.|
|`reparent(reference: reference_object \| reference_object_type \| str, keep_world: bool = False) -> None`|Change the reference object; maintain the world pose when keep_world = True is passed.|
|`world_transform: pose \| None`|Read the currently resolvable world pose; it can be `None` when tracking the reference is unavailable.|
|`is_tracking_available(mode: reference_object_type) -> bool`|Query whether the specified reference mode can currently track.|
|`center_at_view(distance: float, /) -> bool`|Center the window at a specified distance in front of the line of sight; return `True` when positioning is successful.|

`world_transform` returns the world pose of the window's surface center. `position` configures the upper-left offset. After directly assigning `reference_object`, the existing offset is interpreted according to the new reference system. Use `reparent(reference, keep_world = True)` when maintaining the world pose.

`show_dialog(owner_window)` requires the owner to be another interactive window within the same UI runtime. The dialog box must be hidden, not closed, and not in a modal state. Calling this will enter a nested message loop in the same UI thread, temporarily disqualifying the current owner from interaction. It can be called via button or menu events, with the currently interactive dialog box serving as the next owner. Calling during rendering submission will result in an error. For details, see [Session and Nested Modal Loop](/en/advanced/04_session_and_context).

When entering a modal state, `dialog_result` is reset to `dialog_result.none`. Setting other results will request a close. If the processor cancels the close, the dialog box remains active, and the result returns to its previous value. When the result is still `none`, closing via the title bar button or `close()` will succeed, returning to `dialog_result.cancel`. The caller can retain the window instance and read the control values after returning.

When displaying a new ordinary window for the first time, only when `physical_scale` is not explicitly set, the source is determined sequentially from the modal owner of the same session, the current event-dispersing window, the window executing on_load, the current input window, the active window, and the most recently visible ordinary window, inheriting their scaling. Explicitly set values take precedence, including 1.0; the scale can be reset after display. Controls with the same magnification have the same physical size; `set_size()` changes the logical canvas and corresponding physical size.

|Reference objects|Purpose|
|---|---|
|`"world"`|Located in the engine world reference space, maintaining spatial position when the user moves or turns their head|
|`"head"`|Follow the head position and rotation|
|`"left"`|Follow the left-hand controller reference pose|
|`"right"`|Follow the right-hand controller reference pose|
|`"body"`|Follow the position compensated for the neck pivot, maintaining the orientation during calibration; turning the head allows observation of surrounding windows|

When `startup_position = startup_position.none` and `position = vec3()`, `rotation = vec3()`, the upper left corner of the world mode window is located at the initial front reference center.

The modal window of center uses the direct parent window; other center windows prioritize using the same session source provided by the SDK. When the source is omitted, Engine uses the currently selected visible ordinary surface, which can cross sessions for Desktop to launch other apps. Engine arranges the initial depth along the front or back orientation of the source's normal, completing response synchronization to finally position/rotation; subsequent hide and show maintain the determined pose.

`Ctrl+Alt+Pause` maps the center of the Body and the overall World layout to the current head display. When the system reports `Ctrl+Alt+Break`, the same effect occurs. `Ctrl+Pause` displays or hides the Desktop application in the engine configuration.

Movable windows support single-hand grip with the side buttons in World and Body modes; constrained axis rotation is performed by holding different control points on the periphery with both hands. The window can be displayed and interacted with on both front and back sides, with text on the back being a mirror image of the front. When the window's logical size is large enough and movement is enabled, the peripheral control ring occupies the inner space of the logical rectangle; when arranging sub-controls, refer to `get_content_top()` to avoid the title bar.

|Event|Purpose|
|---|---|
|`on_title_changed`|Title change. Parameter is `event_args`.|
|`on_title_foreground_color_changed`|Title text color change. Parameter is `event_args`.|
|`on_title_background_color_changed`|Title bar background color change. Parameter is `event_args`.|
|`on_title_font_changed`|Title font change. Parameter is `event_args`.|
|`on_icon_changed`|Title icon object changes or clears. Parameter is `event_args`.|
|`on_rotation_changed`|Three-dimensional rotation change. Parameter is `event_args`.|
|`on_curvature_changed`|Curvature change. Parameter is `event_args`.|
|`on_curvature_adjust_start`|Start of curvature interactive adjustment. Parameter is `event_args`.|
|`on_curvature_adjust_end`|End of curvature interactive adjustment. Parameter is `interaction_end_event_args`.|
|`on_reference_object_changed`|Reference object change. Parameter is `event_args`.|
|`on_show_title_bar_changed`|Title bar display switch change. Parameter is `event_args`.|
|`on_tracking_mode_set_changed`|The set of allowed mode changes in the title bar. Parameter: `event_args`.|
|`on_show_close_button_changed`|Changes to the close button switch. Parameter: `event_args`.|
|`on_movable_changed`|Changes to the move switch. Parameter: `event_args`.|
|`on_resizable_changed`|Changes to the zoom switch. Parameter: `event_args`.|
|`on_startup_position_changed`|Changes to the start positioning mode. Parameter: `event_args`.|
|`on_curvature_adjustable_changed`|Changes to the curvature interaction adjustment switch. Parameter: `event_args`.|
|`on_load`|Loading during the first display, once per window. Parameter: `event_args`.|
|`on_shown`|Display from hidden state. Parameter: `event_args`.|
|`on_hidden`|Hide. Parameter: `event_args`.|
|`on_closing`|Ask before closing; can be set to `event.cancel = True` to cancel a normal close. Parameter: `cancel_event_args`.|
|`on_closed`|Complete closing; data can include the close state `reason`. Parameter: `event_args`.|
|`on_render_failed`|Failed to submit the drawing. Parameter: `render_error_event_args`.|
|`on_tracking_lost`|Reference object tracking lost. Parameter: `event_args`.|
|`on_tracking_restored`|Reference object tracking restored. Parameter: `event_args`.|
|`on_activated`|Window activation. Parameter: `event_args`.|
|`on_deactivated`|Window loses activation. Parameter: `event_args`.|
|`on_move_start`|Start of moving or constrained rotation. Parameter: `event_args`.|
|`on_move_end`|End of moving or constrained rotation. Parameter: `interaction_end_event_args`.|
|`on_resize_start`|Start of interactive zooming. Parameter: `event_args`.|
|`on_resize_end`|End of interactive zooming. Parameter: `interaction_end_event_args`.|

Three-dimensional position changes use the inherited `on_moved`, and physical width changes use the inherited `on_size_changed`. Window hiding or closing will cancel grabbing, pointer capture, and associated input interfaces. After closing, a new window instance needs to be created for re-display.

### 4.8.checkbox and radiobutton

Both inherit `text_control`, constructed as `checkbox(name)` and `radiobutton(name)`. Read and write properties are `text: str = ""` and `checked: bool = False`; text changes trigger `on_text_changed`, and check state changes trigger `on_checked_changed`. Colors and fonts follow inherited properties. Clicking a checkbox switches the check state; radiobuttons are used for mutually exclusive options within the same parent container.

### 4.9.numericupdown

Inherit `text_control`, constructed as `numericupdown(name)`. The middle text area can edit numerical values, with upper and lower triangular buttons obtaining hover and focus respectively; clicking the adjustment button keeps the focus on numerical operations, and the text input interface is only associated with the text editing area.

|Property|Initial Value and Constraints|
|---|---|
|`value: float`|0.0, finite number, limited between minimum and maximum values|
|`minimum: float`|0.0, must be less than maximum|
|`maximum: float`|100.0, must be greater than minimum|
|`step: float`|1.0, positive finite number|
|`decimal_places: int`|0, range from 0 to 17, controls the number of decimal places displayed|

The relevant event is `on_value_changed/on_minimum_changed/on_maximum_changed/on_step_changed/on_decimal_places_changed`. Modifying the upper and lower limits will correspondingly limit the current value.

### 4.10.slider and progressbar

Both inherit from `control`, construction only requires a name. Publicly available are `minimum: int = 0`, `maximum: int = 100`, and `value: int = 0`, with integers using a signed 64-bit range. Minimum is strictly less than maximum, and value is limited within this range; the event is `on_minimum_changed/on_maximum_changed/on_value_changed`.

`slider` also provides `orientation: orientation = orientation.horizontal`, only accepting `orientation.horizontal` or `orientation.vertical`; events include `on_orientation_changed/on_drag_start/on_drag_end`. Value is modified by dragging the slider or using keyboard navigation. `progressbar` displays progress by range.

### 4.11.listview

`listview(name)` inherits from `selection_control` and presents multi-column text per row. Clicking on the header triggers `on_column_click`, which sorts accordingly. Drag the header separator to adjust the width.

|Interface|Purpose|
|---|---|
|`listview_column(text = "", width = 100)`|`text` and `width` are readable and writable. If the width is positive, modifications will rearrange the view.|
|`listview_item(cell_list = [], icon = None, tag = "")`|`cell_list` saves the text in each column, `icon` is displayed in the first column, and `tag` saves application tags.|
|`column_list: listview_column_collection`|Column collection, supports in-place modification and overall assignment.|
|`item_list: listview_item_collection`|Row collection, supports in-place modification and overall assignment.|
|`selected_index: int`、`selected_item: listview_item \| None`|Read and write main selection, empty selection corresponds to `-1` and `None`.|
|`select_item(index, extend = False, toggle = False)`|Select rows by index. For multiple selections, the selection can be expanded or the target rows can be switched.|
|`selected_item_list: list[listview_item]`、`multi_select: bool`|Read the selection object, set multiple selections.|
|`row_height`、`header_height`|Read and write row height and header height, `header_height = 0` hides headers.|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|Read the number of currently visible rows and scroll bar status.|
|`on_item_list_changed`、`on_column_list_changed`、`on_column_width_changed`|Changes in view content and column width.|
|`on_selection_changed`、`on_row_double_click`、`on_column_click`|Changes in selection, activated rows, and clicking on headers.|

`item.cell_list` is `listview_cell_collection`. Cells can be modified with `item.cell_list[0] = "Updated"` or assigned as a whole. The list maintains selections by row objects, and when sorted, the same batch of row objects is reassigned in the new order.

### 4.12 treeview and tree_node

`treeview(name)` inherits from `selection_control`. The root node is managed through `node_list: tree_node_collection`, and `selected_node: tree_node | None` reads and writes the currently selected object. `row_height` and `vertical_scrollbar_visible` are read-only properties.

`tree_node(text = "", expanded = False, tag = "")` provides read-write properties with the same name. `parent` returns the parent node or `None`, and `node_list` manages child nodes. The expansion state is adjusted through `expand()` and `collapse()`. Each node belongs to a tree collection simultaneously.

The tree view provides `on_node_list_changed`, `on_selection_changed`, `on_node_expanded`, `on_node_collapsed`, and `on_node_activated`. The data field `node` for node events is the node label.

```python
root = easyvrui.tree_node("Project", expanded = True, tag = "root")
child = easyvrui.tree_node("Engine")
root.node_list.append(child)
tree = easyvrui.treeview("treeview_project")
tree.node_list.append(root)
tree.selected_node = child
```

### 4.13 scrollpanel and splitter

`scrollpanel(name)` inherits from `container_control`, and ordinary controls are added through `control_list`. `horizontal_scrollbar_visible/vertical_scrollbar_visible` is set to True by default, each with corresponding change events. The scrolling range is determined by the content, and `on_viewport_changed` is emitted when the viewport changes.

`splitter(name)` inherits from `container_control`, and can hold up to two panel controls, with the order corresponding to the first and second sides.

|Property|Purpose|
|---|---|
|`orientation: orientation = orientation.vertical`|`orientation.vertical` divides the left and right regions with a vertical separator bar. `orientation.horizontal` divides the top and bottom regions with a horizontal separator bar.|
|`split_position: float = 0.5`|The separation ratio is limited and ranges from 0.0 to 1.0.|

The related event is `on_orientation_changed/on_split_position_changed/on_split_start/on_split_end`. The layout is calculated by the container, and dragging the separator bar updates split_position.

### 4.14 image and screen

`image(name)` inherits from `control`:

|Member|Purpose|
|---|---|
|`source: drawing_image \| None`|Image objects|
|`stretch_mode: image_stretch_mode = image_stretch_mode.contain`|Read and write, accepting `image_stretch_mode` as `fill/contain/cover/none`|

fill fills the rectangle, contain maintains the proportion of the display, cover covers the rectangle and crops it, none uses the original size of the image. The event is `on_source_changed/on_stretch_mode_changed/on_source_unavailable`.

`screen(name)` inherits from `control`, used to display the real-time image of the screen:

|Member|Purpose|
|---|---|
|`screen_id: int = 0`|Screen identification|
|`screen_available: bool`|Read-only, whether the current screen is available, initially False|
|`on_screen_id_changed`|Screen selection changes. The parameter is `event_args`.|
|`on_screen_unavailable/on_screen_restored`|Screen unavailability and recovery|

The image is displayed according to the control rectangle, and the mouse pointer follows the display of the screen image. The original image clarity is related to the logical size of the control; when pixel-by-pixel display is required, set the width and height of the screen control to the corresponding monitor resolution. The physical_scale of the window independently controls its physical size.

### 4.15 Icon toolbar and hover prompts

`toolbar`, `toolbar_button`, and `toolbar_button_collection` can be imported from `easyvrui` or `easyvrui.control`, or from their respective sub-modules with the same name. The constructor of `toolbar` only accepts immutable `name`. `toolbar` inherits from `container_control`.

`toolbar_button(name)` inherits from `button`, which is a toolbar item, managed by `toolbar.button_list`. Each button displays an icon, click area, and hover prompt as a whole.

|Object|Property|Purpose|
|---|---|---|
|`toolbar`|`tool_size: int = 40`|The side length of the square tool grid must be a positive integer.|
|`toolbar`|`spacing: float = 6.0`|Finite non-negative spacing.|
|`toolbar`|`button_list: toolbar_button_collection`|Read-only. The tool buttons and separator lines form a directly operable collection.|
|`toolbar_button`|`icon: drawing_image \| None`|Tool icons.|
|`toolbar_button`|Inherited from `tooltip_text: str = ""`|Hover prompt. Empty string for closed prompt.|
|`toolbar_button`|`enabled: bool = True`|Whether it can be executed.|
|`toolbar_button`|`separator: bool = False`|Displayed as a subdivision line.|

`toolbar` provides `on_tool_size_changed/on_spacing_changed`; `toolbar_button` provides `on_click/on_icon_changed` and inherited object events. The toolbar manages the layout, and button responses are triggered by hovering and clicking.

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

In the example, `window_main` and `textbox_entry` are created by the application, and the target text boxes belong to this window. The independent tooltip defaults to a zero rectangle, showing and disappearing when the target is hovered. Text wraps at character boundaries, and the prompt is limited to the window content area. If the height is insufficient, ellipsis are displayed.

### 4.16. Menu Bar and Menu Items

`menu_container` inherits from `container_control` and is a common base class for `menubar` and `menuitem`. Both controls are constructed by name.

`window.menu` can read and write `menubar` or `None`, and changes trigger `on_menu_changed`. The menu bar is located below the title bar. It also belongs to `control_list` of the window: when the menu bar is added to the collection, removed from the current menu bar, or the collection is cleared, `menu` is associated with synchronous updates; setting `menu` also synchronizes the collection ownership. The position of menu items uses the actual index in the collection, with one menu bar per window.

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

In the example, `window_main` is created by the application; execution callbacks are registered through `menuitem_save.on_click += handler`.

|Object|Properties, Methods, and Uses|
|---|---|
|`menu_container`|Inherits from the ordinary `control_list`; the collection only accepts `menuitem`; `owning_menubar` obtains its associated menu bar; `on_item_added/on_item_removed` notifies collection changes.|
|`menuitem`|Can read and write `text/shortcut/checkable/checked/separator/icon`. The read-only property `open: bool` indicates whether the current submenu is expanded. Manage subordinate menus through `control_list`.|
|`menubar`|Can read and write `font/row_height`; `open_menu()` and `close(restore_focus = True)` control the expansion state; `open` and `is_submenu_open(item)` query the expansion state.|

Menu items provide `on_text_changed/on_icon_changed/on_shortcut_changed/on_checkable_changed/on_checked_changed/on_separator_changed`; the menu bar provides `on_font_changed/on_row_height_changed`. Both have `on_opening/on_closed`, and menu item execution uses the inherited `on_click`.

### 4.17.grid

`grid` inherits from `selection_control` and provides multi-column data, selection, and editing.

|Type|Interface|
|---|---|
|`grid_column(text = "", width = 100, editable = True)`|Writable fields: `text/width/editable`|
|`grid_cell(row = 0, column = 0)`|Writable fields: `row/column`, with indices starting from 0.|
|`grid_selection_mode`|`cell/row`|
|`grid_cell_render`|Rendering callback records. `cell/rectangle/value/selected/hovered/editing` can be read and written, and the type of `rectangle` is `render_rectangle`.|

Cell values support `str`, signed 64-bit ranges `int`, finite `float`, and `bool`. The writable property of `grid(name)` is `column_list/row_count/selected_index/selection_mode/multi_select/row_height/header_height/read_only/edit_text`; the read-only property is `editing/edit_cell/edit_error/selected_cell_list`.

|Method|Purpose|
|---|---|
|`grid[row, column]` can read and write|Data Reading and Writing|
|`set_data_provider(row_count, reader, writer = None)`|reader(row, column) Returns value; writer(row, column, value) Handles writing|
|`refresh_data()`|Notifies external data of update|
|`set_cell_renderer(renderer)`|renderer(context, cell) Draws visible cells; None reverts to default|
|`set_edit_validator(validator)`|validator(cell, value) Verifies editing; None clears the verifier|
|`get_value_text(value)`|Static method, converts value to text|
|`select_cell(row, column, extend = False, toggle = False)`、`clear_selection()`、`is_cell_selected(row, column)`|Selection Control|
|`get_cell_at(left, top)`|Queries cells hit by local coordinate|
|`get_cell_rectangle(row, column) -> render_rectangle`|Queries rectangle of specified cell|
|`vertical_scrollbar_visible/horizontal_scrollbar_visible`|Scrollbar Status|
|`visible_row_count`|Current number of visible rows|
|`set_column_width(column, value)`|Adjust column width|
|`begin_edit(row, column)`、`commit_edit()`、`commit_edit(value)`、`cancel_edit()`|Editing Lifecycle, begin/commit returns bool|

Writer and validator can return `None` indicating success, bool indicating result, string indicating failure reason, or `(bool, str)` providing both result and reason. Writing by the data provider must be updated by the writer to the actual data source. Derived classes can override `read_cell_value(row, column)`, `write_cell_value(row, column, value)`, and `render_cell(context, cell)`; writing overrides follow the same return convention.

The event is `on_column_list_changed/on_column_width_changed/on_column_click/on_selection_changed/on_cell_double_click/on_cell_value_changed/on_row_height_changed/on_header_height_changed/on_edit_started/on_edit_committed/on_edit_cancelled/on_edit_failed`. Events use the same subscription method as other controls, `+=/-=`.

Click on the cell you want to edit. IME will be positioned within the visible rectangle of the current editing cell. Read-only columns are used for selection and viewing purposes. `selection_mode` accepts the strings `grid_selection_mode.cell/row` or `"cell"/"row"`. When the column header is too long, ellipsis are displayed. `header_height = 0` hides the header.

Column width defaults to 100. `column_list` returns an independent column record. When assigned to `column_list` or `set_column_width()`, the column width must be positive and the sum of all column widths must be within the range of signed 64-bit integers. Column layout is applied only after successful verification and corresponding events are sent.

Reading `column_list` gets a snapshot, which must be reassigned after modification. Grid cells are read-only for selection and viewing; clickable cells enter editing mode, switching cells aligns focus and inputs the interface. Multiple selections are enabled through `multi_select`, Ctrl switches items, Shift expands selection; entity keyboard modifier keys are only used in entity capture mode for interaction.

## 5. Collection Interface

### 5.1.control_collection

Obtained through the `control_list` of a regular container. Collections maintain order and support search by immutable `name`; name search uses mapping, usually close to constant time. `control_collection(owner: container_control)` can construct independent collections associated with the owner for derived types to extend; the original control_list entry of the owner still points to its built-in collection.

|Signature or Operation|Returns and Purpose|
|---|---|
|`add(item: control)`、`append(item: control)`|Returns the original object added, appending to the end|
|`insert(index: int, item: control)`|Returns the original object added, inserting at the specified position|
|`extend(item_list: Iterable[control], /) -> None`|Append sequentially; retained appended items if an error occurs during the process.|
|`remove(key: str \| int \| control, /) -> control`|Remove and return by name, subscript, or object.|
|`remove_at(index: int)`、`pop(index: int = -1) -> control`|Remove by subscript; defaults to the last item.|
|`clear() -> None`|Remove all child controls.|
|`collection[key] -> control`|Query by name or subscript; throw `KeyError` if name is missing, throw `IndexError` for out-of-bounds cases.|
|`del collection[key]`|Remove by name, subscript, or object; ignore the returned value.|
|`index_of(key: str \| int \| control, /) -> int`|Get the position of an item; integer parameters will be validated and converted to the actual subscript.|
|`key in collection`|Check by name or object identity.|
|`len(collection)`|Number of items.|
|`iter(collection)`|Traverse the snapshot of the object list at that time.|

Read and delete items with negative subscripts, where `-1` indicates the end. When inserting, negative subscripts are first padded with the current length and then limited to between `0` and the actual length; positions greater than the end are appended at the end. Use `collection[start:stop:step]` to get a slice, and `list(collection)` to get a snapshot. The removal method differs from `dispose()`: the object can still be retained and used after removal, and other containers can be added if conditions are met.

Python-derived collections can override `insert(self, index, item)`, `remove(self, index)`, and `clear(self)`. Native virtual calls will be distributed to the corresponding Python methods; in the overridden methods, the same-named method of super can be called to perform base class operations. `append/extend/pop` and negative subscripts accessed by Python are adaptations for collection use.

Collection views retain the Python reference of the owner. The borrowed references obtained from queries maintain their dependencies according to the binding. When a Python-derived control is held by a native collection, its overloaded methods and instance properties remain valid. The reference cycle formed by owner, collection, and Python additional properties participates in GC; removed shared objects can hold independently, with `dispose()` used to explicitly terminate the native object and its resources.

### 5.2.tabpage_collection

Obtained through `tabcontrol.page_list`. `tabpage_collection` inherits from `control_collection`, sharing the same page storage, with the title saved by the page itself. `tabpage_collection(owner: tabcontrol)` can construct an independent page collection associated with the owner; the original page_list entry of the owner remains in the original object. Inserted items must be `tabpage`, and page objects are queried by subscript or name.

|Signature or Operation|Returns and Purpose|
|---|---|
|`add(page: tabpage)`、`append(page: tabpage)`|Append and return the page.|
|`insert(index: int, page: tabpage)`|Return the page and insert it at the specified position.|
|`extend(page_list: Iterable[tabpage], /) -> None`|Append each page sequentially.|
|`remove(key: str \| int \| tabpage, /) -> control`|Remove and return the page.|
|`remove_at(index: int)`、`pop(index: int = -1) -> control`|Remove and return the specified page.|
|`clear() -> None`|Clear all pages.|
|`collection[key] -> tabpage`、`del collection[key]`|Query or remove pages.|
|`index_of(key: str \| int \| tabpage, /) -> int`|Page subscript.|
|`key in collection`|Check by name or page object.|
|`len(collection)`、`bool(collection)`|Quantity and empty status.|
|`iter(collection)`|Iterate through the page snapshots.|

After deleting and inserting pages, adjust the page subscripts according to the actual page relationships. The same collection name must be unique. The removal operation returns a control object of dynamic type; the page remains the original tabpage, and another page_list can be added directly. `list(collection)` returns a snapshot of the page reference.

The page collection supports overriding `insert(self, index, page)` and inheriting the removal extension points.

### 5.3.item_collection

`item_collection` is imported from `easyvrui.control` and is an alias for the native `item_collection` type. Examples are provided by `combobox.item_list`, `listbox.item_list`, or `item_control.item_list`. The content is a string, allowing duplicate text. The Python wrapper for this collection retains the references to its controls and participates in the reference cycle GC.

|Signature or Operation|Returns and Purpose|
|---|---|
|`add(value: str, /) -> None`、`append(value: str, /) -> None`|Append a string|
|`insert(index: int, value: str, /) -> None`|Insert; negative indices and positions exceeding the end are handled according to the collection's insertion rules.|
|`extend(value_list: Iterable[str], /) -> None`|Append sequentially|
|`assign(value_list: list[str], /) -> None`|Replace all content|
|`remove(value: str \| int, /) -> str`|Remove the first matching string, or specify a subscript item; return the removed text|
|`remove_at(index: int)`、`pop(index: int = -1) -> str`|Remove and return the specified item|
|`clear() -> None`|Clear.|
|`collection[index_or_value]`|Read by subscript or text; supports negative subscripts and slicing|
|`collection[index] = value`|Replace the specified text|
|`del collection[index]`|Remove the specified item|
|`index_of(value: str, /) -> int`|The subscript of the first matching text; report an error if not found|
|`value in collection`|Check whether it contains text|
|`len(collection)`、`bool(collection)`|Quantity and empty status.|
|`iter(collection)`|Traverse the text snapshot|

### 5.4.toolbar_button_collection

`toolbar.button_list` provides a toolbar button collection. Query the quantity and empty status through `len(collection)` and `bool(collection)`. Check the members by name or object with `item in collection`. Support integers, negative numbers, slicing, and names with `collection[index_or_name]`. Obtain the position with `index_of(item)`. Accept button objects or name strings with `add(item)`, `add_button(item)`, and `insert(index, item)`. Add a separator with `add_separator(name)`. Remove items with `remove(item)`, `remove_at(index)`, and `clear()`. Iterate using the snapshot.

`listview_column_collection`, `listview_item_collection`, `listview_cell_collection`, and `tree_node_collection` support length, inclusion, positive and negative subscripts, slicing, and iteration. Add with `append/add/insert`, remove with `remove/remove_at/clear`, and replace all content with `assign`. The cell collection also supports subscript assignment and deletion.

### 5.5. Menu collection

The menu uses the same `control_collection` as the regular container, supporting search by name or index, as well as `add/insert/remove/clear`. Multi-level menus are composed of nested menu items. `separator = True` displays separators; `checkable/checked` controls selection; `shortcut` records shortcut keys; `&A` or `(&A)` represent mnemonics.

## 6. Strongly typed events

### 6.1. Subscription method and event_container

The `on_xxx` members of the control provide `event_container`. Events are obtained through objects; callbacks receive the source control `source` and event parameters `event`. The formal parameter name is `handler(source, event)`.

```python
def button_ok_click(source, event):
    source.text = "Clicked"

button_ok.on_click += button_ok_click
button_ok.on_click -= button_ok_click
```

|Signature or Operation|Purpose|
|---|---|
|`add(callback) -> int`|Add a callback and return the subscription token|
|`remove(callback_or_token) -> bool`|Remove a matching callback or token; successful for `True`|
|`event += callback`|Add a callback, retaining the same event object|
|`event -= callback_or_token`|Remove a callback or token, retaining the same event object|
|`clear() -> None`|Remove all callbacks|
|`len(event)`|Number of subscriptions|
|`event.call(source, args)`、`event(source, args)`|Distribute events to current subscribers|
|`bool(event) -> bool`|`True` when subscriptions exist|

Execute in registration order, multiple callbacks can be registered; only one matching subscription is processed at a time. Subscription identifier is used to remove specified callbacks. The `on_state_changed/on_input` of the input component uses the same subscription operation, with callback parameters being `input_ui_state` and `input_event`, respectively.

### 6.2 Event Parameters

Parameter classes can be imported from `easyvrui` or `easyvrui.event`. In the table below, `event_args` is the base class, and the other 18 parameter classes inherit from it. For example, `issubclass(cancel_event_args, event_args)` is derived from `True`. During callback, set the corresponding parameters to `event.cancel` or `event.handled`, and the native dispatch will read the updated state. Collection and tree node parameters provide readable object references, with indices starting from 0.

|Parameter types|Field|Purpose|
|---|---|---|
|`event_args`|None|Changes in click, focus, window lifecycle, and specific properties.|
|`cancel_event_args`|`cancel: bool`|Setting `cancel` before closing the window can cancel a normal close. Forced close always executes.|
|`key_event_args`|`key: str`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`、`handled: bool`|Key names, modifier keys, and consumption status.|
|`text_input_event_args`|`text: str`、`handled: bool`|Submitted text and consumption status.|
|`pointer_event_args`|`hand: str`、`left: float`、`top: float`、`x: float`、`y: float`、`captured: bool`、`cancelled: bool`、`handled: bool`、`has_position: bool`、`has_local_position: bool`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`|Include hand position, window coordinates `left/top`, control local coordinates `x/y`, and modifier keys. Use `has_position` and `has_local_position` to determine whether the corresponding coordinates are valid.|
|`scroll_event_args`|`hand: str`、`delta_x: float`、`delta_y: float`、`handled: bool`|Hand position, horizontal and vertical scroll amounts, and consumption status.|
|`interaction_end_event_args`|`cancelled: bool`|Movement, zoom, curvature adjustment, or drag completion. `cancelled` indicates the operation was canceled.|
|`property_changed_event_args`|`property_name: str`|`property_name` is the name of the changing property. Read the current value through `source`.|
|`control_collection_event_args`|`item: control &#124; None`、`index: int`|Controls in the collection and their indices. `item` for overall table notification is empty.|
|`menu_item_event_args`|`item: menuitem &#124; None`、`index: int`|Menu items and indices.|
|`tabpage_event_args`|`page: tabpage &#124; None`、`index: int`|Tab objects and indices.|
|`listview_column_event_args`|`column: listview_column &#124; None`、`index: int`|ListView column objects and indices. `column` for overall table notification is empty.|
|`listview_item_event_args`|`item: listview_item &#124; None`、`index: int`|ListView item objects and indices. `item` for overall table notification is empty.|
|`grid_column_event_args`|`index: int`、`width: int`|Grid column indices and widths. Read column indices through `index` when clicking on the header.|
|`grid_cell_event_args`|`row: int`、`column: int`、`error: str`|Grid cell row and column indices. `error` contains error descriptions when editing fails.|
|`tree_node_event_args`|`node: tree_node &#124; None`|Tree nodes of operations. `node` is empty when selection is canceled.|
|`render_error_event_args`|`message: str`|Messages of rendering exceptions.|
|`controller_event_args`|`hand: str`、`trigger: bool`、`grip: bool`、`joystick_x: int`、`joystick_y: int`、`joystick_pressed: bool`、`primary: bool`、`secondary: bool`|Handle button presses and joystick status. The joystick axis range is 0 to 255, with `primary` representing left-hand X or right-hand A, and `secondary` representing left-hand Y or right-hand B.|
|`control_input_event_args`|`type: control_input_type`、`hand: str`、`key: str`、`text: str`、`left: float`、`top: float`、`x: float`、`y: float`、`steps: int`、`horizontal: bool`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`、`captured: bool`、`cancelled: bool`、`handled: bool`、`has_position: bool`、`has_local_position: bool`|Input assignment parameters for derived controls. Distinguish inputs through `type`, read fields by type, and set `handled` to indicate consumption.|

The values of `control_input_type` are `none`, `click`, `focus_in`, `focus_out`, `pointer_enter`, `pointer_leave`, `pointer_move`, `pointer_down`, `pointer_up`, `scroll`, `key_down`, `key_up`, `text_input`, `controller_input`.

## 7. Drawing and Custom Controls

### 7.1.render_context

`render_context` is imported from `easyvrui` or `easyvrui.render`. Context is provided by `render(context)` and `render_overlay(context)`, valid only within the current drawing callback.

`render_rectangle` is a floating-point drawing rectangle record, providing writable `left/top/width/height` fields; `render_rectangle()` fields start at 0.0, while `render_rectangle(left, top, width, height)` is constructed based on parameters. `get_rectangle()`, `get_popup_rectangle()`, and `get_inset_rectangle()` return this record. Python drawing integration accepts either this record or a sequence of four numbers, `(left, top, width, height)`, as rectangle parameters.

`context.rectangle` is the tuple of the rectangle currently drawn on the canvas, a convenient property for Python integration. Drawing coordinates use the same canvas reference system; when drawing local content on the control, add the local offset to the returned `left/top`.

|Properties or Signatures|Purpose|
|---|---|
|`rectangle: tuple[float, float, float, float]`|Read-only; the drawing rectangle of the current owner|
|`owner: control`|Read-only; the currently drawn control|
|`get_rectangle(item: control) -> render_rectangle`|Get the drawing rectangle of a specified control|
|`get_popup_rectangle(item: item_control) -> render_rectangle`|Read the pop-up area rectangle of a control item|
|`is_hovered(item: control) -> bool`|Check if a control is in a hovered state|
|`is_hovered(item: control, rectangle) -> bool`|Check if a given rectangle of a specified control is in a hovered state|
|`is_focused(item: control) -> bool`|Query the visual focus of a control|
|`is_blinking() -> bool`|Check if the current insertion point flicker cycle is displayed|
|`is_active(item: window) -> bool`|Check if the window is the current active window|
|`is_blocked(item: window) -> bool`|Check if the query window is blocked by a modal relationship|
|`is_close_button_hovered(item: window) -> bool`|Hover state of the query window close button|
|`get_hovered_item(item: item_control) -> int`|Return the subscript of the referenced item, -1 for no match|
|`fill(rectangle, color: int) -> None`|Fill rectangle|
|`outline(rectangle, color: int, thickness: float = 1.0) -> None`|Draw a rectangular border|
|`draw_line(x1: float, y1: float, x2: float, y2: float, color: int, thickness: float = 2.0) -> None`|Draw a line segment|
|`fill_ellipse(center_x: float, center_y: float, radius_x: float, radius_y: float, color: int) -> None`|Fill an ellipse|
|`outline_ellipse(center_x: float, center_y: float, radius_x: float, radius_y: float, color: int, thickness: float = 1.0) -> None`|Draw an elliptical border|
|`fill_circle(center_x: float, center_y: float, radius: float, color: int) -> None`|Fill a circle|
|`draw_circle(center_x: float, center_y: float, radius: float, color: int, thickness: float = 1.0) -> None`|Draw a circular border|
|`fill_rounded_rectangle(rectangle, radius_x: float, radius_y: float, color: int) -> None`|Fill a rounded rectangle|
|`outline_rounded_rectangle(rectangle, radius_x: float, radius_y: float, color: int, thickness: float = 1.0) -> None`|Draw a rounded rectangular border|
|`draw_text(value: str, font: font, rectangle, color: int, center: bool = False) -> None`|Draw text, `center=True` centered|
|`measure(text: str, font: font) -> float`|Measure the text width|
|`draw_image(image: drawing_image, rectangle, opacity: float = 1.0) -> None`|Draw the image onto the target rectangle|
|`draw_screen(screen_id: int, rectangle) -> None`|Draw the real-time screen of the specified monitor|
|`fill_path(path: drawing_path, color: int) -> None`|Fill a path|
|`outline_path(path: drawing_path, color: int, thickness: float = 1.0) -> None`|Draw the path outline|
|`push_clip(rectangle) -> None`|Press-in cutting rectangle; restricts subsequent drawing with existing cuts|
|`pop_clip() -> None`|Restore the upper-level cut, which must match the press-in|
|`render_control_list(item: window) -> None`|Draw common controls in window collection order|
|`render_overlay_list(item: window) -> None`|Draw the floating layer of controls within the window|
|`render_control(item: control) -> None`|Call the main drawing entry point of the specified control|
|`render_control_overlay(item: control) -> None`|Call the floating layer drawing entry point of the specified control|
|`render_context.get_inset_rectangle(rectangle, left_padding: float, right_padding: float, top_padding: float = 0.0, bottom_padding: float = 0.0) -> render_rectangle`|Static call, calculate the rectangle based on the inner margins of all four sides|
|`context.get_inset_rectangle(item: control, left_padding: float, right_padding: float) -> render_rectangle`|Instance call, calculate the left and right inner shrinks based on the drawing rectangle of the specified control|
|`draw_control(item: control, highlight: bool = True) -> None`|Draw the background and border of general controls; `highlight` controls hover and focus styles|
|`get_foreground(item: text_control) -> int`|Get the text color after considering the available state|

The coordinates must be a finite number. Width, height, and radius cannot be negative; the line width must be greater than `0`; the image transparency range is from `0.0` to `1.0`. The drawing color uses the integer value `0xRRGGBBAA`. Clipping only restricts subsequent drawing and does not change the control rectangle.

The `get_inset_rectangle()` of the instance also accepts static rectangular parameters. The left and right inner margins must be explicitly provided; static calls can independently perform rectangular calculations, while instance calls follow the validity period of the current drawing callback.

The drawing query uses visual focus. During input emptying, the focus appearance can be canceled first, and the logical focus is switched after emptying is completed.

### 7.2.drawing_path

Construction: `drawing_path()`. The default filling rule is `drawing_fill_rule.even_odd`.

|Signature or attribute|Purpose|
|---|---|
|`fill_rule: drawing_fill_rule`|Read-write filling rule|
|`segment_list: list[drawing_path_segment]`|Read-only path segment snapshot|
|`clear() -> None`|Clear the path segment|
|`move_to(x: float, y: float) -> drawing_path`|Move to the starting point of a new subpath|
|`line_to(x: float, y: float) -> drawing_path`|Add a straight line|
|`quadratic_to(control_x: float, control_y: float, end_x: float, end_y: float) -> drawing_path`|Add a quadratic Bézier curve|
|`cubic_to(control1_x: float, control1_y: float, control2_x: float, control2_y: float, end_x: float, end_y: float) -> drawing_path`|Add a cubic Bézier curve|
|`arc_to(end_x: float, end_y: float, radius_x: float, radius_y: float, rotation_degree: float = 0.0, clockwise: bool = True, large_arc: bool = False) -> drawing_path`|Add an elliptical arc to a specified end point; specify radius, elliptical rotation angle, direction, and whether to take the major arc|
|`close() -> drawing_path`|Close the current subpath|

The path addition method and `close()` return the current path, supporting chained calls. Each subpath starts from `move_to()`; for an empty path or after it has just been closed, it is necessary to first use `move_to()` before adding other path segments. The coordinates must be a finite number, and the arc radius cannot be negative. `clear()` clears the path segment and retains the filling rule. `drawing_fill_rule` enumeration includes `even_odd` odd-even filling and `non_zero` non-zero winding filling.

Import `drawing_path_segment` from `easyvrui`. The path segments in `segment_list` have the following fields.

|Field|Purpose|
|---|---|
|`operation: drawing_path_operation`|One of `move/line/quadratic/cubic/arc/close`|
|`value_list: list[float]`|Fixed six numerical slots; `move/line` uses `x,y`; `quadratic` uses four values for control points and endpoints; `cubic` uses six values for two control points and endpoints; `arc` uses the first five values of endpoint, radius, and rotation angle|
|`clockwise: bool`|Whether the arc is clockwise|
|`large_arc: bool`|Whether to select the major arc for the arc|

### 7.3.drawing_image

Construction: `drawing_image(width: int, height: int, pixel_data)`.

`pixel_data` accepts continuous single-byte buffers, such as `bytes/bytearray/memoryview`. The image is arranged line by line, with each pixel being four bytes in order: R, G, B, A; the length must be exactly `width * height * 4`. The width and height must be greater than `0`.

|Member|Purpose|
|---|---|
|`width: int`|Read-only pixel width|
|`height: int`|Read-only pixel height|
|`rgba_data: bytes`|Read-only, RGBA pixel byte copy|
|`load_file(path: str) -> drawing_image`|Static method, loads image files supported by the system, ICO selects the largest image frame|
|`load_memory(data: bytes) -> drawing_image`|Static method, loads from fully encoded image bytes|
|`load_ico(data: bytes) -> drawing_image`|Static method, checks ICO file header and loads icons from memory|
|`encode_ico() -> bytes`|Preserves RGBA pixels, generates PNG single-image ICO losslessly; width and height are 1 to 256 pixels|

### 7.4 Extension points for derived controls

Ordinary controls can be derived in Python, with application state stored in their own members. Method names in Python match the following override signatures; drawing is called by the framework, and callbacks are submitted uniformly after returning.

|Override signatures|Responsibilities|
|---|---|
|`render(self, context)`|Draw the main body; can use `super().render(context)` to draw the native base class body|
|`render_overlay(self, context)`|Draw the pop-up layer; can call the base class's same-named drawing method|
|`is_focusable(self) -> bool`|Define whether to participate in focus navigation|
|`get_content_top(self) -> float`|Define the top offset of the content|
|`get_input_rectangle(self) -> rect`|Return the control's local input area|
|`process_input(self, event)`|Process input, set `event.handled` according to corresponding event rules; call `super().process_input(event)` to retain base class handling|

Container-derived classes have three layout hooks, called by the native framework:

|Override signatures|Return value and function|
|---|---|
|`get_active_control_list(self) -> list[control]`|List of controls currently involved in layout, drawing, and hit detection|
|`is_control_active(self, item: control) -> bool`|Specify whether the control is in the active state|
|`get_managed_control_rectangle(self, item: control, rectangle: rect) -> rect \| None`|Provide the logically rectangular area managed by the container; None follows the original rectangle|

Layout hooks are protected extension points, which Python-derived classes can override, and the corresponding native base class implementations are called through super within the derived class methods. The default set uses `control_list`, and Tab uses `page_list`. Window base class drawing is arranged through the context's `render_control_list` to arrange control drawing.

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

Derived classes of `selection_control` can override `is_blank_at(local_left, local_top)` and `clear_selection()`. Grid-derived classes can override `read_cell_value/write_cell_value/render_cell`, with signatures and writing results specified in the grid section.

## 8. Application loops, connections, and input interfaces

### 8.1 Running functions

|Signature|Purpose|
|---|---|
|`run(application_name: str) -> None`|Run the regular window application loop with the session name `application_name`; return without any loaded and closed windows or when the running environment stops.|
|`set_application_name(application_name: str) -> None`|Register the session name, which must be a non-empty string; `run(application_name)` already includes this step, and the independent main loop is called before the first `pump()`.|
|`pump(timeout_millisecond: int = 0) -> bool`|Assign messages and callbacks, advance the timing status, and submit windows to be updated. Return `True` when waiting for a specified millisecond according to parameters, and continue the loop.|
|`show_input_ui(window: window, rectangle: rect \| Sequence[int], completion = None) -> None`|Open the input interface for associated windows; the rectangular order is `left, top, width, height`.|
|`hide_input_ui(completion = None) -> None`|Request to hide the current input interface, and end the old input path after emptying it.|
|`get_application_directory() -> pathlib.Path`|Locate the application resource directory.|
|`measure_text(text: str, font: font) -> float`|Measure the text width in logical pixels using the specified font.|

The application loop executes events on the UI thread, as well as asynchronous notifications and callbacks for local delivery. The native connections store server events and asynchronous responses separately. The message pump combines these two queues in the order they are received. Internal synchronization requests only wait for their own responses; events that arrive during this time are processed by the subsequent message loop. For more details, see [, IPC, TLS, and connection queue](/en/advanced/03_ipc_tls_protocol).

The session name identifies this program in the engine's application list and serves as a basis for tracking window ownership. The name must be a non-empty string; it remains fixed after a connection is established, and passing a different name will throw an exception. When not explicitly named, the SDK uses the executable file name as the session name.

The input rectangle uses window logical coordinates, representing the text editing area. Associated windows must be current interactive regular application windows; layout/IME sessions and auxiliary windows cannot open the application input area. `completion` indicates whether the operation was successful for `Callable[[bool], None]` or `None`; after a request is issued, the application loop continues to process completion notifications. Displayed windows can still allow `run(application_name)` to run even when hidden; windows are closed when the application ends.

Changes in the focus of editable text controls are coordinated by the control framework; use the above function when the application needs to customize the input area. The engine routes the keyboard to the current window, and the focus inside the window is distributed by the control framework. `Pause` switches the physical keyboard interception mode, and only the editing area needs to display a virtual keyboard and IME interface.

After activating the editing control, the auxiliary input bar below the input area displays the language, IME name, and "Input Method Switch" button. Clicking the button first hides the input interface, then opens a modal selection dialog box: the layout list is selected independently, and the language list is used to filter the IME list. The dialog box retains the temporary selection for each language; clicking "OK" applies the selection, or you can set the selected IME as the default. Canceling will abandon the temporary selection, and returning to the original editing control after closing. In physical keyboard mode with a valid current window, `Alt+Shift` switches the language and restores the last used IME for that language; `Ctrl+Shift` switches the IME within the current language.

During window display, the SDK treats Ctrl+C in this process as a shortcut key on the interface. After the last displayed window closes, the console resumes processing. Ctrl+Break follows the console behavior.

### 8.2 Local and Remote Connections

Establish connections as needed when using windows or high-level application interfaces. Local applications connect to the engine through local discovery information. Remote connection parameters are provided by the startup command line, and the Python API uses the same set of parameters:

|Parameter|Purpose|
|---|---|
|`--easyvrui-host=值`|Host name, IPv4 or bare IPv6 address|
|`--easyvrui-port=值`|Port, omitted as `49537`|
|`--easyvrui-access-credential=值`|Access credentials|
|`--easyvrui-public-key-fingerprint=值`|Server public key SHA-256 fingerprint|

Used in the form of `--name=value`; placed on the same command line as the application's own parameters. Any remote parameter is verified in the remote mode; host, credentials, and fingerprint must be provided, and parameters cannot be repeated or empty; the port range is from `1` to `65535`. For example:

```cmd
python my_vr_app.py --easyvrui-host=192.0.2.10 --easyvrui-port=49537 --easyvrui-access-credential="my credential" --easyvrui-public-key-fingerprint=0000000000000000000000000000000000000000000000000000000000000000
```

Connection and certificate verification failures are reported as exceptions. The application layer can use windows, drawing, and input interfaces; see [Engine protocol reference for complete message field definitions and](./engine_protocol).

### 8.3 Application List and Termination

Application management interfaces can be imported from `easyvrui` or `easyvrui.application_manage`. List reading and process startup are completed on the machine where the process is called, so the application and Engine can be on different machines. A single instance is implemented by the application itself. The application management snapshot includes verified engine session and its windows, including the Desktop, with input components filtered out. Query and termination operations require a verified engine session, and the Desktop and input components are protected by termination operations.

|Signature|Purpose|
|---|---|
|`read_application_entry(manifest_path: str \| Path, language: str = "") -> application_entry`|Read the list and select a name according to the specified language. If the language is empty, use the system language, which will eventually revert to `en`.|
|`launch_application(manifest_path: str, extra_argument_list: Sequence[str] \| None = None) -> int`|Read the `.easyvrui` list and launch the application on this machine, returning the new process PID; `extra_argument_list` is added to the parameters declared in the list. If the list is missing or the launch fails, an exception is thrown.|
|`get_application_snapshot_list() -> list[application_snapshot]`|Query the session snapshot list returned by the engine.|
|`terminate_application(session_id: int) -> bool`|Terminate the process corresponding to the target session, returning the operation result given by the engine.|
|`close_application_window(session_id: int, window_id: int) -> bool`|Request the target session to properly close the specified window, returning whether the event was delivered.|
|`request_application_snapshot_list(completion) -> None`|Asynchronous query of application snapshots.|
|`request_terminate_application(session_id, completion) -> None`|Asynchronously request to end the application.|
|`request_close_application_window(session_id, window_id, completion) -> None`|Asynchronously properly close the window.|

The callback is executed on the application UI thread, receiving `(result, error)`. The snapshot query result is a list; the result of ending the application or closing the window is a boolean value. When successful, `error` is `None`.

#### `application_entry`

`read_application_entry()` will fill in the following read and write properties. The path is based on the directory where the manifest is located. For field rules, see [application manifest and](./application_manifest).

|Property|Purpose|
|---|---|
|`id: str`、`name: str`|The application ID and the display name after matching the completion language.|
|`icon_path: Path \| None`、`icon_data: bytes`|External icon path and the file bytes of the embedded icon.|
|`runtime: application_runtime`|Default `native`, indicating the launch of a native program. `python` indicates the launch of a Python main script.|
|`executable: Path \| None`、`script: Path \| None`|The parsed native program path or Python script path.|
|`argument_list: list[str]`|The launch parameters declared in the list.|
|`type: application_type`|The value can be `application`, `desktop`, `layout`, or `ime`, with default `application`.|

#### `application_snapshot`

|Property|Purpose|
|---|---|
|`session_id: int`|The session identifier assigned by the engine.|
|`process_id: int`|The process number corresponding to the session.|
|`name: str`|The session name.|
|`window_list: list[application_window]`|The list of windows registered for this session.|
|`memory_bytes: int`|The number of bytes occupied by the process memory.|
|`cpu_percent: float`|The percentage of CPU usage by the process.|
|`gpu_percent: float`|The percentage of GPU usage by the process.|

#### `application_window`

|Property|Purpose|
|---|---|
|`id: int`|Window identifier.|
|`name: str`|The application window name provided when creating the window.|
|`title: str`|Window title bar text|
|`visible: bool`|Whether the window is currently visible|

### 8.4 Focus and Tab

Default buttons, text boxes, combo boxes, and lists can gain focus; ordinary containers and labels usually do not participate in Tab navigation. Navigation skips controls on hidden, disabled, and inactive pages. Positive numbers `tab_index` are sorted in ascending order first, followed by the automatic items of `tab_index = 0`; for the same index, they are sorted in ascending order according to the window's absolute logical coordinates, `top`, and then in ascending order according to `left`, with positions also maintaining the traversal order. Therefore, automatic navigation follows a top-to-bottom row order, from left to right at the same height. Reverse navigation uses `Shift+Tab`, and after reaching the boundary, it loops.

When a text box gains focus, the corresponding input area is also updated; when switching the current window, the previous input interface is collapsed. Custom controls declare whether they participate in focus navigation through `focusable`, and handle button presses through `process_input()` or `on_key_down/on_key_up`.

## 9. Standard Dialog Boxes

Import the following functions from `easyvrui` or `easyvrui.dialog`. The call waits for the user to complete and returns the result, continuously processing interface activity during the waiting period. The owner is the direct parent window; the parent window is disabled during the modal period. Dialog boxes inherit their physical_scale, using World and center positioning.

|Signature|Return value|
|---|---|
|`color_dialog(color: int = 0x000000ff, title: str = "", default_color: int = 0x000000ff, owner: window \| None = None) -> int \| None`|Confirm to return to `0xRRGGBBAA`, cancel to return to None|
|`font_dialog(font: font = font(), title: str = "", default_font: font = font(), owner: window \| None = None) -> font \| None`|Confirm to return to the system font, cancel to return to None|
|`messagebox(message: str, title: str = "", button_set = messagebox_button_set.ok, icon = messagebox_icon.none, default_button = dialog_result.none, owner: window \| None = None) -> dialog_result`|Selected standard button|
|`messagebox(message: str, title: str, button_list: list[messagebox_button], icon = messagebox_icon.none, default_button_name: str = "", owner: window \| None = None) -> str`|Name of the selected button|
|`inputbox(prompt: str, title: str = "", default_text: str = "", max_length: int = 0, owner: window \| None = None) -> str \| None`|Confirm to return text, cancel to return None; both empty strings and text cancel are valid inputs|

`messagebox_button(name = "", text = "")` saves the button identifier and displayed text. The message box enumeration members and values are consistent with C++:

|Enumeration|Member|
|---|---|
|`messagebox_icon`|`none=0`、`error=0x10`、`question=0x20`、`warning=0x30`、`information=0x40`|
|`messagebox_button_set`|`ok=0`、`ok_cancel=1`、`abort_retry_ignore=2`、`yes_no_cancel=3`、`yes_no=4`、`retry_cancel=5`|
|`dialog_result`|`none=0`、`ok=1`、`cancel=2`、`abort=3`、`retry=4`、`ignore=5`、`yes=6`、`no=7`|

### 9.1 File Dialog Boxes

```python
file_open_dialog(title = "", initial_directory = None, initial_filename = "", filter_list = [], filter_index = 0, multi_select = False, confirm_text = "", owner = None, directory_changed = None, filter_changed = None)
file_save_dialog(title = "", initial_directory = None, initial_filename = "", filter_list = [], filter_index = 0, default_extension = "", confirm_overwrite = True, confirm_text = "", owner = None, directory_changed = None, filter_changed = None)
```

Opening returns to `list[pathlib.Path]`, canceling to return an empty list. Saving returns to `pathlib.Path`, canceling to return `None`. `initial_directory=None` uses a memory directory. `directory_changed` receives the path, `filter_changed` receives a filtering index starting from 0. Both callbacks receive initial values and subsequent changes.

`file_filter(name, pattern_list)` defines the filter name and file mode. `confirm_text` uses localized button text when empty. The extension can be completed through `default_extension` when saving, and confirmation can be controlled through `confirm_overwrite`.

```python
import easyvrui

path = easyvrui.file_save_dialog(title = "保存", initial_filename = "window1", filter_list = [easyvrui.file_filter("EasyVRUI UI", ["*.easyvruifrm"])], default_extension = "easyvruifrm", owner = owner)
```

### 9.2.language_pack

`language_pack.current` obtains the current SDK language pack. Built-in text is included in the Python native extension, defaulting to the system language selection. `language_pack.load_directory(path)` can explicitly load a custom language pack from a specified directory. This directory provides basic text with `en.json`, and other files are named according to the language code.

|Properties or Operations|Purpose|
|---|---|
|`locale: str`|Read or set the current language code|
|`available_locale_list: list[str]`|Language code provided by the current language pack|
|`key_list: list[str]`|Language keys available for querying under `locale`|
|`len(pack)`、`key in pack`|Number of language keys and member queries|
|`pack[key]`|Read text, throw `KeyError` for missing keys|
|`pack.format(key, *args)`|Substitute parameters into placeholders such as `{0}`, `{1}`, etc.|

## 10. Independent Layout and IME Applications

### 10.1. Enumeration and Component Information

|Type|Enumeration Members|
|---|---|
|`input_role`|`layout` Virtual Keyboard Layout, `ime` Input Method|
|`input_provider_state`|`stopped` Not Started, `starting` Starting, `running` Running|

`provider_info()` Default records can be constructed, fields are read-only:

|Field|Type and Default Values|Purpose|
|---|---|---|
|`id`|`int = 0`|Component Identifiers in the Engine|
|`name`|`str = ""`|Display Name|
|`language`|`str = "en"`|IME Language Code, commonly zh/en/ja, also supports other non-empty codes; layout records use default values|
|`role`|`input_role.ime`|Component Roles|
|`state`|`input_provider_state.stopped`|Startup Status|
|`configured`|`bool = False`|Whether from Persistent Configuration|
|`active`|`bool = False`|Whether it is the Component Currently Selected in the Query Session|
|`default_provider`|`bool = False`|Whether it is the Persistent Default IME|
|`process_id`|`int = 0`|Component Process ID|
|`error`|`str = ""`|Last Error Message of the Component|

List records are snapshots. Records are retained after the configured component exits and become not started; components registered dynamically and not written to the configuration are removed from the list after exiting.

The language of the IME is used for language grouping, and the protocol record of the layout omits this field. Python's provider_info.language is a read-only string; selecting a specific IME also determines the current input language.

### 10.2.input_ui_state

Construction: `input_ui_state()`.

|Read-Write Fields|Default Values and Purposes|
|---|---|
|`active: bool`|`False`; Whether the component is currently active in the input path|
|`physical: bool`|`False`; Whether it is currently in physical keyboard mode|
|`rectangle: render_rectangle \| None`|`None`; The positioning rectangle of the current component auxiliary window, in order of `left/top/width/height`|

In physical keyboard mode, the layout interface is collapsed. The layout state `rectangle` can be set to `None`. IME determines whether to display its prompt window based on the state; the English shell IME can have no interface at all.

### 10.3.input_event

Structure: `input_event()`. Fields can be set as follows:

|Field|Default Values and Purposes|
|---|---|
|`event_type: str`|`""`; Key events use `"key_down"/"key_up"`, text submission uses `"ime_submit"`.|
|`key: str`|`""`; Logical key names|
|`text: str`|`""`; Text related to the current input|
|`shift: bool`|`False`; Shift state|
|`ctrl: bool`|`False`; Ctrl state|
|`alt: bool`|`False`; Alt state|
|`meta: bool`|`False`; Windows/Meta key state|
|`handled: bool`|`False`; IME sets it to `True` for event consumption|

Read-only attribute `type` returns `input_event_type`, with members being `unknown`, `key_down`, `key_up`, and `ime_submit`.

### 10.4.input_provider

Structure: `input_provider()`. Ordinary applications can query components, while layout and IME applications create component objects and register them. It is recommended to derive this class to override the processing function.

|Property|Purpose|
|---|---|
|`provider_list: list[provider_info]`|Read-only; List snapshot of the last received components|
|`role: input_role`|Read-only; Currently registered roles, initially set to `ime` if not registered|
|`input_ui_state: input_ui_state`|Read-only; Snapshot of the current input path state|
|`session_id: int`|Read-only; Current session number, 0 if not connected|
|`connected: bool`|Read-only; Component connection status|
|`draining: bool`|Read-only; Whether the component is emptying input|
|`active: bool`|Read-only; Current state of `active`|
|`physical: bool`|Read-only; Current state of `physical`|

|Signature|Purpose|
|---|---|
|`register_provider(role: input_role = input_role.ime, default_provider: bool = False, name: str = "", language: str = "en") -> None`|Initiate component registration; Subsequent applications process the registration results. `default_provider` indicates applying to become the default component. language is only used for IME and must be a non-empty language code, defaulting to en|
|`send_event(event: input_event) -> None`|Send an event to the current input path|
|`commit_text(text: str, /) -> None`|IME submits the final text; layout calls will report role errors|
|`begin_input_task() -> None`|Register an unfinished input asynchronous task|
|`finish_input_task() -> None`|Complete a registered task; Must be paired with the start|
|`run() -> None`|Run the input component loop; initiate registration with the default IME role if not registered|
|`process_state(state: input_ui_state, /) -> None`|Can be overridden; handle changes in active path, mode, and positioning|
|`process_input(event: input_event, /) -> None`|Can be overridden; process keyboard inputs received by IME|
|`process_drain() -> None`|Can be overridden; complete the necessary application tasks for emptying|

After registration, the session is fixed to layout or IME role; the component window is marked as a auxiliary surface by the framework and Engine, which automatically positions and scales according to the associated input area. The set `reference_object` is ignored by Engine. These windows are used for keyboard, candidate, or prompt interfaces. Regular applications open the input area through `show_input_ui()`.

The input status callback first executes `process_state()`, then triggers `on_state_changed`. IME keys first execute `process_input()`, then trigger `on_input`; finally, when `handled=False`, the keys continue to be forwarded to the application, and when `handled=True`, they are consumed by IME. The submitted text uses `commit_text()`. layout sends keys to IME, which then processes or forwards them. IME candidate and combination states are maintained by the IME application itself.

|Event|Callback signature and usage|
|---|---|
|`on_state_changed`|`callback(state: input_ui_state) -> None`, changes in input path status|
|`on_input`|`callback(event: input_event) -> None`, IME receives key; can modify `handled`|

When the input interface is disabled, switched, or collapsed, the component receives a notification of emptying. Asynchronous tasks should be registered with `begin_input_task()` in advance, and completed with `finish_input_task()` after submission; during emptying, wait for old tasks and pending results to complete, then the component interface confirms the completion. `process_drain()` is suitable for ending its own buffering work. Unregistered, inactive, or completed emptying confirmations will not enter valid input paths.

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

This example only demonstrates processing and forwarding interfaces. Actual applications should maintain event pairing with the pressing, releasing, and modifying states of corresponding keys, and determine text mapping according to the required keyboard layout.

## 11. Languages and exceptions

|Signature|Purpose|
|---|---|
|`get_error_language() -> str`|Read the current error prompt language|
|`select_error_language(language: str, /) -> None`|Switch the prompt language, supports `zh/en/ja`|
|`get_localized_error(key: str, *argument_list) -> str`|Get prompt text by pressing the language key, and convert format parameters to a string|

These three functions can be imported from `easyvrui` or `easyvrui.common.error`. The initial language is selected based on the system's preferred language.

|Type or function|Purpose|
|---|---|
|`error_diagnostic(location = None, condition = "")`|Construct a diagnosis based on the calling position or the given `error_diagnostic`. Each field can also be specified with `error_diagnostic(file, line, column, function, condition)`|
|`engine_error(key: error_key, argument_list = [], location = None, condition = "")`|Engine error, inherit from `RuntimeError`. Read-only `key` is an enumeration value of `error_key`|
|`request_error(language_key: str, message: str, argument_list: list[str], diagnostic)`|Request error, inherit from `RuntimeError`. `diagnostic` can use existing diagnostic objects or exceptions with diagnostic fields|
|`localized_invalid_argument(key: language_key, argument_list = [], location = None, expression = "")`|Localization parameter error, inherit from `ValueError`. Read-only `key` is an enumeration value of `language_key`|
|`localized_runtime_error(key: language_key, argument_list = [], location = None, expression = "")`|Localized run error, inherit from `RuntimeError`. Read-only `key` is an enumeration value of `language_key`|
|`get_error_diagnostic(error: BaseException) -> error_diagnostic`|Read the diagnosis carried by the exception, use the calling position to generate a diagnosis for ordinary exceptions|
|`get_error_message(error: BaseException) -> str`|Read or generate a single-line exception text with diagnostic information|

Both `error_diagnostic` and the above four exceptions provide `get_message(key = "", detail = "")`, which is used to format a single-line diagnosis based on existing sources, given error keys, and descriptions. They share the following read-only properties.

|Property|Purpose|
|---|---|
|`file: str`|Diagnostic source file|
|`line: int`|Line number|
|`column: int`|Column number|
|`function: str`|Function name|
|`condition: str`|Failure conditions|

The exception also has read-only properties `language_key: str` and `argument_list: list[str]`, which record the language key string and format parameter list respectively. `str(error)` returns the full text of the exception in the format of `文件:行号:列号: error: 条件 [错误键] 说明`, where the error key and description are displayed according to the actual information.

## 12. Control property index

The following properties are arranged by the type of control they are declared in. Derived controls inherit properties from the base class.

|Definition hierarchy|Property|Access|
|---|---|---|
|`control`|`rect`|Reading and Writing|
|`control`|`background_color`|Reading and Writing|
|`control`|`visible`|Reading and Writing|
|`control`|`enabled`|Reading and Writing|
|`control`|`tab_index`|Reading and Writing|
|`text_control`|`foreground_color`|Reading and Writing|
|`text_control`|`font`|Reading and Writing|
|`selection_control`|`clear_selection_on_blank_click`|Reading and Writing|
|`item_control`|`selected_index`|Reading and Writing|
|`item_control`|`selected_item`|Read-only|
|`item_control`|`row_height`|Reading and Writing|
|`label`|`text`|Reading and Writing|
|`button`|`text`|Reading and Writing|
|`textbox`|`multiline`|Reading and Writing|
|`textbox`|`max_length`|Reading and Writing|
|`textbox`|`text`|Reading and Writing|
|`textbox`|`read_only`|Reading and Writing|
|`textbox`|`selectable`|Reading and Writing|
|`textbox`|`horizontal_scrollbar_visible`|Reading and Writing|
|`textbox`|`vertical_scrollbar_visible`|Reading and Writing|
|`textbox`|`selection_start`|Reading and Writing|
|`textbox`|`selection_length`|Reading and Writing|
|`textbox`|`selected_text`|Reading and Writing|
|`textbox`|`can_undo`、`can_redo`|Read-only|
|`combobox`|`dropdown_style`、`dropped_down`|Reading and Writing|
|`combobox`|`text`|Reading and Writing|
|`tabcontrol`|`selected_index`|Reading and Writing|
|`tabcontrol`|`tab_position`|Reading and Writing|
|`tabcontrol`|`tab_size`|Reading and Writing|
|`tabcontrol`|`page_close_button_visible`|Reading and Writing|
|`tabcontrol`|`tab_font`|Reading and Writing|
|`tabcontrol`|`tab_foreground_color`|Reading and Writing|
|`tabcontrol`|`tab_background_color`|Reading and Writing|
|`tabcontrol`|`selected_tab_foreground_color`|Reading and Writing|
|`tabcontrol`|`selected_tab_background_color`|Reading and Writing|
|`window`|`title`|Reading and Writing|
|`window`|`title_foreground_color`|Reading and Writing|
|`window`|`title_background_color`|Reading and Writing|
|`window`|`title_font`|Reading and Writing|
|`window`|`physical_scale`|Reading and Writing|
|`window`|`curvature`|Reading and Writing|
|`window`|`startup_position`|Reading and Writing|
|`window`|`curvature_adjustable`|Reading and Writing|
|`window`|`position`|Reading and Writing|
|`window`|`rotation`|Reading and Writing|
|`window`|`reference_object`|Reading and Writing|
|`window`|`show_title_bar`|Reading and Writing|
|`window`|`tracking_mode_set`|Reading and Writing|
|`window`|`show_close_button`|Reading and Writing|
|`window`|`movable`|Reading and Writing|
|`window`|`resizable`|Reading and Writing|
|`checkbox`|`checked`|Reading and Writing|
|`radiobutton`|`checked`|Reading and Writing|
|`numericupdown`|`value`|Reading and Writing|
|`numericupdown`|`minimum`|Reading and Writing|
|`numericupdown`|`maximum`|Reading and Writing|
|`numericupdown`|`step`|Reading and Writing|
|`numericupdown`|`decimal_places`|Reading and Writing|
|`slider`|`minimum`|Reading and Writing|
|`slider`|`maximum`|Reading and Writing|
|`slider`|`value`|Reading and Writing|
|`slider`|`orientation`|Reading and Writing|
|`progressbar`|`minimum`|Reading and Writing|
|`progressbar`|`maximum`|Reading and Writing|
|`progressbar`|`value`|Reading and Writing|
|`treeview`|`selected_node`|Reading and Writing|
|`scrollpanel`|`horizontal_scrollbar_visible`|Reading and Writing|
|`scrollpanel`|`vertical_scrollbar_visible`|Reading and Writing|
|`image`|`stretch_mode`|Reading and Writing|
|`splitter`|`orientation`|Reading and Writing|
|`splitter`|`split_position`|Reading and Writing|
|`screen`|`screen_id`|Reading and Writing|
|`grid`|`selection_mode`|Reading and Writing|
|`grid`|`multi_select`|Reading and Writing|
|`grid`|`row_height`|Reading and Writing|
|`grid`|`header_height`|Reading and Writing|
|`grid`|`read_only`|Reading and Writing|
|`grid`|`selected_index`|Reading and Writing|
|`grid`|`row_count`|Reading and Writing|
|`menuitem`|`text`|Reading and Writing|
|`menuitem`|`shortcut`|Reading and Writing|
|`menuitem`|`checkable`|Reading and Writing|
|`menuitem`|`checked`|Reading and Writing|
|`menuitem`|`separator`|Reading and Writing|
|`menubar`|`font`|Reading and Writing|
|`menubar`|`row_height`|Reading and Writing|
|`toolbar_button`|`separator`|Reading and Writing|
|`toolbar_button`|`enabled`|Reading and Writing|
|`toolbar_button`|`tooltip_text`|Reading and Writing|
|`toolbar`|`tool_size`|Reading and Writing|
|`toolbar`|`spacing`|Reading and Writing|
|`item_control`|`item_list`|Reading and Writing|
|`window`|`icon`|Reading and Writing|
|`menuitem`|`icon`|Reading and Writing|
|`toolbar_button`|`icon`|Reading and Writing|
|`image`|`source`|Reading and Writing|
|`listview`|`column_list`|Reading and Writing|
|`listview`|`item_list`|Reading and Writing|
|`grid`|`column_list`|Reading and Writing|

## 13. Python operator protocol index

|Protocol methods|Usage entry|
|---|---|
|`__eq__`|Comparison of values of the same type for `vec3/font/rect/color/reference_object`|
|`__add__`、`__sub__`|Vector addition and subtraction|
|`__mul__`、`__rmul__`|Vector multiplication with scalars; quaternions, pose combination|
|`__matmul__`|Pose combination using `@`|
|`__int__`、`__index__`、`__str__`|Integer, index integer, text conversion for colors|
|`__len__`、`__contains__`、`__getitem__`、`__delitem__`、`__iter__`|Length, inclusion, index, deletion, and traversal of sets|
|`__setitem__`|String item collection and subscript assignment for `grid[row, column]`|
|`__iadd__`、`__isub__`、`__bool__`|Addition, removal, and subscription check for event containers|
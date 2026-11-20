# window

`window` is the top-level spatial surface submitted to Engine and also serves as the container for sub-controls. Settings tools, status panels, and modal dialogs can all start from `window`. Each `window` has its own independent dimensions, display status, and spatial reference object.

Inherits [the common control API](/en/guide/controls/common-api#control) and [the container API](/en/guide/controls/common-api#container-control).

## Default appearance

When creating a new `window`, the title comes from the construction name, with logical dimensions of 640×360, hidden status, and reference object being `world`. After calling `show()`, the title bar displays the default icon, tracking selection entry, and close entry. The screenshot only adjusts the surface dimensions, with observation items marked using `label`.

Default appearance of ![window:](/images/en/window_default.png)

## Property comparison

|Position|Property changes|Observation results|
|---|---|---|
|Top left|Default title bar|Display standard title, tracking selection entry, and close entry|
|Top right|`title_foreground_color`, `title_background_color`, and `title_font`|The title is changed to warm-colored bold font, with the title bar background configured independently.|
|Bottom left|`show_close_button = False`|Close entry hidden in the title bar|
|Bottom right|`show_title_bar = False`|The entire title bar is hidden, and the content area can be moved up|

Comparison of ![window properties with](/images/en/window_comparison.png)

## Interface reference

C++ properties can be read and written through the access methods in the table; Python accesses them through the same-named properties. The event parameters in the table use C++ type names, with the corresponding Python types omitting the `_t` suffix. Common members are found in the basic interface of [,](/en/guide/controls/common-api).

### Property

|Property|C++|Purpose and default values|
|---|---|---|
|`title`|`get_title`、`set_title`|Title text, initially the construction name.|
|`title_foreground_color`、`title_background_color`|`get_title_foreground_color`、`set_title_foreground_color`、`get_title_background_color`、`set_title_background_color`|Title text and background color, respectively defaulting to `0xFFFFFFFF` and `0x244565FF`. The active state also affects the color scheme of the title bar.|
|`title_font`|`get_title_font`、`set_title_font`|Title font, defaulting to Segoe UI, 20 logical pixels.|
|`icon`|`get_icon`、`set_icon`|Title icon, initially the SDK icon; can be cleared by assigning `None` or leaving it empty for `shared_ptr`.|
|`menu`|`get_menu`、`set_menu`|`menubar` associated with the command area below the title bar, initially empty.|
|`show_title_bar`、`show_close_button`|`get_show_title_bar`、`set_show_title_bar`、`get_show_close_button`、`set_show_close_button`|Display switch for the title bar and standard close entry, initially true.|
|`tracking_mode_set`|`get_tracking_mode_set`、`set_tracking_mode_set`|Allow switching modes in the title bar, defaulting to including `world`, `body`, `left`, `right`, and `head`. An empty set hides the entry.|
|`movable`、`resizable`、`curvature_adjustable`|`get_movable`、`set_movable`、`get_resizable`、`set_resizable`、`get_curvature_adjustable`、`set_curvature_adjustable`|Control hand movement and rotation, interactive zooming, and interactive curvature adjustment respectively, initially set to true.|
|`physical_scale`|`get_physical_scale`、`set_physical_scale`|It’s a positive finite scaling factor, with an initial value of 1.0. Each logical pixel corresponds to 1 millimeter. When displayed for the first time, the scaling can be inherited from the source, without any explicit configuration being required.|
|`physical_width`、`physical_height`|`get_physical_width`、`get_physical_height`|Read-only, surface expansion width and height in meters.|
|`curvature`|`get_curvature`、`set_curvature`|Curvature, in meters' reciprocal, defaulting to 0.0 for a plane. The product of curvature and expansion width must be less than `2π`.|
|`position`、`rotation`|`get_position`、`set_position`、`get_rotation`、`set_rotation`|Initially all zero. Position is the offset relative to the upper left corner of the reference object, in meters, and rotation is the XYZ Euler angles, in degrees.|
|`startup_position`|`get_startup_position`、`set_startup_position`|First positioning method, defaulting to `center`. `none` uses the configured reference object and pose.|
|`reference_object`|`get_reference_object`、`set_reference_object`|Spatial reference object, defaulting to `world`.|
|`world_transform`|`get_world_transform`|Read-only, representing the world pose of the surface center. When the reference is unavailable, it returns `None` or an empty `optional`.|
|`loaded`、`closed`|`get_loaded`、`get_closed`|Read-only, representing completion of the first load and being closed, initially set to false.|
|`auxiliary`|`get_auxiliary`、`set_auxiliary`|Auxiliary surface flag, initially false. Surfaces in IME and layout sessions are associated with the input area by the Engine.|
|`dialog_result`|`get_dialog_result`、`set_dialog_result`|Initially `none`. During the modal period, assigning a valid result will close the window and return to that result.|
|`visible`、`rect`|`get_visible`、`set_visible`、`get_rect`、`set_rect`|Inherited display state and logical rectangle. Hidden after construction, initial size is 640×360.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`window(name)`|`window(name)`|Construct the top-level surface.|
|`show()`、`hide()`|`show()`、`hide()`|Show and hide surfaces. The first `show()` triggers loading, subsequent show and hide retain the window.|
|`close(force=False)`|`close(force=false)`|Request closure. Returns whether it has been closed; forced closure skips the cancellation process.|
|`activate()`|`activate()`|Request activation of an existing surface.|
|`show_dialog(owner_window)`|`show_dialog(owner_window)`|Synchronously run its own modal loop, temporarily preventing direct owner interaction. Returns `dialog_result` when closed.|
|`set_size(width,height)`|`set_size(width,height)`|Set positive logical width and height.|
|`reparent(reference,keep_world=False)`|`reparent(reference,keep_world=false)`|Switch reference object, allowing saving of world pose.|
|`is_tracking_available(mode)`|`get_is_tracking_available(mode)`|Query whether the specified reference object is available.|
|`center_at_view(distance)`|`center_at_view(distance)`|Center in front of the line of sight by the given number of meters, returning the positioning result.|
|`get_default_icon()`|`get_default_icon()`|Static method, obtaining the SDK default icon.|

### Event

|Event|Triggering conditions and parameters.|
|---|---|
|`on_title_changed`、`on_title_foreground_color_changed`、`on_title_background_color_changed`、`on_title_font_changed`|Change the title text, color, or font.|
|`on_icon_changed`、`on_menu_changed`|Changes to icons or associated `menubar`.|
|`on_show_title_bar_changed`、`on_show_close_button_changed`、`on_tracking_mode_set_changed`|Changes to the title bar, close entrance, or tracking selection set.|
|`on_movable_changed`、`on_resizable_changed`、`on_curvature_adjustable_changed`|Changes to space interaction switches.|
|`on_rotation_changed`、`on_curvature_changed`、`on_startup_position_changed`、`on_reference_object_changed`|Changes to rotation, curvature, start positioning method, or reference object. 3D position changes use the inherited `on_moved`.|
|`on_load`、`on_shown`、`on_hidden`|Triggered upon initial load, display, and hide.|
|`on_closing`、`on_closed`|Use `cancel_event_args_t` before closing, and set `cancel`; trigger `on_closed` after successful closing.|
|`on_render_failed`|Drawing submission failed with parameter `render_error_event_args_t`.|
|`on_tracking_lost`、`on_tracking_restored`|Reference object lost or restored.|
|`on_activated`、`on_deactivated`|Current surface activated or deactivated.|
|`on_move_start`、`on_move_end`、`on_resize_start`、`on_resize_end`、`on_curvature_adjust_start`、`on_curvature_adjust_end`|Start and end of interactive movement, zooming, and curvature adjustment. The end event uses `interaction_end_event_args_t`.|

## Independent routine

After startup, click "Switch Title Bar Color" to observe changes in the title bar background. Click again to restore the initial color. The event loop exits after closing the window.

First, prepare, build, and install](/en/basics/01_install_and_setup) using [environment. Open an x64 CMD with MSVC configured in the root directory of the tutorial repository, using the actual installed SDK path.

### C++

```bat
cmake -S examples/guide/controls/window-and-text/window/cpp -B .work/example_window -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_window --config Release
.work\example_window\Release\tutorial_window.exe
```

The above executable file path corresponds to the Visual Studio generator. When using single-configuration Ninja, the executable file is directly located in the build directory.

<<< ../../../../../examples/guide/controls/window-and-text/window/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\window\python\run.cmd
```

<<< ../../../../../examples/guide/controls/window-and-text/window/python/window_demo.py

### Run the effect

The effect of running ![window independently is](/images/en/window_demo.png).

## Common issues and practices.

- Logical coordinates and physical pose are configured separately. Use `position`, `rotation`, and `reference_object` to modify physical placement, and use `rect` or `set_size()` to adjust control layout.
- Set `startup_position = none` first when explicitly controlling the first-frame pose. Use `reparent(..., keep_world=True)` when there is an existing surface with a changed reference frame and position remains unchanged.
- `hide()` is suitable for temporary hiding. `close()` ends the instance lifecycle, and a new instance is created when the same interface is opened again. After hiding the standard close entrance, a clear close operation should be retained in the application process.
- `show_dialog()` uses other `window` in the same application that can be interacted with as its owner. Dialog box instances should enter modal mode before the first display.
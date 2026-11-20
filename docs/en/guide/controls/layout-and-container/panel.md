# panel

`panel` organizes a group of controls in a parent-child relationship, suitable for grouping connection status, local parameters, operation areas, or a set of mutually exclusive options together. The child controls added to `control_list` use coordinates relative to `panel`, and when `panel` is moved, the group moves accordingly.

The inherited general members are found in the [container interface](/en/guide/controls/common-api#container-control).

## Default appearance

The control background and border are drawn by default. An empty `panel` only displays its rectangular outline, and after adding child controls, it is drawn using the local coordinates of the group.

The default appearance of ![panel](/images/en/panel_default.png)

## Property comparison

The left side retains the default border, background, and title. The right side modifies `background_color` and adds another layer of `panel` with a background inside. The default border depends on the SDK rendering style, and custom borders can be drawn in the rendering of derived controls.

Comparison of properties between ![panel and](/images/en/panel_comparison.png)

## Interface reference

Property names in the Python usage table. C++ is read and written through corresponding methods, and uses `control_base &source` and type references in the table to subscribe to events. `event_args_t` without additional fields indicates that the state has been updated, and the callback reads the new value through `source`. The Python event type names are omitted for `_t`.

### Property

|Property|C++|Types, default values, and uses|
|---|---|---|
|`rect`|`get_rect`、`set_rect`|Inherited logical rectangle, with child control positions relative to this rectangle.|
|`background_color`|`get_background_color`、`set_background_color`|Inherited RGBA background color, using the SDK control background color by default.|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|Inherited display and interaction switches. Can be used to control a group of controls.|
|`control_list`|`get_control_list`|Read-only collection entry, used for adding, deleting, sorting, and indexing directly child controls.|
|`active_item_list`|`get_active_item_list`|Read-only, current list of active child controls.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`panel(name)`|`panel(name)`|Construct a regular container.|
|`control_list.add(item)`|`get_control_list().add(item)`|Add child controls to the parent level.|
|`control_list.remove(item)`|`get_control_list().remove(item)`|Remove child controls from the collection and return to the object.|
|`show()`、`hide()`|`show()`、`hide()`|Display or hide this group of content.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|Directly add or remove child controls. `item` is the control, and `index` is the position in the collection.|
|`on_background_color_changed`、`on_visible_changed`、`on_enabled_changed`|`event_args_t`|Inherited background or status changes.|
|`on_moved`、`on_size_changed`|`event_args_t`|Inherited position or size changes.|

## Independent routine

The main `panel` group displays synchronization services. The inner `panel` shows connection details; clicking "Hide connection details" hides the entire section, and clicking again restores it. The effect diagram shows the restored interface.

Prepare, build, and install](/en/basics/01_install_and_setup) by pressing [. The following command is executed in the x64 developer CMD at the root directory of the tutorial repository. Change the example SDK path to the actual installation location.

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/panel/cpp -B .work/example_panel -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_panel --config Release
.work\example_panel\Release\tutorial_panel.exe
```

The Visual Studio generator places the executable file in the `Release` subdirectory. The single-config Ninja generator directly outputs to the build directory.

<<< ../../../../../examples/guide/controls/layout-and-container/panel/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\panel\python\run.cmd
```

<<< ../../../../../examples/guide/controls/layout-and-container/panel/python/panel_demo.py

### Run the effect

Independent routine effect of ![panel](/images/en/panel_demo.png)

## Common problems and layout practices

- When nested, use parent-level coordinates layer by layer. To query the final surface rectangle, read `absolute_rectangle`, and continue using `rect` for layout configuration.
- `panel` is suitable for fixed-size grouping. Use [scrollpanel](./scrollpanel) when the content exceeds the visible area and scrolling is required.
- [radiobutton](../selection-and-status/radiobutton) form a group within the same direct parent container. Use different `panel` to isolate independent option groups.
# scrollpanel

`scrollpanel` is a container with a cropped viewport. It’s suitable for scrolling through logs, settings, and other controls that span across a single screen. The local rectangle of the child controls determines the range of content that can be displayed. The scrolling offset changes their position within the viewport. The area outside the viewport is cropped by the SDK.

The inherited general members are found in the [container interface](/en/guide/controls/common-api#container-control).

## Default appearance

The default horizontal and vertical scroll bars are both true, with offsets starting from 0. An empty viewport uses a standard background and border; when the switches are true, areas are reserved for the corresponding scroll bars.

![scrollpanel default appearance](/images/en/scrollpanel_default.png)

## Property comparison

Both sides use the same 6-row records and the same viewport. The left side is at the top, showing the first 3 rows. The right side has been scrolled down to show the subsequent records. The content on both sides is trimmed at the edges of the viewport.

![scrollpanel properties comparison with](/images/en/scrollpanel_comparison.png)

## Interface reference

Property names in the Python usage table. C++ is read and written through corresponding methods, and uses `control_base &source` and type references in the table to subscribe to events. `event_args_t` without additional fields indicates that the state has been updated, and the callback reads the new value through `source`. The Python event type names are omitted for `_t`.

### Property

|Property|C++|Types, default values, and uses|
|---|---|---|
|`horizontal_scrollbar_visible`|`get_horizontal_scrollbar_visible`、`set_horizontal_scrollbar_visible`|False by default. Controls the horizontal scroll bar and the area it occupies in the viewport.|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`、`set_vertical_scrollbar_visible`|False by default. Controls the vertical scroll bar and vertical joystick scrolling.|
|`control_list`|`get_control_list`|Read-only collection entry for sub-controls. The rectangular areas of direct sub-controls are used to calculate the content range.|
|`visible`、`enabled`|`set_visible`、`set_enabled`|Inherited read/write switch. Hiding or disabling stops the scrolling of the scroll bars.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`scrollpanel(name)`|`scrollpanel(name)`|Constructs a scalable and scrollable container. Daily applications control the viewport through scroll bars and handles.|
|`control_list.add(item)`|`get_control_list().add(item)`|Adds sub-controls using content coordinates.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_horizontal_scrollbar_visible_changed`、`on_vertical_scrollbar_visible_changed`|`event_args_t`|The corresponding scroll bar switch actually changes.|
|`on_viewport_changed`|`event_args_t`|Inherited viewport change notification. Triggers when scrolling or content changes affect the viewport.|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|Sub-controls are added or removed, with parameters including `item` and `index`.|

## Independent routine

“Synchronized Log” arranges 6 logs by local vertical coordinate. Enables vertical scrolling and disables horizontal scroll bars. Move the joystick down after pointing at the log area, or scroll the vertical scroll bar. The result shows the scrolled records.

Prepare, build, and install](/en/basics/01_install_and_setup) by pressing [. The following command is executed in the x64 developer CMD at the root directory of the tutorial repository. Change the example SDK path to the actual installation location.

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/scrollpanel/cpp -B .work/example_scrollpanel -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_scrollpanel --config Release
.work\example_scrollpanel\Release\tutorial_scrollpanel.exe
```

The Visual Studio generator places the executable file in the `Release` subdirectory. The single-config Ninja generator directly outputs to the build directory.

<<< ../../../../../examples/guide/controls/layout-and-container/scrollpanel/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\scrollpanel\python\run.cmd
```

<<< ../../../../../examples/guide/controls/layout-and-container/scrollpanel/python/scrollpanel_demo.py

### Run the effect

![scrollpanel independent routine effect](/images/en/scrollpanel_demo.png)

## Common problems and layout practices

- Leaves space for the visible scroll bars and control content. Horizontal scroll bars can be turned off when only up and down scrolling are needed, freeing up the bottom viewport area.
- Scrolling depends on content outside the viewport. Checks the actual position and size of sub-controls, especially whether the ends of the content exceed the visible range.
- After hiding sub-controls, their rectangular areas still participate in calculating the content range. When it's necessary to shorten the scrolling area, update the sub-controls' rectangular areas or remove the corresponding controls from the collection.
- Offset is a protected implementation interface. Ordinary applications use user interaction for scrolling, using `on_viewport_changed` to observe changes. The diagram shows setting the offset to the full row boundary in the WARP test host to demonstrate the cropping effect.
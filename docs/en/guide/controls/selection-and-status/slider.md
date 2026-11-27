# slider

`slider` provides a continuous drag experience within a finite integer range, suitable for real-time settings such as volume percentage, brightness level, and speed gear. The SDK converts the pointer position into a range ratio and rounds it to an integer. The range increases from left to right horizontally and from bottom to top vertically. When the keyboard focus is within `slider`, the direction keys → and ↑ increase by 1, while ← and ↓ decrease by 1.

The inherited general members are found in the [common control interface](/en/guide/controls/common-api#control).

## Default appearance

The default range is `[0, 100]`, with an initial value of 0 and a direction of `horizontal`. The pointer slider is displayed at the left end, with the track arranged along the horizontal axis of the control.

Default appearance of ![slider:](/images/en/slider_default.png)

## Property comparison

The upper left corner is `horizontal` with a value of 65. The right side displays the same value as `vertical`, with the upper end representing the maximum value. The lower left corner sets the range to `[-20, 20]`, with a value of 10 corresponding to 75% of the position. When disabled, the track and slider use a weakened color scheme.

Comparison of ![slider properties with](/images/en/slider_comparison.png)

## Interface reference

Property names in the Python usage table. C++ is read and written through corresponding methods, and uses `control_base &source` and type references in the table to subscribe to events. `event_args_t` without additional fields indicates that the state has been updated, and the callback reads the new value through `source`. The Python event type names are omitted for `_t`.

### Property

|Property|C++|Types, default values, and uses|
|---|---|---|
|`minimum`|`get_minimum`、`set_minimum`|`int64_t`, default 0. The new lower limit must be less than the current upper limit.|
|`maximum`|`get_maximum`、`set_maximum`|`int64_t`, default 100. The new upper limit must be greater than the current lower limit.|
|`value`|`get_value`、`set_value`|`int64_t`, default 0. When the value exceeds the range, it will clip onto the endpoints, and boundary adjustments will also correct the current value.|
|`orientation`|`get_orientation`、`set_orientation`|Default is `orientation_t::horizontal`. Python uses `orientation.horizontal` or `orientation.vertical`.|
|`focusable`|`is_focusable`|Inherits read-only capability, returning true.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`slider(name)`|`slider(name)`|Construct the control. Use the inherited `focus()` to request focus.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_minimum_changed`、`on_maximum_changed`|`event_args_t`|The actual change of the range endpoints.|
|`on_value_changed`|`event_args_t`|The actual change of integer values, including pointer, direction key, program assignment, or boundary clipping.|
|`on_orientation_changed`|`event_args_t`|The track direction changes.|
|`on_drag_start`|`event_args_t`|The pointer is pressed and dragging starts.|
|`on_drag_end`|`interaction_end_event_args_t`|The dragging ends. The canceled drag can be identified through `cancelled`.|

## Independent routine

Monitors volume starting from 35. When dragging `slider`, `on_value_changed` synchronously updates `progressbar` and the explanatory text. A screenshot shows the state after dragging the slider to the high volume area.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). The following command is executed in the x64 developer CMD at the root directory of the tutorial repository. Change the example SDK path to the actual installation location.

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/slider/cpp -B .work/example_slider -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_slider --config Release
.work\example_slider\Release\tutorial_slider.exe
```

The Visual Studio generator places the executable file in the `Release` subdirectory. The single-config Ninja generator directly outputs to the build directory.

<<< ../../../../../examples/guide/controls/selection-and-status/slider/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\slider\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/slider/python/slider_demo.py

### Run the effect

Independent routine effect of ![slider:](/images/en/slider_demo.png)

## Common problems and layout practices

- The vertical layout should reserve height for the track, width for the slider, and the laser hit area. Only when switching `orientation`, the original `rect` size remains unchanged.
- Update immediate feedback with `on_value_changed`, using `on_drag_end` as a signal that the pointer drag is complete. When keyboard adjustments are needed, handle the business state uniformly along the value change path.
- For precise decimal input, use [numericupdown on](./numericupdown). When using in conjunction with [progressbar and](./progressbar), first align the value ranges of both.
# numericupdown

`numericupdown` accepts finite small numbers, suitable for parameters such as gains, ratios, time intervals, and other parameters that require precise input or fixed increments. The internal editing area receives numbers. Input is submitted by pressing Enter or moving away from the editing focus. The upper and lower areas on the right are adjusted according to `step`; the content being edited is submitted before any operation.

For inherited general members, see the [text style interface](/en/guide/controls/common-api#text-control).

## Default appearance

Default values are `value = 0.0`, `minimum = 0.0`, `maximum = 100.0`, `step = 1.0`, `decimal_places = 0`. The display area shows 0 in integer form, with the upper and lower operation areas on the right.

![numericupdown default appearance](/images/en/numericupdown_default.png)

## Property comparison

The first line displays the default value of 0. The second line includes a negative range, with the lower limit shown as −2.00. The third line increases by 0.25 steps to 1.25, and the fourth line retains the same value while disabling the control. `decimal_places` determines the number of decimal places to display.

![numericupdown property comparison](/images/en/numericupdown_comparison.png)

## Interface reference

Property names in the Python usage table. C++ is read and written through corresponding methods, and uses `control_base &source` and type references in the table to subscribe to events. `event_args_t` without additional fields indicates that the state has been updated, and the callback reads the new value through `source`. The Python event type names are omitted for `_t`.

### Property

|Property|C++|Types, default values, and uses|
|---|---|---|
|`value`|`get_value`、`set_value`|`double`, default 0.0. It must be a finite value; out-of-range values are clipped to the current range.|
|`minimum`|`get_minimum`、`set_minimum`|`double`, default 0.0. Finite and less than the current upper limit.|
|`maximum`|`get_maximum`、`set_maximum`|`double`, default 100.0. Finite and greater than the current lower limit.|
|`step`|`get_step`、`set_step`|`double`, default 1.0. Positive finite number used for upper and lower adjustments.|
|`decimal_places`|`get_decimal_places`、`set_decimal_places`|`uint32_t`, default 0, supporting values from 0 to 17. Controls the display of fixed decimal places; after decimal points are enabled, English decimal marks are accepted.|
|`focusable`|`is_focusable`|Read-only. The editing area, increase area, and decrease area are different focus positions of the same control.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`numericupdown(name)`|`numericupdown(name)`|Construct the control. Set the initial value using `value` or `set_value()`.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_value_changed`|`event_args_t`|The submitted value actually changes. Each key input in the editing buffer does not necessarily result in a numerical change.|
|`on_minimum_changed`、`on_maximum_changed`|`event_args_t`|The range endpoints actually change. Changing the range may immediately trigger a value change.|
|`on_step_changed`、`on_decimal_places_changed`|`event_args_t`|The step size or decimal places actually change.|

## Independent routine

In this example, the gain is limited between 0.00 and 2.00, with an initial value of 0.75. Clicking the upper adjustment area displays 1.00, and the status text is updated accordingly. Activating the editing area also allows direct input of values and submission by pressing Enter.

Prepare, build, and install](/en/basics/01_install_and_setup) by pressing [. The following command is executed in the x64 developer CMD at the root directory of the tutorial repository. Change the example SDK path to the actual installation location.

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/numericupdown/cpp -B .work/example_numericupdown -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_numericupdown --config Release
.work\example_numericupdown\Release\tutorial_numericupdown.exe
```

The Visual Studio generator places the executable file in the `Release` subdirectory. The single-config Ninja generator directly outputs to the build directory.

<<< ../../../../../examples/guide/controls/selection-and-status/numericupdown/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\numericupdown\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/numericupdown/python/numericupdown_demo.py

### Run the effect

![numericupdown independent routine effect](/images/en/numericupdown_demo.png)

## Common problems and layout practices

- Reserve space for negative signs, decimal points, required number of digits, and the right adjustment area. Increasing the size of `font` also increases `rect.height`.
- `decimal_places` controls format and character filtering; business precision should be agreed upon separately. Directly setting `value` also allows input of finite values not in the `step` sequence.
- When adjusting the range, first set the side that can maintain `minimum < maximum`. When saving data, read `value`; invalid inputs will restore the current value's formatted display.
- In the editing area, adjustments can be made using Up or Down when the focus is within the editing area. When the focus is on the increase or decrease area, adjustments can be made using Enter or Space.
# checkbox

`checkbox` represents a boolean option that can be independently toggled, such as whether to play the notification sound. Multiple `checkbox` options can be selected simultaneously or restored to the unchecked state individually.

Inherit the public control interface [, as well as the text style interfaces](/en/guide/controls/common-api#control) and [from](/en/guide/controls/common-api#text-control).

## Default appearance

Default value for `checked = False`, can be focused and enabled. The blank box indicates unselected status; the screenshot shows it with text filled in.

Default appearance of ![checkbox, equivalent to](/images/en/checkbox_default.png).

## Property comparison

Four lines sequentially display unselected, selected, disabled after selection, and font and color details. Disabled and selected states can coexist; the checkmark and text brightness represent these two states respectively.

Comparison of ![checkbox properties with](/images/en/checkbox_comparison.png).

## Interface reference

C++ properties can be read and written through the access methods in the table; Python accesses them through the same-named properties. The event parameters in the table use C++ type names, with the corresponding Python types omitting the `_t` suffix. Common members are found in the basic interface of [,](/en/guide/controls/common-api).

### Property

|Property|C++|Purpose and default values|
|---|---|---|
|`text`|`get_text`、`set_text`|Option description, default value is an empty string.|
|`checked`|`get_checked`、`set_checked`|Boolean selection state, initially false.|
|`focusable`|`is_focusable`|Order of focusability.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`checkbox(name)`|`checkbox(name)`|Creates an independent binary option.|

### Event

|Event|Triggering conditions and parameters.|
|---|---|
|`on_text_changed`|Actual text changes are displayed, with parameter being `event_args_t`.|
|`on_checked_changed`|Actual changes to `checked`, including user interaction and program-defined values. Parameter is `event_args_t`.|
|`on_click`|Inherited activation event. `on_checked_changed` is used when maintaining the selected state persistently.|

## Independent routine

Initially, only the "Show unread status" option is selected. After checking "Play notification sound," the other option remains selected, and the status text is updated. Switching again can turn off the notification sound.

First, prepare, build, and install](/en/basics/01_install_and_setup) using [environment. Open an x64 CMD with MSVC configured in the root directory of the tutorial repository, using the actual installed SDK path.

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/checkbox/cpp -B .work/example_checkbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_checkbox --config Release
.work\example_checkbox\Release\tutorial_checkbox.exe
```

The above executable file path corresponds to the Visual Studio generator. When using single-configuration Ninja, the executable file is directly located in the build directory.

<<< ../../../../../examples/guide/controls/selection-and-status/checkbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\checkbox\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/checkbox/python/checkbox_demo.py

### Run the effect

Independent execution effect of ![checkbox with](/images/en/checkbox_demo.png).

## Common issues and practices.

- Initialize by restoring `checked` from configuration first, then subscribe to `on_checked_changed` to avoid treating the restoration state as a new operation.
- Use state events uniformly for persistence. When restoring multiple options in batches, merge multiple changes into one save operation at the business layer.
- The current interface provides two boolean states. For clearly mutually exclusive options, use [radiobutton and](./radiobutton).
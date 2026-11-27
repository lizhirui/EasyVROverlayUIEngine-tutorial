# radiobutton

`radiobutton` is suitable for selecting from the same group of options, such as notification strategies. `radiobutton` within the same direct parent container constitutes a group. Create `panel` for multiple independent groups.

Inherit the public control interface [, as well as the text style interfaces](/en/guide/controls/common-api#control) and [from](/en/guide/controls/common-api#text-control).

## Default appearance

Initially not selected, focusable, and displayed with hollow circles. The default text is empty; only sample text and rectangles should be filled in for screenshots.

Default appearance of ![radiobutton:](/images/en/radiobutton_default.png)

## Property comparison

The first and second lines show hollow circles and solid selected dots. The third line displays disabled and unselected text with circles. The fourth line changes the font, foreground color, and background color.

Attribute comparison between ![radiobutton and](/images/en/radiobutton_comparison.png)

## Interface reference

C++ properties can be read and written through the access methods in the table; Python accesses them through the same-named properties. The event parameters in the table use C++ type names, with the corresponding Python types omitting the `_t` suffix. Common members are found in the basic interface of [,](/en/guide/controls/common-api).

### Property

|Property|C++|Purpose and default values|
|---|---|---|
|`text`|`get_text`、`set_text`|Option description, default value is an empty string.|
|`checked`|`get_checked`、`set_checked`|Boolean selection state, default false. When set to true, remove any other selected `radiobutton` within the same direct parent container.|
|`focusable`|`is_focusable`|Order of focusability.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`radiobutton(name)`|`radiobutton(name)`|Create a mutually exclusive option. Set the default item after adding to the parent container.|

### Event

|Event|Triggering conditions and parameters.|
|---|---|
|`on_checked_changed`|Triggered when selected or deselected, with parameter `event_args_t`. Switching within the group may first receive an event to cancel the old item.|
|`on_text_changed`|Actual text changes are displayed, with parameter being `event_args_t`.|
|`on_click`|Inherited activation event. It's advisable to use `on_checked_changed` to track the current group value.|

## Independent routine

Two `radiobutton`s belong to the same `panel`. Initially set to "Only receive important notifications"; after choosing "Receive all notifications", observe the cancellation of the old item and the update of the status text.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Open an x64 CMD with MSVC configured in the root directory of the tutorial repository, using the actual installed SDK path.

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/radiobutton/cpp -B .work/example_radiobutton -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_radiobutton --config Release
.work\example_radiobutton\Release\tutorial_radiobutton.exe
```

The above executable file path corresponds to the Visual Studio generator. When using single-configuration Ninja, the executable file is directly located in the build directory.

<<< ../../../../../examples/guide/controls/selection-and-status/radiobutton/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\radiobutton\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/radiobutton/python/radiobutton_demo.py

### Run the effect

Independent operation effect of ![radiobutton:](/images/en/radiobutton_demo.png)

## Common issues and practices.

- First add all options to the common parent container, then set the default selected item to ensure that group rules can check other options.
- Check the source of `checked` when there is a change in status. Selected events are suitable for submitting business enumeration, while canceled events are suitable for clearing old item states.
- If the business requires always having options, explicitly set the default item during initialization and avoid programmatically setting the current item to false.
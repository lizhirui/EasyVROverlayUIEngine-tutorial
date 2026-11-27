# button

`button` maps a user operation to a specific command, such as applying settings, confirming, or re-editing. Use concise text to describe the operation result, and update `enabled` when the command is temporarily unavailable.

Inherit the public control interface [, as well as the text style interfaces](/en/guide/controls/common-api#control) and [from](/en/guide/controls/common-api#text-control).

## Default appearance

By default, it is focused, visible, and enabled. `text` initially remains empty, with set text centered within the control rectangle. Screenshots should only include text and the rectangle.

![button default appearance:](/images/en/button_default.png)

## Property comparison

Four lines sequentially display the default, font and color, disabled, and focus border states. The same text allows for direct comparison of state differences. Alignment follows fixed control drawing rules.

![button property comparison:](/images/en/button_comparison.png)

## Interface reference

C++ properties can be read and written through the access methods in the table; Python accesses them through the same-named properties. The event parameters in the table use C++ type names, with the corresponding Python types omitting the `_t` suffix. Common members are found in the basic interface of [,](/en/guide/controls/common-api).

### Property

|Property|C++|Purpose and default values|
|---|---|---|
|`text`|`get_text`、`set_text`|Text for reading, writing, and displaying, initially a empty string.|
|`focusable`、`enabled`、`tab_index`|`is_focusable`、`get_enabled`、`set_enabled`、`get_tab_index`、`set_tab_index`|Can be focused, defaultly enabled. `tab_index` participates in the Tab order of `window`.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`button(name)`|`button(name)`|Create a `button`.|
|`focus()`、`activate()`|`focus()`、`activate()`|Inherits interface. The former requests focus, while the latter triggers the activation path programmatically.|

### Event

|Event|Triggering conditions and parameters.|
|---|---|
|`on_text_changed`|The title text actually changes, with the parameter being `event_args_t`.|
|`on_click`|Inherited activation event, with the parameter being `event_args_t`.|
|`on_focus_in`、`on_focus_out`、`on_enabled_changed`|Inherited event, suitable for observing focus and availability status.|

## Independent routine

After clicking "Submit Settings," the status text is updated, the submission entry is disabled, and "Reedit" becomes available. Clicking "Reedit" restores the initial state.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Open an x64 CMD with MSVC configured in the root directory of the tutorial repository, using the actual installed SDK path.

### C++

```bat
cmake -S examples/guide/controls/window-and-text/button/cpp -B .work/example_button -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_button --config Release
.work\example_button\Release\tutorial_button.exe
```

The above executable file path corresponds to the Visual Studio generator. When using single-configuration Ninja, the executable file is directly located in the build directory.

<<< ../../../../../examples/guide/controls/window-and-text/button/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\button\python\run.cmd
```

<<< ../../../../../examples/guide/controls/window-and-text/button/python/button_demo.py

### Run the effect

![button independent routine execution effect:](/images/en/button_demo.png)

## Common issues and practices.

- When submitting network or disk tasks, the available status is updated first, and then the UI is refreshed via `begin_invoke()` after completion, avoiding time spent on event callback processing.
- Place business calls within `on_click`, so clicks and programmatic activations share a single path. When multiple `button`s are enabled consecutively, set a clear `tab_index`.
- Temporary disablement and permanent removal use `enabled` and container collection operations respectively, providing readable hints for the disabled state.
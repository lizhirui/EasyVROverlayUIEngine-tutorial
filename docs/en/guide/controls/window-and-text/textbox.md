# textbox

`textbox` is used for single-line names, phrases, or multi-line notes. It provides cursor, selection, copy, undo, and redo functions, and integrates with IME and layout through the SDK when input conditions are met.

Inherit the public control interface [, as well as the text style interfaces](/en/guide/controls/common-api#control) and [from](/en/guide/controls/common-api#text-control).

## Default appearance

Default single-line, selectable, and editable. Both scroll bars are disabled. Screenshot is used to fill in sample text.

Default appearance of ![textbox:](/images/en/textbox_default.png)

## Property comparison

From top to bottom: default, `read_only`, `enabled = False`, multi-line, and vertical scroll bars. `read_only` retains normal text color and selection capability; disabled status reduces text brightness. The current SDK's `textbox` does not have `password` mask attribute; use an entry with password processing for sensitive input.

Comparison of ![textbox properties with](/images/en/textbox_comparison.png)

## Interface reference

C++ properties can be read and written through the access methods in the table; Python accesses them through the same-named properties. The event parameters in the table use C++ type names, with the corresponding Python types omitting the `_t` suffix. Common members are found in the basic interface of [,](/en/guide/controls/common-api).

### Property

|Property|C++|Purpose and default values|
|---|---|---|
|`text`|`get_text`、`set_text`|Text, initially empty. Assignment applies multi-line and length restrictions.|
|`read_only`|`get_read_only`、`set_read_only`|Initially disabled. After enabling, it retains cursor, selection, and copy functions, preventing users from changing text.|
|`selectable`|`get_selectable`、`set_selectable`|Initially enabled. Disabling returns text selection and editing paths; the control still retains focus.|
|`multiline`|`get_multiline`、`set_multiline`|Initially disabled. Enabling retains line breaking and supports Enter for line breaking.|
|`horizontal_scrollbar_visible`、`vertical_scrollbar_visible`|`get_horizontal_scrollbar_visible`、`set_horizontal_scrollbar_visible`、`get_vertical_scrollbar_visible`、`set_vertical_scrollbar_visible`|Initially both disabled. Control horizontal and vertical scroll bars respectively.|
|`max_length`|`get_max_length`、`set_max_length`|Upper limit of text code points; 0 means no limit by default.|
|`selection_start`、`selection_length`|`get_selection_start`、`set_selection_start`、`get_selection_length`、`set_selection_length`|Starting point and length of the selection, represented by code point indices; both are 0 initially.|
|`selected_text`|`get_selected_text`、`set_selected_text`|Current selection text, initially empty. Assignment will replace the selection by the program, and can also be used to update read-only fields.|
|`can_undo`、`can_redo`|`get_can_undo`、`get_can_redo`|Read-only, indicating whether there are executable undo or redo records.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`textbox(name)`|`textbox(name)`|Create a `textbox`.|
|`select(start,length=0)`|`select(start,length=0u)`|Set the valid selection; 0 length means moving the insertion position.|
|`undo()`、`redo()`|`undo()`、`redo()`|Undo or redo the edit, returning whether it was successful.|

### Event

|Event|Triggering conditions and parameters.|
|---|---|
|`on_text_changed`、`on_read_only_changed`、`on_selectable_changed`|The text or corresponding switch has actually changed, with parameter `event_args_t`.|
|`on_selection_changed`、`on_max_length_changed`、`on_multiline_changed`|Changes in selection, length limit, or multi-line settings, with parameter `event_args_t`.|
|`on_horizontal_scrollbar_visible_changed`、`on_vertical_scrollbar_visible_changed`|Changes in corresponding scroll bar switches, with parameter `event_args_t`.|
|`on_text_input`|Text input notification, with parameter `text_input_event_args_t`.|

## Independent routine

Run and edit any line, observing the status text update. Clicking "Select All Notes" requests `textbox` focus and selects the field text. The effect shows the highlighting after selecting all.

First, prepare, build, and install](/en/basics/01_install_and_setup) using [environment. Open an x64 CMD with MSVC configured in the root directory of the tutorial repository, using the actual installed SDK path.

### C++

```bat
cmake -S examples/guide/controls/window-and-text/textbox/cpp -B .work/example_textbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_textbox --config Release
.work\example_textbox\Release\tutorial_textbox.exe
```

The above executable file path corresponds to the Visual Studio generator. When using single-configuration Ninja, the executable file is directly located in the build directory.

<<< ../../../../../examples/guide/controls/window-and-text/textbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\textbox\python\run.cmd
```

<<< ../../../../../examples/guide/controls/window-and-text/textbox/python/textbox_demo.py

### Run the effect

Independent execution effect of ![textbox:](/images/en/textbox_demo.png)

## Common issues and practices.

- First set `multiline`, then assign initial content to `text`. Single-line mode removes line breaking; CRLF and CR are unified as LF within the editor.
- Program updates, interactive editing, and selection replacement follow length and text boundaries. Group characters' boundaries may include multiple code points.
- Use `read_only` for viewing and copying, `label` for displaying only text, and `enabled = False` for temporarily blocking interaction.
- For the final text on the business side, use `on_text_changed` and read from `text`. In multi-line input, do not interpret each Enter as a submission.
# toolbar

`toolbar` is placed in a fixed rectangle in sequence with `toolbar_button`, ready for immediate use. The container is responsible for size, spacing, cutting, and button layout. The button collection is made public by `button_list`. For inherited members, see the [container interface and](/en/guide/controls/common-api#container-control).

## Default appearance

Two icons and one separator are added to the diagram. The control uses the default tool size, spacing, and color scheme.

Default appearance of ![toolbar:](/images/en/toolbar_default.png)

## Property comparison

The top remains with the default size and spacing. The bottom uses a tool size of 56 logical pixels and a spacing of 14 logical pixels, with the right-side operation items disabled.

Comparison of ![toolbar properties with](/images/en/toolbar_comparison.png)

## Interface reference

C++ reads and writes attributes using the methods in the table. In Python, access is done through attributes with the same name. Callbacks receive `source` and `event`. Each strong-type parameter in the table inherits from `event_args_t`; basic parameters do not have additional fields. Python type names are omitted in `_t`.

### Property

|Property|C++ access methods|Types, default values, and uses|
|---|---|---|
|`button_list`|`get_button_list`|`toolbar_button_collection` manages the order and ownership of buttons.|
|`tool_size`、`spacing`|`get_tool_size`、`set_tool_size`、`get_spacing`、`set_spacing`|The tool size defaults to 40 logical pixels, must be a positive integer. The spacing defaults to 6.0 logical pixels, must be a non-negative finite value.|
|`focusable`|`is_focusable`|Read-only; containers and items have their own focus rules.|

### Method

|Method|Purpose|
|---|---|
|`toolbar(name)`|Construction.|
|`button_list.add(item)`、`button_list.insert(index,item)`|Append or insert operation items.|
|`button_list.add_separator(name)`|Python appends separators by name. C++ first creates an item with `get_button_list().add(name)` and then calls the `set_separator(true)` of that item.|
|`button_list.remove(item)`、`button_list.clear()`|Remove or clear items. C++ first calls `get_button_list()`.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_tool_size_changed`、`on_spacing_changed`|`event_args_t`|Actual changes in size and spacing.|

## toolbar_button

|Member|Purpose|
|---|---|
|`toolbar_button(name)`|Create items that can be added to `button_list`.|
|`icon`、`get_icon/set_icon`|Read and write the optional `drawing_image`.|
|`separator`、`get_separator/set_separator`|Control whether items are used as separators.|
|`enabled`、`tooltip_text`|Inherited interaction switches and hover descriptions.|
|`on_icon_changed`、`on_click`|All parameters are `event_args_t`, indicating that icon changes are associated with business command activation.|

Access items by index or name through `toolbar_button_collection`. The regular rectangle of the button is managed by the associated `toolbar`.

## Independent routine

Clicking the blue icon triggers "Request Preview". The icon is created with 4-byte RGBA data, and the hover description indicates the purpose of the command.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Execute the command in the x64 Developer CMD of the tutorial root directory, and replace the SDK installation path in the example.

### C++

```bat
cmake -S examples/guide/controls/command-and-display/toolbar/cpp -B .work/example_toolbar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_toolbar --config Release
.work\example_toolbar\Release\tutorial_toolbar.exe
```

When using a single-configured Ninja, run the executable directly from the build directory.

<<< ../../../../../examples/guide/controls/command-and-display/toolbar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\toolbar\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/toolbar/python/toolbar_demo.py

### Run the effect

Independent execution of the ![toolbar with](/images/en/toolbar_demo.png)

## Common problems and layout practices

- Reserve width and height for the icon hit area. When the total width of the item increases, increase the container width or reduce the number of currently displayed operation items.
- Use separators to distinguish different tasks. Use `enabled` to represent commands that are temporarily unavailable.
- Use `tooltip_text` to describe the meaning of the icon. The image itself is used through shared drawing resources.
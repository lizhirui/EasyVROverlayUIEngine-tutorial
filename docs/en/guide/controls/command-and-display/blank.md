# blank

`blank` is a placeholder control for storage names, rectangles, and set positions. The designer can use it to reserve positions for custom controls that will be inserted later. When the application loads content, it reads its local `rect` and replaces the set item with a real control. For inherited members, see the [public control interface and](/en/guide/controls/common-api#control).

## Default appearance

`blank` itself is transparent and does not draw. The border visible in the diagram comes from the parent `panel`, used to indicate the content area where the placeholder rectangle is located.

![blank default appearance](/images/en/blank_default.png)

## Property comparison

The left side of `panel` contains `blank`, while `label` is used on the right side at the same local position. The actual text and interactive capabilities come from the replaced control.

![blank property comparison with](/images/en/blank_comparison.png)

## Interface reference

C++ reads and writes attributes using the methods in the table. In Python, access is done through attributes with the same name. Callbacks receive `source` and `event`. Each strong-type parameter in the table inherits from `event_args_t`; basic parameters do not have additional fields. Python type names are omitted in `_t`.

### Property

|Property|C++ access methods|Types, default values, and uses|
|---|---|---|
|`name`、`type`、`id`、`parent`、`disposed`|`get_name`、`get_type`、`get_id`、`get_parent`、`get_disposed`|The read and write rules are the same as `control_base`, with `type` being `blank`.|
|`rect`、`tag`|`get_rect`、`set_rect`、`get_tag`、`set_tag`|Inherited local rectangles and application markers.|
|`absolute_rectangle`、`owning_window`|`get_absolute_rectangle`、`get_owning_window`|Inherited surface rectangles and window query.|
|`focused`|`get_focused`|Read-only, `blank` cannot gain focus.|

### Method

|Method|Purpose|
|---|---|
|`blank(name)`|Create placeholder items, adding, removing, or replacing them through the container's `control_list`.|
|`dispose()`、`invalidate()`、`begin_invoke(callback)`|Inherited lifecycle and thread scheduling methods.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_moved`、`on_size_changed`、`on_viewport_changed`|`event_args_t`|Inherited geometry and viewport notifications.|
|`on_tag_changed`、`on_disposed`|`event_args_t`|Inherited marking and release events.|
|`on_property_changed`|`property_changed_event_args_t`|Publicly configurable property changes, carried by `property_name`.|

## Public member restrictions

`blank` retains layout and ownership functionality. Its visibility, enablement, focus, input, background, hover prompts, and Tab properties do not belong to this type of public interface. In Python, access to hidden members will result in `AttributeError`. The application should leave the visual effects and interactive events to the replaced control.

## Independent routine

After clicking "Load Content," the program copies the placeholder rectangle, inserts `label` at the original index, and disables the loading operation. The diagram shows the replaced state.

Prepare, build, and install the](/en/basics/01_install_and_setup) Engine according to the [environment. Execute the command in the x64 Developer CMD of the tutorial root directory, and replace the SDK installation path in the example.

### C++

```bat
cmake -S examples/guide/controls/command-and-display/blank/cpp -B .work/example_blank -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_blank --config Release
.work\example_blank\Release\tutorial_blank.exe
```

When using a single-configured Ninja, run the executable directly from the build directory.

<<< ../../../../../examples/guide/controls/command-and-display/blank/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\blank\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/blank/python/blank_demo.py

### Run the effect

![blank independent execution effect](/images/en/blank_demo.png)

## Common problems and layout practices

- First record `rect` and set positions, then remove the original placeholder item. The replacement work is placed on the associated UI thread.
- When retaining a stable identifier, the name in the design file can be used to find the position, but the names within the set must be unique.
- The reserved size should consider the final control's font, padding, and focus style.
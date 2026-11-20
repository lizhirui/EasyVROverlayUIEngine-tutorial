# combobox

`combobox` compresses limited options into a single input area. `dropdown_list` is suitable for configuration items that can only be selected from preset values, while `dropdown` also allows free single-line input. Both modes share the string collection, selection index, and dropdown layers.

For inherited general members, refer to the [text style interface,](/en/guide/controls/common-api#text-control), and [string selection and collection interfaces,](/en/guide/controls/common-api#item-control).

## Default appearance

The default mode is `dropdown_list`, `item_list` is empty, `selected_index = -1`, `text` is empty, `dropped_down = False`. The diagram shows the closed empty control.

Default appearance of ![combobox,](/images/en/combobox_default.png)

## Property comparison

The first line displays existing options in `dropdown_list`. The second line switches to `dropdown`, entering "every 45 minutes" outside the collection, with the index being `-1`. The third line shows `dropped_down = True`, with the pointer located at the currently selected "every 15 minutes".

Property comparison of ![combobox,](/images/en/combobox_comparison.png)

## Interface reference

Property names in the Python usage table. C++ is read and written through corresponding methods, and uses `control_base &source` and type references in the table to subscribe to events. `event_args_t` without additional fields indicates that the state has been updated, and the callback reads the new value through `source`. The Python event type names are omitted for `_t`.

### Property

|Property|C++|Types, default values, and uses|
|---|---|---|
|`dropdown_style`|`get_dropdown_style`、`set_dropdown_style`|Default `dropdown_list`. Use `combobox_dropdown_style_t` or Python's `combobox_dropdown_style` enumeration.|
|`text`|`get_text`、`set_text`|Currently visible text. Non-empty values in `dropdown_list` must match one item in the collection. `dropdown` allows custom values.|
|`dropped_down`|`get_dropped_down`、`set_dropped_down`|Reads and writes the dropdown layer state; it defaults to collapsed. The control must be interactive, and the item collection must not be empty for it to expand.|
|`selected_index`|`get_selected_index`、`set_selected_index`|0 starts the index; default `-1`. Assigning a valid index makes the item visible.|
|`selected_item`|`get_selected_item`|Read-only, current item string. Returns an empty string when no selection is made.|
|`item_list`|`get_item_list`|Default empty collection. C++ calls `assign` to replace all items, and Python can assign an entire list from the iterable string collection.|
|`row_height`|`get_row_height`、`set_row_height`|Default 32 logical pixels, must be greater than 0. Adjusting the row height of the dropdown items.|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|Inherited from `selection_control`, default false. Native `combobox` follows the base class's judgment of blank areas, and the program clears the selection using `clear_selection()`.|
|`focusable`|`is_focusable`|Read-only, supports keyboard focus. Text is received through the input area in editable mode.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`combobox(name)`|`combobox(name)`|Construct the control.|
|`clear_selection()`|`clear_selection()`|Clear the selection, returning the index to `-1`.|
|`is_blank_at(local_left, local_top)`|`is_blank_at(local_left, local_top)`|Inherited blank area query. Native `combobox` follows the base class implementation, returning false.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_dropdown_style_changed`|`event_args_t`|The mode has actually changed. When switching back to `dropdown_list`, the custom non-matching text will be cleared.|
|`on_text_changed`|`event_args_t`|The displayed text has actually changed. Use the callback source to read the latest `text`.|
|`on_text_input`|`text_input_event_args_t`|Text input in the editable mode includes `text` and `handled`.|
|`on_item_list_changed`|`event_args_t`|The collection content has actually changed. Read `item_list` again and check the current selection.|
|`on_selected_index_changed`|`event_args_t`|`selected_index` has actually changed.|
|`on_selection_changed`|`event_args_t`|The selected index has actually changed. The changes in the displayed text are reported by `on_text_changed`.|
|`on_row_height_changed`|`event_args_t`|The line height has changed.|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|The selection switch changes when clicking on the blank space.|

## Independent routine

Run the "synchronization cycle". After expansion, select "every 15 minutes", and the status text will be updated to the selected cycle. The examples only accept the listed selections based on business enumeration.

Prepare, build, and install](/en/basics/01_install_and_setup) by pressing [. The following command is executed in the x64 developer CMD at the root directory of the tutorial repository. Change the example SDK path to the actual installation location.

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/combobox/cpp -B .work/example_combobox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_combobox --config Release
.work\example_combobox\Release\tutorial_combobox.exe
```

The Visual Studio generator places the executable file in the `Release` subdirectory. The single-config Ninja generator directly outputs to the build directory.

<<< ../../../../../examples/guide/controls/collection-and-data/combobox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\combobox\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/combobox/python/combobox_demo.py

### Run the effect

The effect of the independent routine of ![combobox on](/images/en/combobox_demo.png)

## Common problems and layout practices

- Fill in `item_list` first, then set `selected_index`, or assign a non-empty value to `dropdown_list.text`. Use `selected_index` or the stable business key when saving the list option.
- When allowing custom input, read `text`. The index `-1` may still correspond to a valid custom string. Save the custom text that needs to be retained before switching back to `dropdown_list`.
- Leave surface space for the dropdown stack. The SDK displays items according to the available area. Insufficient space will reduce the number of visible items; expand `window` and adjust `row_height` if necessary.
- Access `dropped_down` through properties. Monitor `on_selection_changed` or `on_text_changed` when observing the results.
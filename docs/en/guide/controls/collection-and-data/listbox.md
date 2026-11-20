# listbox

`listbox` displays a string group permanently within a fixed area and maintains a single selection. Suitable for file categories, task records, and other interfaces that require direct comparison of adjacent options. Long lists can be scrolled using a scroll bar or the joystick of the alignment control. The selected item and current scroll position serve different purposes.

For inherited general members, refer to the [text style interface,](/en/guide/controls/common-api#text-control), and [string selection and collection interfaces,](/en/guide/controls/common-api#item-control).

## Default appearance

The default collection is empty, with a line height of 30 logical pixels, and the index is `-1`. The screenshot sets the control rectangle, retaining the default border and background.

![listbox default appearance:](/images/en/listbox_default.png)

## Property comparison

The left side uses a default line height of 30, selecting the second item. The right side changes the line height to 42 and selects the last item; the SDK automatically scrolls to show the item. Both sides have 8 items, with a scroll bar and selection highlights for easy viewing and selection.

![listbox property comparison:](/images/en/listbox_comparison.png)

## Interface reference

Property names in the Python usage table. C++ is read and written through corresponding methods, and uses `control_base &source` and type references in the table to subscribe to events. `event_args_t` without additional fields indicates that the state has been updated, and the callback reads the new value through `source`. The Python event type names are omitted for `_t`.

### Property

|Property|C++|Types, default values, and uses|
|---|---|---|
|`selected_index`|`get_selected_index`、`set_selected_index`|0 starts the index; default `-1`. Assigning a valid index makes the item visible.|
|`selected_item`|`get_selected_item`|Read-only, current item string. Returns an empty string when no selection is made.|
|`item_list`|`get_item_list`|Default empty collection. C++ calls `assign` to replace all items, and Python can assign an entire list from the iterable string collection.|
|`row_height`|`get_row_height`、`set_row_height`|Default 30 logical pixels, must be greater than 0.|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|Default false. When enabled, it allows clearing selections by hitting the blank area of the control item area.|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`|Read-only, determined based on the number of items and the actual viewport.|
|`focusable`|`is_focusable`|Read-only, supports keyboard navigation.|
|`visible`、`enabled`|`set_visible`、`set_enabled`|Inherited read/write switch; hiding or disabling it also ends the ongoing scroll bar dragging.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`listbox(name)`|`listbox(name)`|Construct the control.|
|`clear_selection()`|`clear_selection()`|Clear the selection, returning the index to `-1`.|
|`is_blank_at(local_left, local_top)`|`is_blank_at(local_left, local_top)`|Determines whether the click point is in the blank area of the item area based on local coordinates.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_item_list_changed`|`event_args_t`|The collection content has actually changed. Read `item_list` again and check the current selection.|
|`on_selected_index_changed`|`event_args_t`|`selected_index` has actually changed.|
|`on_selection_changed`|`event_args_t`|The actual index changes when selected. After replacing the collection, the current item can also be read through `on_item_list_changed`.|
|`on_row_height_changed`|`event_args_t`|The line height has changed.|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|The selection switch changes when clicking on the blank space.|

## Independent routine

“Sync Task” loads 8 items. Clicking the third item “Sync Image” updates the status text. Scroll down to view the last item, and use the direction keys to change the selection.

Prepare, build, and install](/en/basics/01_install_and_setup) by pressing [. The following command is executed in the x64 developer CMD at the root directory of the tutorial repository. Change the example SDK path to the actual installation location.

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/listbox/cpp -B .work/example_listbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_listbox --config Release
.work\example_listbox\Release\tutorial_listbox.exe
```

The Visual Studio generator places the executable file in the `Release` subdirectory. The single-config Ninja generator directly outputs to the build directory.

<<< ../../../../../examples/guide/controls/collection-and-data/listbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\listbox\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/listbox/python/listbox_demo.py

### Run the effect

![listbox independent routine effect:](/images/en/listbox_demo.png)

## Common problems and layout practices

- The viewport height starts from integer multiples of the line height. When the font size increases, the line height increases accordingly to avoid text edge rubbing or showing part of the next line at the same time.
- Use `selected_index >= 0` to determine if a selection exists. An empty string can also be an item; checking `selected_item` separately cannot distinguish between the two cases.
- The scroll position is maintained by the control internally. To locate a specific item, you can assign the corresponding index to `selected_index`.
- When columns, icons, or data objects are needed, `listview` or `grid` can be used in the application.
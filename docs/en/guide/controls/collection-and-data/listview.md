# listview

`listview` presents a group of object records in multiple columns. Each `listview_column` describes the column header and logical pixel width, while `listview_item` contains several string cells and optional icons. The list is responsible for scrolling, selection, column width dragging, and row interactions. See [text style interface for inherited members;](/en/guide/controls/common-api#text-control) for other details.

## Default appearance

The default column set and item set are empty. The row height is 30 pixels, and the header height is 32 pixels. The selection index is `-1`, and multiple selections are disabled.

![listview default appearance](/images/en/listview_default.png)

## Property comparison

The left side uses the default column width and single selection. The right side widens the task columns, increases the row height, and enables multiple selections, selecting the first and third records.

![listview property comparison](/images/en/listview_comparison.png)

## Interface reference

C++ reads and writes attributes using the methods in the table. In Python, access is done through attributes with the same name. Callbacks receive `source` and `event`. Each strong-type parameter in the table inherits from `event_args_t`; basic parameters do not have additional fields. Python type names are omitted in `_t`.

### Property

|Property|C++ access methods|Types, default values, and uses|
|---|---|---|
|`column_list`、`item_list`|`get_column_list`、`get_item_list`|Operable column and row sets. Python supports overall assignment, using `assign` for C++.|
|`selected_index`|`get_selected_index`、`set_selected_index`|Main selection index, default `-1`.|
|`selected_item`|`get_selected_item`、`set_selected_item`|Main selection object, empty selection is `None` or `nullptr`.|
|`selected_item_list`|`get_selected_item_list`|Read-only, reads the currently selected object.|
|`multi_select`|`get_multi_select`、`set_multi_select`|Boolean value, default false. Enabling supports extended selection and switching selections.|
|`row_height`、`header_height`|`get_row_height`、`set_row_height`、`get_header_height`、`set_header_height`|Default values are 30 and 32 respectively, set in positive logical pixels.|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|`get_visible_row_count`、`get_vertical_scrollbar_visible`、`get_horizontal_scrollbar_visible`|Read-only, queries the number of visible rows after calculation and the scroll bar status.|
|`focusable`|`is_focusable`|Read-only, supports keyboard navigation.|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|Inherited blank click strategy, default false.|

### Method

|Method|Purpose|
|---|---|
|`listview(name)`|Construct a multi-column list.|
|`select_item(index,extend=False,toggle=False)`|Selection index, selectable or switchable.|
|`clear_selection()`|Clear the selection area.|
|`is_blank_at(local_left,local_top)`|Determine the blank item area based on the control's local coordinates.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_column_list_changed`、`on_column_width_changed`、`on_column_click`|`listview_column_event_args_t`|Click on the column set, column width, or header, and locate the columns using `column` and `index`.|
|`on_item_list_changed`、`on_row_double_click`|`listview_item_event_args_t`|Row set or content changes, double-click on rows, and locate using `item` and `index`. Set operations may only carry changes in the set.|
|`on_selection_changed`|`event_args_t`|Read the selection attribute after the main item or selected set changes.|
|`on_row_height_changed`、`on_header_height_changed`|`event_args_t`|Two types of height changes.|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|Inherited blank selection strategy changes.|

## listview_column and listview_item

|Type|Properties or methods|Purpose|
|---|---|---|
|`listview_column`|`listview_column(text="", width=100)`|Create a column description.|
|`listview_column`|`text`, `width`, and C++ use their respective `get_` and `set_`.|Modify the title and width of the surviving column objects.|
|`listview_item`|`listview_item(cell_list=[], icon=None, tag="")`|Create a single-row string cell that can be associated with images and business markers.|
|`listview_item`|`cell_list`、`get_cell_list()`|Edit the single-row string. Access by column index.|
|`listview_item`|`icon`, `tag`, and C++ use their respective `get_` and `set_`.|Icons are used in the first column of the list, and `tag` is used to save business identifiers.|

Both types of collections support reading, appending, inserting, removing, and clearing by index. C++ uses shared objects to establish ownership, with Python operations accessing the same collection.

## Independent routine

Select "Synchronize Audio", and the status area displays the current record. Column titles, row objects, and selection status are updated individually.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Execute the command in the x64 Developer CMD of the tutorial root directory, and replace the SDK installation path in the example.

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/listview/cpp -B .work/example_listview -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_listview --config Release
.work\example_listview\Release\tutorial_listview.exe
```

When using a single-configured Ninja, run the executable directly from the build directory.

<<< ../../../../../examples/guide/controls/collection-and-data/listview/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\listview\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/listview/python/listview_demo.py

### Run the effect

The independent execution of ![listview has an effect similar to](/images/en/listview_demo.png).

## Common problems and layout practices

- Use a clear column width and leave space for the scroll bar. When displaying longer local columns, adjust the column width rather than simply widening the entire list.
- Sorting can trigger a re arrangement of the application through `on_column_click`. Saving row objects or business markers may cause the index to change with sorting.
- Interfaces that require typed editing and verification can use [grid](./grid).
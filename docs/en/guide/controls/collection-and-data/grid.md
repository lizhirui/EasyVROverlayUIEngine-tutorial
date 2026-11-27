# grid

`grid` is responsible for selecting, editing, and verifying typed tables, rows, or cells. A small number of values can be directly stored in the control, or application data can be associated through reading and writing callbacks. Before editing is completed, the editing buffer and submitted values are maintained separately. For inherited members, see the [text style interface and](/en/guide/controls/common-api#text-control).

## Default appearance

The default column collection is empty, with 0 rows. The `cell` selection mode is used, with no initial selection. The default border, background, and initial state are retained in the diagram.

![grid default appearance](/images/en/grid_default.png)

## Property comparison

The left side shows a whole row selection and activation of `read_only`. The right side shows cell selection, with the first row's values being edited. Data can still be selected and viewed in read-only mode.

![grid attribute comparison](/images/en/grid_comparison.png)

## Interface reference

C++ reads and writes attributes using the methods in the table. In Python, access is done through attributes with the same name. Callbacks receive `source` and `event`. Each strong-type parameter in the table inherits from `event_args_t`; basic parameters do not have additional fields. Python type names are omitted in `_t`.

### Property

|Property|C++ access methods|Types, default values, and uses|
|---|---|---|
|`column_list`|`get_column_list`、`set_column_list`|`grid_column_t` array, with columns containing `text`, `width`, and `editable`. The read list is suitable for overall rewriting, and the width of each column can be updated through `set_column_width`.|
|`row_count`|`get_row_count`、`set_row_count`|Controls the number of rows in the model. When using a data provider, it is determined by the configured data scale.|
|`selection_mode`、`multi_select`|`get_selection_mode`、`set_selection_mode`、`get_multi_select`、`set_multi_select`|Default `cell`, false. Supports `row` and multiple selections.|
|`selected_index`|`get_selected_index`、`set_selected_index`|The index of the main selected row, defaulting to `-1`.|
|`selected_cell_list`|`get_selected_cell_list`|Read-only, list of `grid_cell_t` positions.|
|`row_height`、`header_height`|`get_row_height`、`set_row_height`、`get_header_height`、`set_header_height`|Logical pixel heights of rows and headers, defaulting to 30 and 32 respectively.|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|`get_visible_row_count`、`get_vertical_scrollbar_visible`、`get_horizontal_scrollbar_visible`|Read-only viewport state.|
|`read_only`|`get_read_only`、`set_read_only`|Control-level editing switch, defaulting to false. The `editable` of columns further restricts editing.|
|`editing`、`edit_cell`、`edit_error`|`get_editing`、`get_edit_cell`、`get_edit_error`|Read-only, indicating whether editing is in progress, current coordinates, and error descriptions.|
|`edit_text`|`get_edit_text`、`set_edit_text`|Readable and writable editing buffer, used for text editing paths.|
|`focusable`|`is_focusable`|Read-only, supports keyboard focus.|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|Inherited blank selection strategy.|

### Method

|Method|Purpose|
|---|---|
|`grid(name)`|Constructing tables.|
|`get_cell_value(row,column)`、`set_cell_value(row,column,value)`|Reading and writing typed values in C++. In Python, read or assign values through `item[row, column]`. `grid_value_t` supports strings, `int64_t`, `double`, and `bool`.|
|`set_data_provider(row_count,reader,writer)`、`refresh_data()`|Read and write as needed after attaching a data provider. Update the current display after model changes. Use the reading interface to display when the writer is omitted.|
|`set_cell_renderer(renderer)`、`set_edit_validator(validator)`|Customize drawing and submission verification through callbacks.|
|`get_value_text(value)`|Convert typed values to display text.|
|`get_cell_at(local_left,local_top)`、`get_cell_rectangle(row,column)`|Query between coordinates and cell rectangles.|
|`get_cell_selected(row,column)`、`select_cell(row,column,extend,toggle)`、`clear_selection()`|Check, set, or clear the selection area. Python checks through `is_cell_selected(row, column)`.|
|`is_blank_at(local_left,local_top)`|Query whether local coordinates fall within the blank area of table items.|
|`set_column_width(column,value)`|Modify the logical pixel width of a single column.|
|`begin_edit(row,column)`、`commit_edit()`、`commit_edit(value)`、`cancel_edit()`|Enter, submit, or cancel editing. Check if submission was successful.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_column_list_changed`|`event_args_t`|Changes to the column definition set.|
|`on_column_width_changed`、`on_column_click`|`grid_column_event_args_t`|Obtain column information through `index` and `width`.|
|`on_selection_changed`|`event_args_t`|Read the new selected coordinates.|
|`on_row_height_changed`、`on_header_height_changed`|`event_args_t`|Update the height of rows or headers.|
|`on_cell_double_click`、`on_cell_value_changed`|`grid_cell_event_args_t`|Double-click or change actual values, including `row` and `column`.|
|`on_edit_started`、`on_edit_committed`、`on_edit_cancelled`、`on_edit_failed`|`grid_cell_event_args_t`|Edit lifecycle. Read `error` or `edit_error` if failed.|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|Update the blank selection strategy.|

## Data model and editing

`grid_cell_t` describes two 0-start coordinates: `row` and `column`. `grid_cell_render_t` also carries the rectangle, current value, and states of `selected`, `hovered`, and `editing`. Python corresponds to types `grid_cell`, `grid_column`, and `grid_cell_render`.

|Callback|Python parameters|C++ parameters|
|---|---|---|
|Read data|`reader(row, column)`|`reader(row, column)`|
|Write data|`writer(row, column, value)`|`writer(row, column, value, error)`|
|Verify and submit|`validator(cell, value)`|`validator(cell, value, error)`|
|Draw cells|`renderer(context, cell)`|`renderer(context, cell)`|

Read the cell value returned by the callback. C++ writers and verifiers report results with boolean values, and errors can be returned as the last writable string. Python returns `True` or `None` for success, `False` for refusal, strings with explanations for refusal, and can also return `(accepted, error)`. Specific signatures are found in [, Python API,](/en/reference/python_api), and [C++ API,](/en/reference/cpp_api).

For initial configuration, set the number of columns and rows first, then write to cells. When submitting, convert the text based on the initial type. The application can first verify the changes before updating the business model.

## Independent routine

Double-click the value corresponding to "parallel tasks", enter 6 and submit. The status at the bottom is updated from `on_edit_committed`.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Execute the command in the x64 Developer CMD of the tutorial root directory, and replace the SDK installation path in the example.

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/grid/cpp -B .work/example_grid -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_grid --config Release
.work\example_grid\Release\tutorial_grid.exe
```

When using a single-configured Ninja, run the executable directly from the build directory.

<<< ../../../../../examples/guide/controls/collection-and-data/grid/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\grid\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/grid/python/grid_demo.py

### Run the effect

The independent execution of the ![grid results in](/images/en/grid_demo.png).

## Common problems and layout practices

- The column headers and cell sizes must be such that both text and scroll bars can be displayed properly. When you need to display elements at the same height, first determine the font size, and then choose the row height.
- Data providers may be frequently read during redrawing. Prepare data and cache in advance to avoid blocking the UI thread during reading or rendering callbacks.
- The save success status should be monitored by `on_edit_committed`. Display diagnostics in `on_edit_failed` and keep the content pending editing visible.
# treeview

`treeview` displays data with parent-child relationships, such as workspace directories, task categories, and expandable outlines. The SDK only arranges the nodes in the expanded path into a visible sequence and then renders the corresponding lines based on the viewport. `tree_node` manages business nodes, while `treeview` manages the current selection, scrolling, and input. For inherited members, see the [text style interface](/en/guide/controls/common-api#text-control).

## Default appearance

The root collection is initially empty, the selection is empty, and the line height is 30 logical pixels. When there is no content, the viewport displays the default background and border.

Default appearance of ![treeview:](/images/en/treeview_default.png)

## Property comparison

The left-side root node is collapsed. The right-side displays root nodes with the same name, selects child nodes, and adjusts the foreground color. Indentation and expansion markers indicate the level, and selected lines emphasize the current position.

Comparison of ![treeview properties with](/images/en/treeview_comparison.png)

## Interface reference

C++ reads and writes attributes using the methods in the table. In Python, access is done through attributes with the same name. Callbacks receive `source` and `event`. Each strong-type parameter in the table inherits from `event_args_t`; basic parameters do not have additional fields. Python type names are omitted in `_t`.

### Property

|Property|C++ access methods|Types, default values, and uses|
|---|---|---|
|`node_list`|`get_node_list`|Root node collection, initially empty. Python allows for whole-value assignments; C++ is replaced by the `assign` of the collection.|
|`selected_node`|`get_selected_node`、`set_selected_node`|Readable and writable, initially set to `None` or `nullptr`. When selecting valid nodes, the current tree node object is required.|
|`row_height`|`get_row_height`|Read-only, default 30 logical pixels.|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`|Read-only, calculated based on the number of visible nodes and the viewport.|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|Inherited boolean switch, default false.|
|`focusable`|`is_focusable`|Read-only, allows navigation using direction keys.|

### Method

|Method|Purpose|
|---|---|
|`treeview(name)`|Construct the root container.|
|`clear_selection()`|Clear the current selection.|
|`is_blank_at(local_left,local_top)`|Determine whether the local coordinates of the control fall outside the blank item area of the node lines.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_node_list_changed`|`event_args_t`|Changes in the structure of the node collection.|
|`on_selection_changed`|`tree_node_event_args_t`|Selection changes, accessing new nodes through `node`. When the selection is cleared, the nodes are empty.|
|`on_node_expanded`、`on_node_collapsed`|`tree_node_event_args_t`|Expand or collapse nodes.|
|`on_node_activated`|`tree_node_event_args_t`|Double-click on nodes or activate with the keyboard.|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|Changes in the selection strategy for blank areas.|

## tree_node

|Properties or methods|C++ access methods|Purpose|
|---|---|---|
|`tree_node(text="", expanded=False, tag="")`|`tree_node(text, expanded, tag)`|Construct nodes, initially collapsed.|
|`text`、`tag`|`get_text/set_text`、`get_tag/set_tag`|Set display text and business markers.|
|`expanded`|`get_expanded/set_expanded`|Save the collapsed state, or call `expand()`, `collapse()`.|
|`parent`|`get_parent()`|Read-only, returns the direct parent node. Nodes that are roots or outside the collection return empty.|
|`node_list`|`get_node_list()`|Child node collection. Adjust the structure through `add`, `insert`, `remove`, `clear`, and read by index.|

The `tag` node can store stable business identifiers. The title and expansion status are set separately.

## Independent routine

Run "Task Classification", expand "Synchronous Tasks", and select "Check Report". Choose a callback to read text from `event.node` and update the status.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Execute the command in the x64 Developer CMD of the tutorial root directory, and replace the SDK installation path in the example.

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/treeview/cpp -B .work/example_treeview -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_treeview --config Release
.work\example_treeview\Release\tutorial_treeview.exe
```

When using a single-configured Ninja, run the executable directly from the build directory.

<<< ../../../../../examples/guide/controls/collection-and-data/treeview/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\treeview\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/treeview/python/treeview_demo.py

### Run the effect

The independent routine of ![treeview has achieved results of](/images/en/treeview_demo.png).

## Common problems and layout practices

- First add child nodes to the root node's `node_list`, then add the root node to `treeview`. Maintain a single ownership before adding; when moving nodes, remove them from the original collection first.
- Reserve width for multi-level indentation, expansion markers, and scroll bars. Use short titles; detailed explanations can be placed in another `label`.
- Consider empty selections when processing `on_selection_changed`. `tag` can be used to restore business selections during filtering or refreshing.
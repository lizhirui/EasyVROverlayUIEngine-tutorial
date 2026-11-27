# tabcontrol

`tabcontrol` manages multiple `tabpage` within the same rectangle. The page title comes from the respective `tabpage.text`, while the content is placed in the page's own `control_list`. Only active pages occupy the content area, making them suitable for switching between overview, history, and configuration tasks.

The inherited general members are found in the [container interface](/en/guide/controls/common-api#container-control).

## Default appearance

The `selected_index = -1` of an empty `tabcontrol`. It is automatically selected when the first page is added. The "Overview" and "History" `tabpage` are included in the diagram, with their tab positions set in `top` and default dimensions of 36 logical pixels.

The default appearance of ![tabcontrol for](/images/en/tabcontrol_default.png).

## Property comparison

The left side uses `top` and displays the first page. The right side is changed to `left`; after widening the tab area, the second page is selected. The `text` on the second page is changed from "History" to "Synchronization Record," and the background of the selected tab is updated.

A comparison of the properties of ![tabcontrol with](/images/en/tabcontrol_comparison.png).

## Interface reference

Property names in the Python usage table. C++ is read and written through corresponding methods, and uses `control_base &source` and type references in the table to subscribe to events. `event_args_t` without additional fields indicates that the state has been updated, and the callback reads the new value through `source`. The Python event type names are omitted for `_t`.

### Property

|Property|C++|Types, default values, and uses|
|---|---|---|
|`page_list`|`get_page_list`|An entry for a collection of read-only pages, initially empty. The elements must be `tabpage`.|
|`selected_index`|`get_selected_index`、`set_selected_index`|A signed index, where `-1` indicates unselected. It is automatically selected when the first page is added. Valid indices are `-1` or the 0-based index of existing pages.|
|`selected_page`|`get_selected_page`|Read-only. When no page is selected, Python returns `None`, and C++ returns `nullptr`.|
|`tab_position`|`get_tab_position`、`set_tab_position`|`top`, `bottom`, `left`, `right`, with default `top`.|
|`tab_size`|`get_tab_size`、`set_tab_size`|A positive integer, defaulting to 36 logical pixels. The top and bottom correspond to the height of the corresponding tabs, and the left and right correspond to the width of the corresponding tabs.|
|`tab_font`|`get_tab_font`、`set_tab_font`|The font for the tab title inherits the default values from the SDK font.|
|`tab_foreground_color`、`tab_background_color`|`get_tab_foreground_color`、`set_tab_foreground_color`、`get_tab_background_color`、`set_tab_background_color`|The text color and background color for regular tabs.|
|`selected_tab_foreground_color`、`selected_tab_background_color`|`get_selected_tab_foreground_color`、`set_selected_tab_foreground_color`、`get_selected_tab_background_color`、`set_selected_tab_background_color`|The text color and background color for selected tabs.|
|`page_close_button_visible`|`get_page_close_button_visible`、`set_page_close_button_visible`|Default false. Displays a close entry; the application processes the request when the user triggers it.|
|`focusable`|`is_focusable`|Read-only, supports focus navigation for tabs and scroll entries.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`tabcontrol(name)`|`tabcontrol(name)`|Construct the control.|
|`page_list.add(page)`|`get_page_list().add(page)`|Adding new pages. Inserted using `insert` by index, removed using `remove`, and cleared using `clear`.|
|`page_list[index]`、`page_list[name]`|`get_page_list()[index]`、`get_page_list()[name]`|Accessing `tabpage` by index or name. C++ can also call `get_page(index)` or `get_page(name)`.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_selected_index_changed`、`on_selection_changed`|`event_args_t`|The actual change occurs when the index is selected. After a page is deleted, the same index may point to another page; changes in the collection are observed through page events.|
|`on_tab_position_changed`、`on_tab_size_changed`、`on_tab_font_changed`|`event_args_t`|Changes in tab position, size, or font.|
|`on_tab_foreground_color_changed`、`on_tab_background_color_changed`|`event_args_t`|Color changes for regular tabs.|
|`on_selected_tab_foreground_color_changed`、`on_selected_tab_background_color_changed`|`event_args_t`|Color changes for selected tabs.|
|`on_page_added`、`on_page_removed`、`on_page_text_changed`|`tabpage_event_args_t`|Adding, removing, or changing the title of a page. Parameters `page` and `index` provide the index of the page and the event occurrence.|
|`on_page_close`|`tabpage_event_args_t`|The user requests closure. After confirmation and saving, the application removes the page using `page_list`.|
|`on_page_close_button_visible_changed`|`event_args_t`|The actual change in the tab close entry switch.|

## tabpage

C++’s `tabpage` inherits from `panel`. The Python binding exposes `tabpage` as a derived class of `container_control`.

|Member|C++ or event parameters|Purpose|
|---|---|---|
|`tabpage(name)`|`tabpage(name)`|Construct the page.|
|`text`|`get_text()`、`set_text(value)`|Read and write the display title, defaulting to an empty string.|
|`control_list`|`get_control_list()`|Add the text control for this page.|
|`on_text_changed`|`event_args_t`|Title changes. When the page is associated with `page_list`, the associated `tabcontrol` will receive `on_page_text_changed` with the page and index.|

The page text control is added to the `control_list` of the page, and the page itself is associated with `tabcontrol.page_list` or C++'s `get_page_list()`. The SDK calculates the available content rectangle of the page based on the position and size of the tab. The controls within the page are laid out according to the upper-left corner of that area.

## Independent routine

The “Synchronization Workbench” has two `tabpage`: “Overview” and “History”. By default, the “Overview” is displayed when entering, and the “History” is displayed after clicking. The renderings show the text of the second page and the selected color scheme.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). The following command is executed in the x64 developer CMD at the root directory of the tutorial repository. Change the example SDK path to the actual installation location.

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/tabcontrol/cpp -B .work/example_tabcontrol -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_tabcontrol --config Release
.work\example_tabcontrol\Release\tutorial_tabcontrol.exe
```

The Visual Studio generator places the executable file in the `Release` subdirectory. The single-config Ninja generator directly outputs to the build directory.

<<< ../../../../../examples/guide/controls/layout-and-container/tabcontrol/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\tabcontrol\python\run.cmd
```

<<< ../../../../../examples/guide/controls/layout-and-container/tabcontrol/python/tabcontrol_demo.py

### Run the effect

The independent routine effect of the ![tabcontrol in](/images/en/tabcontrol_demo.png)

## Common problems and layout practices

- Set `selected_index` after adding the page. When deleting a page at any position, refer to the page by object or name to avoid using the old index saved before deletion.
- Place the content control in the corresponding `tabpage`. When the tab size increases, the content area shrinks accordingly. Side tabs need to leave enough width for the complete title and the close entrance.
- Closing the entrance generates a `on_page_close` notification. Decide when to remove it based on the unsaved state of the page, and confirm through `on_page_removed` that the collection has changed.
- Use `tabpage.text` to modify the display title. Business identifiers use constructed names or `tag`.
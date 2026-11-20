# Basic Interface

Each control section lists type-specific members. The following table summarizes the inheritance interfaces used in each example, applicable to C++ and Python. Colors are uniformly represented as `0xRRGGBBAA`, and rectangle sizes are indicated in logical pixels.

## control_base

|Property|C++|Purpose|
|---|---|---|
|`name`、`type`、`id`|`get_name`、`get_type`、`get_id`|Read-only, construction name, control type, and runtime number|
|`tag`|`get_tag`、`set_tag`|Applied-defined string markers|
|`parent`|`get_parent`|Read-only, direct parent object|
|`disposed`|`get_disposed`|Read-only, whether released|

|Method|Purpose|
|---|---|
|`invalidate()`|Request redrawing|
|`dispose()`|Release control-related resources|
|`begin_invoke(callback)`|Pass parameterless callbacks to the corresponding UI thread|

|Event|Parameters and their uses|
|---|---|
|`on_tag_changed`、`on_disposed`|`event_args_t`, indicates changes or release completion|
|`on_property_changed`|`property_changed_event_args_t`, reads changed property names|

## control

|Property|C++|Purpose|
|---|---|---|
|`rect`|`get_rect`、`set_rect`|Logical rectangle, composed of left, top, width, and height|
|`background_color`|`get_background_color`、`set_background_color`|Control background color, displayed according to specific control rules|
|`tooltip_text`|`get_tooltip_text`、`set_tooltip_text`|Hover prompt text, closes prompt with empty string|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|Display and interaction switches|
|`tab_index`|`get_tab_index`、`set_tab_index`|Tab order for focusable controls, initially 0|
|`focusable`、`focused`|`is_focusable`、`get_focused`|Read-only, whether the control can receive focus and whether it currently has focus|
|`absolute_rectangle`|`get_absolute_rectangle`|Read-only, parsed inner rectangle surface|
|`owning_window`|`get_owning_window`|Read-only, belonging to `window`|

|Method|Purpose|
|---|---|
|`show()`、`hide()`|Show or hide the control|
|`focus()`|Request to receive focus|
|`activate()`|Follow programmatic activation path. Event behavior is determined by control type and available status|

|Event|Parameters and their uses|
|---|---|
|`on_tooltip_text_changed`、`on_background_color_changed`、`on_visible_changed`、`on_enabled_changed`、`on_tab_index_changed`|`event_args_t`, corresponding common property actually changes|
|`on_moved`、`on_size_changed`、`on_viewport_changed`|`event_args_t`, changes in position, size, or viewport|
|`on_pointer_enter`、`on_pointer_leave`、`on_pointer_move`、`on_pointer_down`、`on_pointer_up`|`pointer_event_args_t`, pointer entering, leaving, moving, pressing or releasing|
|`on_click`|`event_args_t`, control activation event|
|`on_scroll`|`scroll_event_args_t`, scroll input|
|`on_focus_in`、`on_focus_out`|`event_args_t`, gaining or losing focus|
|`on_key_down`、`on_key_up`|`key_event_args_t`, button pressing or releasing|

## text_control

|Property|C++|Purpose|
|---|---|---|
|`foreground_color`|`get_foreground_color`、`set_foreground_color`|Text foreground color|
|`font`|`get_font`、`set_font`|Font family, font size, bold and italic. Python uses `font`, C++ uses `font_t`|

|Event|Parameters and their uses|
|---|---|
|`on_foreground_color_changed`、`on_font_changed`|`event_args_t`, corresponding style property changes|

## container_control

|Property|C++|Purpose|
|---|---|---|
|`control_list`|`get_control_list`|Read-only collection entry. Modify ownership using `add`, `insert`, `remove`, `clear`|
|`active_item_list`|`get_active_item_list`|Read-only, returns the list of active child controls in the current container|

|Event|Parameters and their uses|
|---|---|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`, contains controls and their positions|

## item_control

`combobox` and `listbox` inherit from `item_control` and `selection_control`. Access `item_collection` through `item_list`. Strings in the collection can be repeated, selected by item index.

|Action|Python|C++|
|---|---|---|
|Append and insert|`add(text)`、`insert(index, text)`|`add(text)`、`insert(index, text)`|
|Remove and clear|`remove(text)`、`remove_at(index)`、`clear()`|`remove(text)`、`remove(index)`、`clear()`|
|Replace all items|Assign a value to `item_list` of the control|`get_item_list().assign(value_list)`|
|Query quantity, empty state, and members|`len(collection)`、`bool(collection)`、`text in collection`|`get_size()`、`is_empty()`、`contains(text)`|
|Access items and find indexes|`collection[index]`、`index_of(text)`|`collection[index]`、`get_item(index)`、`get_index(text)`|

C++ and Python event subscriptions support `+=`, callback reception uses `source` and `event`. Python event parameter type names omit `_t` suffix. Detailed signatures for events and ownership refer to [C++ API](/en/reference/cpp_api) and [Python API](/en/reference/python_api).
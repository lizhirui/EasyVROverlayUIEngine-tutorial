# 基础接口

各控件章节列出类型特有成员。下表集中说明各示例使用的继承接口，适用于C++和Python。颜色统一使用`0xRRGGBBAA`，矩形尺寸以逻辑像素表示。

## control_base

|属性|C++|用途|
|---|---|---|
|`name`、`type`、`id`|`get_name`、`get_type`、`get_id`|只读，构造名称、控件类型与运行时编号|
|`tag`|`get_tag`、`set_tag`|应用定义的字符串标记|
|`parent`|`get_parent`|只读，直接父对象|
|`disposed`|`get_disposed`|只读，是否已释放|

|方法|用途|
|---|---|
|`invalidate()`|请求重新绘制|
|`dispose()`|释放控件相关资源|
|`begin_invoke(callback)`|将无参数回调派发至所属UI线程|

|事件|参数与用途|
|---|---|
|`on_tag_changed`、`on_disposed`|`event_args_t`，标记变化或释放完成|
|`on_property_changed`|`property_changed_event_args_t`，读取变化的属性名称|

## control

|属性|C++|用途|
|---|---|---|
|`rect`|`get_rect`、`set_rect`|逻辑矩形，由左、上、宽、高组成|
|`background_color`|`get_background_color`、`set_background_color`|控件背景色，默认由`render_style`按控件类别分配（如透明容器、输入槽`INPUT_BACKGROUND_COLOR`、窗口`WINDOW_BACKGROUND_COLOR`、按钮/顶栏`CONTROL_BACKGROUND_COLOR`）|
|`tooltip_text`|`get_tooltip_text`、`set_tooltip_text`|悬停提示文字，空字符串关闭提示|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|显示和交互开关|
|`tab_index`|`get_tab_index`、`set_tab_index`|可聚焦控件的Tab顺序，初始为0|
|`focusable`、`focused`|`is_focusable`、`get_focused`|只读，控件可否获得焦点以及当前是否持有焦点|
|`absolute_rectangle`|`get_absolute_rectangle`|只读，相对完整渲染表面左上角的逻辑矩形（窗口自身返回完整表面矩形）|
|`owning_window`|`get_owning_window`|只读，所属的`window`|

|方法|用途|
|---|---|
|`show()`、`hide()`|显示或隐藏控件|
|`focus()`|请求获得焦点|
|`activate()`|走程序化激活路径。事件行为由控件类型及可用状态决定|

|事件|参数与用途|
|---|---|
|`on_tooltip_text_changed`、`on_background_color_changed`、`on_visible_changed`、`on_enabled_changed`、`on_tab_index_changed`|`event_args_t`，对应公共属性实际发生变化|
|`on_moved`、`on_size_changed`、`on_viewport_changed`|`event_args_t`，位置、尺寸或视口变更|
|`on_pointer_enter`、`on_pointer_leave`、`on_pointer_move`、`on_pointer_down`、`on_pointer_up`|`pointer_event_args_t`，指针进入、离开、移动、按下或松开|
|`on_click`|`event_args_t`，控件激活事件|
|`on_scroll`|`scroll_event_args_t`，滚动输入|
|`on_focus_in`、`on_focus_out`|`event_args_t`，获得或失去焦点|
|`on_key_down`、`on_key_up`|`key_event_args_t`，按键按下或松开|

## text_control

|属性|C++|用途|
|---|---|---|
|`foreground_color`|`get_foreground_color`、`set_foreground_color`|文字前景色|
|`font`|`get_font`、`set_font`|字体族、字号、粗体、斜体、下划线（`underline`）与删除线（`strikethrough`）。Python使用`font`，C++使用`font_t`|

|事件|参数与用途|
|---|---|
|`on_foreground_color_changed`、`on_font_changed`|`event_args_t`，相应的样式属性变化|

## container_control

|属性|C++|用途|
|---|---|---|
|`control_list`|`get_control_list`|只读集合入口。用`add`、`insert`、`remove`、`clear`修改归属|
|`active_item_list`|`get_active_item_list`|只读，返回当前容器的活动子控件列表|

|事件|参数与用途|
|---|---|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`，包含控件及其位置|

## item_control

`combobox`和`listbox`继承`item_control`与`selection_control`。通过`item_list`访问`item_collection`。集合中的字符串可以重复，选择以项目索引表示。

|操作|Python|C++|
|---|---|---|
|追加与插入|`add(text)`、`insert(index, text)`|`add(text)`、`insert(index, text)`|
|移除和清空|`remove(text)`、`remove_at(index)`、`clear()`|`remove(text)`、`remove(index)`、`clear()`|
|替换全部项目|对控件的`item_list`整体赋值|`get_item_list().assign(value_list)`|
|查询数量、空状态与成员|`len(collection)`、`bool(collection)`、`text in collection`|`get_size()`、`is_empty()`、`contains(text)`|
|访问项目和查找索引|`collection[index]`、`index_of(text)`|`collection[index]`、`get_item(index)`、`get_index(text)`|

C++和Python的事件订阅均支持`+=`，回调接收`source`与`event`。Python事件参数类型名省略`_t`后缀。事件和所有权的详细签名参见[C++ API](/reference/cpp_api)和[Python API](/reference/python_api)。

# grid

`grid`负责类型化表格、行或单元格选择、编辑与校验。可将少量值直接保存在控件里，也可通过读取和写入回调关联应用数据。编辑完成前，编辑缓冲和已提交值分别维护。 继承成员见[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

默认列集合为空，行数为0，采用`cell`选择模式，初始无选择。图中保留默认边框、背景与初始状态。

![grid默认外观](/images/zh/grid_default.png)

## 属性对比

左侧为整行选择并启用`read_only`。右侧为单元格选择，正在编辑第一行数值。只读状态仍可选择和浏览数据。

![grid属性对比](/images/zh/grid_comparison.png)

## 接口参考

C++用表中的方法读写属性，Python按同名属性访问。回调接收`source`与`event`。表中各强类型参数继承`event_args_t`，基础参数本身没有附加字段。Python类型名省略`_t`。

### 属性

|属性|C++访问方法|类型、默认值与用途|
|---|---|---|
|`column_list`|`get_column_list`、`set_column_list`|`grid_column_t`数组，列含`text`、`width`、`editable`。读取后的列表适合整体回写，单列宽度可通过`set_column_width`更新。|
|`row_count`|`get_row_count`、`set_row_count`|控制模型的行数。使用数据提供者时由配置的数据规模决定。|
|`selection_mode`、`multi_select`|`get_selection_mode`、`set_selection_mode`、`get_multi_select`、`set_multi_select`|默认`cell`、假。支持`row`以及多选。|
|`selected_index`|`get_selected_index`、`set_selected_index`|主选择的行索引，默认`-1`。|
|`selected_cell_list`|`get_selected_cell_list`|只读，`grid_cell_t`位置列表。|
|`row_height`、`header_height`|`get_row_height`、`set_row_height`、`get_header_height`、`set_header_height`|行与表头的逻辑像素高度，默认分别为30和32。|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|`get_visible_row_count`、`get_vertical_scrollbar_visible`、`get_horizontal_scrollbar_visible`|只读视口状态。|
|`read_only`|`get_read_only`、`set_read_only`|控件级编辑开关，默认假。列的`editable`进一步限制编辑。|
|`editing`、`edit_cell`、`edit_error`|`get_editing`、`get_edit_cell`、`get_edit_error`|只读，编辑是否进行、当前坐标和错误说明。|
|`edit_text`|`get_edit_text`、`set_edit_text`|可读写编辑缓冲，用于文字编辑路径。|
|`focusable`|`is_focusable`|只读，支持键盘焦点。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|继承的空白选择策略。|

### 方法

|方法|用途|
|---|---|
|`grid(name)`|构造表格。|
|`get_cell_value(row,column)`、`set_cell_value(row,column,value)`|在C++中读写类型化值。Python通过`item[row, column]`读取或赋值。`grid_value_t`支持字符串、`int64_t`、`double`、`bool`。|
|`set_data_provider(row_count,reader,writer)`、`refresh_data()`|挂接数据提供者后按需读写。模型变化后刷新当前显示。省略写入器时使用读取接口展示。|
|`set_cell_renderer(renderer)`、`set_edit_validator(validator)`|通过回调自定义绘制与提交校验。|
|`get_value_text(value)`|将类型化值转换为显示文本。|
|`get_cell_at(local_left,local_top)`、`get_cell_rectangle(row,column)`|在坐标与单元格矩形之间查询。|
|`get_cell_selected(row,column)`、`select_cell(row,column,extend,toggle)`、`clear_selection()`|检查、设定或清除选区。Python通过`is_cell_selected(row, column)`检查。|
|`is_blank_at(local_left,local_top)`|查询局部坐标是否落在表格项目区空白。|
|`set_column_width(column,value)`|修改单列逻辑像素宽度。|
|`begin_edit(row,column)`、`commit_edit()`、`commit_edit(value)`、`cancel_edit()`|进入、提交或取消编辑。提交返回是否成功。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_column_list_changed`|`event_args_t`|列定义集合变化。|
|`on_column_width_changed`、`on_column_click`|`grid_column_event_args_t`|通过`index`、`width`获取列信息。|
|`on_selection_changed`|`event_args_t`|读取新的选择坐标。|
|`on_row_height_changed`、`on_header_height_changed`|`event_args_t`|行或表头高度更新。|
|`on_cell_double_click`、`on_cell_value_changed`|`grid_cell_event_args_t`|双击或实际值改变，包含`row`和`column`。|
|`on_edit_started`、`on_edit_committed`、`on_edit_cancelled`、`on_edit_failed`|`grid_cell_event_args_t`|编辑生命周期。失败后读取`error`或`edit_error`。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|空白选择策略更新。|

## 数据模型与编辑

`grid_cell_t`描述`row`和`column`两个0起始坐标。`grid_cell_render_t`还携带矩形、当前值与`selected`、`hovered`、`editing`状态。Python对应类型为`grid_cell`、`grid_column`和`grid_cell_render`。

|回调|Python参数|C++参数|
|---|---|---|
|读取数据|`reader(row, column)`|`reader(row, column)`|
|写入数据|`writer(row, column, value)`|`writer(row, column, value, error)`|
|校验提交|`validator(cell, value)`|`validator(cell, value, error)`|
|绘制单元格|`renderer(context, cell)`|`renderer(context, cell)`|

读取回调返回单元格值。C++写入器和校验器通过布尔值报告结果，可用最后的可写字符串返回错误。Python返回`True`或`None`表示成功，`False`表示拒绝，字符串表示带说明的拒绝，也可返回`(accepted, error)`。具体签名见[Python API](/reference/python_api)和[C++ API](/reference/cpp_api)。

首次配置先设置列和行数，再写入单元格。提交时根据初始类型转换编辑文字。应用可先验证修改，再更新业务模型。

## 独立例程

双击“并行任务”对应的值，输入6并提交，底部状态由`on_edit_committed`更新。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程根目录的x64开发者CMD中执行命令，并替换示例中的SDK安装路径。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/grid/cpp -B .work/example_grid -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_grid --config Release
.work\example_grid\Release\tutorial_grid.exe
```

使用单配置Ninja时，从构建目录直接运行可执行文件。

<<< ../../../../examples/guide/controls/collection-and-data/grid/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\grid\python\run.cmd
```

<<< ../../../../examples/guide/controls/collection-and-data/grid/python/grid_demo.py

### 运行效果

![grid独立例程运行效果](/images/zh/grid_demo.png)

## 常见问题与布局实践

- 列标题和单元格尺寸要同时容纳文字与滚动条。需要等高显示时先确定字号，再选择行高。
- 数据提供者可能在重绘时频繁读取。提前准备数据和缓存，避免在读取或渲染回调中阻塞UI线程。
- 保存成功状态应监听`on_edit_committed`。在`on_edit_failed`中显示诊断，并保持待编辑内容可见。

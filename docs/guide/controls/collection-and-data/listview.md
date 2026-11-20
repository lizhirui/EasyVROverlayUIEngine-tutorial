# listview

`listview`用多列呈现一组对象记录。每个`listview_column`描述列标题和逻辑像素宽度，`listview_item`持有若干字符串单元格和可选图标。列表负责滚动、选择、列宽拖动和行交互。 继承成员见[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

默认列集合和项目集合为空，行高30、表头高32逻辑像素，选择索引为`-1`，多选关闭。

![listview默认外观](/images/zh/listview_default.png)

## 属性对比

左侧使用默认列宽和单选。右侧加宽任务列、调高行高并启用多选，同时选中第一、第三条记录。

![listview属性对比](/images/zh/listview_comparison.png)

## 接口参考

C++用表中的方法读写属性，Python按同名属性访问。回调接收`source`与`event`。表中各强类型参数继承`event_args_t`，基础参数本身没有附加字段。Python类型名省略`_t`。

### 属性

|属性|C++访问方法|类型、默认值与用途|
|---|---|---|
|`column_list`、`item_list`|`get_column_list`、`get_item_list`|可操作的列及行集合。Python支持整体赋值，C++使用`assign`。|
|`selected_index`|`get_selected_index`、`set_selected_index`|主选择索引，默认`-1`。|
|`selected_item`|`get_selected_item`、`set_selected_item`|主选择对象，空选择为`None`或`nullptr`。|
|`selected_item_list`|`get_selected_item_list`|只读，读取当前选中的对象。|
|`multi_select`|`get_multi_select`、`set_multi_select`|布尔值，默认假。启用后支持扩展选择和切换选中。|
|`row_height`、`header_height`|`get_row_height`、`set_row_height`、`get_header_height`、`set_header_height`|默认分别为30和32，设置正逻辑像素。|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|`get_visible_row_count`、`get_vertical_scrollbar_visible`、`get_horizontal_scrollbar_visible`|只读，查询计算后的可见行数与滚动条状态。|
|`focusable`|`is_focusable`|只读，支持键盘导航。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|继承的空白点击策略，默认假。|

### 方法

|方法|用途|
|---|---|
|`listview(name)`|构造多列列表。|
|`select_item(index,extend=False,toggle=False)`|选择索引，可扩展或切换选择。|
|`clear_selection()`|清空选区。|
|`is_blank_at(local_left,local_top)`|按控件局部坐标判断项目区空白。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_column_list_changed`、`on_column_width_changed`、`on_column_click`|`listview_column_event_args_t`|列集合、列宽或表头点击，通过`column`和`index`定位列。|
|`on_item_list_changed`、`on_row_double_click`|`listview_item_event_args_t`|行集合或内容变化、行双击，通过`item`和`index`定位。集合操作可能只携带集合变化。|
|`on_selection_changed`|`event_args_t`|主项或选中集合变化后读取选择属性。|
|`on_row_height_changed`、`on_header_height_changed`|`event_args_t`|两类高度变化。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|继承的空白选择策略变化。|

## listview_column与listview_item

|类型|属性或方法|用途|
|---|---|---|
|`listview_column`|`listview_column(text="", width=100)`|创建列描述。|
|`listview_column`|`text`、`width`，C++使用各自的`get_`和`set_`|修改存活列对象的标题和宽度。|
|`listview_item`|`listview_item(cell_list=[], icon=None, tag="")`|创建一行字符串单元格，可关联图像和业务标记。|
|`listview_item`|`cell_list`、`get_cell_list()`|编辑本行字符串。按列索引访问。|
|`listview_item`|`icon`、`tag`，C++使用各自的`get_`和`set_`|图标用于列表首列，`tag`用于保存业务标识。|

两类集合都支持按索引读取及追加、插入、移除、清空。C++使用共享对象建立归属，Python操作同一集合入口。

## 独立例程

选择“同步音频”，状态区显示当前记录。列标题、行对象和选择状态各自更新。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程根目录的x64开发者CMD中执行命令，并替换示例中的SDK安装路径。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/listview/cpp -B .work/example_listview -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_listview --config Release
.work\example_listview\Release\tutorial_listview.exe
```

使用单配置Ninja时，从构建目录直接运行可执行文件。

<<< ../../../../examples/guide/controls/collection-and-data/listview/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\listview\python\run.cmd
```

<<< ../../../../examples/guide/controls/collection-and-data/listview/python/listview_demo.py

### 运行效果

![listview独立例程运行效果](/images/zh/listview_demo.png)

## 常见问题与布局实践

- 使用明确的列宽并留出滚动条。展示较长的局部列时，调整列的宽度而非单纯加宽整个列表。
- 排序可通过`on_column_click`触发应用重排。保存行对象或业务标记，索引可能随排序变化。
- 需要类型化编辑和校验的界面可使用[grid](./grid)。

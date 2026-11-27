# combobox

`combobox`把有限选项压缩到一个输入区域。`dropdown_list`适合只能从预置值选择的配置项，`dropdown`还允许单行自由输入。两种模式共享字符串集合、选择索引和下拉叠层。

继承的通用成员见[文字样式接口](/guide/controls/common-api#text-control)和[字符串选择与集合接口](/guide/controls/common-api#item-control)。

## 默认外观

默认模式是`dropdown_list`，`item_list`为空，`selected_index = -1`，`text`为空，`dropped_down = False`。图中显示关闭的空控件。

![combobox默认外观](/images/zh/combobox_default.png)

## 属性对比

第一行展示`dropdown_list`中的已有选项。第二行切换到`dropdown`，输入集合之外的“每45分钟”，此时索引为`-1`。第三行展示`dropped_down = True`，指针位于当前所选的“每15分钟”。

![combobox属性对比](/images/zh/combobox_comparison.png)

## 接口参考

Python使用表中的属性名。C++通过对应方法读写，并使用`control_base &source`和表中类型的引用订阅事件。无附加字段的`event_args_t`表示状态已更新，回调通过`source`读取新值。Python对应事件类型名省略`_t`。

### 属性

|属性|C++|类型、默认值与用途|
|---|---|---|
|`dropdown_style`|`get_dropdown_style`、`set_dropdown_style`|默认`dropdown_list`。使用`combobox_dropdown_style_t`或Python的`combobox_dropdown_style`枚举。|
|`text`|`get_text`、`set_text`|当前可见文字。`dropdown_list`的非空值必须匹配集合中的一项。`dropdown`允许自定义值。|
|`dropped_down`|`get_dropped_down`、`set_dropped_down`|读写下拉叠层状态，默认收起。控件须可交互且项目集合非空才会展开。|
|`selected_index`|`get_selected_index`、`set_selected_index`|0起始索引，默认`-1`。赋有效索引会使该项进入可见范围。|
|`selected_item`|`get_selected_item`|只读，当前项目字符串。无选择时返回空字符串。|
|`item_list`|`get_item_list`|默认空集合。C++调用`assign`替换全部项目，Python可整体赋可迭代字符串集合中的列表。|
|`row_height`|`get_row_height`、`set_row_height`|默认32逻辑像素，须大于0。调整的是下拉项目行高。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|继承自`selection_control`，默认假。原生`combobox`沿用基类的空白区域判断，程序清除选择使用`clear_selection()`。|
|`focusable`|`is_focusable`|只读，支持键盘焦点。可编辑模式下通过输入区接收文本。|

默认状态下，组合框主体使用`CONTROL_BACKGROUND_COLOR`，弹出列表使用`INPUT_BACKGROUND_COLOR`；显式设置`background_color`时两者共用该颜色（C++派生类可通过受保护的`get_popup_background_color()`读取下拉列表实际背景色）。

### 方法

|Python|C++|用途|
|---|---|---|
|`combobox(name)`|`combobox(name)`|构造控件。|
|`clear_selection()`|`clear_selection()`|清除选择，使索引回到`-1`。|
|`is_blank_at(local_left, local_top)`|`is_blank_at(local_left, local_top)`|继承的空白区域查询。原生`combobox`沿用基类实现，返回假。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_dropdown_style_changed`|`event_args_t`|模式实际改变。切回`dropdown_list`时，自定义非匹配文本会清空。|
|`on_text_changed`|`event_args_t`|显示文字实际变化。使用回调来源读取最新`text`。|
|`on_text_input`|`text_input_event_args_t`|可编辑模式下的文本输入，包含`text`、`handled`。|
|`on_item_list_changed`|`event_args_t`|集合内容实际改变，重新读取`item_list`并检查当前选择。|
|`on_selected_index_changed`|`event_args_t`|`selected_index`实际改变。|
|`on_selection_changed`|`event_args_t`|选中索引实际改变。显示文字变化另由`on_text_changed`报告。|
|`on_row_height_changed`|`event_args_t`|行高改变。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|空白点击清除选择开关改变。|

## 独立例程

运行“同步周期”，展开后选择“每15分钟”，状态文字更新为所选周期。示例依业务枚举只接受已列出的选择。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。以下命令在教程仓库根目录的x64开发者CMD中执行。把示例SDK路径改为实际安装位置。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/combobox/cpp -B .work/example_combobox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_combobox --config Release
.work\example_combobox\Release\tutorial_combobox.exe
```

Visual Studio生成器把可执行文件放在`Release`子目录。单配置Ninja生成器直接输出到构建目录。

<<< ../../../../examples/guide/controls/collection-and-data/combobox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\combobox\python\run.cmd
```

<<< ../../../../examples/guide/controls/collection-and-data/combobox/python/combobox_demo.py

### 运行效果

![combobox独立例程效果](/images/zh/combobox_demo.png)

## 常见问题与布局实践

- 先填入`item_list`再设置`selected_index`或给`dropdown_list.text`赋非空值。保存列表选项时使用`selected_index`或稳定业务键。
- 允许自定义输入时读取`text`，索引`-1`仍可能对应有效的自定义字符串。切回`dropdown_list`前先保存需要保留的自定义文本。
- 给下拉叠层留出表面空间。SDK按可用区域显示项目，空间不足会减少可见项目；必要时扩大`window`并调整`row_height`。
- `dropped_down`通过属性访问。需要观察结果时监听`on_selection_changed`或`on_text_changed`。

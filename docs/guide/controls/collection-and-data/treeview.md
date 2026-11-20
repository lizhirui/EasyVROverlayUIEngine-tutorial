# treeview

`treeview`展示具有父子关系的数据，例如工作区目录、任务分类和可展开的大纲。SDK仅把展开路径中的节点排入可见序列，再依据视口绘制对应行。`tree_node`管理业务节点，`treeview`管理当前选择、滚动和输入。 继承成员见[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

根集合初始为空，选择为空，行高为30逻辑像素。无内容时视口显示默认背景和边框。

![treeview默认外观](/images/zh/treeview_default.png)

## 属性对比

左侧根节点折叠。右侧展开同名根节点、选中子节点并调整前景色。缩进和展开标记显示层级，选中行强调当前位置。

![treeview属性对比](/images/zh/treeview_comparison.png)

## 接口参考

C++用表中的方法读写属性，Python按同名属性访问。回调接收`source`与`event`。表中各强类型参数继承`event_args_t`，基础参数本身没有附加字段。Python类型名省略`_t`。

### 属性

|属性|C++访问方法|类型、默认值与用途|
|---|---|---|
|`node_list`|`get_node_list`|根节点集合，初始为空。Python可整体赋值，C++通过集合的`assign`替换。|
|`selected_node`|`get_selected_node`、`set_selected_node`|可读写，初始为`None`或`nullptr`。选择有效节点时需要使用当前树的节点对象。|
|`row_height`|`get_row_height`|只读，默认30逻辑像素。|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`|只读，按可见节点数量与视口计算。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|继承的布尔开关，默认假。|
|`focusable`|`is_focusable`|只读，可使用方向键导航。|

### 方法

|方法|用途|
|---|---|
|`treeview(name)`|构造根容器。|
|`clear_selection()`|清除当前选择。|
|`is_blank_at(local_left,local_top)`|判断控件局部坐标是否落在节点行以外的空白项目区域。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_node_list_changed`|`event_args_t`|节点集合结构变化。|
|`on_selection_changed`|`tree_node_event_args_t`|选择变化，通过`node`访问新节点。清空选择时节点为空。|
|`on_node_expanded`、`on_node_collapsed`|`tree_node_event_args_t`|节点展开或折叠。|
|`on_node_activated`|`tree_node_event_args_t`|节点双击或键盘激活。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|空白区域选择策略变化。|

## tree_node

|属性或方法|C++访问方法|用途|
|---|---|---|
|`tree_node(text="", expanded=False, tag="")`|`tree_node(text, expanded, tag)`|构造节点，初始折叠。|
|`text`、`tag`|`get_text/set_text`、`get_tag/set_tag`|设置显示文本和业务标记。|
|`expanded`|`get_expanded/set_expanded`|保存折叠状态，也可调用`expand()`、`collapse()`。|
|`parent`|`get_parent()`|只读，返回直接父节点。根或脱离集合的节点返回空。|
|`node_list`|`get_node_list()`|子节点集合。通过`add`、`insert`、`remove`、`clear`调整结构，并以索引读取。|

节点的`tag`可保存稳定业务标识。标题和展开状态分别设置。

## 独立例程

运行“任务分类”，展开“同步任务”并选择“检查报告”。选择回调从`event.node`读取文本并更新状态。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程根目录的x64开发者CMD中执行命令，并替换示例中的SDK安装路径。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/treeview/cpp -B .work/example_treeview -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_treeview --config Release
.work\example_treeview\Release\tutorial_treeview.exe
```

使用单配置Ninja时，从构建目录直接运行可执行文件。

<<< ../../../../examples/guide/controls/collection-and-data/treeview/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\treeview\python\run.cmd
```

<<< ../../../../examples/guide/controls/collection-and-data/treeview/python/treeview_demo.py

### 运行效果

![treeview独立例程运行效果](/images/zh/treeview_demo.png)

## 常见问题与布局实践

- 先把子节点加入根节点的`node_list`，再把根节点加入`treeview`。添加之前保持单一归属，移动节点时先从原集合移除。
- 为多层缩进、展开标记和滚动条预留宽度。使用简短的标题，详细说明可放在另一个`label`。
- 处理`on_selection_changed`时考虑空选择。筛选或刷新时可以用`tag`恢复业务选择。

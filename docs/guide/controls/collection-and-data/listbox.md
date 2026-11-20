# listbox

`listbox`在固定区域内常驻显示一组字符串，并维护单个选择。适合文件类别、任务记录和其他需要直接比较相邻选项的界面。长列表通过滚动条或对准控件的手柄摇杆滚动。选中项目和当前滚动位置服务于不同目的。

继承的通用成员见[文字样式接口](/guide/controls/common-api#text-control)和[字符串选择与集合接口](/guide/controls/common-api#item-control)。

## 默认外观

默认集合为空，行高为30逻辑像素，索引为`-1`。截图设置了控件矩形，保留默认边框和背景。

![listbox默认外观](/images/zh/listbox_default.png)

## 属性对比

左侧使用默认行高30，选择第二项。右侧将行高改为42并选择末项，SDK自动滚到能够看到该项的位置。两侧都使用8个项目，滚动条和选中高亮便于观察位置和选择。

![listbox属性对比](/images/zh/listbox_comparison.png)

## 接口参考

Python使用表中的属性名。C++通过对应方法读写，并使用`control_base &source`和表中类型的引用订阅事件。无附加字段的`event_args_t`表示状态已更新，回调通过`source`读取新值。Python对应事件类型名省略`_t`。

### 属性

|属性|C++|类型、默认值与用途|
|---|---|---|
|`selected_index`|`get_selected_index`、`set_selected_index`|0起始索引，默认`-1`。赋有效索引会使该项进入可见范围。|
|`selected_item`|`get_selected_item`|只读，当前项目字符串。无选择时返回空字符串。|
|`item_list`|`get_item_list`|默认空集合。C++调用`assign`替换全部项目，Python可整体赋可迭代字符串集合中的列表。|
|`row_height`|`get_row_height`、`set_row_height`|默认30逻辑像素，须大于0。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|默认假。启用后允许通过命中控件项目区的空白清除选择。|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`|只读，根据项目数量和实际视口确定。|
|`focusable`|`is_focusable`|只读，支持键盘导航。|
|`visible`、`enabled`|`set_visible`、`set_enabled`|继承的读写开关，隐藏或禁用也会结束正在进行的滚动条拖动。|

### 方法

|Python|C++|用途|
|---|---|---|
|`listbox(name)`|`listbox(name)`|构造控件。|
|`clear_selection()`|`clear_selection()`|清除选择，使索引回到`-1`。|
|`is_blank_at(local_left, local_top)`|`is_blank_at(local_left, local_top)`|按局部坐标判断点击点是否是项目区空白。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_item_list_changed`|`event_args_t`|集合内容实际改变，重新读取`item_list`并检查当前选择。|
|`on_selected_index_changed`|`event_args_t`|`selected_index`实际改变。|
|`on_selection_changed`|`event_args_t`|选中索引实际改变。替换集合后也可通过`on_item_list_changed`读取当前项目。|
|`on_row_height_changed`|`event_args_t`|行高改变。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|空白点击清除选择开关改变。|

## 独立例程

“同步任务”装入8个项目。点击第三项“同步图像”，状态文字更新。向下滚动可查看末尾项目，使用方向键也能改变选择。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。以下命令在教程仓库根目录的x64开发者CMD中执行。把示例SDK路径改为实际安装位置。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/listbox/cpp -B .work/example_listbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_listbox --config Release
.work\example_listbox\Release\tutorial_listbox.exe
```

Visual Studio生成器把可执行文件放在`Release`子目录。单配置Ninja生成器直接输出到构建目录。

<<< ../../../../examples/guide/controls/collection-and-data/listbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\listbox\python\run.cmd
```

<<< ../../../../examples/guide/controls/collection-and-data/listbox/python/listbox_demo.py

### 运行效果

![listbox独立例程效果](/images/zh/listbox_demo.png)

## 常见问题与布局实践

- 视口高度以行高的整数倍为起点。增大字体时同步增大行高，避免文字贴边或同时露出下一行的一部分。
- 使用`selected_index >= 0`判定拥有选择。空字符串也可以是项目，单独检查`selected_item`不能区分这两种情况。
- 滚动位置由控件内部维护。要定位特定项目可为`selected_index`赋对应索引。
- 需要列、图标或数据对象时，可在应用中使用`listview`或`grid`。

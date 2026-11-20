# tabcontrol

`tabcontrol`在同一矩形中管理多个`tabpage`。页面标题来自各自的`tabpage.text`，内容放到页面自己的`control_list`中。只有活动页面占用内容区域，适合在概览、历史、配置等任务之间切换。

继承的通用成员见[容器接口](/guide/controls/common-api#container-control)。

## 默认外观

空`tabcontrol`的`selected_index = -1`。加入第一页时自动选择该页。图中加入了“概览”和“历史”两个`tabpage`，页签位置为`top`，尺寸为默认36逻辑像素。

![tabcontrol默认外观](/images/zh/tabcontrol_default.png)

## 属性对比

左侧使用`top`并显示第一页。右侧改为`left`，加宽页签区后选择第二页，把第二页的`text`从“历史”改为“同步记录”，并改变选中页签背景。

![tabcontrol属性对比](/images/zh/tabcontrol_comparison.png)

## 接口参考

Python使用表中的属性名。C++通过对应方法读写，并使用`control_base &source`和表中类型的引用订阅事件。无附加字段的`event_args_t`表示状态已更新，回调通过`source`读取新值。Python对应事件类型名省略`_t`。

### 属性

|属性|C++|类型、默认值与用途|
|---|---|---|
|`page_list`|`get_page_list`|只读页面集合入口，初始为空。元素必须是`tabpage`。|
|`selected_index`|`get_selected_index`、`set_selected_index`|有符号索引，`-1`表示未选。加入第一页自动选中。合法索引为`-1`或现有页面的0起始索引。|
|`selected_page`|`get_selected_page`|只读。没有选中页时，Python为`None`，C++为`nullptr`。|
|`tab_position`|`get_tab_position`、`set_tab_position`|`top`、`bottom`、`left`、`right`，默认`top`。|
|`tab_size`|`get_tab_size`、`set_tab_size`|正整数，默认为36逻辑像素。顶部与底部对应页签高度，左侧与右侧对应页签宽度。|
|`tab_font`|`get_tab_font`、`set_tab_font`|页签标题字体，继承SDK字体默认值。|
|`tab_foreground_color`、`tab_background_color`|`get_tab_foreground_color`、`set_tab_foreground_color`、`get_tab_background_color`、`set_tab_background_color`|普通页签的文字色与背景色。|
|`selected_tab_foreground_color`、`selected_tab_background_color`|`get_selected_tab_foreground_color`、`set_selected_tab_foreground_color`、`get_selected_tab_background_color`、`set_selected_tab_background_color`|选中页签的文字色与背景色。|
|`page_close_button_visible`|`get_page_close_button_visible`、`set_page_close_button_visible`|默认假。显示关闭入口，用户触发后由应用处理请求。|
|`focusable`|`is_focusable`|只读，支持页签及滚动入口的焦点导航。|

### 方法

|Python|C++|用途|
|---|---|---|
|`tabcontrol(name)`|`tabcontrol(name)`|构造控件。|
|`page_list.add(page)`|`get_page_list().add(page)`|追加页面。用`insert`按索引插入，用`remove`移出，用`clear`清空。|
|`page_list[index]`、`page_list[name]`|`get_page_list()[index]`、`get_page_list()[name]`|按索引或名称访问`tabpage`。C++也可调用`get_page(index)`或`get_page(name)`。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_selected_index_changed`、`on_selection_changed`|`event_args_t`|选择索引实际变化。删除页面后同一索引可能指向另一页，集合变化通过页面事件观察。|
|`on_tab_position_changed`、`on_tab_size_changed`、`on_tab_font_changed`|`event_args_t`|页签位置、尺寸或字体变化。|
|`on_tab_foreground_color_changed`、`on_tab_background_color_changed`|`event_args_t`|普通页签配色变化。|
|`on_selected_tab_foreground_color_changed`、`on_selected_tab_background_color_changed`|`event_args_t`|选中页签配色变化。|
|`on_page_added`、`on_page_removed`、`on_page_text_changed`|`tabpage_event_args_t`|页加入、移除或标题改变。参数`page`和`index`给出页面及事件发生时的索引。|
|`on_page_close`|`tabpage_event_args_t`|用户提出关闭请求。确认保存后由应用通过`page_list`移出页面。|
|`on_page_close_button_visible_changed`|`event_args_t`|页签关闭入口开关实际变化。|

## tabpage

C++的`tabpage`继承`panel`。Python绑定将`tabpage`暴露为`container_control`的派生类。

|成员|C++或事件参数|用途|
|---|---|---|
|`tabpage(name)`|`tabpage(name)`|构造页面。|
|`text`|`get_text()`、`set_text(value)`|读写显示标题，默认空字符串。|
|`control_list`|`get_control_list()`|加入该页的正文控件。|
|`on_text_changed`|`event_args_t`|标题变化。页面已加入`page_list`时，所属`tabcontrol`也会收到带页面和索引的`on_page_text_changed`。|

页面正文控件加入页面的`control_list`，页面本身加入`tabcontrol.page_list`或C++的`get_page_list()`。SDK按照页签的位置和尺寸计算页面的可用内容矩形。页面内的控件按该区域的左上角布局。

## 独立例程

“同步工作台”有“概览”和“历史”两个`tabpage`。进入后默认显示“概览”，点击“历史”后显示最近一次同步结果。效果图展示第二页的正文和选中配色。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。以下命令在教程仓库根目录的x64开发者CMD中执行。把示例SDK路径改为实际安装位置。

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/tabcontrol/cpp -B .work/example_tabcontrol -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_tabcontrol --config Release
.work\example_tabcontrol\Release\tutorial_tabcontrol.exe
```

Visual Studio生成器把可执行文件放在`Release`子目录。单配置Ninja生成器直接输出到构建目录。

<<< ../../../../examples/guide/controls/layout-and-container/tabcontrol/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\tabcontrol\python\run.cmd
```

<<< ../../../../examples/guide/controls/layout-and-container/tabcontrol/python/tabcontrol_demo.py

### 运行效果

![tabcontrol独立例程效果](/images/zh/tabcontrol_demo.png)

## 常见问题与布局实践

- 添加页面后再设置`selected_index`。要删除任意位置的页面时，通过对象或名称引用页面，避免使用删除前保存的旧索引。
- 把内容控件放入对应`tabpage`。页签尺寸增大时内容区域相应缩小，侧边页签需要为完整标题和关闭入口留出宽度。
- 关闭入口产生`on_page_close`通知。根据页面的未保存状态决定何时移出，并通过`on_page_removed`确认集合已经变化。
- 使用`tabpage.text`修改显示标题，业务标识使用构造名称或`tag`。

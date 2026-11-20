# textbox

`textbox`用于单行名称、短语或可换行备注。它提供光标、选择、复制、撤销与重做，并在满足输入条件时通过SDK接入IME和layout。

继承[公共控件接口](/guide/controls/common-api#control)和[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

默认单行、可选择、可编辑，两个滚动条开关均为假。截图填入示例文字。

![textbox默认外观](/images/zh/textbox_default.png)

## 属性对比

从上至下是默认、`read_only`、`enabled = False`、多行与纵向滚动条。`read_only`保留正常文字配色和选择能力，禁用状态会降低文字亮度。当前SDK的`textbox`没有`password`遮罩属性，有敏感输入需求时应使用具备密码处理能力的入口。

![textbox属性对比](/images/zh/textbox_comparison.png)

## 接口参考

C++属性通过表中的访问方法读写，Python通过同名属性访问。表中的事件参数采用C++类型名，Python对应类型省略`_t`后缀。公共成员见[基础接口](/guide/controls/common-api)。

### 属性

|属性|C++|用途与默认值|
|---|---|---|
|`text`|`get_text`、`set_text`|文本，初始为空。赋值应用多行与长度限制。|
|`read_only`|`get_read_only`、`set_read_only`|初始为假。启用后保留光标、选择和复制，阻止用户更改文本。|
|`selectable`|`get_selectable`、`set_selectable`|初始为真。关闭后停用文本选择和编辑路径，控件仍可获得焦点。|
|`multiline`|`get_multiline`、`set_multiline`|初始为假。启用后保留换行并支持Enter换行。|
|`horizontal_scrollbar_visible`、`vertical_scrollbar_visible`|`get_horizontal_scrollbar_visible`、`set_horizontal_scrollbar_visible`、`get_vertical_scrollbar_visible`、`set_vertical_scrollbar_visible`|初始均为假。分别控制横向和纵向滚动条。|
|`max_length`|`get_max_length`、`set_max_length`|文本码点数量上限，默认0表示无限制。|
|`selection_start`、`selection_length`|`get_selection_start`、`set_selection_start`、`get_selection_length`、`set_selection_length`|选区起点和长度，以码点索引表示，初始均为0。|
|`selected_text`|`get_selected_text`、`set_selected_text`|当前选区文本，初始为空。赋值会由程序替换选区，也可用于更新只读字段。|
|`can_undo`、`can_redo`|`get_can_undo`、`get_can_redo`|只读，是否有可执行的撤销或重做记录。|

### 方法

|Python|C++|用途|
|---|---|---|
|`textbox(name)`|`textbox(name)`|创建一个`textbox`。|
|`select(start,length=0)`|`select(start,length=0u)`|设置有效选区，长度0表示移动插入位置。|
|`undo()`、`redo()`|`undo()`、`redo()`|撤销或重做一次编辑，返回是否成功。|

### 事件

|事件|触发条件与参数|
|---|---|
|`on_text_changed`、`on_read_only_changed`、`on_selectable_changed`|文字或对应开关实际改变，参数为`event_args_t`。|
|`on_selection_changed`、`on_max_length_changed`、`on_multiline_changed`|选区、长度上限或多行设置变化，参数为`event_args_t`。|
|`on_horizontal_scrollbar_visible_changed`、`on_vertical_scrollbar_visible_changed`|对应滚动条开关变化，参数为`event_args_t`。|
|`on_text_input`|文本输入通知，参数为`text_input_event_args_t`。|

## 独立例程

运行后编辑任意一行，观察状态文字更新。单击“全选备注”会请求`textbox`焦点，并选中字段文本。效果图展示全选后的高亮。

先按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程仓库根目录打开已配置MSVC的x64 CMD，使用实际安装的SDK路径。

### C++

```bat
cmake -S examples/guide/controls/window-and-text/textbox/cpp -B .work/example_textbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_textbox --config Release
.work\example_textbox\Release\tutorial_textbox.exe
```

上面的可执行文件路径对应Visual Studio生成器。使用单配置Ninja时，可执行文件直接位于构建目录。

<<< ../../../../examples/guide/controls/window-and-text/textbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\textbox\python\run.cmd
```

<<< ../../../../examples/guide/controls/window-and-text/textbox/python/textbox_demo.py

### 运行效果

![textbox独立例程运行效果](/images/zh/textbox_demo.png)

## 常见问题与实践

- 先设置`multiline`再给`text`赋初始内容。单行模式会移除换行，CRLF和CR在编辑器内部统一为LF。
- 程序更新、交互编辑和替换选区都会遵守长度与文本边界。分组字符的边界可能包含多个码点。
- 查看和复制用`read_only`，只显示文字用`label`，暂时阻止交互用`enabled = False`。
- 处理业务侧的最终文字使用`on_text_changed`并读取`text`。多行输入不要把每次Enter都解释成提交。

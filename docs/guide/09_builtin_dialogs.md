# 内建对话框

EasyVRUI提供`messagebox`、`inputbox`、`file_open_dialog`、`file_save_dialog`、`color_dialog`和`font_dialog`。这些函数同步返回结果，在等待中继续分派同一个UI线程的消息。传入当前`window`作为`owner`，可以把确认操作与其直接所有者关联。

## 模态调用与结果

调用`dialog.show_dialog(owner)`时，SDK显示一个尚未显示且尚未关闭的`window`，约束直接所有者的交互，并在本线程运行嵌套消息循环。调用本身直到对话框结束才返回。其他待分派的消息及`begin_invoke()`回调仍能运行，因而调用期间可能重入应用代码。详细的队列处理见[强类型事件与多线程调度](/guide/07_events_dialogs_threading)。

`dialog_result_t`包含`none`、`ok`、`cancel`、`abort`、`retry`、`ignore`、`yes`、`no`。Python枚举为`dialog_result`。窗口进入模态时重置为`none`。给`dialog_result`赋有效结果会触发关闭流程，标题栏关闭通常得到`cancel`。应用应检查结果后再提交业务改动。

```cpp
auto dialog = make_shared<easyvrui::window>(U"window_confirm");
auto button_accept = make_shared<easyvrui::button>(U"button_accept");
button_accept->set_rect({40u, 96u, 180u, 46u});
button_accept->set_text(U"确定");
button_accept->on_click += [owner = dialog.get()](easyvrui::control_base &, easyvrui::event_args_t &)
{
    owner->set_dialog_result(easyvrui::dialog_result_t::ok);
};
dialog->get_control_list().add(button_accept);
auto result = dialog->show_dialog(*window_main);
```

```python
dialog = window("window_confirm")
button_accept = button("button_accept")
button_accept.rect = rect(40, 96, 180, 46)
button_accept.text = "确定"

def button_accept_click(source, event):
    dialog.dialog_result = dialog_result.ok

button_accept.on_click += button_accept_click
dialog.control_list.add(button_accept)
result = dialog.show_dialog(window_main)
```

以上片段在拥有`window_main`的事件处理函数内运行。再次打开时创建新的对话框实例。

## messagebox

用于确认、提示和错误信息。标准重载按`message`、`title`、`button_set`、`icon`、`default_button`和`owner`传参，返回`dialog_result_t`或Python的`dialog_result`。自定义重载接收`messagebox_button_t`或`messagebox_button`列表，元素使用稳定的`name`和显示用的`text`。该重载返回所选按钮名称，直接取消时返回空字符串。

按钮集支持`ok`、`ok_cancel`、`abort_retry_ignore`、`yes_no_cancel`、`yes_no`和`retry_cancel`。指定默认项时选择当前按钮集内的有效结果。

![messagebox保存确认](/images/zh/dialog_messagebox.png)

## inputbox

用于读取简短文本。参数依次为`prompt`、`title`、`default_text`、`max_length`和`owner`。`max_length = 0`表示不限制码点数。确定时返回文本，取消时C++返回空`optional`，Python返回`None`。用户确认空文本是有效返回，使用有无结果区分取消。

![inputbox报告命名](/images/zh/dialog_inputbox.png)

## file_open_dialog

用于选择已有路径。`initial_directory`和`initial_filename`设置起始位置和名称。通过`filter_list`提供`file_filter_t`或Python的`file_filter`，其成员为`name`和`pattern_list`。过滤器索引从0开始。启用`multi_select`可返回多个路径。取消返回空集合。

`confirm_text`可定制确认按钮标题。可选的`directory_changed`和`filter_changed`回调分别接收路径和索引，适合记录下次打开的选项。

![file_open_dialog选择已有文件](/images/zh/dialog_file_open.png)

## file_save_dialog

用于选取目标路径。目录、名称、过滤器和通知回调与`file_open_dialog`对应。可配置`default_extension`和`confirm_overwrite`。返回值为可选路径，取消时C++为空`optional`，Python为`None`。应用取得确认路径后执行实际写入，并处理写入失败。

![file_save_dialog选择报告路径](/images/zh/dialog_file_save.png)

## color_dialog

用于选取`0xRRGGBBAA`颜色。参数为当前`color`、`title`、重置值`default_color`和`owner`。确认后返回所选颜色，取消返回空`optional`或`None`。对话框内的默认操作将预览恢复到调用者指定的重置值。

![color_dialog显示色相与透明度](/images/zh/dialog_color.png)

## font_dialog

用于选择字体族、字号、粗体及斜体。参数为`font`、`title`、`default_font`和`owner`。C++确认时返回包含`font_t`的`optional`，Python返回`font`，取消返回空值。应用可在获取结果后重设控件矩形以适配字号。

![font_dialog显示字体列表和预览](/images/zh/dialog_font.png)

## 提交与取消

|入口|确定时|取消时|
|---|---|---|
|`show_dialog`|应用设置的结果枚举|`cancel`|
|`messagebox`|结果枚举或自定义按钮名称|依据按钮集返回结果，自定义取消为空字符串|
|`inputbox`|文本，包括空字符串|空可选值|
|`file_open_dialog`|路径集合|空集合|
|`file_save_dialog`、`color_dialog`、`font_dialog`|所选路径、颜色或字体|空可选值|

把对话框打开动作放在UI事件中，等待期间避免持有应用锁。对于删除、覆盖和关闭等操作，在确认分支内提交数据。完整调用签名和默认值参见[C++ API](/reference/cpp_api)或[Python API](/reference/python_api)。

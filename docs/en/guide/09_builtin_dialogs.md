# Built-in Dialog Box

EasyVRUI provides `messagebox`, `inputbox`, `file_open_dialog`, `file_save_dialog`, `color_dialog`, and `font_dialog`. These functions return results synchronously, continuing to dispatch messages from the same UI thread during waiting periods. Passing the current `window` as `owner` can associate the confirmation operation with its direct owner.

## Modal Call and Results

When calling `dialog.show_dialog(owner)`, the SDK displays a `window` that has not yet been shown or closed, restricting interaction with the direct owner and causing a nested message loop to run in this thread. The call returns only when the dialog box ends. Other messages pending dispatch and `begin_invoke()` callbacks can still run, allowing reentrance of application code during the call. For detailed queue handling, see [Strong-Type Events and Multithreaded Scheduling](/en/guide/07_events_dialogs_threading).

`dialog_result_t` includes `none`, `ok`, `cancel`, `abort`, `retry`, `ignore`, `yes`, and `no`. Python enumeration is represented as `dialog_result`. When the window enters a modal state, it resets to `none`. Assigning a valid result to `dialog_result` triggers the close process, and closing the title bar usually results in `cancel`. The application should check the results before submitting business changes.

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

The above segments run within the event handling function that has `window_main`. A new dialog box instance is created when it is reopened.

## messagebox

Used for confirmation, prompts, and error messages. Standard overloads accept parameters via `message`, `title`, `button_set`, `icon`, `default_button`, and `owner`, returning `dialog_result_t` or Python's `dialog_result`. Custom overloads receive lists of `messagebox_button_t` or `messagebox_button`, with elements using stable `name` for display and `text` for other purposes. This overload returns the name of the selected button; an empty string is returned when the button is directly canceled.

The button set supports `ok`, `ok_cancel`, `abort_retry_ignore`, `yes_no_cancel`, `yes_no`, and `retry_cancel`. When specifying a default item, the valid result within the current button set is selected.

![messagebox saves the confirmation](/images/en/dialog_messagebox.png).

## inputbox

Used to read short texts. Parameters are sequentially `prompt`, `title`, `default_text`, `max_length`, and `owner`. `max_length = 0` indicates no limit on the number of code points. A text is returned when confirmed; an empty `optional` is returned in C++, and `None` in Python when canceled. An empty text confirmation is considered a valid return, with cancellation distinguished by the presence or absence of results.

![inputbox reports the named](/images/en/dialog_inputbox.png).

## file_open_dialog

Used to select an existing path. `initial_directory` and `initial_filename` set the starting position and name. `filter_list` provides `file_filter_t` or Python's `file_filter`, with members being `name` and `pattern_list`. Filter index starts at 0. Enabling `multi_select` can return multiple paths. Canceling returns an empty collection.

`confirm_text` allows customization of the confirmation button title. Optional `directory_changed` and `filter_changed` callbacks receive the path and index, respectively, suitable for recording options for the next opening.

![file_open_dialog selects an existing file](/images/en/dialog_file_open.png).

## file_save_dialog

Used to select the target path. Directory, name, filters, and notification callbacks correspond to `file_open_dialog`. `default_extension` and `confirm_overwrite` can be configured. The return value is an optional path; when canceled, it returns `optional` for C++, and `None` for Python. After obtaining the confirmation path, the application performs the actual write operation and handles write failures.

![file_save_dialog Select report path](/images/en/dialog_file_save.png)

## color_dialog

Used to select the color of `0xRRGGBBAA`. Parameters include the current `color`, `title`, reset value `default_color`, and `owner`. After confirmation, the selected color is returned; when canceled, it returns `optional` or `None`. The default operation in the dialog box restores the value to the reset value specified by the caller.

![color_dialog Display hue and transparency](/images/en/dialog_color.png)

## font_dialog

Used to select the font family, size, bold, and italic. Parameters include `font`, `title`, `default_font`, and `owner`. C++ returns `optional` containing `font_t`; Python returns `font`; cancellation returns an empty value. The application can reset the control rectangle after obtaining the result to adapt to the font size.

![font_dialog Display font list and preview](/images/en/dialog_font.png)

## Submit and cancel

|Entry|When confirmed|When canceled|
|---|---|---|
|`show_dialog`|Enumeration of application settings results|`cancel`|
|`messagebox`|Result enumeration or custom button name|Return results based on the button set; custom cancel returns an empty string|
|`inputbox`|Text, including an empty string|Empty optional value|
|`file_open_dialog`|Path set|Empty set|
|`file_save_dialog`、`color_dialog`、`font_dialog`|Selected path, color, or font|Empty optional value|

Place the dialog opening action in UI events; avoid holding the application lock during waiting periods. For operations such as deletion, overwriting, and closing, submit data within the confirmation branch. See the complete call signature and default values in [C++ API,](/en/reference/cpp_api), or [, Python API,](/en/reference/python_api).
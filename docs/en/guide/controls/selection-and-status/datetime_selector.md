# datetime_selector

`datetime_selector` inherits from `control` and provides a Gregorian calendar and second-precision time picker. When collapsed it shows the selected local date and time (or empty when unset). Clicking the input area or pressing `Enter`/`Space` while focused toggles the popup panel.

## Appearance and interaction

- **Upper calendar area**: Switch months with the year/month arrows and click a day to update the value immediately.
- **Lower time area**: Adjust hours, minutes, and seconds via increment/decrement buttons or by scrolling with the controller thumbstick or mouse wheel while pointing at a time column.
- **Action buttons**: `Now` fills the current local time, `Clear` resets the value to empty, and `OK`, `Escape`, focus loss, or clicking outside collapses the popup.

## Properties and events

|Member|Python type|C++ type|Description|
|---|---|---|---|
|`datetime`|`datetime.datetime \| None = None`|`std::optional<datetime_t>` (default `std::nullopt`)|Local wall-clock time (years 1–9999, second precision); Python reads a naive `datetime` with `microsecond == 0`|
|`on_datetime_changed`|`handler(source, event_args)`|`event_container<event_args_t>`|Raised after `on_property_changed` (`datetime`) when the value changes|

In Form Designer, `datetime_selector` is available in the toolbox. Editing `datetime` in the property grid opens a dialog embedding the native `datetime_selector` control itself. `.easyvruifrm` stores `YYYY-MM-DD HH:MM:SS` or `null`, and both C++ and Python exports preserve the initial value.

## Example

::: code-group
```python
from datetime import datetime
from easyvrui import datetime_selector, label, rect, run, window

window_main = window("window_main")
window_main.title = "datetime_selector example"
window_main.rect = rect(0, 0, 480, 220)

selector_start = datetime_selector("datetime_selector_start")
selector_start.rect = rect(24, 24, 260, 40)
selector_start.datetime = datetime(2026, 11, 27, 9, 30, 0)

label_value = label("label_value")
label_value.rect = rect(24, 84, 420, 36)
label_value.text = str(selector_start.datetime)

def selector_start_changed(source, event):
    label_value.text = str(source.datetime) if (source.datetime is not None) else "Unset"

selector_start.on_datetime_changed += selector_start_changed
window_main.control_list.add(selector_start)
window_main.control_list.add(label_value)
window_main.show()
run("datetime_selector_demo")
```

```cpp
#include <easyvrui.h>
#include <memory>

int main()
{
    auto window_main = std::make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"datetime_selector example");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 480u, 220u});

    auto selector_start = std::make_shared<easyvrui::datetime_selector>(U"datetime_selector_start");
    selector_start->set_rect(easyvrui::rectangle_t{24u, 24u, 260u, 40u});
    selector_start->set_datetime(easyvrui::datetime_t{2026, 11u, 27u, 9u, 30u, 0u});

    auto label_value = std::make_shared<easyvrui::label>(U"label_value");
    label_value->set_rect(easyvrui::rectangle_t{24u, 84u, 420u, 36u});
    label_value->set_text(easyvrui::format_datetime(*selector_start->get_datetime()));

    selector_start->on_datetime_changed += [selector_start, label_value](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        auto current = selector_start->get_datetime();
        label_value->set_text(current.has_value() ? easyvrui::format_datetime(*current) : U"Unset");
    };
    window_main->get_control_list().add(selector_start);
    window_main->get_control_list().add(label_value);
    window_main->show();
    easyvrui::run(U"datetime_selector_demo");
    return 0;
}
```
:::

See [Python API reference](/en/reference/python_api) and [C++ API reference](/en/reference/cpp_api) for full signatures.

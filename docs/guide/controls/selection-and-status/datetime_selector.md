# datetime_selector

`datetime_selector`继承`control`，提供公历日期与时分秒（秒精度）的可视化选择控件。收起时显示当前选中的本地日期时间（未选择时为空），点击输入区或聚焦时按`Enter`/`Space`展开选择面板。

## 外观与交互

- **上部日历区**：通过年月箭头切换浏览月份，点选日期后立即更新控件值。
- **下部时间区**：提供时、分、秒三列微调，支持按钮循环增减，激光指向对应时间列时也可通过手柄摇杆或滚轮滚动增减。
- **底部操作栏**：`Now`填入当前本地时间，`Clear`清空为空值，`OK`、按`Escape`、失焦或点击面板外部收起面板。

## 属性与事件

|成员|Python类型|C++类型|说明|
|---|---|---|---|
|`datetime`|`datetime.datetime \| None = None`|`std::optional<datetime_t>`（默认`std::nullopt`）|本地钟面时间（年份1至9999，精确到秒）；Python读取为微秒为0的naive `datetime`|
|`on_datetime_changed`|`handler(source, event_args)`|`event_container<event_args_t>`|有效值变化时在`on_property_changed`（`datetime`）之后触发|

在Form Designer中，`datetime_selector`已加入控件栏；属性面板编辑`datetime`属性时直接弹出内嵌原生`datetime_selector`的编辑对话框，`.easyvruifrm`保存为`YYYY-MM-DD HH:MM:SS`字符串或`null`，导出C++与Python窗体时保留初始值。

## 示例

::: code-group
```python
from datetime import datetime
from easyvrui import datetime_selector, label, rect, run, window

window_main = window("window_main")
window_main.title = "datetime_selector示例"
window_main.rect = rect(0, 0, 480, 220)

selector_start = datetime_selector("datetime_selector_start")
selector_start.rect = rect(24, 24, 260, 40)
selector_start.datetime = datetime(2026, 11, 27, 9, 30, 0)

label_value = label("label_value")
label_value.rect = rect(24, 84, 420, 36)
label_value.text = str(selector_start.datetime)

def selector_start_changed(source, event):
    label_value.text = str(source.datetime) if (source.datetime is not None) else "未选择"

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
    window_main->set_title(U"datetime_selector示例");
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
        label_value->set_text(current.has_value() ? easyvrui::format_datetime(*current) : U"未选择");
    };
    window_main->get_control_list().add(selector_start);
    window_main->get_control_list().add(label_value);
    window_main->show();
    easyvrui::run(U"datetime_selector_demo");
    return 0;
}
```
:::

完整签名见[Python API](/reference/python_api)与[C++ API](/reference/cpp_api)。

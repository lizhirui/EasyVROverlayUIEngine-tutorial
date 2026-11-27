# rich_label

`rich_label`继承`text_control`，用于在单个文本区域内混排多段不同颜色、字号或样式的富文本片段，支持单行与多行显示以及水平、垂直对齐。

## 常用属性与事件

|成员|类型与默认值|说明|
|---|---|---|
|`rich_text_list`|`list[rich_text]` / `std::vector<rich_text_t>`，默认空|按顺序渲染的富文本片段列表|
|`multiline`|`bool = False`|开启时保留换行并在宽度不足时折行|
|`horizontal_alignment`|`horizontal_alignment.left`|水平对齐：`left`、`center`、`right`|
|`vertical_alignment`|`vertical_alignment.center`|垂直对齐：`top`、`center`、`bottom`|
|`on_rich_text_list_changed`|`event_args`|富文本片段列表变化时触发|
|`on_multiline_changed`|`event_args`|多行开关变化时触发|
|`on_horizontal_alignment_changed`|`event_args`|水平对齐方式变化时触发|
|`on_vertical_alignment_changed`|`event_args`|垂直对齐方式变化时触发|

每个`rich_text` / `rich_text_t`片段包含文本`text`、可选颜色`color`（省略时沿用控件`foreground_color`）及可选字体覆盖`font`（`rich_text_font` / `rich_text_font_t`，可单独覆盖`family`、`size`、`bold`、`italic`、`underline`、`strikethrough`）。

## 示例

::: code-group
```python
from easyvrui import font, horizontal_alignment, rect, rich_label, rich_text, rich_text_font, run, window

window_main = window("window_main")
window_main.title = "rich_label示例"
window_main.rect = rect(0, 0, 560, 220)

label_summary = rich_label("rich_label_summary")
label_summary.rect = rect(24, 24, 512, 120)
label_summary.multiline = True
label_summary.horizontal_alignment = horizontal_alignment.left
label_summary.rich_text_list = [
    rich_text("状态："),
    rich_text("在线", color = 0x5EE08BFF, font = rich_text_font(bold = True)),
    rich_text("  延迟 12 ms", color = 0x9BB5D6FF),
]
window_main.control_list.add(label_summary)
window_main.show()
run("rich_label_demo")
```

```cpp
#include <easyvrui.h>
#include <memory>

int main()
{
    auto window_main = std::make_shared<easyvrui::window>(U"window_main");
    window_main->set_title(U"rich_label示例");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 560u, 220u});

    auto label_summary = std::make_shared<easyvrui::rich_label>(U"rich_label_summary");
    label_summary->set_rect(easyvrui::rectangle_t{24u, 24u, 512u, 120u});
    label_summary->set_multiline(true);
    easyvrui::rich_text_font_t bold_override{};
    bold_override.bold = true;
    label_summary->set_rich_text_list({
        easyvrui::rich_text_t{U"状态：", std::nullopt, std::nullopt},
        easyvrui::rich_text_t{U"在线", 0x5EE08BFFu, bold_override},
        easyvrui::rich_text_t{U"  延迟 12 ms", 0x9BB5D6FFu, std::nullopt}
    });
    window_main->get_control_list().add(label_summary);
    window_main->show();
    easyvrui::run(U"rich_label_demo");
    return 0;
}
```
:::

完整签名见[Python API](/reference/python_api)与[C++ API](/reference/cpp_api)。

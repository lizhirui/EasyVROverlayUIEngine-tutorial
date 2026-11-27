# rich_label

`rich_label` inherits from `text_control` and renders a sequence of styled text segments with per-segment color and font overrides inside a single text area. It supports single-line and multiline display as well as horizontal and vertical alignment.

## Common properties and events

|Member|Type and default|Description|
|---|---|---|
|`rich_text_list`|`list[rich_text]` / `std::vector<rich_text_t>`, default empty|Ordered list of rich text segments|
|`multiline`|`bool = False`|Preserves line breaks and wraps text when enabled|
|`horizontal_alignment`|`horizontal_alignment.left`|Horizontal alignment: `left`, `center`, or `right`|
|`vertical_alignment`|`vertical_alignment.center`|Vertical alignment: `top`, `center`, or `bottom`|
|`on_rich_text_list_changed`|`event_args`|Raised when the segment list changes|
|`on_multiline_changed`|`event_args`|Raised when `multiline` changes|
|`on_horizontal_alignment_changed`|`event_args`|Raised when `horizontal_alignment` changes|
|`on_vertical_alignment_changed`|`event_args`|Raised when `vertical_alignment` changes|

Each `rich_text` / `rich_text_t` segment holds `text`, an optional `color` (falls back to `foreground_color`), and an optional `font` override (`rich_text_font` / `rich_text_font_t` for `family`, `size`, `bold`, `italic`, `underline`, and `strikethrough`).

## Example

::: code-group
```python
from easyvrui import horizontal_alignment, rect, rich_label, rich_text, rich_text_font, run, window

window_main = window("window_main")
window_main.title = "rich_label example"
window_main.rect = rect(0, 0, 560, 220)

label_summary = rich_label("rich_label_summary")
label_summary.rect = rect(24, 24, 512, 120)
label_summary.multiline = True
label_summary.horizontal_alignment = horizontal_alignment.left
label_summary.rich_text_list = [
    rich_text("Status: "),
    rich_text("Online", color = 0x5EE08BFF, font = rich_text_font(bold = True)),
    rich_text("  Latency 12 ms", color = 0x9BB5D6FF),
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
    window_main->set_title(U"rich_label example");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 560u, 220u});

    auto label_summary = std::make_shared<easyvrui::rich_label>(U"rich_label_summary");
    label_summary->set_rect(easyvrui::rectangle_t{24u, 24u, 512u, 120u});
    label_summary->set_multiline(true);
    easyvrui::rich_text_font_t bold_override{};
    bold_override.bold = true;
    label_summary->set_rich_text_list({
        easyvrui::rich_text_t{U"Status: ", std::nullopt, std::nullopt},
        easyvrui::rich_text_t{U"Online", 0x5EE08BFFu, bold_override},
        easyvrui::rich_text_t{U"  Latency 12 ms", 0x9BB5D6FFu, std::nullopt}
    });
    window_main->get_control_list().add(label_summary);
    window_main->show();
    easyvrui::run(U"rich_label_demo");
    return 0;
}
```
:::

See [Python API reference](/en/reference/python_api) and [C++ API reference](/en/reference/cpp_api) for full signatures.

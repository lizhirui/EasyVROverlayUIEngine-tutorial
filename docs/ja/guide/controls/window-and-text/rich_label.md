# rich_label

`rich_label`は`text_control`を継承し、1つのテキスト領域内でセグメントごとに異なる色やフォントスタイルを組み合わせて表示します。単一行・複数行表示および水平・垂直方向の配置に対応します。

## 主なプロパティとイベント

|メンバー|型と初期値|説明|
|---|---|---|
|`rich_text_list`|`list[rich_text]` / `std::vector<rich_text_t>`、既定は空|描画順のリッチテキストセグメント一覧|
|`multiline`|`bool = False`|有効時に改行を保持し、幅を超える場合は折り返します|
|`horizontal_alignment`|`horizontal_alignment.left`|水平配置：`left`、`center`、`right`|
|`vertical_alignment`|`vertical_alignment.center`|垂直配置：`top`、`center`、`bottom`|
|`on_rich_text_list_changed`|`event_args`|セグメント一覧が変更されたときに発生|
|`on_multiline_changed`|`event_args`|`multiline`が変更されたときに発生|
|`on_horizontal_alignment_changed`|`event_args`|水平配置が変更されたときに発生|
|`on_vertical_alignment_changed`|`event_args`|垂直配置が変更されたときに発生|

各`rich_text` / `rich_text_t`セグメントは`text`、省略可能な`color`（省略時は`foreground_color`を使用）、および省略可能な`font`上書き（`rich_text_font` / `rich_text_font_t`で`family`、`size`、`bold`、`italic`、`underline`、`strikethrough`を個別指定）を保持します。

## 例

::: code-group
```python
from easyvrui import horizontal_alignment, rect, rich_label, rich_text, rich_text_font, run, window

window_main = window("window_main")
window_main.title = "rich_labelの例"
window_main.rect = rect(0, 0, 560, 220)

label_summary = rich_label("rich_label_summary")
label_summary.rect = rect(24, 24, 512, 120)
label_summary.multiline = True
label_summary.horizontal_alignment = horizontal_alignment.left
label_summary.rich_text_list = [
    rich_text("状態："),
    rich_text("オンライン", color = 0x5EE08BFF, font = rich_text_font(bold = True)),
    rich_text("  遅延 12 ms", color = 0x9BB5D6FF),
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
    window_main->set_title(U"rich_labelの例");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 560u, 220u});

    auto label_summary = std::make_shared<easyvrui::rich_label>(U"rich_label_summary");
    label_summary->set_rect(easyvrui::rectangle_t{24u, 24u, 512u, 120u});
    label_summary->set_multiline(true);
    easyvrui::rich_text_font_t bold_override{};
    bold_override.bold = true;
    label_summary->set_rich_text_list({
        easyvrui::rich_text_t{U"状態：", std::nullopt, std::nullopt},
        easyvrui::rich_text_t{U"オンライン", 0x5EE08BFFu, bold_override},
        easyvrui::rich_text_t{U"  遅延 12 ms", 0x9BB5D6FFu, std::nullopt}
    });
    window_main->get_control_list().add(label_summary);
    window_main->show();
    easyvrui::run(U"rich_label_demo");
    return 0;
}
```
:::

完全なシグネチャは[Python APIリファレンス](/ja/reference/python_api)と[C++ APIリファレンス](/ja/reference/cpp_api)を参照してください。

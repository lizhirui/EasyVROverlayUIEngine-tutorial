# datetime_selector

`datetime_selector`は`control`を継承する、グレゴリオ暦の日付と秒精度の時刻選択コントロールです。折りたたみ時は選択中のローカル日時を表示し（未選択時は空）、入力欄をクリックするかフォーカス中に`Enter`/`Space`を押すと選択パネルを展開します。

## 外観と操作

- **上部カレンダー領域**：年・月矢印で表示月を切り替え、日付をクリックすると即座に値が更新されます。
- **下部時刻領域**：時・分・秒の各列でボタンによる循環増減、または対象列を指しながらコントローラーのスティック／ホイールで増減できます。
- **操作ボタン**：`Now`で現在ローカル時刻を入力、`Clear`で未選択状態にクリア、`OK`・`Escape`・フォーカス喪失・パネル外クリックで閉じます。

## プロパティとイベント

|メンバー|Pythonの型|C++の型|説明|
|---|---|---|---|
|`datetime`|`datetime.datetime \| None = None`|`std::optional<datetime_t>`（既定`std::nullopt`）|ローカル壁時計日時（1～9999年、秒精度）。Python読み取りはマイクロ秒0のnaive `datetime`|
|`on_datetime_changed`|`handler(source, event_args)`|`event_container<event_args_t>`|値変更時に`on_property_changed`（`datetime`）の後に発生|

Form Designerのツールボックスに`datetime_selector`が登録されており、プロパティパネルで`datetime`を編集するとネイティブの`datetime_selector`を埋め込んだ編集ダイアログが開きます。`.easyvruifrm`には`YYYY-MM-DD HH:MM:SS`文字列または`null`として保存され、C++およびPythonのエクスポート時に初期値が保持されます。

## 例

::: code-group
```python
from datetime import datetime
from easyvrui import datetime_selector, label, rect, run, window

window_main = window("window_main")
window_main.title = "datetime_selectorの例"
window_main.rect = rect(0, 0, 480, 220)

selector_start = datetime_selector("datetime_selector_start")
selector_start.rect = rect(24, 24, 260, 40)
selector_start.datetime = datetime(2026, 11, 27, 9, 30, 0)

label_value = label("label_value")
label_value.rect = rect(24, 84, 420, 36)
label_value.text = str(selector_start.datetime)

def selector_start_changed(source, event):
    label_value.text = str(source.datetime) if (source.datetime is not None) else "未選択"

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
    window_main->set_title(U"datetime_selectorの例");
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
        label_value->set_text(current.has_value() ? easyvrui::format_datetime(*current) : U"未選択");
    };
    window_main->get_control_list().add(selector_start);
    window_main->get_control_list().add(label_value);
    window_main->show();
    easyvrui::run(U"datetime_selector_demo");
    return 0;
}
```
:::

完全なシグネチャは[Python APIリファレンス](/ja/reference/python_api)と[C++ APIリファレンス](/ja/reference/cpp_api)を参照してください。

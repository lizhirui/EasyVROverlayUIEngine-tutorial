# 空間配置・カスタム描画・Desktopへの登録

ここまでは組み込みの外観を持つコントロールを使い、既定の`world`を基準にウィンドウを置きました。この章では、`render_context`と`drawing_path`でカスタム描画を実装します。`reference_object`と`curvature`でウィンドウを左手首（`left`）に配置し、`.easyvrui`マニフェストでDesktopに登録します。

---

## 1. `window`の空間配置と`vec3`、`quat`、`pose`、`blank`

`world`は空間に固定します。`head`はヘッドセットに追従し、`body`は体の移動に追従しながら較正時の向きを維持します。`left`と`right`は左右それぞれのコントローラーに追従します。`reference_object`で参照対象を選び、対象からのローカルオフセットをメートルで指定します。トラッキング対象のデバイスと姿勢はSteamVRのランタイムから取得します。

![SteamVRの5種類の空間参照対象の概念図](/images/ja/vr_spatial_anchors.png)

次の図はWARPで描画した設定例です。実際に配置された位置と姿勢は`get_world_transform()`またはPythonの`world_transform`で確認できます。`is_tracking_available()`で参照対象がトラッキング可能かを調べます。

![5種類の空間参照対象の設定ビュー](/images/ja/spatial_anchor_config.png)

### 1. `window`空間と外観属性/メソッド

|属性/メソッド|タイプ（Python / C++）|デフォルト値|読み取り/書き込み|説明と注意事項|
|---|---|---|---|---|
|`reference_object`|`reference_object`（Pythonでは列挙値または文字列も指定可能）|`world`|読み書き|参照対象。`world`は空間固定、`body`は体、`head`はヘッドセット、`left`は左コントローラー、`right`は右コントローラーに追従します。|
|`position`|`vec3` / `vec3_t`|`vec3(0, 0, 0)`|読み書き|参照対象からウィンドウの**左上**までの相対オフセット。単位は**メートル**です。|
|`rotation`|`vec3` / `vec3_t`|`vec3(0, 0, 0)`|読み書き|XYZオイラー角。単位は**度**で、合成順序は`Rz * Ry * Rx`です。|
|`physical_scale`|`float` / `double`|`1.0`|読み書き|物理スケール。正の有限値を指定します。`1.0`のとき、`1`論理ピクセルは`1毫米`に対応します。|
|`physical_width` / `physical_height`|`float` / `double`|計算値|読み取り専用|物理的な幅と高さ（メートル）。幅は`rect.width * physical_scale / 1000.0`です。|
|`curvature`|`float` / `double`|`0.0`|読み書き|円筒面の曲率。単位は`m⁻¹`で、`0`は平面です。`k >= 0`と`k * physical_width < 2π`を満たす必要があります。コントローラーからの操作上限は`160°`です。|
|`startup_position`|`startup_position` / `startup_position_t`|`center`|読み書き|`center`の初回表示では、ヘッドセットまたは呼び出し元のウィンドウの正面に配置します。`position`を指定して手首に固定する場合は`none`に切り替えます。|
|`tracking_mode_set`|`set[reference_object_type]`|5種類すべて|読み書き|タイトルバーの`⊕`で選べるモード。空の`set()`を指定するとボタンを非表示にします。|
|`show_title_bar` / `show_close_button` / `movable` / `resizable` / `curvature_adjustable`|`bool`|すべて`True`|読み書き|タイトルバー、閉じるボタン、つかんで移動する操作、右下の縮尺ハンドル、左下の曲率ハンドルを切り替えます。|
|`reparent(ref, keep_world = False)`|メソッド|—|—|参照対象を切り替えます。`keep_world = True`を指定すると、切り替え時のワールド空間での位置と姿勢を保持します。|
|`center_at_view(distance) -> bool`|メソッド|—|—|現在の視線の正面、`distance`メートル先にウィンドウを中央揃えで配置します。|
|`world_transform`（C++では`get_world_transform()`）|`pose \| None` / `optional<pose_t>`|—|読み取り専用|ウィンドウの**中心**の現在のワールド空間の`pose`です。トラッキングが利用できなければ`None`を返します。|

### 2. `vec3`、`quat`、`pose`、および`blank`

- **`vec3(x, y, z)`**：`+`/`-`/スカラー`*`、`calculate_dot_product`、`calculate_cross_product`、`length`、`normalized`をサポート。
- **`quat(x, y, z, w)`**：デフォルトの単位回転`(0,0,0,1)`、`*`の組み合わせ、`euler`、`rotate(v)`、`slerp(target, t)`、`create_from_euler(angles)`、`create_from_axis_angle(axis, angle)`をサポート。
- **`pose(position, rotation)`**：`a * b`（Pythonでも`a @ b`をサポート）、`inverse`、`matrix`、`transform_point(v)`。
- **`blank(name)`**：`control`から継承された純粋な矩形のプレースホルダオブジェクト（`name`/`rect`とジオメトリ/解放イベントのみ保持、`visible`/`enabled`/`render`などのアクセスは`AttributeError`を投げる）。

---

## 2. `render_context`と`drawing_path`で描画する

`get_rectangle()`でコントロールの描画領域を取得し、正規化したデータからローカル座標を計算します。図のサンプルは、`fill_rounded_rectangle()`で背景を塗り、`draw_line()`でサンプル点を結び、`push_clip()`と`pop_clip()`で描画範囲を制限します。アプリはデータの変化やアニメーションの進行時に`invalidate()`を呼び出します。その後の描画の送信はSDKが調整します。

![カスタムサンプリング折れ線のWARPレンダリング効果](/images/ja/spatial_custom_drawing.png)

`control`を継承し、`render(self, context)`（C++では`render(render_context &context) const override`）をオーバーライドすると、`render_context`で描画できます。

|一般的な方法|用途|
|---|---|
|`context.rectangle` / `get_rectangle(item)`|現在のコントロールで矩形を描画する`(left, top, width, height)`を取得する。|
|`is_hovered(item)` / `is_focused(item)`|ハイライト効果を簡単に表示するために、ハイライトとフォーカス状態を照会する。|
|`fill(rect, color)` / `outline(rect, color, thickness=1.0)`|矩形を塗りつぶすか線で描く（色は`0xRRGGBBAA`整数）。|
|`fill_rounded_rectangle(rect, rx, ry, color)` / `outline_rounded_rectangle(...)`|丸みを帯びた矩形。|
|`fill_circle(cx, cy, r, color)` / `draw_circle(cx, cy, r, color, thickness=1.0)`|円と円の境界を塗りつぶす。|
|`fill_ellipse` / `outline_ellipse` / `draw_line`|楕円と線。|
|`draw_text(text, font, rect, color, center=False)` / `measure(text, font)`|文字を描画し、文字の幅を測定する。|
|`draw_image(img, rect, opacity=1.0)` / `draw_screen(id, rect)`|画像やリアルタイムディスプレイの画面を描画する。|
|`fill_path(path, color)` / `outline_path(path, color, thickness=1.0)`|`drawing_path`ベクターパスを描画する。|
|`push_clip(rect)` / `pop_clip()`|矩形のトリミングとスタック/スタック解除（ペアで呼び出す必要がある）。|

**`drawing_path`**：連鎖呼び出し`move_to(x, y)`、`line_to(x, y)`、`quadratic_to(...)`、`cubic_to(...)`、`arc_to(...)`、`close()`をサポートし、`fill_rule`は`even_odd`または`non_zero`で選択可能。

---

## 3. 左手首の文字盤を作りDesktopに登録する

### 手順1　`control`を継承し、`render_context`と`drawing_path`で文字盤を描く

::: code-group
```python [Python（第1步）]
import math
from easyvrui import control, drawing_path, font, rect, run, window

class wrist_dial_control(control):
    def __init__(self, name):
        super().__init__(name)
        self.label_text = "12:00"
        self.accent_color = 0x38BDF8FF

    def render(self, context):
        left, top, width, height = context.rectangle
        cx = left + (width * 0.5)
        cy = top + (height * 0.5)
        radius = min(width, height) * 0.44
        bg_color = 0x1E3A5FFF if context.is_hovered(self) else 0x0F172AFF
        context.fill_circle(cx, cy, radius, bg_color)
        context.draw_circle(cx, cy, radius, self.accent_color, 3.0)
        pointer = drawing_path()
        pointer.move_to(cx, cy).line_to(cx, cy - (radius * 0.65))
        context.outline_path(pointer, 0xFACC15FF, 3.0)
        context.draw_text(self.label_text, font("Segoe UI", 22, True, False), (left, cy + 12.0, width, 34.0), 0xFFFFFFFF, True)

window_main = window("window_main")
window_main.rect = rect(0, 0, 220, 220)
dial_watch = wrist_dial_control("dial_watch")
dial_watch.rect = rect(0, 0, 220, 220)
window_main.control_list.add(dial_watch)
window_main.show()
run("wrist_watch")
```

```cpp [C++（第1步）]
#include <algorithm>
#include <easyvrui.h>
#include <memory>

using namespace std;

class wrist_dial_control : public easyvrui::control
{
    public:
        explicit wrist_dial_control(const u32string &name) : easyvrui::control(name)
        {
        }

    protected:
        void render(easyvrui::render_context &context) const override
        {
            auto rc = context.get_rectangle(*this);
            double cx = rc.left + (rc.width * 0.5);
            double cy = rc.top + (rc.height * 0.5);
            double radius = min(rc.width, rc.height) * 0.44;
            uint32_t bg = context.is_hovered(*this) ? 0x1E3A5FFFu : 0x0F172AFFu;
            context.fill_circle(cx, cy, radius, bg);
            context.draw_circle(cx, cy, radius, 0x38BDF8FFu, 3.0);
            drawing_path pointer;
            pointer.move_to(cx, cy).line_to(cx, cy - (radius * 0.65));
            context.outline_path(pointer, 0xFACC15FFu, 3.0);
            context.draw_text(U"12:00", easyvrui::font_t{U"Segoe UI", 22u, true, false}, easyvrui::render_rectangle_t{rc.left, cy + 12.0, rc.width, 34.0}, 0xFFFFFFFFu, true);
        }
};

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    auto dial_watch = make_shared<wrist_dial_control>(U"dial_watch");
    dial_watch->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    window_main->get_control_list().add(dial_watch);
    window_main->show();
    easyvrui::run(U"wrist_watch");
    return 0;
}
```
:::

---

### 手順2　左手首（`left`）を基準に文字盤を配置する

`startup_position`を`none`に設定し、タイトルバーを非表示にします。`physical_scale = 0.5`で220×220論理ピクセルを11cm四方に縮め、`curvature = 1.2`で手首に沿うよう緩く曲げます。

::: code-group
```python [Python（第2步新增）]
from easyvrui import reference_object_type, startup_position, vec3

window_main.show_title_bar = False
window_main.startup_position = startup_position.none
window_main.reference_object = reference_object_type.left
window_main.physical_scale = 0.5
window_main.curvature = 1.2
window_main.position = vec3(-0.05, 0.06, 0.08)
window_main.rotation = vec3(-45.0, 20.0, 0.0)
```

```cpp [C++（第2步新增）]
window_main->set_show_title_bar(false);
window_main->set_startup_position(easyvrui::startup_position_t::none);
window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
window_main->set_physical_scale(0.5);
window_main->set_curvature(1.2);
window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});
```
:::

---

### 手順3　クリック時に`reparent(..., keep_world=True)`で手首とワールド空間を切り替える

文字盤をクリックすると、その場のワールド位置を保持したまま手首から切り離します。もう一度クリックすると、左手首に追従する表示に戻ります。

::: code-group
```python [Python（第3步新增）]
def dial_watch_click(source, event):
    if window_main.reference_object.type == reference_object_type.left:
        window_main.reparent(reference_object_type.world, keep_world = True)
        dial_watch.accent_color = 0x4ADE80FF
    else:
        window_main.reference_object = reference_object_type.left
        window_main.position = vec3(-0.05, 0.06, 0.08)
        window_main.rotation = vec3(-45.0, 20.0, 0.0)
        dial_watch.accent_color = 0x38BDF8FF
    dial_watch.invalidate()

dial_watch.on_click += dial_watch_click
```

```cpp [C++（第3步新增）]
dial_watch->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
{
    if(window_main->get_reference_object().type == easyvrui::reference_object_type_t::left)
    {
        window_main->reparent(easyvrui::reference_object_t{easyvrui::reference_object_type_t::world}, true);
    }
    else
    {
        window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
        window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
        window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});
    }
};
```
:::

---

### 手順4　`.easyvrui`マニフェストを作成しDesktopに登録する（リモート接続の4引数）

たとえば、スクリプトとマニフェストを`D:\Tools\EasyVRUI\app\wrist_watch\`に置きます。`launch.script`の基準はマニフェストのディレクトリです。マニフェストの絶対パスをDesktopのユーザー設定の`application_list`に追加してDesktopを更新します。付属する一般アプリのマニフェストは、インストーラーが`app/desktop/config.json`に登録します。両方の登録方法は[アプリマニフェスト](/ja/reference/application_manifest)を参照してください。

```json
{
    "id": "wrist_watch",
    "type": "application",
    "name":
    {
        "zh": "左手腕小表盘",
        "en": "Wrist Watch",
        "ja": "左手首ウォッチ"
    },
    "launch":
    {
        "runtime": "python",
        "script": "wrist_watch.py",
        "argument_list": []
    }
}
```

DesktopがSDKを使ってPythonスクリプトを起動すると、インストール済みの`sdk/api/python/`が子プロセスの`PYTHONPATH`の先頭に追加されます。別のコンピューターのCMDから直接起動するときは、そのコンピューターのSDKのパスを設定し、[リモート接続の引数](/ja/reference/engine_protocol)を渡します。

```cmd
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
python -B "D:\Tools\EasyVRUI\app\wrist_watch\wrist_watch.py" --easyvrui-host=192.168.1.50 --easyvrui-port=49537 --easyvrui-access-credential="你的凭据" --easyvrui-public-key-fingerprint=服务公钥SHA256指纹
```

---

## 4. よくある問題と実装上の注意

1. **`position`が初回表示に反映されない場合は`startup_position`を確認します**。`startup_position`が既定の`center`のとき、Engineは最初の`show()`で中央に配置し、事前に指定した`position`を置き換えます。手首や特定の位置に固定する場合は`startup_position.none`を設定します。
2. **カスタムコントロールのメンバーを変更しても描画が更新されないとき**。SDKが変更を監視するのは組み込みプロパティです。独自に追加したPythonやC++のメンバーを変更したら、`self.invalidate()`を呼び出します。
3. **`curvature * physical_width`は`2π`未満にします**。`physical_scale`または`rect.width`を増やす場合は、現在の曲率で1周以上にならないか確認します。

---

::: details この章の実行できるソースコード
::: code-group
```python [Python（完全版） · wrist_watch.py]
from easyvrui import (control, drawing_path, font, rect, reference_object_type, run, startup_position, vec3, window,)

class wrist_dial_control(control):
    def __init__(self, name):
        super().__init__(name)
        self.label_text = "12:00"
        self.accent_color = 0x38BDF8FF

    def render(self, context):
        left, top, width, height = context.rectangle
        cx = left + (width * 0.5)
        cy = top + (height * 0.5)
        radius = min(width, height) * 0.44
        bg_color = 0x1E3A5FFF if context.is_hovered(self) else 0x0F172AFF
        context.fill_circle(cx, cy, radius, bg_color)
        context.draw_circle(cx, cy, radius, self.accent_color, 3.0)
        pointer = drawing_path()
        pointer.move_to(cx, cy).line_to(cx, cy - (radius * 0.65))
        context.outline_path(pointer, 0xFACC15FF, 3.0)
        context.draw_text(self.label_text, font("Segoe UI", 22, True, False), (left, cy + 12.0, width, 34.0), 0xFFFFFFFF, True,)

def main():
    window_main = window("window_main")
    window_main.rect = rect(0, 0, 220, 220)
    window_main.show_title_bar = False
    window_main.startup_position = startup_position.none
    window_main.reference_object = reference_object_type.left
    window_main.physical_scale = 0.5
    window_main.curvature = 1.2
    window_main.position = vec3(-0.05, 0.06, 0.08)
    window_main.rotation = vec3(-45.0, 20.0, 0.0)
    dial_watch = wrist_dial_control("dial_watch")
    dial_watch.rect = rect(0, 0, 220, 220)

    def dial_watch_click(source, event):
        if window_main.reference_object.type == reference_object_type.left:
            window_main.reparent(reference_object_type.world, keep_world = True)
            dial_watch.accent_color = 0x4ADE80FF
        else:
            window_main.reference_object = reference_object_type.left
            window_main.position = vec3(-0.05, 0.06, 0.08)
            window_main.rotation = vec3(-45.0, 20.0, 0.0)
            dial_watch.accent_color = 0x38BDF8FF

        dial_watch.invalidate()

    dial_watch.on_click += dial_watch_click
    window_main.control_list.add(dial_watch)
    window_main.show()
    run("wrist_watch")

if __name__ == "__main__":
    main()
```

```cpp [C++（完全版） · main.cpp]
#include <algorithm>
#include <easyvrui.h>
#include <memory>

using namespace std;

class wrist_dial_control : public easyvrui::control
{
    public:
        explicit wrist_dial_control(const u32string &name) : easyvrui::control(name)
        {
        }

    protected:
        void render(easyvrui::render_context &context) const override
        {
            auto rc = context.get_rectangle(*this);
            double cx = rc.left + (rc.width * 0.5);
            double cy = rc.top + (rc.height * 0.5);
            double radius = min(rc.width, rc.height) * 0.44;
            uint32_t bg = context.is_hovered(*this) ? 0x1E3A5FFFu : 0x0F172AFFu;
            context.fill_circle(cx, cy, radius, bg);
            context.draw_circle(cx, cy, radius, 0x38BDF8FFu, 3.0);
            drawing_path pointer;
            pointer.move_to(cx, cy).line_to(cx, cy - (radius * 0.65));
            context.outline_path(pointer, 0xFACC15FFu, 3.0);
            context.draw_text(U"12:00", easyvrui::font_t{U"Segoe UI", 22u, true, false}, easyvrui::render_rectangle_t{rc.left, cy + 12.0, rc.width, 34.0}, 0xFFFFFFFFu, true);
        }
};

int main()
{
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    window_main->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    window_main->set_show_title_bar(false);
    window_main->set_startup_position(easyvrui::startup_position_t::none);
    window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
    window_main->set_physical_scale(0.5);
    window_main->set_curvature(1.2);
    window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
    window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});

    auto dial_watch = make_shared<wrist_dial_control>(U"dial_watch");
    dial_watch->set_rect(easyvrui::rectangle_t{0u, 0u, 220u, 220u});
    dial_watch->on_click += [=](easyvrui::control_base &, easyvrui::event_args_t &)
    {
        if(window_main->get_reference_object().type == easyvrui::reference_object_type_t::left)
        {
            window_main->reparent(easyvrui::reference_object_t{easyvrui::reference_object_type_t::world}, true);
        }
        else
        {
            window_main->set_reference_object(easyvrui::reference_object_t{easyvrui::reference_object_type_t::left});
            window_main->set_position(easyvrui::vec3_t{-0.05, 0.06, 0.08});
            window_main->set_rotation(easyvrui::vec3_t{-45.0, 20.0, 0.0});
        }
    };

    window_main->get_control_list().add(dial_watch);
    window_main->show();
    easyvrui::run(U"wrist_watch");
    return 0;
}
```
:::
:::
# 初めてのwindowを作成して実行する

環境をインストールし、VRでの基本操作を確認したら、約20行のコードで最初の`window`を作成します。タイトル、案内を表示する`label`、クリックで表示を更新する`button`を配置します。PythonとC++の両方で、実行できる実装を示します。

---

## SDKパス設定

コードを書く前に、インストール済みのSDKを参照するようプロジェクトまたは環境変数を設定します。以下ではインストール先を`D:\Tools\EasyVRUI`とします。

::: code-group
```cmd [Python SDKの設定]
python -m pip install -r "D:\Tools\EasyVRUI\sdk\api\python\requirements.txt"
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
```

```cmake [C++用の最小CMakeLists.txt]
cmake_minimum_required(VERSION 3.24)
project(my_first_vr_window LANGUAGES CXX)

set(EASYVRUI_ENGINE_INTERFACE_ROOT "D:/Tools/EasyVRUI/sdk" CACHE PATH "Installed SDK or EngineInterface directory")
if(EXISTS "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")
    set(EASYVRUI_ENGINE_INTERFACE_ROOT "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface")
endif()
include("${EASYVRUI_ENGINE_INTERFACE_ROOT}/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")

add_executable(my_first_vr_window main.cpp)
target_compile_options(my_first_vr_window PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/utf-8>)
easyvrui_link_selected_api(my_first_vr_window)
easyvrui_deploy_runtime(my_first_vr_window "${EASYVRUI_API_LINK_SHARED}")
```
:::

### C++リンクと実行

`easyvrui_link_selected_api()`はデフォルトで`sdk/engine_interface/lib/engine_interface_static.lib`を`my_first_vr_window.exe`にリンクし、静的CRTを使用します。SDK内蔵の言語パックは実装に伴って実行可能ファイルに含まれます。DLLを選択する際には、CMake設定で`-DEASYVRUI_API_LINK_SHARED=ON`を指定し、対応するインポートライブラリと動的CRTを使用します。`easyvrui_deploy_runtime()`は`sdk/engine_interface/bin/`から`engine_interface.dll`をプログラムの出力ディレクトリにコピーします。

::: tip Pythonバージョン要件
`sdk/api/python/`には`easyvrui`パッケージと、静的リンク版の`engine_interface_native*.pyd`が含まれます。コマンドから直接実行する場合は、このディレクトリを検索パスの先頭に追加します。Pythonインタープリターがパッケージを見つけ、SDKが拡張モジュールを読み込みます。Pythonは`installation.json`に記録されたバージョンに合わせ、拡張モジュールと同じx64版を使用します。チュートリアルの`python/run.cmd`を使う場合、環境変数`EASYVRUI_SDK_ROOT`で任意のインストール先の`sdk/`を指定できます。
:::

---

## 最初の`window`例

SteamVRと、インストール先にある`bin/easyvrui_engine.exe`を起動します。次のコードを`first_window.py`または`main.cpp`として保存します。

::: code-group
```python [Python（first_window.py）]
from easyvrui import button, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "我的第一个VR窗口"
    window_main.rect = rect(0, 0, 520, 260)
    label_status = label("label_status")
    label_status.rect = rect(36, 76, 448, 48)
    label_status.text = "点一下下面的按钮试试看！"
    button_hello = button("button_hello")
    button_hello.rect = rect(36, 150, 200, 48)
    button_hello.text = "点我打招呼"

    def button_hello_click(source, event):
        label_status.text = "你好，VR世界！"

    button_hello.on_click += button_hello_click
    window_main.control_list.add(label_status)
    window_main.control_list.add(button_hello)
    window_main.show()
    run("my_first_vr_app")

if __name__ == "__main__":
    main()
```

<<< ../../../examples/basics/03_first_window/cpp/main.cpp
:::

### プログラムの実行

::: code-group
```cmd [Python版の実行]
python first_window.py
```

```cmd [C++版のビルドと実行]
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
build\my_first_vr_window.exe
```
:::

SteamVRでサンプルのタイトル「我的第一个VR窗口」の`window`を見つけます。コントローラーのレーザーで「点我打招呼」の`button`をクリックすると、`label`の表示が更新されます。

---

## 初期表示とクリック時の変化

次の図は、この章のC++サンプルのウィンドウをWARPで描画した日本語表示です。初期状態では案内の`label`と、操作する`button`が表示されます。

![最初のウィンドウの初期状態](/images/ja/basics_first_initial.png)

テストホストがクリックを`button_hello`に届けると、サンプルと同じ`on_click`コールバックが動き、`label_status.text`が「こんにちは、VRの世界！」に変わります。

![ボタンをクリックした後のラベルの更新](/images/ja/basics_first_clicked.png)

## 初期化とイベントのディスパッチ

サンプルでは、EasyVROverlayUIEngineアプリの初期化とイベント処理を5つの手順で行います。

### 1. コントロール名の指定（`name`）

```python
window_main = window("window_main")
label_status = label("label_status")
```

コントロールの構築時に、同じコンテナー内で一意な空でない`name`を渡します。構築後は読み取り専用です。`コントロール型_用途`のように型名と用途を組み合わせると、`button_hello`のような名前になり、Form Designerが出力するメンバーの命名とそろいます。

### 2. 位置とサイズの設定（`rect`）

- 子コントロールの`rect(left, top, width, height)`は、**親コンテナーの左上**を原点とする論理ピクセル座標です。
- `window`自体の`rect.left`と`rect.top`は、3D空間の配置には使いません。`width`と`height`がサイズを決めます。タイトルバーの高さは約44～56pxなので、最初の子コントロールは通常`top = 76`付近に配置します。
- 既定の`physical_scale = 1.0`では、**1000論理ピクセルが1メートル**です。1論理ピクセルが約1ミリメートルに相当するため、`520 × 260`のウィンドウの物理的な幅は約0.52メートルになります。

### 3. 型付きイベントを登録する（`on_click += ...`）

```python
def button_hello_click(source, event):
    label_status.text = "你好，VR世界！"

button_hello.on_click += button_hello_click
```

すべてのイベントコールバックは、2つの引数**`(source, event)`**を受け取ります。
- `source`はイベントを発生させたコントロールのインスタンスです。この例では`button_hello`が入ります。
- `event`は型付きイベント引数オブジェクトです。通常のクリックには`event_args`（C++では`easyvrui::event_args_t`）が渡されます。キー入力やウィンドウを閉じる際に発生するイベントには、`key`や`cancel`などの固有フィールドを持つイベント引数型が渡されます。

### 4. コントロールをウィンドウに追加する（`control_list.add`）

新しく作成された`label`と`button`は、`window_main.control_list.add(...)`（C++では`window_main->get_control_list().add(...)`）を通じて`window`のコントロール集合に加えられた後、レイアウト、レンダリング、レーザーヒット検出に参加します。

### 5. `show()`と`run("my_first_vr_app")`

- `window_main.show()`：Engineに表示要求を送信し、デフォルトでは中央配置でユーザーの前方に置かれ、既存のウィンドウの深さを自動的にずらします。
- `run("my_first_vr_app")`：セッション名を登録し、メインのメッセージループに入り、レーザーイベント、キーボード入力、増分描画を処理し続け、すべてのウィンドウが閉じるまで続けます。

::: info C++文字列プレフィックス`U"..."`の説明
C++ SDKでは`std::u32string`（UTF-32エンコーディング）を使用してインターフェーステキストとコントロール名を表し、多言語文字とユニコードコードポイントを正確に処理します。`U"..."`の文字リテラルを使用すると、`std::u32string`を直接構築できます。
:::

次の章では、可視化**Form Designer**を使用してドラッグ操作で迅速にインターフェースを構築し、コードをエクスポートする方法を紹介します。

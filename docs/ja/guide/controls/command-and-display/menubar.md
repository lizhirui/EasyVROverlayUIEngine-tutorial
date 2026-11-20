# menubar

`menubar`はウィンドウ上部の階層メニューです。最上位の`menuitem`はメニューを開く入口になり、子の`menuitem`はコマンドやサブメニューになります。`menubar`を`window.menu`に設定すると、`window`がレイアウト、フォーカス、コマンドへのアクセスを管理します。継承メンバーは[コンテナーのインターフェース](/ja/guide/controls/common-api#container-control)を参照してください。

## 既定の外観

既定の行高は32論理ピクセルで、フォントはSDKの既定値です。図は「タスク」「表示」の2つの最上位`menuitem`を標準の位置に置き、メニューを閉じた状態です。

![menubarデフォルト外観](/images/ja/menubar_default.png)

## プロパティの比較

比較図では行高を42論理ピクセルにし、フォントを変更しています。上は`Alt`を押している間の表示で、最上位メニューの`T`と`V`に下線が付きます。下は`Alt`を単独で押して離した後、方向キーで「タスク」を開いた状態です。各項目のニーモニックの下線、ショートカット`Ctrl+R`、チェック状態、無効な項目が確認できます。

![menubar属性比較](/images/ja/menubar_comparison.png)

## ニーモニックとキーボードによるメニュー操作

`menuitem.text`では、`&`の直後の文字をニーモニックにできます。たとえば`任务(&T)`は「任务(T)」と表示されます。`Alt`を押している間やキーボードでメニューを操作している間は、ニーモニックの`T`に下線が付きます。`Alt`を単独で押して離すと、メニューのキーボード操作に入るか、そこから抜けます。方向キーで移動し、ニーモニックで項目を選び、`Enter`で現在のコマンドを実行できます。`&`自体を表示するには`&&`と書きます。

物理キーボードモードでは、`Alt+Shift`でIMEの言語を切り替えても、現在の`textbox`の編集フォーカスが維持されます。同じ階層の`menuitem`には別々のニーモニックを指定します。よく使うコマンドには、直接実行できるショートカットを`shortcut`に指定できます。

## APIリファレンス

C++の表ではメソッドを使用してプロパティを読み書きし、Pythonでは同名のプロパティを使用してアクセスします。コールバックは`source`と`event`を受け取ります。表の各型付きイベント引数は`event_args_t`から継承し、基本パラメータ自体には追加フィールドがありません。Pythonの型名では`_t`を省略します。

### プロパティ

|プロパティ|C++でのメソッドアクセス|型、デフォルト値、用途|
|---|---|---|
|`font`、`row_height`|`get_font`、`set_font`、`get_row_height`、`set_row_height`|フォントと正の論理ピクセル行高、デフォルト行高32。|
|`open`|`get_is_open`|Pythonの読み取り専用プロパティで、メニューナビゲーション状態を示します。|
|`owning_menubar`|`get_menubar`|読み取り専用、所属`menubar`を照会します。|
|`control_list`|`get_control_list`|ルート`menuitem`の集合。サブメニューの内容は対応する項目の`control_list`に置かれます。|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|継承されたオン/オフ。可視性やインタラクティビティをオフにすると、アクティブなメニューブランチに影響を与えます。|
|`focusable`|`is_focusable`|読み取り専用、メニューフォーカスをサポートします。|

### メソッド

|メソッド|用途|
|---|---|
|`menubar(name)`|メニューオブジェクトを構築し、`window.menu`に割り当てます。|
|`open_menu()`、`close(restore_focus=True)`|Pythonではメニュー状態に入ったり出たりします。C++の入るメソッドは`open()`で、クローズ時もフォーカスを復元する選択肢があります。|
|`is_submenu_open(item)`|指定されたサブメニューが開いているかを照会します。C++のメソッドは`get_is_submenu_open(item)`です。|

### イベント

|イベント|パラメータのタイプ|トリガー条件|
|---|---|---|
|`on_font_changed`、`on_row_height_changed`|`event_args_t`|フォントサイズまたは行高の設定変更。|
|`on_opening`、`on_closed`|`event_args_t`|メニューの開始と閉じる通知。|
|`on_item_added`、`on_item_removed`|`menu_item_event_args_t`|サブアイテムの集合操作、`item`、`index`を含む。|

## menuitem

|プロパティ|用途|
|---|---|
|`text`|表示文字。`&`を使用してマークアップキーを指定できる。|
|`icon`|オプションの`drawing_image`。|
|`shortcut`|コマンドのショートカットキー、例えば`Ctrl+R`。|
|`checkable`、`checked`|選択可能なコントロールと現在の選択状態。|
|`separator`|分割アイテムの表示。|
|`open`|Pythonの読み取り専用アトリビュート、このアイテムのサブメニューが開いているかをチェックする。C++では所属`menubar`を使用して検索する。|
|`control_list`|管理サブ`menuitem`を使用して、ネストされたメニューを作成する。|

`menuitem(name)`を使用して作成する。C++のアトリビュートは`get_`、`set_`を使用してアクセスする。プロジェクトイベントには`on_text_changed`、`on_icon_changed`、`on_shortcut_changed`、`on_checkable_changed`、`on_checked_changed`、`on_separator_changed`、`on_opening`、`on_closed`、および継承された`on_click`が含まれ、パラメータは`event_args_t`である。サブセットも同様に`on_item_added`と`on_item_removed`を提供する。

## 実行できるサンプル

「タスク」を開いて「記録を更新」を選択する。コマンド処理関数は状態文字を更新する。キーボード入力を受け取るウィンドウ内で`Alt`を単独で押すこともでき、方向キーでメニューを展開し、`Enter`でコマンドを実行するか、直接`Ctrl+R`を押すこともできる。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)を押してEngineを起動する。チュートリアルのルートディレクトリのx64デベロッパCMDでコマンドを実行し、サンプルでのSDKインストールパスを置き換える。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/menubar/cpp -B .work/example_menubar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_menubar --config Release
.work\example_menubar\Release\tutorial_menubar.exe
```

シングルコンフィギネーションのNinjaを使用する場合、ビルドディレクトリから直接実行ファイルを実行する。

<<< ../../../../../examples/guide/controls/command-and-display/menubar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\menubar\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/menubar/python/menubar_demo.py

### 実行結果

![menubar独立例程の実行効果](/images/ja/menubar_demo.png)

## よくある質問とレイアウト実践

- トップエリアは`window.menu`でレイアウトされる。本文コントロールには、タイトルバーとメニューがある高さを予約する必要がある。
- 同じビジネスコマンドを`on_click`に集中させることで、レーザー、マークアップキー、ショートカットキーをロジックで共有できる。
- コマンド名は各言語の文字数に適したものであるべきだ。サブメニューのショートカットキーでトリガー文字とアイコンに余白を残す。

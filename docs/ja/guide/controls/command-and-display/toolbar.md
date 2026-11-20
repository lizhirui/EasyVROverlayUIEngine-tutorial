# toolbar

`toolbar`は固定矩形内に`toolbar_button`を順番に配置し、即座に使用できる操作です。コンテナはサイズ、間隔、クリッピング、ボタンのレイアウトを担当します。ボタン集合は`button_list`で公開されます。継承メンバーについては[コンテナインターフェース](/ja/guide/controls/common-api#container-control)をご覧ください。

## 既定の外観

図には2つのアイコンと1つのセパレーターが追加されます。コントロールはデフォルトのツールサイズ、間隔、色合いを使用します。

![toolbarデフォルト外観](/images/ja/toolbar_default.png)

## プロパティの比較

上側はデフォルトのサイズと間隔を維持します。下側は56の論理ピクセルのツールサイズ、14の論理ピクセル間隔を使用し、右側の操作項目は無効化されています。

![toolbar属性比較](/images/ja/toolbar_comparison.png)

## APIリファレンス

C++では表のメソッドで属性を読み書きします。Pythonでは同名の属性を参照します。コールバックは`source`と`event`を受け取ります。表の各型付きイベント引数は`event_args_t`から継承し、基本パラメータには追加のフィールドがありません。Pythonの型名は`_t`を省略します。

### プロパティ

|プロパティ|C++でのメソッドアクセス|型、デフォルト値、用途|
|---|---|---|
|`button_list`|`get_button_list`|`toolbar_button_collection`はボタンの順序と所属を管理します。|
|`tool_size`、`spacing`|`get_tool_size`、`set_tool_size`、`get_spacing`、`set_spacing`|ツールサイズはデフォルトで40の論理ピクセルで、正の整数でなければなりません。間隔はデフォルトで6.0の論理ピクセルで、非負の有限値でなければなりません。|
|`focusable`|`is_focusable`|読み取り専用で、コンテナとエントリにはそれぞれのフォーカスルールがあります。|

### メソッド

|メソッド|用途|
|---|---|
|`toolbar(name)`|構築。|
|`button_list.add(item)`、`button_list.insert(index,item)`|エントリを追加または挿入する操作。|
|`button_list.add_separator(name)`|Pythonでは名前でセパレーターを追加します。C++ではまず`get_button_list().add(name)`でエントリを作成し、そのエントリの`set_separator(true)`を呼び出します。|
|`button_list.remove(item)`、`button_list.clear()`|エントリを削除またはクリアする操作。C++ではまず`get_button_list()`を呼び出します。|

### イベント

|イベント|パラメータの型|トリガー条件|
|---|---|---|
|`on_tool_size_changed`、`on_spacing_changed`|`event_args_t`|サイズと間隔の実際の変化。|

## toolbar_button

|メンバー|用途|
|---|---|
|`toolbar_button(name)`|`button_list`に追加できるエントリを作成します。|
|`icon`、`get_icon/set_icon`|`drawing_image`を読み書きできます。|
|`separator`、`get_separator/set_separator`|エントリをセパレーターとして使用するかどうかを制御します。|
|`enabled`、`tooltip_text`|継承されたインタラクティブスイッチとハイライト説明。|
|`on_icon_changed`、`on_click`|パラメータはすべて`event_args_t`で、アイコンの変化とビジネスコマンドのアクティベーションを示します。|

`toolbar_button_collection`を使用してインデックスまたは名前でエントリにアクセスします。ボタンの通常の矩形は所属する`toolbar`で管理されます。

## 実行できるサンプル

青いアイコンをクリックすると「リクエスト済みプレビュー」がトリガーされます。アイコンは4のバイトRGBAデータで作成され、ハイライト説明はコマンドの目的を示します。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)を通じてEngineを起動します。チュートリアルのルートディレクトリのx64デベロッパーCMDでコマンドを実行し、サンプルでのSDKインストールパスを置き換えます。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/toolbar/cpp -B .work/example_toolbar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_toolbar --config Release
.work\example_toolbar\Release\tutorial_toolbar.exe
```

シングルコンフィギュレーションのNinjaを使用する場合、ビルドディレクトリから直接実行ファイルを実行します。

<<< ../../../../../examples/guide/controls/command-and-display/toolbar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\toolbar\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/toolbar/python/toolbar_demo.py

### 実行結果

![toolbar独立例程运行效果](/images/ja/toolbar_demo.png)

## よくある質問とレイアウト実践

- アイコンのヒット範囲に幅と高さを確保する。項目の総幅が増加すると、コンテナの幅を増やすか、現在同時に表示されている操作数を減らす。
- 異なるタスクを区別するためにセパレーターを使用する。`enabled`で一時的に使用できないコマンドを示す。
- `tooltip_text`でアイコンの意味を説明する。画像自体は共有描画リソースを使用して表示される。

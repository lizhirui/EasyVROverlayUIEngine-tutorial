# treeview

`treeview`は、ワークスペースディレクトリ、タスクカテゴリ、展開可能なアウトラインなど、親子関係を持つデータを表示します。SDKは展開パス内のノードを可視化シーケンスに配置し、ビューポートに基づいて対応する行を描画します。`tree_node`はビジネスノードを管理し、`treeview`は現在の選択、スクロール、入力を管理します。継承メンバーについては[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を参照してください。

## 既定の外観

ルート集合は初期状態で空で、選択は空で、行の高さは30論理ピクセルです。内容がない場合、ビューポートにはデフォルトの背景と境界線が表示されます。

![treeviewデフォルト外観](/images/ja/treeview_default.png)

## プロパティの比較

左側のルートノードは折りたたまれています。右側では同名のルートノードが展開され、選択された子ノードが前景色で調整されます。折りたたみと展開のマークは階層を示し、選択された行は現在の位置を強調します。

![treeview属性比較](/images/ja/treeview_comparison.png)

## APIリファレンス

C++の表のメソッドは属性を読み書きしますが、Pythonでは同名の属性にアクセスします。コールバックは`source`と`event`を受け取ります。表の各型付きイベント引数は`event_args_t`を継承し、基本パラメータには追加のフィールドがありません。Pythonの型名は`_t`を省略します。

### プロパティ

|プロパティ|C++でのメソッドアクセス|型、デフォルト値、用途|
|---|---|---|
|`node_list`|`get_node_list`|ルートノード集合は初期状態で空です。Pythonでは全体を代入でき、C++では集合の`assign`を使用して置き換えます。|
|`selected_node`|`get_selected_node`、`set_selected_node`|読み書き可能で、初期状態は`None`または`nullptr`です。有効なノードを選択する場合は、現在のツリーのノードオブジェクトを使用する必要があります。|
|`row_height`|`get_row_height`|読み取り専用で、デフォルトは30論理ピクセルです。|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`|読み取り専用で、視点内の可視ノードの数に基づいて計算されます。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|継承されたブールスイッチで、デフォルトは偽です。|
|`focusable`|`is_focusable`|読み取り専用で、方向キーを使用してナビゲートできます。|

### メソッド

|メソッド|用途|
|---|---|
|`treeview(name)`|ルートコンテナを構築します。|
|`clear_selection()`|現在の選択をクリアします。|
|`is_blank_at(local_left,local_top)`|コントロールの局部座標がノード行の外側の空白領域に含まれるかどうかを判断します。|

### イベント

|イベント|パラメータのタイプ|トリガー条件|
|---|---|---|
|`on_node_list_changed`|`event_args_t`|ノード集合の構造が変更されます。|
|`on_selection_changed`|`tree_node_event_args_t`|選択が変更され、`node`を使用して新しいノードにアクセスします。選択をクリアするとノードは空になります。|
|`on_node_expanded`、`on_node_collapsed`|`tree_node_event_args_t`|ノードが展開または折りたたまれます。|
|`on_node_activated`|`tree_node_event_args_t`|ノードがダブルクリックされたり、キーボードでアクティブになったりします。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|空白領域の選択戦略が変更されます。|

## tree_node

|属性またはメソッド|C++でのメソッドアクセス|用途|
|---|---|---|
|`tree_node(text="", expanded=False, tag="")`|`tree_node(text, expanded, tag)`|ノードを構築し、初期状態で折りたたまれています。|
|`text`、`tag`|`get_text/set_text`、`get_tag/set_tag`|表示テキストとビジネスマークを設定します。|
|`expanded`|`get_expanded/set_expanded`|折りたたみ状態を保存し、`expand()`や`collapse()`を呼び出すこともできます。|
|`parent`|`get_parent()`|読み取り専用で、直接の親ノードを返します。ルートまたは集合から離れたノードは空を返します。|
|`node_list`|`get_node_list()`|子ノードの集合。`add`、`insert`、`remove`、`clear`を使用して構造を調整し、インデックスで読み出します。|

ノードの`tag`は安定したビジネス識別子を保存できます。タイトルと展開状態は別々に設定されます。

## 実行できるサンプル

「タスク分類」を実行し、「同期タスク」を展開して「チェックレポート」を選択します。`event.node`からテキストを読み取り、状態を更新するためのコールバックを選択します。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)をクリックしてEngineを起動します。チュートリアルのルートディレクトリのx64デベロッパCMDでコマンドを実行し、サンプルでのSDKインストールパスを変更してください。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/treeview/cpp -B .work/example_treeview -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_treeview --config Release
.work\example_treeview\Release\tutorial_treeview.exe
```

シングルコンフィギュレーションのNinjaを使用する場合、ビルドディレクトリから直接実行ファイルを実行します。

<<< ../../../../../examples/guide/controls/collection-and-data/treeview/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\treeview\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/treeview/python/treeview_demo.py

### 実行結果

![treeview独立例程実行効果](/images/ja/treeview_demo.png)

## よくある質問とレイアウト実践

- まず子ノードをルートノードの`node_list`に追加し、次にルートノードを`treeview`に追加します。追加する前に単一の所属を維持し、ノードを移動する際は元の集合から削除します。
- 複数層の縮小、展開マーク、スクロールバーに余裕を確保します。簡潔なタイトルを使用し、詳細な説明は別の`label`に記載できます。
- `on_selection_changed`を処理する際は空選択を考慮してください。フィルタリングまたは更新時には`tag`を使用してビジネス選択を復元できます。

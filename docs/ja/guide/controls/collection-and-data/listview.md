# listview

`listview`は複数列で一組のオブジェクトレコードを表示します。各`listview_column`は列のタイトルと論理ピクセル幅を記述し、`listview_item`には複数の文字列セルとオプションのアイコンが含まれます。リストはスクロール、選択、列幅のドラッグ操作、行のインタラクションを担当します。継承メンバーについては[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を参照してください。

## 既定の外観

デフォルトの列集合と項目集合は空で、行の高さは30、表頭の高さは32の論理ピクセルです。選択インデックスは`-1`で、マルチ選択はオフです。

![listviewデフォルト外観](/images/ja/listview_default.png)

## プロパティの比較

左側はデフォルトの列幅で単一選択です。右側はタスク列を広げ、行の高さを上げ、マルチ選択を有効にし、第一と第三の記録を選択します。

![listview属性比較](/images/ja/listview_comparison.png)

## APIリファレンス

C++ではテーブルのメソッドで属性を読み書きします。Pythonでは同名の属性を参照します。コールバックは`source`と`event`を受け取ります。テーブルの各型付きイベント引数は`event_args_t`を継承し、基本パラメータには追加のフィールドがありません。Pythonの型名は`_t`を省略します。

### プロパティ

|プロパティ|C++でのメソッドアクセス|型、デフォルト値、用途|
|---|---|---|
|`column_list`、`item_list`|`get_column_list`、`get_item_list`|操作可能な列と行の集合。Pythonでは全体の値付けがサポートされ、C++では`assign`を使用します。|
|`selected_index`|`get_selected_index`、`set_selected_index`|主選択インデックス、デフォルトは`-1`です。|
|`selected_item`|`get_selected_item`、`set_selected_item`|主選択オブジェクト、空の選択は`None`または`nullptr`です。|
|`selected_item_list`|`get_selected_item_list`|読み取り専用、現在選択されているオブジェクトを読み取ります。|
|`multi_select`|`get_multi_select`、`set_multi_select`|ブール値、デフォルトは偽です。有効にすると、拡張選択と選択の切り替えがサポートされます。|
|`row_height`、`header_height`|`get_row_height`、`set_row_height`、`get_header_height`、`set_header_height`|デフォルトはそれぞれ30と32で、正の論理ピクセルを設定します。|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|`get_visible_row_count`、`get_vertical_scrollbar_visible`、`get_horizontal_scrollbar_visible`|読み取り専用、計算後の表示可能な行数とスクロールバーの状態を照会します。|
|`focusable`|`is_focusable`|読み取り専用、キーボードナビゲーションをサポートします。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|継承された空白クリック戦略、デフォルトは偽です。|

### メソッド

|メソッド|用途|
|---|---|
|`listview(name)`|複数列のリストを構築します。|
|`select_item(index,extend=False,toggle=False)`|選択インデックス、拡張または選択の切り替えが可能です。|
|`clear_selection()`|選択範囲をクリアします。|
|`is_blank_at(local_left,local_top)`|コントロールの局部座標で項目領域の空白を判断します。|

### イベント

|イベント|パラメータのタイプ|トリガー条件|
|---|---|---|
|`on_column_list_changed`、`on_column_width_changed`、`on_column_click`|`listview_column_event_args_t`|列集合、列幅、または表頭のクリックで、`column`と`index`を使用して列を位置決めします。|
|`on_item_list_changed`、`on_row_double_click`|`listview_item_event_args_t`|行集合または内容の変化、行のダブルクリックで、`item`と`index`を使用して位置決めします。集合操作は集合の変化のみを含むことがあります。|
|`on_selection_changed`|`event_args_t`|主項目または選択集合の変化後に選択属性を読み取ります。|
|`on_row_height_changed`、`on_header_height_changed`|`event_args_t`|二種類の高さの変化。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|継承された空白選択戦略の変化。|

## listview_columnとlistview_item

|タイプ|属性またはメソッド|用途|
|---|---|---|
|`listview_column`|`listview_column(text="", width=100)`|列の説明を作成します。|
|`listview_column`|`text`、`width`、C++ではそれぞれの`get_`と`set_`を使用します。|生存列オブジェクトのタイトルと幅を変更します。|
|`listview_item`|`listview_item(cell_list=[], icon=None, tag="")`|画像とビジネスマークに関連付けられる一行の文字列セルを作成します。|
|`listview_item`|`cell_list`、`get_cell_list()`|この一行の文字列を編集します。列インデックスでアクセスします。|
|`listview_item`|`icon`、`tag`、C++ではそれぞれの`get_`と`set_`を使用します。|アイコンはリストの最初の列に使用され、`tag`はビジネス識別を保存するために使用されます。|

両方の集合はインデックスで読み取り、追加、挿入、削除、クリアが可能です。C++では共有オブジェクトを使用して所属を確立し、Pythonでは同じ集合の操作インターフェースを使用します。

## 実行できるサンプル

「オーディオ同期」を選択すると、状態エリアに現在の記録が表示されます。列タイトル、行オブジェクト、選択状態がそれぞれ更新されます。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルのルートディレクトリのx64デベロッパCMDでコマンドを実行し、サンプルでのSDKインストールパスを置き換えます。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/listview/cpp -B .work/example_listview -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_listview --config Release
.work\example_listview\Release\tutorial_listview.exe
```

シングルコンフィギュレーションのNinjaを使用する場合、ビルドディレクトリから直接実行ファイルを実行します。

<<< ../../../../../examples/guide/controls/collection-and-data/listview/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\listview\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/listview/python/listview_demo.py

### 実行結果

![listview独立例程運用効果](/images/ja/listview_demo.png)

## よくある質問とレイアウト実践

- 明確な列幅を使用し、スクロールバーを残します。長い局部列を表示する場合は、列の幅を変更するか、リスト全体を広げるのではなく調整します。
- ソートは`on_column_click`を使用してアプリの再配置をトリガーできます。行オブジェクトやビジネスマークを保存すると、インデックスはソートによって変わる可能性があります。
- 型化された編集と検証が必要なインターフェースには[grid](./grid)を使用できます。

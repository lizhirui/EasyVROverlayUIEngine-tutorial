# grid

`grid`は、型化されたテーブル、行、またはセルを選択し、編集および検証を行います。少量の値を直接コントロールに保存することも、読み取りと書き込みのコールバックを通じてアプリケーションデータを関連付けることもできます。編集が完了するまで、編集バッファと提出済み値がそれぞれ保持されます。継承メンバーについては[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を参照してください。

## 既定の外観

デフォルトの列集合は空で、行数は0で、`cell`の選択モードを採用し、初期は選択されていません。図にはデフォルトの境界線、背景、および初期状態が保持されています。

![gridデフォルト外観](/images/ja/grid_default.png)

## プロパティの比較

左側は行全体を選択し`read_only`を有効にしています。右側はセルを選択し、最初の行の数値を編集しています。読み取り専用状態でもデータを選択し、閲覧することができます。

![grid属性比較](/images/ja/grid_comparison.png)

## APIリファレンス

C++では表のメソッドで属性を読み書きし、Pythonでは同名の属性を通じてアクセスします。コールバックは`source`と`event`を受け取ります。表の各型付きイベント引数は`event_args_t`を継承し、基本パラメータには追加のフィールドがありません。Pythonの型名は`_t`を省略します。

### プロパティ

|プロパティ|C++でのメソッドアクセス|型、デフォルト値、および用途|
|---|---|---|
|`column_list`|`get_column_list`、`set_column_list`|`grid_column_t`配列は、`text`、`width`、`editable`を含みます。読み取ったリストは全体を書き戻すのに適しており、列の幅は`set_column_width`を通じて更新できます。|
|`row_count`|`get_row_count`、`set_row_count`|モデルの行数を制御します。データプロバイダーを使用する場合は、設定されたデータの規模によって決定されます。|
|`selection_mode`、`multi_select`|`get_selection_mode`、`set_selection_mode`、`get_multi_select`、`set_multi_select`|デフォルトは`cell`、偽です。`row`および複数選択をサポートします。|
|`selected_index`|`get_selected_index`、`set_selected_index`|主に選択された行のインデックスで、デフォルトは`-1`です。|
|`selected_cell_list`|`get_selected_cell_list`|読み取り専用で、`grid_cell_t`位置リストです。|
|`row_height`、`header_height`|`get_row_height`、`set_row_height`、`get_header_height`、`set_header_height`|行とヘッドの論理ピクセル高さで、デフォルトはそれぞれ30と32です。|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|`get_visible_row_count`、`get_vertical_scrollbar_visible`、`get_horizontal_scrollbar_visible`|読み取り専用の視点状態です。|
|`read_only`|`get_read_only`、`set_read_only`|コントロールレベルの編集オン/オフで、デフォルトは偽です。列の`editable`は編集をさらに制限します。|
|`editing`、`edit_cell`、`edit_error`|`get_editing`、`get_edit_cell`、`get_edit_error`|読み取り専用で、編集が行われているか、現在の座標とエラー説明です。|
|`edit_text`|`get_edit_text`、`set_edit_text`|読み書き可能な編集バッファで、テキスト編集パスに使用されます。|
|`focusable`|`is_focusable`|読み取り専用で、キーボードのフォーカスをサポートします。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|継承された空白選択戦略です。|

### メソッド

|メソッド|用途|
|---|---|
|`grid(name)`|テーブルを構築します。|
|`get_cell_value(row,column)`、`set_cell_value(row,column,value)`|C++で型化された値を読み書きします。Pythonでは`item[row, column]`を通じて読み取りまたは代入します。`grid_value_t`は文字列、`int64_t`、`double`、`bool`をサポートします。|
|`set_data_provider(row_count,reader,writer)`、`refresh_data()`|データプロバイダーを接続した後、必要に応じて読み書きします。モデルが変更された後、現在の表示を更新します。書き込み器を省略する場合は、読み取りインターフェースを使用して表示します。|
|`set_cell_renderer(renderer)`、`set_edit_validator(validator)`|コールバックを通じてカスタムな描画と提出検証を行います。|
|`get_value_text(value)`|型化された値を表示テキストに変換します。|
|`get_cell_at(local_left,local_top)`、`get_cell_rectangle(row,column)`|座標とセル矩形の間で検索します。|
|`get_cell_selected(row,column)`、`select_cell(row,column,extend,toggle)`、`clear_selection()`|選択範囲のチェック、設定、または削除。Pythonでは`is_cell_selected(row, column)`を使用してチェックします。|
|`is_blank_at(local_left,local_top)`|局部座標がテーブル項目の空白部分に含まれているかを確認します。|
|`set_column_width(column,value)`|単一列の論理ピクセル幅を変更します。|
|`begin_edit(row,column)`、`commit_edit()`、`commit_edit(value)`、`cancel_edit()`|編集の開始、送信、またはキャンセル。送信の成功を返します。|

### イベント

|イベント|パラメータのタイプ|トリガー条件|
|---|---|---|
|`on_column_list_changed`|`event_args_t`|列定義の集合の変更。|
|`on_column_width_changed`、`on_column_click`|`grid_column_event_args_t`|`index`、`width`を使用して列情報を取得します。|
|`on_selection_changed`|`event_args_t`|新しい選択座標を読み取ります。|
|`on_row_height_changed`、`on_header_height_changed`|`event_args_t`|行またはヘッドの高さを更新します。|
|`on_cell_double_click`、`on_cell_value_changed`|`grid_cell_event_args_t`|ダブルクリックまたは実際の値の変更、`row`および`column`を含みます。|
|`on_edit_started`、`on_edit_committed`、`on_edit_cancelled`、`on_edit_failed`|`grid_cell_event_args_t`|編集のライフサイクル。失敗した場合`error`または`edit_error`を読み取ります。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|空白選択戦略の更新。|

## データモデルと編集

`grid_cell_t`は`row`および`column`の2つの0開始座標を説明します。`grid_cell_render_t`には矩形、現在の値、および`selected`、`hovered`、`editing`の状態が含まれます。Pythonの対応するタイプは`grid_cell`、`grid_column`、および`grid_cell_render`です。

|コールバック|Pythonパラメータ|C++パラメータ|
|---|---|---|
|データの読み取り|`reader(row, column)`|`reader(row, column)`|
|データの書き込み|`writer(row, column, value)`|`writer(row, column, value, error)`|
|送信の検証|`validator(cell, value)`|`validator(cell, value, error)`|
|セルを描画する|`renderer(context, cell)`|`renderer(context, cell)`|

コールバックからセル値を読み取ります。C++のライターと検証器はブール値で結果を報告し、最後の書き込み可能な文字列でエラーメッセージを返します。Pythonは`True`または`None`で成功を表し、`False`で拒否を表し、文字列で説明付きの拒否を表し、`(accepted, error)`を返すこともできます。具体的な署名は[Python API](/ja/reference/python_api)および[C++ API](/ja/reference/cpp_api)を参照してください。

最初の設定では、列と行数を設定した後、セルにデータを書き込みます。コミット時には、初期の型に基づいて編集テキストを変換します。アプリケーションは、変更を先に検証した後、ビジネスモデルを更新することができます。

## 実行できるサンプル

“並行タスク”に対応する値をダブルクリックし、6を入力して送信します。下部の状態は`on_edit_committed`で更新されます。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルのルートディレクトリのx64開発者CMDでコマンドを実行し、サンプルでのSDKインストールパスを置き換えます。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/grid/cpp -B .work/example_grid -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_grid --config Release
.work\example_grid\Release\tutorial_grid.exe
```

シングルコンフィギュレーションのNinjaを使用する場合、ビルドディレクトリから直接実行ファイルを実行します。

<<< ../../../../../examples/guide/controls/collection-and-data/grid/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\grid\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/grid/python/grid_demo.py

### 実行結果

![grid独立例程運行効果](/images/ja/grid_demo.png)

## よくある質問とレイアウト実践

- 列タイトルとセルサイズは、テキストとスクロールバーを同時に収容する必要があります。等高表示が必要な場合は、まずフォントサイズを決定し、次に行の高さを選択します。
- データプロバイダーは、レンダリング時に頻繁に読み出す可能性があります。データとキャッシュを事前に準備し、読み出しやレンダリングのコールバックでUIスレッドをブロックしないようにしてください。
- 保存成功状態は`on_edit_committed`を監視するべきです。`on_edit_failed`で診断を表示し、編集待ちの内容を表示できる状態に保つ必要があります。

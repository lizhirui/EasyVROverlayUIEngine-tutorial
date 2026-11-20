# textbox

`textbox`は、単行の名前、フレーズ、または改行可能なメモに使用されます。カーソル、選択、コピー、元に戻す、やり直す機能を提供し、入力条件を満たす場合はSDKを通じてIMEとlayoutに接続します。

[公共コントロールインターフェース](/ja/guide/controls/common-api#control)および[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を継承します。

## 既定の外観

デフォルトでは単行、選択可能、編集可能ですが、2つのスクロールバーのスイッチは偽です。スクリーンショットには例示テキストが入力されています。

![textboxデフォルト外観](/images/ja/textbox_default.png)

## プロパティの比較

上から下へはデフォルト、`read_only`、`enabled = False`、多行および縦スクロールバーです。`read_only`は通常の文字色と選択機能を保持し、無効状態では文字の明るさが低下します。現在のSDKの`textbox`には`password`のマスク属性がありません。機密情報の入力が必要な場合は、パスワード処理機能を持つ入力を使用してください。

![textbox属性比較](/images/ja/textbox_comparison.png)

## APIリファレンス

C++属性は表内のアクセスメソッドを通じて読み書きされ、Pythonは同名の属性を通じてアクセスされます。表内のイベントパラメータはC++の型名を使用し、Pythonの対応する型には`_t`の接尾辞を省略します。公共メンバーは[基本インターフェース](/ja/guide/controls/common-api)を参照してください。

### プロパティ

|プロパティ|C++|用途と既定値|
|---|---|---|
|`text`|`get_text`、`set_text`|テキストは初期値で空です。値を設定すると多行および長さの制限が適用されます。|
|`read_only`|`get_read_only`、`set_read_only`|初期値は偽です。有効にするとカーソル、選択、コピーが保持され、ユーザーがテキストを変更するのを防ぎます。|
|`selectable`|`get_selectable`、`set_selectable`|初期値は真です。無効にするとテキストの選択と編集機能が無効になり、コントロールは依然としてフォーカスを取得できます。|
|`multiline`|`get_multiline`、`set_multiline`|初期値は偽です。有効にすると改行が保持され、Enterキーでの改行がサポートされます。|
|`horizontal_scrollbar_visible`、`vertical_scrollbar_visible`|`get_horizontal_scrollbar_visible`、`set_horizontal_scrollbar_visible`、`get_vertical_scrollbar_visible`、`set_vertical_scrollbar_visible`|初期値はすべて偽です。それぞれ横スクロールバーと縦スクロールバーを制御します。|
|`max_length`|`get_max_length`、`set_max_length`|テキストのコードポイント数の上限で、デフォルトの0は無制限を意味します。|
|`selection_start`、`selection_length`|`get_selection_start`、`set_selection_start`、`get_selection_length`、`set_selection_length`|選択範囲の開始点と長さは、コードポイントのインデックスで表され、初期値はすべて0です。|
|`selected_text`|`get_selected_text`、`set_selected_text`|現在の選択範囲のテキストは初期値で空です。値を設定すると、選択範囲が値で置き換えられ、読み取り専用のフィールドを更新するためにも使用できます。|
|`can_undo`、`can_redo`|`get_can_undo`、`get_can_redo`|読み取り専用で、実行可能な取消しまたは戻る記録があるかどうか。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`textbox(name)`|`textbox(name)`|一つの`textbox`を作成します。|
|`select(start,length=0)`|`select(start,length=0u)`|有効な選択範囲を設定します。長さ0は挿入位置の移動を意味します。|
|`undo()`、`redo()`|`undo()`、`redo()`|編集の取消しまたは戻るを行い、成功したかどうかを返します。|

### イベント

|イベント|発生条件と引数|
|---|---|
|`on_text_changed`、`on_read_only_changed`、`on_selectable_changed`|文字または対応するスイッチが実際に変更され、パラメータは`event_args_t`です。|
|`on_selection_changed`、`on_max_length_changed`、`on_multiline_changed`|選択範囲、長さの上限、または多行設定の変更、パラメータは`event_args_t`です。|
|`on_horizontal_scrollbar_visible_changed`、`on_vertical_scrollbar_visible_changed`|対応するスクロールバーオプションの変更、パラメータは`event_args_t`です。|
|`on_text_input`|テキスト入力の通知、パラメータは`text_input_event_args_t`です。|

## 実行できるサンプル

実行後に任意の行を編集し、状態のテキストが更新されるのを観察します。「全選択メモ」をクリックすると`textbox`のフォーカスを要求し、フィールドのテキストを選択します。全選択後のハイライトを示す効果図が表示されます。

まず[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルのリポジトリのルートディレクトリで、MSVCが設定されたx64 CMDを開き、実際にインストールされたSDKのパスを使用します。

### C++

```bat
cmake -S examples/guide/controls/window-and-text/textbox/cpp -B .work/example_textbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_textbox --config Release
.work\example_textbox\Release\tutorial_textbox.exe
```

上記の実行ファイルのパスはVisual Studioジェネレーターに対応しています。単一構成のNinjaを使用する場合、実行ファイルはビルドディレクトリに直接存在します。

<<< ../../../../../examples/guide/controls/window-and-text/textbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\textbox\python\run.cmd
```

<<< ../../../../../examples/guide/controls/window-and-text/textbox/python/textbox_demo.py

### 実行結果

![textbox独立例程運用効果](/images/ja/textbox_demo.png)

## よくある問題と実装上の注意

- まず`multiline`を設定し、次に`text`に初期内容を割り当てます。単行模式では改行が削除され、Editor内ではCRLFとCRはLFとして統一されます。
- プログラムの更新、インタラクティブな編集、選択範囲の置換は、長さとテキストの境界に従います。グループ化された文字の境界には複数のコードポイントが含まれることがあります。
- 表示とコピーには`read_only`を使用し、文字のみ表示には`label`を使用し、一時的にインタラクションを阻止するには`enabled = False`を使用します。
- ビジネス側の最終文字には`on_text_changed`を使用し、`text`を読み取ります。多行入力では、Enterキーを毎回送信として解釈しないようにします。

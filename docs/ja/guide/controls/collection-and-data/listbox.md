# listbox

`listbox`は固定領域内に一連の文字列を常駐表示し、単一の選択を維持します。ファイルカテゴリ、タスク記録、および隣接するオプションを直接比較する必要がある他のインターフェースに適しています。長いリストはスクロールバーまたはコントロールのジョイスティックでスクロールします。選択された項目と現在のスクロール位置は異なる目的に使用されます。

継承された一般的なメンバーについては[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)および[文字列選択と集合インターフェース](/ja/guide/controls/common-api#item-control)を参照してください。

## 既定の外観

デフォルトの集合は空で、行高は30論理ピクセル、インデックスは`-1`です。スクリーンショットではコントロールの矩形が設定され、デフォルトのフレームと背景が保持されます。

![listboxデフォルト外観](/images/ja/listbox_default.png)

## プロパティの比較

左側はデフォルトの行高30を使用し、2番目の項目を選択します。右側では行高を42に変更し、最後の項目を選択し、SDKはその項目が見える位置に自動的にスクロールします。両側とも8項目を使用し、スクロールバーと選択されたハイライトで位置と選択が容易になります。

![listbox属性比較](/images/ja/listbox_comparison.png)

## APIリファレンス

Pythonでは表の属性名を使用します。C++は対応するメソッドを使用して読み書きし、`control_base &source`と表のタイプの参照を使用してイベントをサブスクライブします。追加フィールドのない`event_args_t`は状態が更新されたことを意味し、コールバックは`source`を使用して新しい値を読み取ります。Pythonの対応するイベントタイプ名は`_t`を省略します。

### プロパティ

|プロパティ|C++|タイプ、デフォルト値、および用途|
|---|---|---|
|`selected_index`|`get_selected_index`、`set_selected_index`|0は開始インデックスで、デフォルトは`-1`です。有効なインデックスを割り当てると、その項目が表示範囲に入ります。|
|`selected_item`|`get_selected_item`|読み取り専用で、現在の項目の文字列です。選択されていない場合は空文字列を返します。|
|`item_list`|`get_item_list`|デフォルトの空集合です。C++では`assign`を使用してすべての項目を置き換え、Pythonではイテラブルな文字列集合のリストを全体として割り当てることができます。|
|`row_height`|`get_row_height`、`set_row_height`|デフォルトは30論理ピクセルで、0よりも大きくなければなりません。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|デフォルトは偽です。有効にすると、コントロールの項目領域の空白を通じて選択を解除できます。|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`|読み取り専用で、項目の数と実際の視野角に応じて決定されます。|
|`focusable`|`is_focusable`|読み取り専用で、キーボードナビゲーションをサポートします。|
|`visible`、`enabled`|`set_visible`、`set_enabled`|継承された読み書きのオン/オフスイッチで、隠すか無効にすると、進行中のスクロールバーのドラッグも終了します。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`listbox(name)`|`listbox(name)`|コントロールの構築。|
|`clear_selection()`|`clear_selection()`|選択を解除し、インデックスを`-1`に戻します。|
|`is_blank_at(local_left, local_top)`|`is_blank_at(local_left, local_top)`|ローカル座標を使用して、クリック点が項目領域の空白かどうかを判断します。|

### イベント

|イベント|パラメータタイプ|トリガー条件|
|---|---|---|
|`on_item_list_changed`|`event_args_t`|集合の内容が実際に変更された場合、`item_list`を再読み取りして現在の選択を確認します。|
|`on_selected_index_changed`|`event_args_t`|`selected_index`が実際に変更されました。|
|`on_selection_changed`|`event_args_t`|選択されたインデックスが実際に変更されました。集合を置き換えた後でも`on_item_list_changed`を使用して現在の項目を読み取ることができます。|
|`on_row_height_changed`|`event_args_t`|行高が変更されました。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|空白クリックで選択スイッチが変更されます。|

## 実行できるサンプル

“同期タスク”は8項目をインストールします。3項目目の“同期画像”をクリックすると、状態テキストが更新されます。下にスクロールすると最後の項目を確認でき、方向キーを使用して選択を変更することもできます。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)をに従いEngineを起動します。以下のコマンドはチュートリアルリポジトリのルートディレクトリのx64デベロッパCMDで実行されます。サンプルSDKのパスを実際のインストール場所に変更してください。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/listbox/cpp -B .work/example_listbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_listbox --config Release
.work\example_listbox\Release\tutorial_listbox.exe
```

Visual Studioジェネレーターは実行可能ファイルを`Release`サブディレクトリに配置します。シングルコンフィギュレーションのNinjaジェネレーターは直接ビルドディレクトリに出力します。

<<< ../../../../../examples/guide/controls/collection-and-data/listbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\listbox\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/listbox/python/listbox_demo.py

### 実行結果

![listbox独立例程効果](/images/ja/listbox_demo.png)

## よくある質問とレイアウト実践

- 視点の高さは行の高さの整数倍を基準にします。フォントを大きくすると同期して行の高さも大きくなり、テキストが端に寄ったり、次の行の一部が見えるのを避けます。
- `selected_index >= 0`を使用して選択があることを判定します。空文字列も項目になり得ますので、`selected_item`だけでこれら2つの状況を区別することはできません。
- スクロール位置はコントロール内部で維持されます。特定の項目を特定するには`selected_index`に対応するインデックスを割り当てることができます。
- 列、アイコン、またはデータオブジェクトが必要な場合は、アプリ内で`listview`または`grid`を使用できます。

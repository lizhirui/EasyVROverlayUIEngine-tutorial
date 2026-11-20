# combobox

`combobox`は限られたオプションを一つの入力領域に圧縮します。`dropdown_list`はプリセット値からのみ選択可能な設定項目に適しており、`dropdown`では単行の自由入力も可能です。両方のモードは文字列集合、選択インデックス、ドロップダウンオーバーレイを共有します。

継承された一般的なメンバーは[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)および[文字列選択と集合インターフェース](/ja/guide/controls/common-api#item-control)を参照してください。

## 既定の外観

デフォルトモードは`dropdown_list`、`item_list`は空、`selected_index = -1`、`text`は空、`dropped_down = False`です。図には閉じた空のコントロールが表示されています。

![comboboxデフォルト外観](/images/ja/combobox_default.png)

## プロパティの比較

第一行は`dropdown_list`の既存のオプションを表示します。第二行は`dropdown`に切り替え、“毎45分”を入力し、インデックスは`-1`です。第三行は`dropped_down = True`を表示し、ポインタは現在選択されている“毎15分”に位置しています。

![combobox属性比較](/images/ja/combobox_comparison.png)

## APIリファレンス

Pythonでは表の属性名を使用します。C++では対応するメソッドを使用して読み書きし、`control_base &source`と表の型の参照を使用してイベントをサブスクライブします。追加フィールドのない`event_args_t`は状態が更新されたことを意味し、コールバックは`source`を通じて新しい値を読み取ります。Pythonの対応するイベントタイプ名は`_t`を省略します。

### プロパティ

|プロパティ|C++|タイプ、デフォルト値、および用途|
|---|---|---|
|`dropdown_style`|`get_dropdown_style`、`set_dropdown_style`|デフォルトは`dropdown_list`です。`combobox_dropdown_style_t`を使用するか、Pythonの`combobox_dropdown_style`列挙値を使用します。|
|`text`|`get_text`、`set_text`|現在表示されている文字。`dropdown_list`の非空値は集合内の項目と一致する必要があります。`dropdown`ではカスタム値を許可します。|
|`dropped_down`|`get_dropped_down`、`set_dropped_down`|ドロップダウンオーバーレイの状態を読み書きし、デフォルトでは折りたたまれています。コントロールがインタラクティブであり、項目集合が空でなければ展開されます。|
|`selected_index`|`get_selected_index`、`set_selected_index`|0の開始インデックス、デフォルトは`-1`です。有効なインデックスを割り当てると、その項目が表示範囲に入ります。|
|`selected_item`|`get_selected_item`|読み取り専用、現在の項目の文字列。選択されていない場合は空の文字列を返します。|
|`item_list`|`get_item_list`|デフォルトでは空の集合です。C++では`assign`を呼び出してすべての項目を置き換え、Pythonではイテラブルな文字列集合のリストをそのまま代入できます。|
|`row_height`|`get_row_height`、`set_row_height`|デフォルトは32の論理ピクセルで、0よりも大きくなければなりません。調整されるのはドロップダウンの項目の行の高さです。|
|`clear_selection_on_blank_click`|`get_clear_selection_on_blank_click`、`set_clear_selection_on_blank_click`|`selection_control`から継承され、デフォルトでは偽です。ネイティブの`combobox`は基クラスの空白領域判断を継続し、プログラムによる選択のクリアには`clear_selection()`を使用します。|
|`focusable`|`is_focusable`|読み取り専用、キーボードのフォーカスをサポートします。編集モードでは入力領域からテキストを受け取ります。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`combobox(name)`|`combobox(name)`|コントロールを構築します。|
|`clear_selection()`|`clear_selection()`|選択をクリアし、インデックスを`-1`に戻します。|
|`is_blank_at(local_left, local_top)`|`is_blank_at(local_left, local_top)`|継承された空白領域のクエリ。ネイティブの`combobox`は基クラスの実装を継続し、偽を返します。|

### イベント

|イベント|パラメータタイプ|トリガー条件|
|---|---|---|
|`on_dropdown_style_changed`|`event_args_t`|モードが実際に変更されます。`dropdown_list`に戻すとき、カスタムでマッチしないテキストはクリアされます。|
|`on_text_changed`|`event_args_t`|文字の実際の変化を表示します。コールバックの来源から最新の`text`を読み取ります。|
|`on_text_input`|`text_input_event_args_t`|編集可能なモードでのテキスト入力には`text`、`handled`が含まれます。|
|`on_item_list_changed`|`event_args_t`|集合の内容が実際に変更され、`item_list`を再読み取りして現在の選択を確認します。|
|`on_selected_index_changed`|`event_args_t`|`selected_index`が実際に変更されます。|
|`on_selection_changed`|`event_args_t`|選択されたインデックスが実際に変更されます。文字の変化は別途`on_text_changed`によって報告されます。|
|`on_row_height_changed`|`event_args_t`|行の高さが変更されます。|
|`on_clear_selection_on_blank_click_changed`|`event_args_t`|空白をクリックして選択を解除するスイッチが変更されます。|

## 実行できるサンプル

「同期周期」を実行して、展開後に「毎15分」を選択すると、状態文字が選択された周期に更新されます。例は業務上の列挙値に基づき、リストに示された選択肢のみを受け入れます。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)をに従いEngineを起動します。以下のコマンドはチュートリアルのリポジトリのルートディレクトリにあるx64デベロッパーCMDで実行されます。例のSDKパスは実際のインストール場所に変更してください。

### C++

```bat
cmake -S examples/guide/controls/collection-and-data/combobox/cpp -B .work/example_combobox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_combobox --config Release
.work\example_combobox\Release\tutorial_combobox.exe
```

Visual Studioのジェネレーターは実行可能ファイルを`Release`のサブディレクトリに置きます。シングルコンフィギネーションのNinjaジェネレーターは直接ビルドディレクトリに出力します。

<<< ../../../../../examples/guide/controls/collection-and-data/combobox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\collection-and-data\combobox\python\run.cmd
```

<<< ../../../../../examples/guide/controls/collection-and-data/combobox/python/combobox_demo.py

### 実行結果

![comboboxの独立したエクスペリエンス](/images/ja/combobox_demo.png)

## よくある質問とレイアウトの実践

- まず`item_list`を入力し、次に`selected_index`を設定するか、`dropdown_list.text`に空でない値を割り当てます。リストを保存する際には`selected_index`または安定したビジネスキーを使用します。
- カスタム入力が許可される場合、`text`を読み取りますが、インデックス`-1`は依然として有効なカスタム文字列に対応する可能性があります。`dropdown_list`に戻す前に、保持したいカスタムテキストを保存してください。
- ドロップダウンのレイヤーに表面スペースを確保してください。SDKは利用可能な領域に応じて項目を表示します。スペースが不足すると見える項目が減少します。必要に応じて`window`を拡大し、`row_height`を調整してください。
- `dropped_down`はプロパティを通じてアクセスします。結果を観察する必要がある場合は`on_selection_changed`または`on_text_changed`を監視してください。

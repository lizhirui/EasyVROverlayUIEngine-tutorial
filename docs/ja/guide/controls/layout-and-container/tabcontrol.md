# tabcontrol

`tabcontrol`は同じ矩形内で複数の`tabpage`を管理します。ページタイトルはそれぞれの`tabpage.text`から取得され、内容はページ自身の`control_list`に配置されます。内容領域を占有するのはアクティブなページのみで、概要、履歴、設定などのタスク間で切り替えに適しています。

継承された一般的なメンバーは[コンテナインターフェース](/ja/guide/controls/common-api#container-control)を参照してください。

## 既定の外観

空`tabcontrol`の`selected_index = -1`。最初のページが追加されると自動的に選択されます。図には「概要」と「履歴」の2つの`tabpage`が追加され、タブの位置は`top`で、サイズはデフォルトの36論理ピクセルです。

![tabcontrolデフォルト外観](/images/ja/tabcontrol_default.png)

## プロパティの比較

左側は`top`を使用して最初のページを表示します。右側は`left`に変更され、タブ領域を広げて第二ページを選択し、第二ページの`text`を「履歴」から「同期記録」に変更し、選択されたタブの背景を変更します。

![tabcontrol属性比較](/images/ja/tabcontrol_comparison.png)

## APIリファレンス

Pythonでは表の属性名を使用します。C++では対応するメソッドを使用して読み書きし、`control_base &source`と表の型の参照を使用してイベントをサブスクライブします。追加フィールドのない`event_args_t`は状態が更新されたことを意味し、コールバックは`source`を使用して新しい値を読み取ります。Pythonの対応するイベントタイプ名は`_t`を省略します。

### プロパティ

|プロパティ|C++|タイプ、デフォルト値、用途|
|---|---|---|
|`page_list`|`get_page_list`|読み取り専用のページ集合のエントリは、初期状態では空です。要素は`tabpage`でなければなりません。|
|`selected_index`|`get_selected_index`、`set_selected_index`|符号付きインデックスで、`-1`は選択されていないことを意味します。最初のページに追加されると自動的に選択されます。合法なインデックスは`-1`または既存のページの0の開始インデックスです。|
|`selected_page`|`get_selected_page`|読み取り専用。選択されたページがない場合、Pythonでは`None`、C++では`nullptr`です。|
|`tab_position`|`get_tab_position`、`set_tab_position`|`top`、`bottom`、`left`、`right`、デフォルトは`top`です。|
|`tab_size`|`get_tab_size`、`set_tab_size`|正の整数で、デフォルトは36論理ピクセルです。上部と下部は対応するタブの高さ、左側と右側は対応するタブの幅です。|
|`tab_font`|`get_tab_font`、`set_tab_font`|タブタイトルのフォントは、SDKのフォントのデフォルト値を継承します。|
|`tab_foreground_color`、`tab_background_color`|`get_tab_foreground_color`、`set_tab_foreground_color`、`get_tab_background_color`、`set_tab_background_color`|通常のタブのテキスト色と背景色。|
|`selected_tab_foreground_color`、`selected_tab_background_color`|`get_selected_tab_foreground_color`、`set_selected_tab_foreground_color`、`get_selected_tab_background_color`、`set_selected_tab_background_color`|選択されたタブのテキスト色と背景色。|
|`page_close_button_visible`|`get_page_close_button_visible`、`set_page_close_button_visible`|デフォルトは偽です。閉じるエントリを表示し、ユーザーがトリガーした後、アプリケーションがリクエストを処理します。|
|`focusable`|`is_focusable`|読み取り専用で、タブとスクロールエントリのフォーカスナビゲーションをサポートします。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`tabcontrol(name)`|`tabcontrol(name)`|構造コントロール。|
|`page_list.add(page)`|`get_page_list().add(page)`|新しいページを追加します。`insert`を使用してインデックスで挿入し、`remove`を使用して取り除き、`clear`を使用してクリアします。|
|`page_list[index]`、`page_list[name]`|`get_page_list()[index]`、`get_page_list()[name]`|インデックスまたは名前で`tabpage`にアクセスします。C++では`get_page(index)`または`get_page(name)`を呼び出すこともできます。|

### イベント

|イベント|パラメータタイプ|トリガー条件|
|---|---|---|
|`on_selected_index_changed`、`on_selection_changed`|`event_args_t`|選択インデックスの実際の変化。ページを削除した後、同じインデックスが別のページを指す可能性があり、集合の変化はページイベントを通じて観察されます。|
|`on_tab_position_changed`、`on_tab_size_changed`、`on_tab_font_changed`|`event_args_t`|タブの位置、サイズ、またはフォントの変更。|
|`on_tab_foreground_color_changed`、`on_tab_background_color_changed`|`event_args_t`|通常のタブの色の変更。|
|`on_selected_tab_foreground_color_changed`、`on_selected_tab_background_color_changed`|`event_args_t`|選択されたタブの色の変更。|
|`on_page_added`、`on_page_removed`、`on_page_text_changed`|`tabpage_event_args_t`|ページの追加、削除、またはタイトルの変更。パラメータ`page`と`index`は、ページとイベントが発生した時のインデックスを指定します。|
|`on_page_close`|`tabpage_event_args_t`|ユーザーが閉じる要求を提出します。保存が確認された後、アプリケーションは`page_list`を通じてページを削除します。|
|`on_page_close_button_visible_changed`|`event_args_t`|タブの閉じるための入力スイッチの実際の変更。|

## tabpage

C++の`tabpage`は`panel`を継承します。Pythonのバインディングは`tabpage`を`container_control`の派生クラスとして公開します。

|メンバー|C++またはイベントパラメータ|用途|
|---|---|---|
|`tabpage(name)`|`tabpage(name)`|ページの構築。|
|`text`|`get_text()`、`set_text(value)`|表示タイトルの読み取りと書き込み、デフォルトでは空文字列です。|
|`control_list`|`get_control_list()`|そのページに本文コントロールを追加します。|
|`on_text_changed`|`event_args_t`|タイトルの変更。ページが`page_list`に追加された場合、所属する`tabcontrol`はページとインデックスを含む`on_page_text_changed`を受け取ります。|

ページ本文コントロールがページの`control_list`に追加される場合、ページ自体が`tabcontrol.page_list`に追加されるか、C++の`get_page_list()`に追加されます。SDKはタブの位置とサイズに基づいてページの利用可能なコンテンツの矩形を計算します。ページ内のコントロールはその領域の左上角に配置されます。

## 実行できるサンプル

“同期ワークステーション”には“概要”と“履歴”の2つの`tabpage`があります。表示後はデフォルトで“概要”が表示され、“履歴”をクリックすると最新の同期結果が表示されます。効果図は2ページ目の本文と選択された色を表示しています。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。以下のコマンドはチュートリアルリポジトリのルートディレクトリのx64開発者CMDで実行されます。サンプルSDKのパスを実際のインストール場所に変更してください。

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/tabcontrol/cpp -B .work/example_tabcontrol -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_tabcontrol --config Release
.work\example_tabcontrol\Release\tutorial_tabcontrol.exe
```

Visual Studioジェネレーターは実行可能ファイルを`Release`のサブディレクトリに置きます。シングルコンフィギュレーションのNinjaジェネレーターは直接ビルドディレクトリに出力します。

<<< ../../../../../examples/guide/controls/layout-and-container/tabcontrol/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\tabcontrol\python\run.cmd
```

<<< ../../../../../examples/guide/controls/layout-and-container/tabcontrol/python/tabcontrol_demo.py

### 実行結果

![tabcontrol独立例程効果](/images/ja/tabcontrol_demo.png)

## よくある質問とレイアウト実践

- ページを追加した後に`selected_index`を設定します。任意の位置のページを削除する場合は、オブジェクトや名前を使用してページを参照し、削除前に保存された古いインデックスを使用しないようにします。
- コンテンツコントロールを対応する`tabpage`に配置します。タブのサイズが大きくなるとコンテンツエリアもそれに応じて縮小され、サイドタブには完全なタイトルと閉じるボタンの幅を確保する必要があります。
- 閉じるための入力スイッチが`on_page_close`の通知を生成します。ページの未保存状態に応じていつ削除するかを決定し、`on_page_removed`を通じて集合が変更されたことを確認します。
- `tabpage.text`を使用して表示タイトルを変更し、ビジネスロゴには構築名または`tag`を使用します。

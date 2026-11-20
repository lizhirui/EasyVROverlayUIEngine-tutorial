# 共通インターフェース

各コントロールの章では、タイプ特有のメンバーが列挙されています。以下の表では、各サンプルで使用される継承インターフェースを説明しています。色は`0xRRGGBBAA`を使用し、矩形のサイズは論理ピクセルで表現されています。

## control_base

|プロパティ|C++|用途|
|---|---|---|
|`name`、`type`、`id`|`get_name`、`get_type`、`get_id`|読み取り専用、構築名、コントロールタイプ、実行時番号|
|`tag`|`get_tag`、`set_tag`|定義された文字列マーカーを適用|
|`parent`|`get_parent`|読み取り専用、直接の親オブジェクト|
|`disposed`|`get_disposed`|読み取り専用、解放されているかどうか|

|メソッド|用途|
|---|---|
|`invalidate()`|再描画の要求|
|`dispose()`|コントロール関連リソースの解放|
|`begin_invoke(callback)`|パラメータのないコールバックを所属するUIスレッドに配布|

|イベント|パラメータと用途|
|---|---|
|`on_tag_changed`、`on_disposed`|`event_args_t`、変更または解放が完了したことをマーク|
|`on_property_changed`|`property_changed_event_args_t`、変更されたプロパティ名を読み取る|

## control

|プロパティ|C++|用途|
|---|---|---|
|`rect`|`get_rect`、`set_rect`|論理的な矩形、左、上、幅、高さで構成される|
|`background_color`|`get_background_color`、`set_background_color`|コントロールの背景色、具体的なコントロールの描画規則に従って表示される|
|`tooltip_text`|`get_tooltip_text`、`set_tooltip_text`|ハイライトテキスト、空文字列でハイライトをオフにする|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|表示とインタラクティブなオン/オフ|
|`tab_index`|`get_tab_index`、`set_tab_index`|フォーカス可能なコントロールのTab順序、初期値は0|
|`focusable`、`focused`|`is_focusable`、`get_focused`|読み取り専用、コントロールがフォーカスを取得できるか、現在フォーカスを持っているか|
|`absolute_rectangle`|`get_absolute_rectangle`|読み取り専用、解析後の表面内矩形|
|`owning_window`|`get_owning_window`|読み取り専用、所属する`window`|

|メソッド|用途|
|---|---|
|`show()`、`hide()`|コントロールの表示または非表示|
|`focus()`|フォーカスを取得する要求|
|`activate()`|プログラム化されたアクティブ化パス。イベントの動作はコントロールタイプと利用可能な状態によって決定される|

|イベント|パラメータと用途|
|---|---|
|`on_tooltip_text_changed`、`on_background_color_changed`、`on_visible_changed`、`on_enabled_changed`、`on_tab_index_changed`|`event_args_t`、対応する共有プロパティが実際に変更されたことを示す|
|`on_moved`、`on_size_changed`、`on_viewport_changed`|`event_args_t`、位置、サイズ、または視野の変更|
|`on_pointer_enter`、`on_pointer_leave`、`on_pointer_move`、`on_pointer_down`、`on_pointer_up`|`pointer_event_args_t`、指が入る、離れる、移動する、押す、または離れる|
|`on_click`|`event_args_t`、コントロールのアクティブ化イベント|
|`on_scroll`|`scroll_event_args_t`、スクロール入力|
|`on_focus_in`、`on_focus_out`|`event_args_t`、フォーカスを取得または失う|
|`on_key_down`、`on_key_up`|`key_event_args_t`、キーが押されたり離されたりする|

## text_control

|プロパティ|C++|用途|
|---|---|---|
|`foreground_color`|`get_foreground_color`、`set_foreground_color`|テキストの前景色|
|`font`|`get_font`、`set_font`|フォント族、サイズ、太字、斜体。Pythonでは`font`を使用し、C++では`font_t`を使用する|

|イベント|パラメータと用途|
|---|---|
|`on_foreground_color_changed`、`on_font_changed`|`event_args_t`、対応するスタイルプロパティの変更|

## container_control

|プロパティ|C++|用途|
|---|---|---|
|`control_list`|`get_control_list`|読み取り専用の集合エントリ。`add`、`insert`、`remove`、`clear`を使用して所属を変更|
|`active_item_list`|`get_active_item_list`|読み取り専用、現在のコンテナのアクティブなサブコントロールリストを返す|

|イベント|パラメータと用途|
|---|---|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`、コントロールとその位置を含む|

## item_control

`combobox`と`listbox`は`item_control`と`selection_control`を継承する。`item_list`を使用して`item_collection`にアクセスする。集合内の文字列は重複可能で、選択は項目インデックスで表される。

|操作|Python|C++|
|---|---|---|
|追加と挿入|`add(text)`、`insert(index, text)`|`add(text)`、`insert(index, text)`|
|削除とクリア|`remove(text)`、`remove_at(index)`、`clear()`|`remove(text)`、`remove(index)`、`clear()`|
|全項目の置換|コントロールの`item_list`全体に値を代入|`get_item_list().assign(value_list)`|
|数量、空状態、メンバーの照会|`len(collection)`、`bool(collection)`、`text in collection`|`get_size()`、`is_empty()`、`contains(text)`|
|項目のアクセスとインデックスの検索|`collection[index]`、`index_of(text)`|`collection[index]`、`get_item(index)`、`get_index(text)`|

C++とPythonのイベントサブスクリプションは`+=`をサポートし、コールバックは`source`と`event`を受け取ります。Pythonイベントパラメータのタイプ名には`_t`の接尾辞を省略します。イベントと所有権の詳細な署名については[C++ API](/ja/reference/cpp_api)および[Python API](/ja/reference/python_api)を参照してください。

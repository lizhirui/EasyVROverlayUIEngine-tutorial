# window

`window`はEngineに送信されるトップレベルの空間表面であり、子コントロールのコンテナでもあります。設定ツール、状態パネル、モダルダイアログはすべて`window`から始まります。各`window`は独立したサイズ、表示状態、空間参照オブジェクトを持っています。

[公共コントロールインターフェース](/ja/guide/controls/common-api#control)および[コンテナインターフェース](/ja/guide/controls/common-api#container-control)を継承します。

## 既定の外観

新しい`window`を作成する際のタイトルは構築名から取得され、論理サイズは640×360で、状態は非表示、参照オブジェクトは`world`です。`show()`を呼び出すと、タイトルバーにデフォルトのアイコンが表示され、追跡選択エントリと閉じるエントリが表示されます。スクリーンショットでは表面のサイズのみ調整され、`label`で観察項目が示されています。

![windowデフォルト外観](/images/ja/window_default.png)

## プロパティの比較

|位置|属性の変更|観察結果|
|---|---|---|
|左上|デフォルトのタイトルバー|標準タイトル、追跡選択エントリ、閉じるエントリを表示|
|右上|`title_foreground_color`、`title_background_color`、`title_font`|タイトルを暖色系の太字に変更し、タイトルバーの背景を独立して設定|
|左下|`show_close_button = False`|タイトルバーを非表示にする閉じるエントリ|
|右下|`show_title_bar = False`|タイトルバー全体を非表示にし、コンテンツエリアを上に移動可能|

![window属性比較](/images/ja/window_comparison.png)

## APIリファレンス

C++属性は表内のアクセスメソッドで読み書きされ、Pythonは同名の属性でアクセスされます。表内のイベントパラメータはC++の型名を使用し、Pythonの対応する型には`_t`の接尾辞を省略します。公共メンバーは[基本インターフェース](/ja/guide/controls/common-api)を参照してください。

### プロパティ

|プロパティ|C++|用途と既定値|
|---|---|---|
|`title`|`get_title`、`set_title`|タイトル文字は、初期状態で構築名です。|
|`title_foreground_color`、`title_background_color`|`get_title_foreground_color`、`set_title_foreground_color`、`get_title_background_color`、`set_title_background_color`|タイトル文字と背景色は、それぞれデフォルトで`0xFFFFFFFF`と`0x244565FF`です。アクティブ状態もタイトルバーの色を変更します。|
|`title_font`|`get_title_font`、`set_title_font`|タイトルフォントは、デフォルトでSegoe UI、20の論理ピクセルです。|
|`icon`|`get_icon`、`set_icon`|タイトルアイコンは、初期状態でSDKアイコンで、`None`に設定するか`shared_ptr`を空にすることで削除できます。|
|`menu`|`get_menu`、`set_menu`|タイトルバーの下のコマンドエリアに関連する`menubar`は、初期状態で空です。|
|`show_title_bar`、`show_close_button`|`get_show_title_bar`、`set_show_title_bar`、`get_show_close_button`、`set_show_close_button`|タイトルバーと標準の閉じるエントリの表示スイッチは、初期状態で真です。|
|`tracking_mode_set`|`get_tracking_mode_set`、`set_tracking_mode_set`|タイトルバーの切り替えモードを許可するもので、デフォルトでは`world`、`body`、`left`、`right`、`head`が含まれます。空の集合はエントリを非表示にします。|
|`movable`、`resizable`、`curvature_adjustable`|`get_movable`、`set_movable`、`get_resizable`、`set_resizable`、`get_curvature_adjustable`、`set_curvature_adjustable`|ハンドルによる移動と回転、インタラクティブなズーム、インタラクティブな曲率調整をそれぞれ制御し、初期状態では真です。|
|`physical_scale`|`get_physical_scale`、`set_physical_scale`|正の有限ズーム倍率は、初期状態で1.0です。各論理ピクセルの基準は1ミリメートルで、初回表示時にはソースから明示的に設定されていないズームを継承できます。|
|`physical_width`、`physical_height`|`get_physical_width`、`get_physical_height`|只读、表面の展開幅と高さ、単位はメートルです。|
|`curvature`|`get_curvature`、`set_curvature`|曲率、単位はメートルの逆数、デフォルトでは0.0は平面です。曲率と展開幅の積は`2π`未満でなければなりません。|
|`position`、`rotation`|`get_position`、`set_position`、`get_rotation`、`set_rotation`|初期値はすべて0です。位置は参照対象の左上角からの偏移、単位はメートル、回転はXYZオイラー角、単位は度です。|
|`startup_position`|`get_startup_position`、`set_startup_position`|初回位置設定方法、デフォルトは`center`です。`none`では設定された参照対象と姿勢を使用します。|
|`reference_object`|`get_reference_object`、`set_reference_object`|空間参照対象、デフォルトは`world`です。|
|`world_transform`|`get_world_transform`|読み取り専用、表面中心の世界姿勢を示します。参照が使用できない場合は`None`または空の`optional`を返します。|
|`loaded`、`closed`|`get_loaded`、`get_closed`|只读、それぞれ初回の読み込み完了および閉じたことを示します。初期値は偽です。|
|`auxiliary`|`get_auxiliary`、`set_auxiliary`|補助表面マーク、初期値は偽です。IMEとレイアウトセッション中の表面はEngineによって入力エリアに関連付けられます。|
|`dialog_result`|`get_dialog_result`、`set_dialog_result`|初期値は`none`です。モーダル期間中に有効な結果が与えられるとウィンドウが閉じられ、その結果が返されます。|
|`visible`、`rect`|`get_visible`、`set_visible`、`get_rect`、`set_rect`|継承された表示状態と論理矩形。構築後は隠れ、初期サイズは640×360です。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`window(name)`|`window(name)`|トップレベルの表面を構築します。|
|`show()`、`hide()`|`show()`、`hide()`|表面の表示と非表示。初回`show()`で読み込みがトリガーされ、その後の表示と非表示はウィンドウを保持します。|
|`close(force=False)`|`close(force=false)`|閉じる要求。閉じたかどうかを返し、強制的な閉じる場合はキャンセルプロセスをスキップします。|
|`activate()`|`activate()`|既存の表面をアクティブにする要求。|
|`show_dialog(owner_window)`|`show_dialog(owner_window)`|自身のモーダルループを同期して実行し、一時的に直接所有者のインタラクションを阻止します。閉じる際は`dialog_result`を返します。|
|`set_size(width,height)`|`set_size(width,height)`|正の論理幅と高さを設定します。|
|`reparent(reference,keep_world=False)`|`reparent(reference,keep_world=false)`|参照対象を切り替え、世界姿勢を保存することができます。|
|`is_tracking_available(mode)`|`get_is_tracking_available(mode)`|指定された参照対象が使用可能かどうかを問い合わせます。|
|`center_at_view(distance)`|`center_at_view(distance)`|指定されたメートル数で視線前方に中央に配置し、位置設定結果を返します。|
|`get_default_icon()`|`get_default_icon()`|静的なメソッドで、SDKのデフォルトアイコンを取得します。|

### イベント

|イベント|発生条件と引数|
|---|---|
|`on_title_changed`、`on_title_foreground_color_changed`、`on_title_background_color_changed`、`on_title_font_changed`|タイトル文字、配色、またはフォントが変更されます。|
|`on_icon_changed`、`on_menu_changed`|アイコンまたは関連する`menubar`が変更されます。|
|`on_show_title_bar_changed`、`on_show_close_button_changed`、`on_tracking_mode_set_changed`|タイトルバー、閉じる入口、またはトラッキング選択集合が変更されます。|
|`on_movable_changed`、`on_resizable_changed`、`on_curvature_adjustable_changed`|空間インタラクションのスイッチが変更されます。|
|`on_rotation_changed`、`on_curvature_changed`、`on_startup_position_changed`、`on_reference_object_changed`|回転、曲率、位置設定方法の開始または参照対象が変更されます。3D位置の変更は継承された`on_moved`を使用します。|
|`on_load`、`on_shown`、`on_hidden`|それぞれ初回の読み込み、表示、非表示時にトリガーされます。|
|`on_closing`、`on_closed`|閉じる前は`cancel_event_args_t`を使用し、`cancel`を設定できます。成功後は`on_closed`をトリガーします。|
|`on_render_failed`|描画の送信に失敗した場合、パラメータは`render_error_event_args_t`です。|
|`on_tracking_lost`、`on_tracking_restored`|参照対象が失われたり復元されたりします。|
|`on_activated`、`on_deactivated`|現在の表面がアクティブになったり、アクティブにならなかったりします。|
|`on_move_start`、`on_move_end`、`on_resize_start`、`on_resize_end`、`on_curvature_adjust_start`、`on_curvature_adjust_end`|インタラクティブな移動、スケーリング、曲率の調整の開始と終了。終了イベントは`interaction_end_event_args_t`を使用します。|

## 実行できるサンプル

起動後に「タイトル色を切り替え」を押すと、タイトルバーの背景が変わります。もう一度押すと初期の配色に戻ります。ウィンドウを閉じるとイベントループが終了します。

[環境構築・ビルド・インストール](/ja/basics/01_install_and_setup)の手順でEngineを起動します。チュートリアルのリポジトリのルートで、MSVCを設定したx64用の開発者コマンドプロンプトを開きます。SDKのパスは実際のインストール先に置き換えます。

### C++

```bat
cmake -S examples/guide/controls/window-and-text/window/cpp -B .work/example_window -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_window --config Release
.work\example_window\Release\tutorial_window.exe
```

上記の実行ファイルのパスはVisual Studioジェネレーターに対応しています。単一構成のNinjaを使用する場合、実行ファイルは直接ビルドディレクトリにあります。

<<< ../../../../../examples/guide/controls/window-and-text/window/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\window\python\run.cmd
```

<<< ../../../../../examples/guide/controls/window-and-text/window/python/window_demo.py

### 実行結果

![ウィンドウの独立した実行例の効果](/images/ja/window_demo.png)

## よくある問題と実装上の注意

- 論理座標と物理位置は別々に設定します。物理配置の変更には`position`、`rotation`、`reference_object`を使用し、コントロールのレイアウト調整には`rect`または`set_size()`を使用します。
- 最初のフレームの位置を明示的に制御する場合は、まず`startup_position = none`を設定します。既存の表面が参照系を変更し、位置を保持している場合は`reparent(..., keep_world=True)`を使用します。
- `hide()`は一時的に非表示に適しています。`close()`はインスタンスのライフサイクルを終了し、同じインターフェースを開くときに新しいインスタンスを作成します。標準のクローズ入口を隠した後、アプリケーションのフロー内で明確なクローズ操作を保持する必要があります。
- `show_dialog()`は、同じアプリケーション内で相互作用可能な他の`window`を所有者として使用します。ダイアログインスタンスは、最初に表示される前にモダルモードに入るべきです。

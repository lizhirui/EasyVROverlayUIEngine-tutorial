# Python APIリファレンス

コントロールの使用法と完全な例は[コントロールカタログ](/ja/guide/)を参照してください。ウィンドウ、イベント、スレッドスケジューリングについては、それぞれ[window](/ja/guide/controls/window-and-text/window)と[強制型イベントとマルチスレッドスケジューリング](/ja/guide/07_events_dialogs_threading)をご覧ください。

通常のコントロールのnameは`type_用途`を使用し、例えば`button_ok`です。デザイナーからエクスポートされたパブリックコントロールのメンバーのnameは同じ名前で、`button_ok`を通じて直接アクセスできます。フォームクラス名はデザインファイル名に対応しています。

この記事では`easyvrui`のパブリックインターフェースと呼び出し規則について説明します。メソッドシグネチャーは`self`を省略します。

## 1.インポートと実行の規約

### 1.1.アプリケーションの構成

インストール後のPythonアプリケーションは、インストールルートディレクトリ内の`sdk/api/python/`を使用します。このディレクトリには`easyvrui/`、静的リンク版の`engine_interface_native*.pyd`、拡張モジュールの記述ファイル`engine_interface_native.json`、`requirements.txt`が含まれます。インタプリタは、インストール記録に記載されたCPythonバージョンとx64アーキテクチャに一致している必要があります。DesktopまたはFile ManagerがSDKを通じてリストを起動する際、サブプロセスの`PYTHONPATH`はこのディレクトリを先に指定し、元の値を保持します。`EASYVRUI_NATIVE_DIR`もこのディレクトリを指します。CMDから直接例を実行する場合、まずこのディレクトリを`PYTHONPATH`に先に指定します。

ソースから開発する場合は、同じ構成で`repo/sdk/engine_interface/build.bat`と`repo/sdk/api/python/build.bat`を実行します。`repo/sdk/api/python/`をモジュール検索パスに追加し、`EASYVRUI_NATIVE_DIR`に`repo/sdk/api/python/build/bin/`を指定します。ローダーは`EASYVRUI_ENGINE_INTERFACE`が指すライブラリの親ディレクトリからも拡張を検索します。DLLリンク版の拡張には、対応する`engine_interface.dll`が必要です。

Python APIの実行部分は、標準ライブラリとプレコンパイルされた拡張を使用します。自分のPython依存関係は、対応するアプリケーンディレクトリ内の`requirements.txt`に記録します。サンプルアプリケーションは`repo/app/demo/python`にあり、そのコントロール派生クラスはアプリケーンスンプルに属しています。

```python
from easyvrui import button, rect, run, window

window_main = window("window_main")
window_main.title = "Example"
button_ok = button("button_ok")
button_ok.rect = rect(40, 90, 180, 44)
button_ok.text = "OK"
window_main.control_list.add(button_ok)
window_main.show()
run("example")
```

### 1.2.モジュールと名前空間

`import easyvrui`はパブリックエントリーを提供します。サブモジュール内のコントロールと値型は、同じネイティブクラスを参照します。

|インポート位置|パブリックインターフェース|
|---|---|
|`easyvrui`|コントロール、値型、イベント、グラフィック、ダイアログボックス、アプリケーション関数、入力コンポーネント|
|`easyvrui.application`|`run`、`set_application_name`、`pump`、入力インターフェースおよびアプリケーンマネージング関数|
|`easyvrui.application_management`|アプリケーンリスト、起動、実行スナップショットおよびセッションとウィンドウ管理|
|`easyvrui.control`|コントロールおよびその集合|
|`easyvrui.common.color/rect/font`|色、矩形、フォント|
|`easyvrui.common.error`|言語選択とローカライゼーションエラー|
|`easyvrui.geometry`|`vec3`、`quat`、`pose`|
|`easyvrui.dialog`|標準ダイアログボックス関数、ファイルフィルタリングおよびメッセージボックスの一覧|
|`easyvrui.event`|`event_container`および強制型イベントパラメータ|
|`easyvrui.render`|`render_context`、`drawing_path`、`drawing_image`、`drawing_fill_rule`|
|`easyvrui.input`|`input_provider`、ロール、入力イベント、コンポーネント状態|

以下の表は`easyvrui`のトップレベルアプリケーンフェイスをリストしています。

|名前|名前|名前|名前|
|---|---|---|---|
|`application_entry`|`application_runtime`|`application_snapshot`|`application_type`|
|`application_window`|`blank`|`button`|`cancel_event_args`|
|`checkbox`|`close_application_window`|`color`|`color_dialog`|
|`combobox`|`combobox_dropdown_style`|`container_control`|`control`|
|`control_base`|`control_collection`|`control_collection_event_args`|`control_input_event_args`|
|`control_input_type`|`controller_event_args`|`dialog_result`|`drawing_fill_rule`|
|`drawing_image`|`drawing_path`|`drawing_path_operation`|`drawing_path_segment`|
|`engine_error`|`error_diagnostic`|`error_key`|`event_args`|
|`event_container`|`file_filter`|`file_open_dialog`|`file_save_dialog`|
|`font`|`font_dialog`|`get_application_directory`|`get_application_snapshot_list`|
|`get_error_diagnostic`|`get_error_language`|`get_error_message`|`get_language_key`|
|`get_localized_error`|`get_preferred_ui_language`|`get_reference_object_type_name`|`grid`|
|`grid_cell`|`grid_cell_event_args`|`grid_cell_render`|`grid_column`|
|`grid_column_event_args`|`grid_selection_mode`|`hide_input_ui`|`image`|
|`image_stretch_mode`|`input_event`|`input_event_type`|`input_provider`|
|`input_provider_state`|`input_role`|`input_ui_state`|`inputbox`|
|`interaction_end_event_args`|`item_collection`|`item_control`|`key_event_args`|
|`keyboard_key`|`keyboard_modifier`|`label`|`language_key`|
|`language_pack`|`launch_application`|`listbox`|`listview`|
|`listview_cell_collection`|`listview_column`|`listview_column_collection`|`listview_column_event_args`|
|`listview_item`|`listview_item_collection`|`listview_item_event_args`|`localized_invalid_argument`|
|`localized_runtime_error`|`measure_text`|`menu_container`|`menu_item_event_args`|
|`menubar`|`menuitem`|`messagebox`|`messagebox_button`|
|`messagebox_button_set`|`messagebox_icon`|`numericupdown`|`orientation`|
|`panel`|`parse_keyboard_key`|`parse_reference_object_type`|`pointer_event_args`|
|`pose`|`progressbar`|`property_changed_event_args`|`provider_info`|
|`pump`|`quat`|`radiobutton`|`read_application_entry`|
|`rect`|`reference_object`|`reference_object_type`|`render_context`|
|`render_error_event_args`|`render_rectangle`|`render_style`|`request_application_snapshot_list`|
|`request_close_application_window`|`request_error`|`request_terminate_application`|`run`|
|`screen`|`scroll_event_args`|`scrollpanel`|`select_error_language`|
|`selection_control`|`set_application_name`|`show_input_ui`|`slider`|
|`splitter`|`startup_position`|`tab_position`|`tabcontrol`|
|`tabpage`|`tabpage_collection`|`tabpage_event_args`|`terminate_application`|
|`text_control`|`text_input_event_args`|`textbox`|`toolbar`|
|`toolbar_button`|`toolbar_button_collection`|`tree_node`|`tree_node_collection`|
|`tree_node_event_args`|`treeview`|`vec3`|`window`|

### 1.3.デザインファイルのエクスポートレイアウト

生成されたPythonのレイアウトファイルでは`import easyvrui`を使用します。すべての非rootコントロールは`self.<control.name>`で公開され、属性名はコントロール名と完全に一致します。名前は設計全体で一意であり、C++とPythonの識別子規則に従い、root SDKの公開エントリを避けています。

生成されたクラス自体は`__init__`のみであり、デフォルトの名前は設計のルートノードの名前を使用します。例えば`def __init__(self, name = "sample_form"):`です。コンストラクタはコントロールを作成し、`control_list`または`page_list`を使用して所属関係を確立し、属性と値の記録を初期化します。

画像とアイコンは`easyvrui.drawing_image.load_file()`などのSDKの描画リソースインターフェースを呼び出します。ビジネスクラスはフォームインスタンスを持ち、同名の属性を使用してイベントをバインドし、コントロールの属性を読み取りおよび変更します。

Form Designerは独立したアプリケーションであり、設計ファイルの拡張子は`.easyvruifrm`で、PythonとC++の設計コードをエクスポートできます。propertygrid属性パネルはこのアプリケーション内で派生されたコントロールであり、一般的なアプリケーションでは一般的なgridを使用します。生成されたPythonの設計クラスは、公開APIを使用してコントロールを作成し、属性を設定し、コンテナを組み立てます。

### 1.4.パラメータ、戻り値、データタイプ

インターフェーステーブルはPythonのタイプで記述されます。バインドで明確に名前が宣言されているパラメータは、キーワード実参を使用できます。一部の直接マッピングされたメソッドは、位置パラメータのみ登録されています。以下の署名での`/`は、位置に従って呼び出されるべきであり、関数署名の位置パラメータに基づいています。

|タイプ|呼び出し規約|
|---|---|
|`str`|Unicodeテキスト；コントロール名、表示テキスト、フォントファミリーなどは通常のPython文字列を使用します。|
|`int`|無符号64ビットフィールドは`0`から`2**64-1`を受け入れます。色は`0`から`2**32-1`を受け入れます。有符号64ビットフィールドは`-(2**63)`から`2**63-1`を受け入れます。|
|`float`|対応する双精度数値；空間位置、回転角度、スケーリング、および描画座標は、インターフェースの要求に従って有限性と範囲をチェックします。|
|`bool`|スイッチ；アプリケーションコードは`True`または`False`を渡すべきです。|
|`None`|オブジェクトがない、選択項目がない、または選択可能な値が欠けている場合；具体的な意味は対応するインターフェースを参照してください。|
|`list`、`set`|属性から読み取る際は通常、スナップショットが得られます。スナップショットを変更した後は、属性に再代入する必要があります。専用の集合タイプについては、集合の章を参照してください。|

テキスト位置はUnicodeコードポイントでカウントされ、Pythonの`len(text)`とスライスインデックスと一致します。組み合わせ文字、バリアントセレクタ、および複数のコードポイントエモーションは複数の位置を占める可能性があります。ユーザーインタラクションでのカーソルの移動と削除は、テキスト境界に従って処理されます。プログラムがセレクタを設定する際は、合法的なテキスト位置を使用する必要があります。

### 1.5.オブジェクト、スレッド、および更新

スレッドを作成し、コントロールとウィンドウを操作する。コンテナ内のオブジェクトは同じアプリケーション実行環境に属する。`begin_invoke()`は他のスレッドからスレッド上の作業を計画するために使用され、実際の実行はアプリケーションが`run()`または`pump()`を継続して呼び出すことに依存する。コールバックはできるだけ早く返されるべきであり、時間がかかる作業はバックグラウンドスレッドに移行し、`begin_invoke()`を通じてコントロールを更新する。

通常のコントロールのコンストラクタは`型(name: str)`に統一される。`name`は空であってはならず、空の文字を含んではならない。構築後は読み取り専用である。同じ集合内では名前は一意であり、重複して名前を追加すると例外が発生する。一つのコントロールには一つの親コンテナのみが存在し、ループ親子関係を形成してはならない。

コントロールのプロパティはアプリケーション内で読み書きされる。表示に影響を与えるプロパティの変更は再描画を計画する。カスタムの描画は通常のPythonメンバーの変更後に`invalidate()`を呼び出す。アプリケーションは入力、イベント、および送信待ちの更新をループ処理する。`render()`が返された後、この描画はフレームワークによって一括で送信される。描画コールバックでは、描画インターフェースを順番に呼び出す。

## 2.基本値タイプ

### 2.1.rect

インポート。`from easyvrui import rect`。

構築。`rect(left: int = 0, top: int = 60, width: int = 160, height: int = 40)`。

|メンバー|読み書き|用途|
|---|---|---|
|`left: int`|読み書き|論理矩形の左位置|
|`top: int`|読み書き|論理矩形の上位置|
|`width: int`|読み書き|論理幅|
|`height: int`|読み書き|論理高さ|
|`a == b -> bool`|演算子|フィールドごと比較|

4つのフィールドはすべて符号付き64ビット整数である。独立した`rect`オブジェクトは自身の値を保存する。`control.rect`から取得したオブジェクトはそのコントロールに関連するビューであり、したがって`button_ok.rect.left = 80`は直接コントロールを更新する。独立した矩形を`control.rect`に割り当てる際は値に従って書き込む。コントロールの矩形は`width > 0`、`height > 0`を要求する。

通常のサブコントロールの位置は親コンテナに対してである。ウィンドウの`rect.left/top`は空間位置に参加せず、ウィンドウの位置は`position`を使用する。

### 2.2.color

構築は`color(value: int | color = 0)`である。色の整数は`0xRRGGBBAA`を使用し、高さは24ビットでRGB、最低8ビットは透明度である。透明度`0`は完全に透明で、`255`は完全に不透明である。

|メンバー|用途|
|---|---|
|`value: int`|完全な色値を読み書きし、範囲は符号付き32ビット整数である|
|`r: int`、`g: int`、`b: int`、`a: int`|赤、緑、青、透明度の成分を読み書きし、範囲は`0`から`255`である|
|`rgba: list[int]`|読み取り専用で、赤、緑、青、透明度を順番に返す|
|`hex_string: str`|読み取り専用で、`0x`プレフィックス付きの8ビット16進色テキスト|
|`color.create_from_rgba(r: int, g: int, b: int, a: int = 255) -> color`|4つの成分で色を構築する|
|`color.create_from_hex(text: str) -> color`|8ビット16進色テキストを解析し、`0x`プレフィックスをサポートする|
|`create_with_alpha(alpha: int, /) -> color`|透明度を置換した後の新しい色を返す|
|`int(value)`、`value.__index__()`|完全な色の整数を取得する|
|`str(value)`|16進数色文字の取得|
|`a == b`|完全な色値の比較|

コントロールの色属性は色の整数と`color`オブジェクトを受け入れ、読み取り時には`int`を返します。描画メソッドの色パラメータは整数を使用し、`int(color_object)`で変換できます。

### 2.3.font

`font(family: str = "Segoe UI", size: int = font.DEFAULT_SIZE, bold: bool = False, italic: bool = False)`として構築されます。クラス定数`font.DEFAULT_SIZE`は`18`です。

|メンバー|用途|
|---|---|
|`family: str`|システムフォントの名前の読み取りと書き込み|
|`size: int`|無符号64ビット整数の論理サイズの読み取りと書き込み|
|`bold: bool`|太字の状態の読み取りと書き込み|
|`italic: bool`|斜体の状態の読み取りと書き込み|
|`a == b`|フィールドごと比較|

フォントをコントロールに割り当てる際、`family`は空ではなく、空文字を含まない必要があり、`size`は`0`より大きくなければなりません。コントロールの`font`属性を読み取ると、独立したフォント値が得られます。サイズを変更する際には、まず`style = textbox_text.font`を取得し、次に`style.size = 22`を設定し、`style`をコントロールに戻します。

### 2.4.vec3

`vec3(x: float = 0.0, y: float = 0.0, z: float = 0.0)`として構築されます。`x/y/z`は読み取りと書き込みが可能です。

|メンバー|用途|
|---|---|
|`a == b`|成分ごとの近似比較|
|`a + b -> vec3`、`a - b -> vec3`|成分ごとの加減算|
|`value * scalar -> vec3`、`scalar * value -> vec3`|スカラー倍算|
|`calculate_dot_product(other: vec3, /) -> float`|点積|
|`calculate_cross_product(other: vec3, /) -> vec3`|叉積|
|`length: float`|読み取り専用、ベクトルの長さ|
|`normalized: vec3`|読み取り専用、同じ方向の単位ベクトルを返す。方向が0、小さすぎる、または非有限値を含む場合は例外を投げる|
|`vec3.is_equal(left: float, right: float) -> bool`|双精度epsilonと数値のサイズで二つのスカラーを近似比較する|

空間位置はメートルで、ウィンドウのオイラー角は度で表される。ウィンドウ位置を変更する際は全体を割り当てる、例えば`window_main.position = vec3(0.1, 0.0, 0.0)`。

### 2.5.quat

`quat(x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0)`として構築されます。`x/y/z/w`は読み取りと書き込みが可能で、デフォルト値は単位回転を表します。

|メンバー|用途|
|---|---|
|`a * b -> quat`|回転を組み合わせる、まず`b`を適用し、次に`a`を適用する|
|`length: float`|読み取り専用、四元数の長さ|
|`normalized: quat`|読み取り専用、単位四元数|
|`inverse: quat`|読み取り専用、逆回転|
|`euler: vec3`|読み取り専用、度で表されるXYZオイラー角|
|`rotate(value: vec3, /) -> vec3`|回転ベクトル|
|`slerp(target: quat, amount: float) -> quat`|四元数の最短弧に沿って補間し、進捗`0.0`は現在の回転に対応し、`1.0`は目標回転に対応する|
|`quat.create_from_axis_angle(axis: vec3, angle: float) -> quat`|指定された単位軸を中心に回転し、角度は度単位|
|`quat.create_from_axis_basis(a: vec3, b: vec3, c: vec3, /) -> quat`|回転後の3つの直交基軸から回転を構築する|
|`quat.create_from_euler(angles: vec3) -> quat`|度で表されるXYZオイラー角から回転を構築する|

オイラー角の組み合わせは`Rz * Ry * Rx`を満たす。`euler`を読み取ると、等価な角度が得られる可能性があります。

### 2.6.pose

`pose(position: vec3 = vec3(), rotation: quat = quat())`として構築されます。`position/rotation`は読み取りと書き込みが可能です。

|メンバー|用途|
|---|---|
|`a * b -> pose`、`a @ b -> pose`|姿勢を組み合わせる、まず`b`を適用し、次に`a`を適用する|
|`inverse: pose`|読み取り専用、逆姿勢|
|`matrix: tuple[tuple[float, ...], ...]`|読み取り専用、行ごとに4×4のホモジニアス変換行列を返す、最後の列には平行移動成分が含まれる|
|`transform_point(value: vec3, /) -> vec3`|局所点をその姿勢の参照系に変換する|

ウィンドウの設定可能な位置と回転はそれぞれ`position`と`rotation`である

## 3.コントロールはツリーと共通規約を継承する

```text
control_base
└── control
    ├── blank
    ├── text_control
    │   ├── button
    │   │   └── toolbar_button
    │   ├── checkbox
    │   ├── selection_control
    │   │   ├── item_control
    │   │   │   ├── combobox
    │   │   │   └── listbox
    │   │   ├── grid
    │   │   ├── listview
    │   │   └── treeview
    │   ├── label
    │   ├── numericupdown
    │   ├── radiobutton
    │   ├── textbox
    ├── container_control
    │   ├── menu_container
    │   │   ├── menubar
    │   │   └── menuitem
    │   ├── panel
    │   │   └── tabpage
    │   ├── scrollpanel
    │   ├── splitter
    │   ├── tabcontrol
    │   ├── toolbar
    │   └── window
    ├── image
    ├── progressbar
    ├── screen
    └── slider
```

派生物クラスは祖先が公開する属性、メソッド、イベントを継承する；blankのインスタンスの隠蔽ルールは対応する章を参照。通常のコントロールは`型(name: str)`で作成される。`control_base`はPython派生物クラスに`super().__init__(name: str, type: str)`を提供し、control_baseインスタンスを直接作成するとTypeErrorが発生する。`menu_container(name: str, type: str)`はメニューコンテナの基類の構築入口を提供する。Pythonコントロールの派生方法は「描画とカスタムコントロール」を参照。

Pythonアクセスアダプターは`control/text_control/selection_control/item_control/container_control`の`(name: str, type: str)`構築をオーバーライドし、カスタム派生物タイプがタイプ名を指定するためのものである；これらのタイプの単引数構築はそれぞれのネイティブタイプ名を使用する。

### 3.1.属性アクセス

ドットを使用して属性を読み取り、例えば`textbox_entry.text`、代入を使用して可読属性を変更、例えば`textbox_entry.text = "Hello"`。

`control_list`と`page_list`は直接操作可能な集合の入口であり、集合メソッドを使用して所属を変更する。`item_list`は文字列項目が直接操作可能な集合であり、全体の代入でテキストリストを置き換えることができる。他の通常のリストや集合属性は通常スナップショットを返し、変更後には再代入が必要である。イベントメンバーは`+=/-=`を使用して購読する。

### 3.2.control_base

Python派生物クラスはコンストラクタで`super().__init__(name, type)`を呼び出してネイティブ基類の初期化を完了する。

|属性|読み書き|用途|
|---|---|---|
|`name: str`|読み取り専用|構築時に決定されるオブジェクト名|
|`tag: str`|読み書き|保存された文字列マーカーを適用する、デフォルトでは空文字列。値が変更されると`on_tag_changed`がトリガーされ、コールバック名は`handler(source, event_args)`|
|`type: str`|読み取り専用|オブジェクトのコントロールタイプ名；Python派生物クラスは対応するネイティブコントロールタイプを使用する|
|`disposed: bool`|読み取り専用|解放されているかどうか、初期値は`False`|
|`id: int`|読み取り専用|オブジェクト番号|
|`parent: container_control \| None`|読み取り専用|直接の親コンテナ|

|署名|用途|
|---|---|
|`invalidate() -> None`|再描画の要求|
|`dispose() -> None`|オブジェクトと関連リソースの解放；コンテナは子オブジェクトも一緒に処理する|
|`begin_invoke(callback: Callable[[], None], /) -> None`|オブジェクトの作成スレッドでコールバックを実行する；オブジェクトが無効になった後に実行されていない呼び出しはキャンセルされる|
|`process_input(event: control_input_event_args, /) -> None`|オブジェクトに分配された入力の処理；派生物クラスによってカバーされることがある|

|イベント|用途|
|---|---|
|`on_disposed`|オブジェクトの解放。パラメータは`event_args`|
|`on_property_changed`|属性が変更されたときにトリガーされ、`event.property_name`は変更された属性名です。パラメータは`property_changed_event_args`です。|

### 3.3.control

一般的な可視コントロールで、矩形、背景、可視性、利用可能性、Tab順序を追加します。

|属性|タイプと初期値|用途|
|---|---|---|
|`rect`|`rect(0, 60, 160, 40)`|コントロールの論理矩形で、サブフィールドを変更できます。|
|`tooltip_text`|`str = ""`|ハイライトポップ。ウィンドウがコントロールにレーザーポインタが指すときにテキストを表示します。|
|`background_color`|`int = 0x162738FF`|背景色|
|`visible`|`bool = True`|表示するかどうか|
|`enabled`|`bool = True`|インタラクティブを受け入れるかどうか|
|`tab_index`|`int = 0`|Tabナビゲーションの順序で、符号なしの64ビット整数を使用します。|

|署名|用途|
|---|---|
|`show() -> None`|コントロールを表示する|
|`hide() -> None`|コントロールを隠す|
|`focus() -> None`|そのコントロールにフォーカスを移動する要求|
|`activate() -> None`|コントロールのプログラム動作を実行する、例えばボタンクリックや項目選択をトリガーする|
|`focusable: bool`|キーボードフォーカスが得られるかどうかを検索する；通常の`control`はデフォルトで`False`、派生クラスでカバー可能|
|`absolute_rectangle: rect`|ウィンドウ内のコントロールの論理矩形を返す|
|`get_input_rectangle() -> rect`|独立した矩形を返し、コントロールのローカル入力領域を説明する、派生クラスでカバー可能|
|`focused: bool`|フォーカス状態を検索する|
|`owning_window: window \| None`|所属するウィンドウを返す|
|`get_content_top() -> float`|トップコンテンツのオフセットを取得する；通常のコントロールは`0.0`、ウィンドウはタイトルバーとコントロールリングを考慮する|
|`render(context: render_context, /) -> None`|コントロールの本体を描画する、カバー可能|
|`render_overlay(context: render_context, /) -> None`|ポップメニューなどの描画内容を描画する、カバー可能|

Tabナビゲーションは現在のウィンドウで可視、利用可能、フォーカス可能なコントロールのみを選択する、`Tab`は前進、`Shift+Tab`は後退。`tab_index = 0`は座標で順序を決定する；正の値で順序を明示的に指定可能。具体的な順序とループ規則は後のフォーカスセクションを参照。

|イベント|用途|
|---|---|
|`on_background_color_changed`|背景色の変更。パラメータは`event_args`です。|
|`on_visible_changed`|可視性の変更。パラメータは`event_args`です。|
|`on_enabled_changed`|利用可能性の変更。パラメータは`event_args`です。|
|`on_tab_index_changed`|Tab順序の変更。パラメータは`event_args`です。|
|`on_moved`|二次元位置の変更；ウィンドウ内では三次元位置の変更も通知される。パラメータは`event_args`です。|
|`on_size_changed`|論理サイズの変更；ウィンドウの物理比率の変更もサイズ通知を発行する。パラメータは`event_args`です。|
|`on_pointer_enter`|レーザーポインタの入る。パラメータは`pointer_event_args`です。|
|`on_pointer_leave`|レーザーポインタの出る。パラメータは`pointer_event_args`です。|
|`on_pointer_move`|レーザーポインタの移動。パラメータは`pointer_event_args`です。|
|`on_pointer_down`|レーザーでトリガーされた押し。パラメータは`pointer_event_args`です。|
|`on_pointer_up`|レーザーでトリガーされた離す。パラメータは`pointer_event_args`です。|
|`on_click`|クリックが完了する。パラメータは`event_args`です。|
|`on_scroll`|スクロール入力。パラメータは`scroll_event_args`です。|
|`on_viewport_changed`|スクロールビューの変化時にトリガーされる。パラメータは`event_args`。|
|`on_focus_in`|フォーカスを取得する。パラメータは`event_args`。|
|`on_focus_out`|フォーカスを失う。パラメータは`event_args`。|
|`on_key_down`|キーボードが押される。パラメータは`key_event_args`。|
|`on_key_up`|キーボードが離される。パラメータは`key_event_args`。|

#### blank

`blank(name: str)`は`easyvrui`、`easyvrui.control`、または`easyvrui.control.blank`からインポートされ、controlを継承し、命名矩形のプレースホルダを保存するために使用される。

|基本属性|呼び出しルール|
|---|---|
|`name: str`|構築時に指定され、読み取り専用|
|`rect: rect`|読み書き可能；矩形のサブフィールドを更新可能|

on_moved、on_size_changed、on_property_changed、on_disposedは利用可能に保たれる。`dispose()`、`disposed`、`invalidate()`、`begin_invoke(callback)`は基クラスのライフサイクルとスケジューリングルールを継承する。オブジェクトの識別と解放状態のクエリはcontrol_baseの規約に従う。

|インスタンスの隠蔽エントリ|行動|
|---|---|
|`visible/enabled/background_color/tab_index`|読み取りまたは代入はAttributeErrorを投げる|
|`show/hide/focus/activate/focusable`|インスタンスのアクセスはAttributeErrorを投げる|
|`render/render_overlay/process_input/get_input_rectangle/get_content_top`|インスタンスのアクセスはAttributeErrorを投げる|
|背景色、可視性、可用性、タブの順序の変化イベント、およびレーザー、クリック、スクロール、フォーカス、キーボード、ハンドルイベント|インスタンスのアクセスはAttributeErrorを投げる|

ネイティブオブジェクトは依然としてフレームワークによってcontrol基クラスのインターフェースを通じて管理可能である；ネイティブのレイアウトは`visible`と`enabled`を`False`として扱う。Pythonインスタンスはblankの属性アクセスエントリを通じて上記の隠蔽ルールに従う。

```python
from easyvrui import blank, rect

blank_content = blank("blank_content")
blank_content.rect = rect(24, 80, 600, 320)
```

### 3.4.text_control

文字表示に関連するスタイルを提供する。この基クラスはスタイルのみを追加する；具体的な`text`は`label/button/textbox/combobox`などのタイプによって提供される。

|属性|タイプと初期値|用途|
|---|---|---|
|`foreground_color`|`int = 0xD1DEF0FF`|文字の背景色|
|`font`|`font()`|文字のフォント|

イベント。`on_foreground_color_changed`は背景色が変更された時にトリガーされる。`on_font_changed`はフォントが変更された時にトリガーされる。

### 3.5.selection_control

`selection_control`は`easyvrui`、`easyvrui.control`、または`easyvrui.control.selection_control`からインポートされ、`text_control`を継承する。`item_control`、`grid`、`listview`、および`treeview`はこの層を継承し、`listbox/combobox`は`item_control`を継承する。Pythonのカスタム派生クラスは`clear_selection()`を実装し`is_blank_at(local_left, local_top)`をオーバーライドすることができる；具体的なコントロールから派生する際には`super()`を通じてネイティブの実装を再利用することができる。

|メンバー|用途|
|---|---|
|`clear_selection_on_blank_click: bool = False`|空白をクリックしたときに項目をクリアするかどうかの選択、空白をクリックしたときの選択戦略|
|`on_clear_selection_on_blank_click_changed`|空白をクリックして選択をキャンセルする設定の変化時にトリガーされる。パラメータは`event_args`。|
|`is_blank_at(local_left, local_top) -> bool`|ローカル座標が項目領域内の空白かどうかを検索し、カバー可能|
|`clear_selection() -> None`|項目選択の削除；カスタムselection_control派生クラスが実装を担当|

listbox、treeview、grid、listviewの項目領域の空白部分をクリックすると、テキスト編集を終了し、IME/layoutを閉じ、集合コントロールのキーボードナビゲーションのフォーカスを保持する。Trueに設定すると項目選択を解除し、Falseに設定すると項目選択を保持する。表頭、スクロールバー、列幅調整エリア、ポップアップオプションはそれぞれの機能に応じて処理される。別のテキストボックスに切り替えると、ワンクリックでフォーカスと入力インターフェースの移動が完了する。ボタンなどのコントロールはそれぞれのフォーカスとTab行動を保持する

### 3.6.item_control

文字列項目、単一選択、行ごとのスクロールを含むベースクラスで、デフォルトではフォーカスされる

|属性|タイプと初期値|読み書き及び用途|
|---|---|---|
|`item_list`|`item_collection`、初期は空|集合を変更可能；全体の値は`list[str]`を受け入れる|
|`selected_index`|`int = -1`|読み書き。`-1`は選択されていないことを示し、他の値は既存の項目のインデックスでなければならない|
|`selected_item`|`str = ""`|読み取り専用；現在選択されている項目で、選択されていない場合は空文字列|
|`row_height`|`int = 32`|読み書き；各行の論理的な高さで、`0`よりも大きくなければならない|

項目集合を変更すると、範囲を超えた選択項目が削除され、スクロール位置が有効範囲に制限される。イベントは`on_item_list_changed`、`on_selected_index_changed`、`on_selection_changed`、`on_row_height_changed`で、それぞれ項目、インデックス、選択、スクロール、行高の変化を通知する

### 3.7.container_control、panel、tabpage

`container_control`は`control`を継承する。通常のサブコントロールは直接操作可能な集合で管理される：

|メンバー|用途|
|---|---|
|`active_item_list: list[control]`|現在表示およびインタラクションに参加している直接コントロールを検索する|
|`control_list: control_collection`|読み取り専用集合のエントリ|
|`on_control_added`|コントロールが追加されるときにトリガーされる。`control_collection_event_args`を通じてコントロールの`item`とそのインデックス`index`を読み取る|
|`on_control_removed`|コントロールが削除されるときにトリガーされる。`control_collection_event_args`を通じてコントロールの`item`と削除前のインデックス`index`を読み取る|

```python
from easyvrui import button, panel

panel_main = panel("panel_main")
button_ok = button("button_ok")
button_ok.text = "OK"
panel_main.control_list.add(button_ok)
button_same = panel_main.control_list["button_ok"]
button_removed = panel_main.control_list.remove(button_ok)
panel_main.control_list.add(button_removed)
```

`panel(name)`は通常のコンテナである。`tabpage(name)`はタブの内容コンテナで、ページの本文は自身の`control_list`で構成される。ページの所属は`tabcontrol.page_list`で管理される

|タブの属性またはイベント|用途|
|---|---|
|`text: str = ""`|タブのタイトルで、変更後は所属する`tabcontrol`を更新する|
|`on_text_changed`|タブのタイトルが変更されるときにトリガーされる。パラメータは`event_args`である|

## 4.具体的なコントロール

### 4.1.label

`text_control`を継承する。構築。`label(name: str)`

|メンバー|用途|
|---|---|
|`text: str = ""`|読み書きで文字を表示する|
|`on_text_changed`|文字の変更。パラメータは`event_args`である|

ラベルは文字を表示するために使用され、デフォルトではキーボードナビゲーションには参加しません。

### 4.2.button

`text_control`を継承する。構築。`button(name: str)`

|メンバー|用途|
|---|---|
|`text: str = ""`|読み書きボタンの文字|
|`on_text_changed`|文字の変更。パラメータは`event_args`である|
|継承された`on_click`|実行ボタンのビジネスロジック|

ボタンはフォーカス可能です。ボタンクリック処理関数は、所属ウィンドウの`dialog_result`属性を設定してモーダル状態を終了できます。

### 4.3.textbox

継承`text_control`。構造。`textbox(name: str)`。フォーカス可能で、テキストの選択、編集、スクロールが提供されます。

|属性|タイプと初期値|読み書き及び用途|
|---|---|---|
|`text`|`str = ""`|読み書き；テキスト内容|
|`read_only`|`bool = False`|読み書き；インタラクティブな編集を制限|
|`selectable`|`bool = True`|読み書き；カーソル、選択、インタラクティブ入力を許可するかどうか|
|`multiline`|`bool = False`|読み書き；マルチ行編集とEnterによる改行を有効にする|
|`horizontal_scrollbar_visible`|`bool = False`|読み書き；横向きスクロールバーの表示オン/オフ|
|`vertical_scrollbar_visible`|`bool = False`|読み書き；縦向きスクロールバーの表示オン/オフ|
|`max_length`|`int = 0`|読み書き；コードポイントの最大数。`0`は制限なしを意味します|
|`selection_start`|`int = 0`|読み書き；選択範囲の小端位置|
|`selection_length`|`int = 0`|読み書き；選択範囲のコードポイントの長さ|
|`selected_text`|`str = ""`|読み書き、現在の選択範囲のテキストを読み取ります。プログラム方式で選択範囲を置き換え、読み取り専用のテキストボックスを含みます|
|`can_undo`、`can_redo`|`bool = False`|読み取り専用；現在の編集履歴が取り消しまたは再実行をサポートしているかどうか|

|署名|用途|
|---|---|
|`select(start: int, length: int = 0) -> None`|開始位置と長さで選択；長さが`0`の場合、挿入位置を移動します|
|`undo() -> bool`|一度の編集を取り消す。成功した場合`True`を返します|
|`redo() -> bool`|再編集を実行する。成功した場合`True`を返します|

テキストの設定と置換はマルチ行および長さの制約を適用します。`\r\n`と`\r`は`\n`に統一され、単行モードでは改行が除去されます。フィルタリングとトリミングは完全なテキスト境界を保持します。選択範囲の位置は有効範囲内に制限され、境界外の位置は選択方向に応じて調整されます。スクロールバーのオン/オフは`multiline`によって表示と改行の能力をそれぞれ制御します

`read_only = True`はカーソル、選択、コピーを保持し、インタラクティブな入力と削除はテキストを変更しないようにします。`selectable = False`の場合、コントロールは依然としてフォーカスを得ることができ、テキストカーソル、選択、入力編集、IME/layoutインターフェースはすべて無効になりますが、`text`属性を使用して表示内容を更新することは依然として可能です

|イベント|用途|
|---|---|
|`on_text_changed`|テキスト内容の変更。パラメータは`event_args`です|
|`on_read_only_changed`|読み取り専用スイッチの変更。パラメータは`event_args`です|
|`on_selectable_changed`|選択およびインタラクティブ入力スイッチの変更。パラメータは`event_args`です|
|`on_selection_changed`|選択範囲または挿入位置の変更。パラメータは`event_args`です|
|`on_max_length_changed`|長さの制限の変更。パラメータは`event_args`です|
|`on_multiline_changed`|複数行スイッチの変更。パラメータは`event_args`です。|
|`on_horizontal_scrollbar_visible_changed`|横スクロールバーのスイッチの変更。パラメータは`event_args`です。|
|`on_vertical_scrollbar_visible_changed`|縦スクロールバーのスイッチの変更。パラメータは`event_args`です。|
|`on_text_input`|テキスト編集入力通知|

縦方向の内容がスクロール可能な場合、レーザーをテキストボックスの後ろに向けて、対応するハンドルスティックで上下にスクロールし、偏向の大きさで速度を決定します。または、スクロールバーをドラッグすることもできます。

テキストエディタにフォーカスがある場合、Ctrl+Zで変更を取り消し、Ctrl+YまたはCtrl+Shift+Zで変更を復元します。これらのキーはアプリケーションメニューのショートカットよりも優先されます。

### 4.4.combobox

`item_control`を継承する。構築。`combobox(name: str)`

|属性|タイプと初期値|用途|
|---|---|---|
|`dropdown_style`|`combobox_dropdown_style.dropdown_list`|`dropdown`は編集可能で、`dropdown_list`はリストから選択します。|
|`dropped_down`|`bool = False`|ドロップダウンリストが展開されるかどうか、読み書き可能です。|
|`text`|`str = ""`|表示または編集されたテキスト；既存の項目を選択すると、その項目に同期します。|

イベントは`on_dropdown_style_changed`、`on_text_changed`です。項目と選択イベントは`item_control`から継承されます。

`dropdown_list`の場合、空でない`text`は既存の項目と一致する必要があります。空文字列に設定すると、選択をクリアできます。`dropdown`の場合、新しいテキストにより`selected_index`は`-1`になります。選択された項目は常に`selected_index/selected_item`で読み取ります。ドロップダウンリストはクリックで展開されます。レーザーが現在指している項目のみがハイライト表示されます。

### 4.5.listbox

`item_control`から継承されます。構造。`listbox(name: str)`。このレイヤーでは、デフォルトで`row_height`を`30`に変更し、その他の公開属性、メソッド、イベントは継承インターフェースを使用します。

表示可能な行数を超えた場合、自動的に縦スクロールバーが提供されます。レーザーがリストを指している場合、対応するハンドルスティックで上下にスクロールするか、スクロールバーをドラッグできます。`selected_index = -1`は選択を解除します。

### 4.6.tabcontrol

`container_control`を継承する。構築。`tabcontrol(name: str)`

|属性|タイプと初期値|読み書き及び用途|
|---|---|---|
|`page_list`|`tabpage_collection`、初期は空|読み取り専用のコレクションエントリ、ページとタブのテキストを管理します。|
|`selected_index`|`int = -1`|読み書き可能；現在のページのサブスコア、`-1`は選択されていないページを表します。|
|`page_close_button_visible`|`bool = False`|読み書き可能；タブの閉じるボタンを表示するかどうか|
|`selected_page`|`tabpage \| None`|読み取り専用；現在のページオブジェクト|
|`tab_position`|`tab_position.top`|読み書き可能；列挙型または`"top"/"bottom"/"left"/"right"`文字列を受け入れます。|
|`tab_size`|`int = 36`|読み書き可能；タブバーの厚さは`0`以上でなければなりません。|
|`tab_font`|`font()`|読み書き可能；タブのフォント|
|`tab_foreground_color`|`int = 0xD1DEF0FF`|読み書き可能；通常のタブテキストの色|
|`tab_background_color`|`int = 0x162738FF`|読み書き可能；通常のタブの背景色|
|`selected_tab_foreground_color`|`int = 0xFFFFFFFF`|読み書き可能；選択されたタブテキストの色|
|`selected_tab_background_color`|`int = 0x316B9AFF`|読み書き可能；選択されたタブの背景色|

`tab_position`の列挙型は`easyvrui`からインポートでき、メンバーは`top/bottom/left/right`です。

ページは`page_list.add(page)`を通じて追加され、タブの外観とアクティブなページは`tabcontrol`によって管理されます。メインコンテンツエリアはコンテナの背景を使用し、ハイライト効果は特定のタブに作用します。`tabcontrol`は`page_list`を統一して使用し、その`control_list`へのアクセスは、ベースクラスのエントリー呼び出しを含む場合、`page_list_required`診断を含む`RuntimeError`を投げ出します。

|イベント|用途|
|---|---|
|`on_selected_index_changed`|選択されたページのサブスコアの変化。パラメータは`event_args`です。|
|`on_selection_changed`|ページの選択の変化。パラメータは`event_args`です。|
|`on_tab_position_changed`|タブバーの位置の変化。パラメータは`event_args`です。|
|`on_tab_size_changed`|タブバーの厚さの変化。パラメータは`event_args`です。|
|`on_tab_font_changed`|ページのフォントの変化。パラメータは`event_args`です。|
|`on_tab_foreground_color_changed`|通常のタブのテキスト色の変化。パラメータは`event_args`です。|
|`on_tab_background_color_changed`|通常のタブの背景色の変化。パラメータは`event_args`です。|
|`on_selected_tab_foreground_color_changed`|選択されたタブのテキスト色の変化。パラメータは`event_args`です。|
|`on_selected_tab_background_color_changed`|選択されたタブの背景色の変化。パラメータは`event_args`です。|
|`on_page_added`|ページの追加；データには`page/index/text`が含まれます。パラメータは`tabpage_event_args`です。|
|`on_page_removed`|ページの削除；データには`page/index`が含まれます。パラメータは`tabpage_event_args`です。|
|`on_page_text_changed`|タブのタイトルの変化時にトリガーされます。`tabpage_event_args.page.text`を通じて現在のタイトルを読み取ります。|
|`on_page_close`|タブの閉じる要求時にトリガーされます。`tabpage_event_args`を通じてタブ`page`とそのインデックス`index`を読み取ります。|
|`on_page_close_button_visible_changed`|タブの閉じるボタンの表示設定の変化。パラメータは`event_args`です。|

`page`イベントフィールドはページオブジェクトの数値識別子であり、`index`は`0`から始まります。集合を通じてページオブジェクトを取得します。

```python
from easyvrui import label, rect, tabcontrol, tabpage

tabcontrol_main = tabcontrol("tabcontrol_main")
tabcontrol_main.rect = rect(20, 80, 560, 260)
tabpage_general = tabpage("tabpage_general")
label_info = label("label_info")
label_info.rect = rect(20, 20, 300, 36)
label_info.text = "General settings"
tabpage_general.control_list.add(label_info)
tabpage_general.text = "General"
tabcontrol_main.page_list.add(tabpage_general)
tabcontrol_main.selected_index = 0
```

タブの閉じるアイコンをクリックするか、タブにフォーカスした時にDeleteを押すと`on_page_close`がトリガーされます。確認保存後、`page_list`から`event.page`が削除されます。

### 4.7.window

`container_control`を継承します。構造。`window(name: str)`。ウィンドウは初期に隠され、`title`は初期に`name`、`rect`は初期に`rect(0, 0, 640, 360)`、`background_color`は初期に`0x0D1624FF`です。

`startup_position`の列挙は`easyvrui`、`easyvrui.control`、または`easyvrui.control.window`からインポートでき、メンバーは`none/center`です。

centerは初めての位置決め時にソースウィンドウと平行に中央に配置され、ヘッドアップデートの法線に沿って前進します。モダンワンドは直接の親ウィンドウを使用します。有効なソースがない場合はヘッドアップデートで中央に配置され、初期距離は`max(1.2, max(physical_width, physical_height))`メートルです。Engineは各セッションで見える普通のウィンドウを組み合わせて初期の深さを決定し、SDKのイベントループによってposition/rotationに同期します。位置決めは一度だけ適用され、その後の隠しと表示は現在の位置姿勢を保持します。noneは設定された参照対象と位置姿勢を使用します。入力コンポーネントの補助ウィンドウはEngineによって入力エリアの位置決めが行われます。

|属性|タイプと初期値|読み書き及び用途|
|---|---|---|
|`title`|`str = name`|読み書き；タイトルのテキスト|
|`title_foreground_color`|`int = 0xFFFFFFFF`|読み書き；タイトルのテキスト色|
|`title_background_color`|`int = 0x244565FF`|読み書き；タイトルバーの背景色|
|`title_font`|`font("Segoe UI", 20)`|読み書き；タイトルフォント|
|`icon`|`drawing_image \| None、既定はネイティブアイコン`|読み書き；タイトルバーの左側アイコン、比例縮小して垂直中央に配置；Noneに設定時はタイトルが左側のスペースを直接使用|
|`window.get_default_icon() -> drawing_image`|静的方法、ネイティブのデフォルトアイコンを読み取り；iconに値を設定してデフォルト値に戻す|
|`curvature`|`float = 0.0`|読み書き；円柱曲面の曲率、単位はメートルの逆数、0は平面を表す|
|`physical_scale`|`float = 1.0`|読み書き；論理ピクセルの物理サイズの縮小倍率、正の有限数でなければならない；1倍の時は各論理ピクセルが1ミリメートル|
|`position`|`vec3()`|読み書き；ウィンドウの左上角が参照対象に対する位置のオフセット、単位はメートル|
|`rotation`|`vec3()`|読み書き；XYZオールラウンド角、単位は度|
|`reference_object`|`reference_object()`|読み書き。`type: reference_object_type`を含む参照対象レコード、デフォルトはworld|
|`show_title_bar`|`bool = True`|読み書き；タイトルバーを表示するかどうか|
|`tracking_mode_set`|`set[reference_object_type]`|読み書き；タイトルバーのトラッキングセレクター内のパターン集合、初期には`world/body/left/right/head`を含む|
|`show_close_button`|`bool = True`|読み書き；タイトルバーの閉じるボタン|
|`movable`|`bool = True`|読み書き；ハンドルで移動と回転を許可するかどうか|
|`resizable`|`bool = True`|読み書き；インタラクティブな縮小を許可するかどうか|
|`startup_position`|`startup_position.center`|読み書き；列挙型または`"none"/"center"`文字列を受け入れる。noneの場合は初期位置と姿勢を使用；centerは初めて表示時にはソースウィンドウと平行に中央に配置し、ヘッドディスプレイの前に移動する。有効なソースがない場合はヘッドディスプレイの中央に配置|
|`curvature_adjustable`|`bool = True`|読み書き；左下角の曲率ボタンの表示とインタラクション、閉じると現在のドラッグとジョイスティック調整が即座にキャンセルされ、再起動後にtriggerを離してから調整を開始できる|

`physical_scale = 1.0`の時は各論理ピクセルが1ミリメートルに対応する。`rect.width * physical_scale / 1000.0`は表面の展開幅で、曲面ウィンドウ内では展開の弧長に対応する。`curvature`はkと記し、展開幅はWと記す：属性の合法範囲は有限の`k >= 0`であり、`k * W < 2π`である；曲率とスケールを設定する際にはこの関係を満たす必要がある。ウィンドウの左下角のハンドル入力でインタラクティブに調整する際には、160°の安全な弧角の上限を使用する；このインタラクティブな上限は属性の合法範囲ごとに処理される。左右下角の入力はtriggerで保持され、離すまで選択とレーザーキャプチャを維持する；曲率はジョイスティックで左右に調整し、サイズはジョイスティックで上下に調整し、左下角をダブルクリックすると平面に戻る

`reference_object_type`の列挙型には`world/body/head/left/right`が含まれる。`reference_object()`はデフォルトのworldレコードを構築し、`reference_object(type)`はその列挙型を受け取る；レコードの`type`は読み書き可能。`get_reference_object_type_name(value: reference_object_type) -> str`は名前を返し、`parse_reference_object_type(value: str) -> reference_object_type`は名前を解析する。2つのreference_objectレコードはtypeで比較される；列挙型と比較する際には`item.reference_object.type`を使用し、名前と比較する際には`get_reference_object_type_name(item.reference_object.type)`を使用する

Pythonのアクセス適応では、`reference_object`で値を設定し、`reparent()`パラメータでreference_objectの記録、reference_object_typeの列挙、または5種類のモード名の文字列を使用できます。reference_objectの読み取りは常に記録を返します。`tracking_mode_set`の値設定は`set`または`frozenset`を受け入れ、要素は列挙であるか、アクセス適応のモード文字列、またはreference_objectの記録を使用できます。読み取りは列挙のスナップショットを返します。空の集合は切り替えボタンを隠し、モードを追加する必要がある場合は全体を再設定します。

|その他の状態属性|読み書き及び用途|
|---|---|
|`closed: bool`|読み取り専用；是否已关闭、初期値は`False`|
|`loaded: bool`|読み取り専用；是否已经首次显示、初期値は`False`|
|`dialog_result: dialog_result`|読み取り・書き込み可能、モーダル状態に入ると`none`にリセットされます。モーダル期間中に`none`以外の値を設定するとウィンドウが閉じ、直接閉じると`cancel`に戻ります。|
|`physical_width: float`|読み取り専用；展開幅、`rect.width * physical_scale / 1000`に等しい|
|`physical_height: float`|読み取り専用；実際の高さ、`rect.height * physical_scale / 1000`に等しい|
|`auxiliary: bool`|読み取り・書き込み可能；補助入力面のマーク、初期値は`False`；IME/layoutセッションのウィンドウが自動的に補助面となり、Engineが位置、参照、追従入力ウィンドウのスケーリングを維持します。|

|署名|用途|
|---|---|
|`show() -> None`|通常のウィンドウを表示；初回表示時にロードイベントがトリガーされます。|
|`hide() -> None`|ウィンドウを隠し、対応するインタラクションをキャンセルする；そのウィンドウの活動モーダル状態を終了します。|
|`activate() -> None`|そのウィンドウのアクティブ化を要求します。|
|`show_dialog(owner_window: window) -> dialog_result`|モーダルウィンドウを同期して表示し、その間に直接所有者を無効にしてUIイベントを配布し続けます。閉じた後、結果の列挙を返します。|
|`close(force: bool = False) -> bool`|ウィンドウを閉じる要求、成功した場合は`True`を返します。forceがTrueの場合は閉じるキャンセルコールバックをスキップします。|
|`set_size(width: int, height: int, /) -> None`|論理的な矩形の幅と高さを設定し、`0`より大きくなければなりません。|
|`reparent(reference: reference_object \| reference_object_type \| str, keep_world: bool = False) -> None`|参照対象を変更する；keep_world=Trueを渡した場合は世界の姿勢を保持します。|
|`world_transform: pose \| None`|現在解析可能な世界の姿勢を読み取ります；参照を追跡できない場合は`None`になります。|
|`is_tracking_available(mode: reference_object_type) -> bool`|指定された参照モードが現在追跡可能かどうかを調べます。|
|`center_at_view(distance: float, /) -> bool`|視線前方の指定されたメートル数でウィンドウを中央に配置し、位置決めに成功した場合は`True`を返します。|

`world_transform`はウィンドウ面の中心の世界の姿勢を返します。`position`は左上角のオフセットを設定します。直接`reference_object`で値を設定した後、既存のオフセットは新しい参照系で解釈されます。世界の姿勢を保持する必要がある場合は`reparent(reference, keep_world = True)`を使用します。

`show_dialog(owner_window)`は、所有者が同じUIランタイム内で互いに操作可能な他のウィンドウであることを要求します。ダイアログボックスは隠されていて、まだ閉じられておらず、モーダル状態にはなっていません。この呼び出しは、同じUIスレッド内でネストされたメッセージループに入り、直接の所有者は一時的に操作可能でなくなります。ボタンやメニューイベントから呼び出すことができ、現在操作可能なダイアログボックスを次の所有者として使用します。レンダリングの送信中に呼び出すとエラーが発生します。詳細は[セッションとネストされたモーダルループ](/ja/advanced/04_session_and_context)をご覧ください。

モーダル状態に入ると、`dialog_result`は`dialog_result.none`にリセットされます。他の結果を設定すると、閉じる要求が行われます。プロセッサが閉じるをキャンセルすると、ダイアログボックスは活動状態を維持し、結果は設定前の値に戻ります。結果が依然として`none`の場合は、タイトルバーからの閉じるボタンまたは`close()`で成功して閉じ、`dialog_result.cancel`に戻ります。呼び出し元はウィンドウインスタンスを保持し、戻った後にコントロールの値を読み取ります。

通常の新しいウィンドウを初めて表示する際、`physical_scale`が明示的に設定されていない場合にのみ、同じセッションのモーダルオーナー、現在のイベントディスパッチウィンドウ、on_loadが実行中のウィンドウ、現在の入力ウィンドウ、活動ウィンドウ、最近見える通常のウィンドウから順にソースを決定し、そのスケーリングを継承します。明示的に設定された値が優先され、1.0を含みます。表示後、再びスケールを設定できます。同じ倍率で、同じロジックサイズのコントロールは同じ物理サイズを持ちます。`set_size()`はロジックキャンバスと対応する物理サイズを変更します。

|参照対象|用途|
|---|---|
|`"world"`|エンジン世界の参照空間に位置し、ユーザーが移動したり頭を回したりすると空間位置を維持します。|
|`"head"`|頭部の位置と回転に従います。|
|`"left"`|左手コントローラーの参照姿勢に従います。|
|`"right"`|右手コントローラーの参照姿勢に従います。|
|`"body"`|首の軸の補正位置に従い、校正時の向きを維持します；頭を回すと周囲のウィンドウを観察できます。|

`startup_position = startup_position.none`および`position = vec3()`、`rotation = vec3()`の場合、世界モードのウィンドウの左上角は初期の正面参照中心に位置します。

centerのモーダルウィンドウは直接の親ウィンドウを使用します；他のcenterウィンドウはSDKが提供する同じセッションのソースを優先的に使用します。ソースが省略される場合は、Engineが現在選択されている見える通常の表面を使用し、セッションを超えてDesktopから他のAppを起動することができます。Engineはソースの正面または背面の法線に沿って、初期の深度を配置し、応答同期の最終的なposition/rotationを完了します；その後の隠しと表示は、確定された姿勢を維持します。

`Ctrl+Alt+Pause`はBodyの中心とWorldの全体レイアウトを現在のヘッドディスプレイにマッピングし、システムが`Ctrl+Alt+Break`と報告するときと同じ効果が得られます。`Ctrl+Pause`はエンジン設定内のDesktopアプリケーションを表示または隠します。

可移動ウィンドウは、WorldモードとBodyモードでサイドキーを使用した片手でのグリップがサポートされています。両手で外周の異なるコントロールポイントを別々に握り、軸回転を制限します。ウィンドウの前後両面で表示およびインタラクティブ操作が可能で、背面のテキストは正面の鏡像です。ウィンドウの論理サイズが十分に大きく、移動が可能な場合、外周のコントロールリングは論理矩形の内側の空間を占めます。サブコントロールを配置する際は、`get_content_top()`を参照してタイトルバーを避けることができます。

|イベント|用途|
|---|---|
|`on_title_changed`|タイトル変更。パラメータは`event_args`です。|
|`on_title_foreground_color_changed`|タイトルテキストの色変更。パラメータは`event_args`です。|
|`on_title_background_color_changed`|タイトルバーの背景色変更。パラメータは`event_args`です。|
|`on_title_font_changed`|タイトルフォントの変更。パラメータは`event_args`です。|
|`on_icon_changed`|タイトルアイコンオブジェクトの変更またはクリア。パラメータは`event_args`です。|
|`on_rotation_changed`|3D回転の変更。パラメータは`event_args`です。|
|`on_curvature_changed`|曲率の変更。パラメータは`event_args`です。|
|`on_curvature_adjust_start`|曲率のインタラクティブ調整開始。パラメータは`event_args`です。|
|`on_curvature_adjust_end`|曲率のインタラクティブ調整終了。パラメータは`interaction_end_event_args`です。|
|`on_reference_object_changed`|参照対象の変更。パラメータは`event_args`です。|
|`on_show_title_bar_changed`|タイトルバーの表示オン/オフの変更。パラメータは`event_args`です。|
|`on_tracking_mode_set_changed`|タイトルバーの許可されるモード集合の変更。パラメータは`event_args`です。|
|`on_show_close_button_changed`|閉じるボタンのオン/オフの変更。パラメータは`event_args`です。|
|`on_movable_changed`|移動スイッチの変更。パラメータは`event_args`です。|
|`on_resizable_changed`|ズームスイッチの変更。パラメータは`event_args`です。|
|`on_startup_position_changed`|位置決めモードの開始。パラメータは`event_args`です。|
|`on_curvature_adjustable_changed`|曲率のインタラクティブ調整スイッチの変更。パラメータは`event_args`です。|
|`on_load`|最初の表示時にロードされ、各ウィンドウごとに1回。パラメータは`event_args`です。|
|`on_shown`|隠れ状態からの表示。パラメータは`event_args`です。|
|`on_hidden`|隠す。パラメータは`event_args`です。|
|`on_closing`|閉じる前に確認。`event.cancel = True`で通常の閉じるをキャンセルできます。パラメータは`cancel_event_args`です。|
|`on_closed`|閉じるを完了；データには閉じる`reason`が含まれます。パラメータは`event_args`です。|
|`on_render_failed`|描画の送信に失敗。パラメータは`render_error_event_args`です。|
|`on_tracking_lost`|参照対象のトラッキングが失われた。パラメータは`event_args`です。|
|`on_tracking_restored`|参照対象のトラッキングが復元された。パラメータは`event_args`です。|
|`on_activated`|ウィンドウのアクティブ化。パラメータは`event_args`です。|
|`on_deactivated`|ウィンドウのアクティブ化が失われた。パラメータは`event_args`です。|
|`on_move_start`|移動または回転の制限開始。パラメータは`event_args`です。|
|`on_move_end`|移動または回転の制限終了。パラメータは`interaction_end_event_args`です。|
|`on_resize_start`|インタラクティブズームの開始。パラメータは`event_args`です。|
|`on_resize_end`|インタラクティブズームの終了。パラメータは`interaction_end_event_args`です。|

三次元位置の変化は継承された`on_moved`を使用し、物理的な幅の変化は継承された`on_size_changed`を使用します。ウィンドウが隠れたり閉じられたりすると、キャプチャ、ポインタキャプチャ、関連する入力インターフェースが解除されます。閉じた後は、新しいウィンドウインスタンスを作成して再表示する必要があります。

### 4.8.checkboxとradiobutton

両者は`text_control`を継承し、`checkbox(name)`と`radiobutton(name)`で構築されます。読み書き属性は`text: str = ""`と`checked: bool = False`です；テキストの変更は`on_text_changed`をトリガーし、チェック状態の変更は`on_checked_changed`をトリガーします。色とフォントは継承された属性を使用します。checkboxをクリックするとチェック状態が切り替わります；radiobuttonは同じ親コンテナ内の排他的なオプションに使用されます。

### 4.9.numericupdown

継承された`text_control`を使用し、`numericupdown(name)`で構築されます。中間のテキストエリアは編集可能な数値であり、上下の三角ボタンはそれぞれホバーとフォーカスを取得します；調整ボタンをクリックすると数値操作のフォーカスが保持され、テキスト入力インターフェースはテキスト編集エリアのみに関連します。

|属性|初期値と制約|
|---|---|
|`value: float`|0.0、有限数、最小値と最大値の間で制限されます|
|`minimum: float`|0.0、maximumより小さくなければなりません|
|`maximum: float`|100.0、minimumより大きくなければなりません|
|`step: float`|1.0、正の有限数|
|`decimal_places: int`|0、範囲0から17まで、表示される小数の桁数を制御します|

関連するイベントは`on_value_changed/on_minimum_changed/on_maximum_changed/on_step_changed/on_decimal_places_changed`です。上下の限界を変更すると、現在の値が相応に制限されます。

### 4.10.sliderとprogressbar

両者は`control`を継承し、名前のみを指定します。`minimum: int = 0`、`maximum: int = 100`、`value: int = 0`を公開し、整数は符号付き64の範囲を使用します。minimumはmaximumより厳密に小さく、valueはその範囲内で制限されます；イベントは`on_minimum_changed/on_maximum_changed/on_value_changed`です。

`slider`は`orientation: orientation = orientation.horizontal`も提供し、`orientation.horizontal`または`orientation.vertical`のみを受け入れます；イベントには`on_orientation_changed/on_drag_start/on_drag_end`が含まれます。スライダーをドラッグするかキーボードでナビゲートしてvalueを変更します。`progressbar`は範囲に応じて進捗を表示します。

### 4.11.listview

`listview(name)`は`selection_control`を継承し、複数の列のテキストを行ごとに表示します。表頭をクリックすると`on_column_click`がトリガーされ、それに基づいてソートされます。表頭のセパレータをドラッグして幅を調整できます。

|インターフェース|用途|
|---|---|
|`listview_column(text = "", width = 100)`|`text`と`width`は読み書き可能です。幅が正の場合、変更するとビューが再配置されます。|
|`listview_item(cell_list = [], icon = None, tag = "")`|`cell_list`は各列のテキストを保存し、`icon`は最初の列に表示され、`tag`はアプリケーションのタグを保存します。|
|`column_list: listview_column_collection`|列の集合は、その場で変更や全体の値の割り当てをサポートします。|
|`item_list: listview_item_collection`|行の集合も、その場で変更や全体の値の割り当てをサポートします。|
|`selected_index: int`、`selected_item: listview_item \| None`|読み書きのメイン選択は、空の選択は`-1`と`None`に対応します。|
|`select_item(index, extend = False, toggle = False)`|下のマーカーで行を選択します。複数選択時は選択範囲を拡大したり、目的の行を切り替えたりできます。|
|`selected_item_list: list[listview_item]`、`multi_select: bool`|選択範囲オブジェクトを読み取り、複数選択を設定します。|
|`row_height`、`header_height`|行の高さと表頭の高さを読み書きします。`header_height = 0`は表頭を隠します。|
|`visible_row_count`、`vertical_scrollbar_visible`、`horizontal_scrollbar_visible`|現在表示されている行数とスクロールバーの状態を読み取ります。|
|`on_item_list_changed`、`on_column_list_changed`、`on_column_width_changed`|ビューの内容と列の幅の変化を監視します。|
|`on_selection_changed`、`on_row_double_click`、`on_column_click`|選択の変化、アクティブな行の変更、表頭のクリックを監視します。|

`item.cell_list`は`listview_cell_collection`です。`item.cell_list[0] = "Updated"`を使用してセルを変更することも、全体に値を設定することもできます。リストは行ごとに選択範囲を保持し、ソート時には同じ行グループを新しい順序で再設定します。

### 4.12.treeviewとtree_node

`treeview(name)`は`selection_control`を継承します。ルートノードは`node_list: tree_node_collection`を通じて管理され、`selected_node: tree_node | None`は現在選択されているオブジェクトを読み書きします。`row_height`と`vertical_scrollbar_visible`は読み取り専用の属性です。

`tree_node(text = "", expanded = False, tag = "")`は同じ名前の読み取り専用および書き込み専用の属性を提供します。`parent`は親ノードを返すか`None`を返し、`node_list`は子ノードを管理します。`expand()`と`collapse()`を通じて展開状態を調整します。各ノードは一つのツリー集合に属しています。

ツリービューは`on_node_list_changed`、`on_selection_changed`、`on_node_expanded`、`on_node_collapsed`、`on_node_activated`を提供します。ノードイベントのデータフィールド`node`はノードタグです。

```python
root = easyvrui.tree_node("Project", expanded = True, tag = "root")
child = easyvrui.tree_node("Engine")
root.node_list.append(child)
tree = easyvrui.treeview("treeview_project")
tree.node_list.append(root)
tree.selected_node = child
```

### 4.13.scrollpanelとsplitter

`scrollpanel(name)`は`container_control`を継承し、`control_list`を通じて通常のコントロールを追加します。`horizontal_scrollbar_visible/vertical_scrollbar_visible`はデフォルトでTrueであり、それぞれに対応するイベントがあります。スクロール範囲は内容によって決定され、視野の変化は`on_viewport_changed`を発行します。

`splitter(name)`は`container_control`を継承し、最大で2つのパネルコントロールを収容でき、順序は第一側と第二側に対応します。

|属性|用途|
|---|---|
|`orientation: orientation = orientation.vertical`|`orientation.vertical`は垂直の分割バーで左右の領域を分割します。`orientation.horizontal`は水平の分割バーで上下の領域を分割します。|
|`split_position: float = 0.5`|分割比率は限られており、0.0から1.0の間にあります。|

関連イベントは`on_orientation_changed/on_split_position_changed/on_split_start/on_split_end`です。レイアウトはコンテナによって計算され、分割バーのドラッグによってsplit_positionが更新されます。

### 4.14.imageとscreen

`image(name)`は`control`を継承します：

|メンバー|用途|
|---|---|
|`source: drawing_image \| None`|画像オブジェクト|
|`stretch_mode: image_stretch_mode = image_stretch_mode.contain`|読み取り専用、`image_stretch_mode`の`fill/contain/cover/none`を受け入れます。|

fillは矩形を満たし、containは比率を保持して完全に表示し、coverは比率を保持して矩形を覆い、カットします。noneは画像の元のサイズを使用します。イベントは`on_source_changed/on_stretch_mode_changed/on_source_unavailable`です。

`screen(name)`は`control`を継承し、画面のリアルタイム画像を表示するために使用されます：

|メンバー|用途|
|---|---|
|`screen_id: int = 0`|画面識別|
|`screen_available: bool`|読み取り専用、現在の画面が使用可能かどうか、初期値はFalseです。|
|`on_screen_id_changed`|画面の選択変化。パラメータは`event_args`です。|
|`on_screen_unavailable/on_screen_restored`|画面が使用できない場合と復帰|

画面はコントロールの矩形に従って表示され、マウスポインタは画面の表示に合わせて動きます。原始の画面の鮮明さはコントロールの論理サイズに関連しています。ピクセル単位での表示が必要な場合、screenコントロールの幅と高さを対応するディスプレイの解像度に設定します。ウィンドウのphysical_scaleは、その物理サイズを独立して制御します。

### 4.15. アイコンツールバーとホバーテキスト

`toolbar`、`toolbar_button`、`toolbar_button_collection`は`easyvrui`または`easyvrui.control`からインポートすることができ、またはそれぞれの同名のサブモジュールからインポートすることができます。`toolbar`のコンストラクタは不変の`name`のみを受け入れます。`toolbar`は`container_control`を継承します。

`toolbar_button(name)`は`button`を継承し、ツールバー項目であり`toolbar.button_list`によって管理されます。各ボタンはアイコン、クリックエリア、ホバーテキストを一つの全体として表示します。

|オブジェクト|属性|用途|
|---|---|---|
|`toolbar`|`tool_size: int = 40`|正方形のツールグリッドの辺の長さで、正の整数でなければなりません。|
|`toolbar`|`spacing: float = 6.0`|有限の非負の間隔|
|`toolbar`|`button_list: toolbar_button_collection`|読み取り専用で、ツールボタンおよびセパレーションラインの直接操作可能な集合です。|
|`toolbar_button`|`icon: drawing_image \| None`|ツールアイコン|
|`toolbar_button`|継承された`tooltip_text: str = ""`|ホバーテキスト、空の文字列はテキストの表示を停止します。|
|`toolbar_button`|`enabled: bool = True`|実行可能かどうか|
|`toolbar_button`|`separator: bool = False`|セパレーションラインとして表示される|

`toolbar`は`on_tool_size_changed/on_spacing_changed`を提供します。`toolbar_button`は`on_click/on_icon_changed`および継承されたオブジェクトイベントを提供します。ツールバーはレイアウトを管理し、ボタンはホバーとクリックに応答します。

```python
from easyvrui import drawing_image, toolbar, toolbar_button

toolbar_main = toolbar("toolbar_main")
toolbar_main.rect.width = 200
toolbar_main.rect.height = 40
button_add = toolbar_button("toolbar_button_add")
button_add.icon = drawing_image(1, 1, bytes([120, 210, 255, 255]))
button_add.tooltip_text = "Add an item"
toolbar_main.button_list.add(button_add)
button_separator = toolbar_button("toolbar_button_separator")
button_separator.separator = True
toolbar_main.button_list.add(button_separator)
window_main.control_list.add(toolbar_main)
textbox_entry.tooltip_text = "Enter the text to translate."
```

例での`window_main`と`textbox_entry`はアプリケーションによって作成され、ターゲットテキストボックスはそのウィンドウに属します。独立したツールトップはデフォルトでゼロの矩形で、ターゲットにホバーすると表示され、ホバーを離れると消失します。テキストは文字境界に沿って改行され、ヒントボックスはウィンドウのコンテンツ領域内に制限され、高さが不足している場合は省略号が表示されます。

### 4.16. メニューバーとメニュー項目

`menu_container`は`container_control`を継承し、`menubar`と`menuitem`の共通のベースクラスです。両方のコントロールは名前で構築されます。

`window.menu`は`menubar`または`None`を読み取りおよび書き込み可能で、変化は`on_menu_changed`をトリガーします。メニューバーはタイトルバーの下に位置します。それはウィンドウの`control_list`にも属します：集合にメニューバーを追加したり、現在のメニューバーを削除したり、集合をクリアしたりすると、`menu`は関連する同期更新を行います。`menu`の設定も集合の所属を同期します。メニュー項目の位置は集合内の実際のインデックスを使用し、各ウィンドウには1つのメニューバーが使用されます。

```python
from easyvrui import menubar, menuitem

menubar_main = menubar("menubar_main")
menuitem_file = menuitem("menuitem_file")
menuitem_file.text = "File"
menuitem_save = menuitem("menuitem_save")
menuitem_save.text = "Save"
menuitem_save.shortcut = "Ctrl+S"
menuitem_file.control_list.add(menuitem_save)
menubar_main.control_list.add(menuitem_file)
window_main.menu = menubar_main
```

例での`window_main`はアプリケーションによって作成されます；コールバックの実行は`menuitem_save.on_click += handler`を通じて登録されます。

|オブジェクト|属性、メソッド、用途|
|---|---|
|`menu_container`|通常の`control_list`を継承します；集合は`menuitem`のみを受け入れます。`owning_menubar`は所属するメニューバーを取得します。`on_item_added/on_item_removed`は集合の変化を通知します|
|`menuitem`|`text/shortcut/checkable/checked/separator/icon`を読み取りおよび書き込み可能です。読み取り専用の属性`open: bool`は現在のサブメニューが展開されているかどうかを示します。`control_list`を通じて下位メニューを管理します|
|`menubar`|`font/row_height`を読み取りおよび書き込み可能です。`open_menu()`と`close(restore_focus = True)`は展開状態を制御します。`open`と`is_submenu_open(item)`は展開状態を照会します|

メニュー項目は`on_text_changed/on_icon_changed/on_shortcut_changed/on_checkable_changed/on_checked_changed/on_separator_changed`を提供し、メニューバーは`on_font_changed/on_row_height_changed`を提供します。両方とも`on_opening/on_closed`があり、メニュー項目は継承された`on_click`を使用して実行されます。

### 4.17.grid

`grid`は`selection_control`を継承し、複数列のデータ、選択、編集を提供します。

|タイプ|インターフェース|
|---|---|
|`grid_column(text = "", width = 100, editable = True)`|書き込み可能なフィールド`text/width/editable`|
|`grid_cell(row = 0, column = 0)`|書き込み可能なフィールド`row/column`で、インデックスは0から始まります。|
|`grid_selection_mode`|`cell/row`|
|`grid_cell_render`|レンダリングコールバック記録。`cell/rectangle/value/selected/hovered/editing`は読み書き可能で、`rectangle`のタイプは`render_rectangle`です。|

セル値は`str`、符号付き64ビット範囲の`int`、有限`float`および`bool`をサポートします。`grid(name)`の書き込み可能なプロパティは`column_list/row_count/selected_index/selection_mode/multi_select/row_height/header_height/read_only/edit_text`で、読み取り可能なプロパティは`editing/edit_cell/edit_error/selected_cell_list`です。

|メソッド|用途|
|---|---|
|`grid[row, column]`は読み書き可能です。|データの読み書き|
|`set_data_provider(row_count, reader, writer = None)`|reader(row, column)は戻り値を返し、writer(row, column, value)は書き込みを処理します。|
|`refresh_data()`|外部データが更新されたことを通知します。|
|`set_cell_renderer(renderer)`|renderer(context, cell)は可視セルをレンダリングし、Noneはデフォルトに戻ります。|
|`set_edit_validator(validator)`|validator(cell, value)は編集をチェックし、Noneはチェッカーをクリアします。|
|`get_value_text(value)`|静的なメソッドで、値をテキストに変換します。|
|`select_cell(row, column, extend = False, toggle = False)`、`clear_selection()`、`is_cell_selected(row, column)`|選択制御|
|`get_cell_at(left, top)`|ローカル座標で指定されたセルを検索します。|
|`get_cell_rectangle(row, column) -> render_rectangle`|指定されたセルの矩形を検索します。|
|`vertical_scrollbar_visible/horizontal_scrollbar_visible`|スクロールバーの状態|
|`visible_row_count`|現在可視の行数|
|`set_column_width(column, value)`|列の幅を調整します。|
|`begin_edit(row, column)`、`commit_edit()`、`commit_edit(value)`、`cancel_edit()`|編集ライフサイクルで、begin/commitはboolを返します。|

writerとvalidatorは`None`で成功を示し、boolで結果を示し、文字列で失敗の理由を示すか、`(bool, str)`で結果と理由を同時に示します。データプロバイダーの書き込みは、writerによって実際のデータソースを更新する必要があります。派生クラスは`read_cell_value(row, column)`、`write_cell_value(row, column, value)`、および`render_cell(context, cell)`をカバーすることができます。書き込みのカバーは同じ返却規則を使用します。

イベントは`on_column_list_changed/on_column_width_changed/on_column_click/on_selection_changed/on_cell_double_click/on_cell_value_changed/on_row_height_changed/on_header_height_changed/on_edit_started/on_edit_committed/on_edit_cancelled/on_edit_failed`です。イベントは他のコントロールと同じ`+=/-=`のサブスクリプション方法を使用します。

クリックしてセルを編集でき、IMEは現在編集中のセルの可視矩形に位置します。読み取り専用の列は選択と表示に使用されます。`selection_mode`は`grid_selection_mode.cell/row`または`"cell"/"row"`文字列を受け入れます。表のヘッダー背景はコントロールの幅を満たし、列タイトルが長すぎると省略号が表示されます。`header_height = 0`はヘッダーを隠します。

列の幅はデフォルトで100です。`column_list`は独立した列レコードを返します。`column_list`に値を割り当てるか`set_column_width()`を呼び出すとき、列の幅は正でなければならず、すべての列の幅の合計は符号付き64ビット整数の範囲内でなければなりません。チェックが成功した後に列のレイアウトが適用され、対応するイベントが発行されます。

`column_list`を読み取ってスナップショットを取得し、変更後は再び代入する必要があります。Gridセルは読み取り専用で選択や表示に使用され、編集可能なセルをクリックすると編集に入り、セルを切り替えて焦点を移動し、入力インターフェースを操作します。複数選択は`multi_select`で有効になり、Ctrlキーを使って項目を切り替え、Shiftキーを使って選択を拡大します。物理キーボードの修飾キーは、実体がキャプチャモードで相互作用する場合にのみ使用されます。

## 5.集合インターフェース

### 5.1.control_collection

通常のコンテナの`control_list`を通じて取得します。集合は順序を保ち、不変の`name`で検索をサポートします。名前の検索はマッピングを使用し、通常は定数時間で完了します。`control_collection(owner: container_control)`を使用すると、ownerに関連する独立した集合を構築し、派生タイプで拡張することができます。ownerの元のcontrol_listエントリは依然としてその内蔵集合を指しています。

|署名または操作|戻り値と用途|
|---|---|
|`add(item: control)`、`append(item: control)`|元のオブジェクトに追加し、末尾に置きます。|
|`insert(index: int, item: control)`|元のオブジェクトに追加し、指定された位置に挿入します。|
|`extend(item_list: Iterable[control], /) -> None`|順番に追加します。途中でエラーが発生した場合でも、追加された項目は保持されます。|
|`remove(key: str \| int \| control, /) -> control`|名前、サブスカラス、またはオブジェクトで削除し、オブジェクトを返します。|
|`remove_at(index: int)`、`pop(index: int = -1) -> control`|サブスカラスで削除し、デフォルトでは最後の項目です。|
|`clear() -> None`|すべての子コントロールを削除します。|
|`collection[key] -> control`|名前またはサブスカラスで検索します。名前が欠けている場合は`KeyError`を投げ、境界を超えた場合は`IndexError`を投げます。|
|`del collection[key]`|名前、サブスカラス、またはオブジェクトで削除し、戻り値は無視します。|
|`index_of(key: str \| int \| control, /) -> int`|項目の位置を取得します。整数パラメータはチェックされ、実際のサブスカラスに変換されます。|
|`key in collection`|名前またはオブジェクトのアイデンティティでチェックします。|
|`len(collection)`|項目の数|
|`iter(collection)`|その時のオブジェクトリストのスナップショットをトラバースします。|

負のサブスカラスを許可し、`-1`は末尾を表します。挿入時には、負のサブスカラスを現在の長さに加えた後、`0`からその長さまで制限します。末尾を超える位置は最後に追加されます。`collection[start:stop:step]`を使用してスライスを取得し、`list(collection)`を使用してスナップショットを取得します。削除は`dispose()`の用途とは異なります。削除後もオブジェクトを保持し、使用することができ、条件が満たされる場合は他のコンテナに追加することができます。

Python派生集合は`insert(self, index, item)`、`remove(self, index)`、および`clear(self)`をカバーすることができ、ネイティブの仮想呼び出しは対応するPythonメソッドに分散されます。カバーされたメソッドでは、superの同名のメソッドを呼び出してベースクラス操作を完了することができます。Python接続の`append/extend/pop`と負のサブスカラスは、集合の使用に適応しています。

集合ビューは、所属するownerのPython参照を保持し、検索によって得られた借用参照はバインドによって依存関係を維持します。Python派生コントロールがネイティブ集合によって保持される場合、その再定義されたメソッドとインスタンスプロパティは有効です。owner、集合、およびPythonの追加プロパティによって形成される参照リングはGCに関与します。削除された共有オブジェクトは独立して保持することができ、`dispose()`はネイティブオブジェクトとそのリソースを明示的に終了するために使用されます。

### 5.2.tabpage_collection

`tabcontrol.page_list`を通じて取得します。`tabpage_collection`は`control_collection`を継承し、同じページストレージを共有します。タイトルはページ自体によって保存されます。`tabpage_collection(owner: tabcontrol)`はownerに関連する独立したページ集合を構築できます。ownerの元のpage_listエントリは元のオブジェクトを保持します。挿入項目は`tabpage`でなければならず、下添字または名前でページオブジェクトを検索します。

|署名または操作|戻り値と用途|
|---|---|
|`add(page: tabpage)`、`append(page: tabpage)`|ページを追加して返します。|
|`insert(index: int, page: tabpage)`|指定された位置にページを挿入して返します。|
|`extend(page_list: Iterable[tabpage], /) -> None`|各ページを順番に追加します。|
|`remove(key: str \| int \| tabpage, /) -> control`|ページを外して返します。|
|`remove_at(index: int)`、`pop(index: int = -1) -> control`|指定されたページを外して返します。|
|`clear() -> None`|すべてのページをクリアします。|
|`collection[key] -> tabpage`、`del collection[key]`|ページを検索または外します。|
|`index_of(key: str \| int \| tabpage, /) -> int`|ページの下添字。|
|`key in collection`|名前またはページオブジェクトで検査します。|
|`len(collection)`、`bool(collection)`|数量と空の状態。|
|`iter(collection)`|ページスナップショットをトラバースします。|

ページを削除または挿入した後、選択したページの下添字を実際のページ関係に応じて調整します。同じ集合名は一意です。削除操作は動的型のコントロールオブジェクトを返します。実際には依然として元のtabpageであり、別のpage_listに直接追加できます。`list(collection)`はページ参照スナップショットを返します。

ページ集合は`insert(self, index, page)`と継承された削除拡張点をカバーします。

### 5.3.item_collection

`item_collection`は`easyvrui.control`から導入され、ネイティブ`item_collection`タイプの別名です。インスタンスは`combobox.item_list`、`listbox.item_list`、または`item_control.item_list`によって提供されます。内容は文字列で、重複したテキストを許可します。この集合のPythonパッケージは所属するコントロール参照を保持し、参照環GCに参加します。

|署名または操作|戻り値と用途|
|---|---|
|`add(value: str, /) -> None`、`append(value: str, /) -> None`|文字列を追加します。|
|`insert(index: int, value: str, /) -> None`|挿入します。負の下添字および末尾を超える位置は集合の挿入規則に従って処理されます。|
|`extend(value_list: Iterable[str], /) -> None`|順番に追加します。|
|`assign(value_list: list[str], /) -> None`|すべての内容を置き換えます。|
|`remove(value: str \| int, /) -> str`|最初の一致する文字列を削除するか、指定された下添字項目を指定して、削除されたテキストを返します。|
|`remove_at(index: int)`、`pop(index: int = -1) -> str`|指定された項目を削除して返します。|
|`clear() -> None`|クリアします。|
|`collection[index_or_value]`|下添字またはテキストで読み取ります。負の下添字、スライスをサポートします。|
|`collection[index] = value`|指定されたテキストを置き換えます。|
|`del collection[index]`|指定された項目を削除します。|
|`index_of(value: str, /) -> int`|最初の一致するテキストの下添字。見つからない場合はエラーを報告します。|
|`value in collection`|テキストが含まれているかをチェックします。|
|`len(collection)`、`bool(collection)`|数量と空の状態。|
|`iter(collection)`|テキストスナップショットをトラバースします。|

### 5.4.toolbar_button_collection

`toolbar.button_list`はツールバーボタンの集合を提供します。`len(collection)`と`bool(collection)`を通じて数量と空の状態を検索し、`item in collection`は名前またはオブジェクトでメンバーを検査します。`collection[index_or_name]`は整数、負数、スライス、名前をサポートします。`index_of(item)`を通じて位置を取得し、`add(item)`、`add_button(item)`、`insert(index, item)`はボタンオブジェクトまたは名前の文字列を受け入れ、`add_separator(name)`はセパレータを追加し、`remove(item)`、`remove_at(index)`、`clear()`は項目を外します。スナップショットを繰り返し使用します。

`listview_column_collection`、`listview_item_collection`、`listview_cell_collection`、`tree_node_collection`は、長さ、包含、正負のサブスカラス、スライス、イテレーションをサポートします。`append/add/insert`で追加し、`remove/remove_at/clear`で削除し、`assign`で全内容を置き換えます。セル集合は、サブスカラス値の設定や削除もサポートします。

### 5.5.メニュー集合

メニューは、通常のコンテナと同じ`control_collection`を使用し、名前またはインデックスで検索することができ、`add/insert/remove/clear`もサポートします。マルチレベルのメニューは、メニュー項目がネストされて構成されます。`separator = True`はセパレーターを表示し、`checkable/checked`はチェックを制御し、`shortcut`はショートカットキーを記録し、`&A`または`(&A)`はニーモニックキーを示します。

## 6.強制型イベント

### 6.1.サブスクリプションの方法はevent_containerと同じです。

コントロールの`on_xxx`メンバーは`event_container`を提供します。イベントコンテナはオブジェクトから取得され、コールバックはソースコントロールの`source`とイベントパラメータの`event`を受け取ります。パラメータの名前は`handler(source, event)`です。

```python
def button_ok_click(source, event):
    source.text = "Clicked"

button_ok.on_click += button_ok_click
button_ok.on_click -= button_ok_click
```

|署名または操作|用途|
|---|---|
|`add(callback) -> int`|追加コールバックとサブスクリプショントークンを返します。|
|`remove(callback_or_token) -> bool`|マッチするコールバックまたはトークンを削除します。成功した場合は`True`です。|
|`event += callback`|コールバックを追加し、同じイベントオブジェクトを保持します。|
|`event -= callback_or_token`|コールバックまたはトークンを削除し、同じイベントオブジェクトを保持します。|
|`clear() -> None`|すべてのコールバックを削除します。|
|`len(event)`|サブスクリプション数|
|`event.call(source, args)`、`event(source, args)`|現在のサブスクライバーにイベントを配布します。|
|`bool(event) -> bool`|サブスクリプションがある場合は`True`です。|

登録順に実行し、同じコールバックは複数登録できます。削除するたびに、マッチするサブスクリプションのみが処理されます。サブスクリプション識別子は、指定されたコールバックを削除するために使用されます。入力コンポーネントの`on_state_changed/on_input`は同じサブスクリプション操作を使用し、コールバックパラメータはそれぞれ`input_ui_state`、`input_event`です。

### 6.2.イベントパラメータ

パラメータクラスは`easyvrui`または`easyvrui.event`からインポートできます。下の表では、`event_args`は空のクラスであり、他の18種類のパラメータクラスはそれを継承します。例えば`issubclass(cancel_event_args, event_args)`は`True`です。コールバック中に対応するパラメータを設定する`event.cancel`または`event.handled`で、ネイティブの配布は書き込み状態を読み取ります。集合およびツリーノードのパラメータは、読み取り可能なオブジェクト参照を提供し、インデックスは0から始まります。

|パラメータタイプ|フィールド|用途|
|---|---|---|
|`event_args`|なし|クリック、フォーカス、ウィンドウのライフサイクルおよび固有の属性の変化。|
|`cancel_event_args`|`cancel: bool`|ウィンドウを閉じる前に`cancel`を設定すると、通常の閉じる操作をキャンセルできます。強制閉じる操作は常に実行されます。|
|`key_event_args`|`key: str`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`、`handled: bool`|キーナンバー、マウスキー、消費状態。|
|`text_input_event_args`|`text: str`、`handled: bool`|送信されたテキストと消費状態。|
|`pointer_event_args`|`hand: str`、`left: float`、`top: float`、`x: float`、`y: float`、`captured: bool`、`cancelled: bool`、`handled: bool`、`has_position: bool`、`has_local_position: bool`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`|手元、ウィンドウ座標`left/top`、コントロールのローカル座標`x/y`、およびマウスキーを含みます。`has_position`と`has_local_position`を使用して、対応する座標が有効かどうかを判断します。|
|`scroll_event_args`|`hand: str`、`delta_x: float`、`delta_y: float`、`handled: bool`|手元、横スクロール量、縦スクロール量、および消費状態。|
|`interaction_end_event_args`|`cancelled: bool`|移動、スケーリング、曲率調整、またはドラッグが終了しました。`cancelled`は操作がキャンセルされたことを示します。|
|`property_changed_event_args`|`property_name: str`|`property_name`は変更可能な属性名です。`source`を使用して現在の値を読み取ります。|
|`control_collection_event_args`|`item: control &#124; None`、`index: int`|集合内のコントロールとインデックス。全体の表通知の`item`は空です。|
|`menu_item_event_args`|`item: menuitem &#124; None`、`index: int`|メニュー項目とインデックス。|
|`tabpage_event_args`|`page: tabpage &#124; None`、`index: int`|タブオブジェクトとインデックス。|
|`listview_column_event_args`|`column: listview_column &#124; None`、`index: int`|ListView列オブジェクトとインデックス。全体の表通知の`column`は空です。|
|`listview_item_event_args`|`item: listview_item &#124; None`、`index: int`|ListView項目オブジェクトとインデックス。全体の表通知の`item`は空です。|
|`grid_column_event_args`|`index: int`、`width: int`|Grid列のインデックスと幅。ヘッダーをクリックすると、`index`を使用して列インデックスを読み取ります。|
|`grid_cell_event_args`|`row: int`、`column: int`、`error: str`|Gridセル行列のインデックス。編集が失敗した場合、`error`にはエラー説明が含まれます。|
|`tree_node_event_args`|`node: tree_node &#124; None`|操作のツリーノード。選択がキャンセルされた場合、`node`は空です。|
|`render_error_event_args`|`message: str`|レンダリングエラーのメッセージ。|
|`controller_event_args`|`hand: str`、`trigger: bool`、`grip: bool`、`joystick_x: int`、`joystick_y: int`、`joystick_pressed: bool`、`primary: bool`、`secondary: bool`|ハンドルキーとジョイスティックの状態。ジョイスティックの軸範囲は0から255までで、`primary`は左手のXまたは右手のA、`secondary`は左手のYまたは右手のBです。|
|`control_input_event_args`|`type: control_input_type`、`hand: str`、`key: str`、`text: str`、`left: float`、`top: float`、`x: float`、`y: float`、`steps: int`、`horizontal: bool`、`shift: bool`、`ctrl: bool`、`alt: bool`、`meta: bool`、`captured: bool`、`cancelled: bool`、`handled: bool`、`has_position: bool`、`has_local_position: bool`|派生コントロールの入力割り当てパラメータ。`type`を使用して入力を区別し、タイプに応じてフィールドを読み取り、`handled`を設定することで消費済みとマークできます。|

`control_input_type`の値は`none`、`click`、`focus_in`、`focus_out`、`pointer_enter`、`pointer_leave`、`pointer_move`、`pointer_down`、`pointer_up`、`scroll`、`key_down`、`key_up`、`text_input`、`controller_input`です。

## 7.描画とカスタムコントロール

### 7.1.render_context

`render_context`は`easyvrui`または`easyvrui.render`からインポートされます。コンテキストは`render(context)`と`render_overlay(context)`によって提供され、現在の描画コールバック内でのみ有効です。

`render_rectangle`は浮動小数点描画矩形レコードで、書き込み可能な`left/top/width/height`フィールドを提供します。`render_rectangle()`の各フィールドは初期値として0.0で、`render_rectangle(left, top, width, height)`はパラメータによって構築されます。`get_rectangle()`、`get_popup_rectangle()`、および`get_inset_rectangle()`はこのレコードを返します。Pythonの描画アクセスは、このレコードまたは4つの数値のシーケンス`(left, top, width, height)`を矩形パラメータとして同時に受け入れます。

`context.rectangle`は現在のコントロールが描画キャンバス内の矩形のタプルで、Pythonアクセスの便利な属性です。描画座標は同じキャンバス参照系を使用します。コントロールの局部内容を描画する際には、局部オフセットを返される`left/top`に加えます。

|属性またはシグネチャー|用途|
|---|---|
|`rectangle: tuple[float, float, float, float]`|読み取り専用；現在のownerの描画矩形|
|`owner: control`|読み取り専用；現在描画中のコントロール|
|`get_rectangle(item: control) -> render_rectangle`|指定されたコントロールの描画矩形を取得する|
|`get_popup_rectangle(item: item_control) -> render_rectangle`|項目コントロールのポップアップ領域矩形を読み取りする|
|`is_hovered(item: control) -> bool`|コントロールがハイライト状態かどうかを検索する|
|`is_hovered(item: control, rectangle) -> bool`|指定されたコントロールの指定矩形がハイライト状態かどうかを検索する|
|`is_focused(item: control) -> bool`|コントロールの視覚フォーカスを検索する|
|`is_blinking() -> bool`|現在の挿入点のフラッシュ周期が表示されるかどうかを検索する|
|`is_active(item: window) -> bool`|ウィンドウが現在アクティブなウィンドウかどうかを検索する|
|`is_blocked(item: window) -> bool`|ウィンドウがモダル関係でブロックされているかを検索する|
|`is_close_button_hovered(item: window) -> bool`|ウィンドウの閉じるボタンのハイライト状態を検索する|
|`get_hovered_item(item: item_control) -> int`|参照される項目のサブスコアを返す、ヒットしなければ-1|
|`fill(rectangle, color: int) -> None`|矩形を充填する|
|`outline(rectangle, color: int, thickness: float = 1.0) -> None`|矩形の境界線を描画する|
|`draw_line(x1: float, y1: float, x2: float, y2: float, color: int, thickness: float = 2.0) -> None`|線分を描画する|
|`fill_ellipse(center_x: float, center_y: float, radius_x: float, radius_y: float, color: int) -> None`|楕円を充填する|
|`outline_ellipse(center_x: float, center_y: float, radius_x: float, radius_y: float, color: int, thickness: float = 1.0) -> None`|楕円の境界線を描画する|
|`fill_circle(center_x: float, center_y: float, radius: float, color: int) -> None`|円を充填する|
|`draw_circle(center_x: float, center_y: float, radius: float, color: int, thickness: float = 1.0) -> None`|円の境界線を描画する|
|`fill_rounded_rectangle(rectangle, radius_x: float, radius_y: float, color: int) -> None`|丸みを帯びた長方形を充填する|
|`outline_rounded_rectangle(rectangle, radius_x: float, radius_y: float, color: int, thickness: float = 1.0) -> None`|丸みを帯びた長方形の境界線を描画する|
|`draw_text(value: str, font: font, rectangle, color: int, center: bool = False) -> None`|文字を描画する、`center=True`は中央に配置|
|`measure(text: str, font: font) -> float`|文字の幅を測定する|
|`draw_image(image: drawing_image, rectangle, opacity: float = 1.0) -> None`|画像を目的の矩形に描画する|
|`draw_screen(screen_id: int, rectangle) -> None`|指定されたディスプレイのリアルタイム画面を描画する|
|`fill_path(path: drawing_path, color: int) -> None`|パスを充填する|
|`outline_path(path: drawing_path, color: int, thickness: float = 1.0) -> None`|パスの輪郭を描画する|
|`push_clip(rectangle) -> None`|クロップされた矩形に圧入する；既存のクロップと共に後続の描画を制限する|
|`pop_clip() -> None`|上のクロップを復元する、圧入と一致する必要がある|
|`render_control_list(item: window) -> None`|ウィンドウの集合順序に従って通常のコントロールを描画する|
|`render_overlay_list(item: window) -> None`|ウィンドウ内のコントロールのフロートを描画する|
|`render_control(item: control) -> None`|指定されたコントロールの本体描画エントリを呼び出す|
|`render_control_overlay(item: control) -> None`|指定されたコントロールのフロート描画エントリを呼び出す|
|`render_context.get_inset_rectangle(rectangle, left_padding: float, right_padding: float, top_padding: float = 0.0, bottom_padding: float = 0.0) -> render_rectangle`|静的呼び出し、四辺の内側のピッチで矩形を計算する|
|`context.get_inset_rectangle(item: control, left_padding: float, right_padding: float) -> render_rectangle`|インスタンス呼び出し、指定されたコントロールの描画矩形で左右の内側を計算する|
|`draw_control(item: control, highlight: bool = True) -> None`|一般的なコントロールの背景と境界線を描画する。`highlight`はハイライトやフォーカススタイルを制御する|
|`get_foreground(item: text_control) -> int`|利用可能な状態を考慮した後の文字色を取得する|

座標は有限数でなければならない。幅と高さ、半径は負でできない；線の幅は`0`以上でなければならない；画像の透明度は`0.0`から`1.0`の範囲である。描画色は`0xRRGGBBAA`の整数を使用する。クロップは後続の描画のみを制限し、コントロールの矩形を変更しない

インスタンスの`get_inset_rectangle()`は静的な矩形パラメータも受け入れる。左右の内側のピッチは明示的に提供する必要がある；静的呼び出しは独立して矩形を計算することができ、インスタンス呼び出しは現在の描画コールバックの有効期限に従う

描画クエリは視覚的なフォーカスを使用する。入力がドレイン中の間はフォーカスの外観をキャンセルすることができ、ドレインが完了した後に論理的なフォーカスが切り替わる

### 7.2.drawing_path

構築。`drawing_path()`。デフォルトの充填規則は`drawing_fill_rule.even_odd`である

|署名または属性|用途|
|---|---|
|`fill_rule: drawing_fill_rule`|読み取り/書き込みの充填規則|
|`segment_list: list[drawing_path_segment]`|読み取り専用のパスセグメントのスナップショット|
|`clear() -> None`|パスセグメントをクリアする|
|`move_to(x: float, y: float) -> drawing_path`|新しいサブパス始点に移動する|
|`line_to(x: float, y: float) -> drawing_path`|直線を追加する|
|`quadratic_to(control_x: float, control_y: float, end_x: float, end_y: float) -> drawing_path`|二次ベジェ曲線を追加する|
|`cubic_to(control1_x: float, control1_y: float, control2_x: float, control2_y: float, end_x: float, end_y: float) -> drawing_path`|三次ベジェ曲線を追加する|
|`arc_to(end_x: float, end_y: float, radius_x: float, radius_y: float, rotation_degree: float = 0.0, clockwise: bool = True, large_arc: bool = False) -> drawing_path`|指定された終点への楕円弧に追加する；指定された半径、楕円の回転角、方向、および大きな弧を取るかどうか|
|`close() -> drawing_path`|現在のサブパスを閉じる|

パス追加方法と`close()`は現在のパスを返し、連鎖呼び出しをサポートします。各サブパスは`move_to()`から始まります。空のパスや直後に閉じたパスには、先に`move_to()`を使用して他のパスセグメントを追加する必要があります。座標は有限数でなければならず、円弧の半径は負になってはなりません。`clear()`はパスセグメントを削除し、塗りつぶしルールを保持します。`drawing_fill_rule`の列挙には`even_odd`の偶奇塗りつぶし、`non_zero`の非ゼロ巻き込み塗りつぶしが含まれます。

`easyvrui`から`drawing_path_segment`をインポートします。`segment_list`のパスセグメントには以下のフィールドがあります。

|フィールド|用途|
|---|---|
|`operation: drawing_path_operation`|`move/line/quadratic/cubic/arc/close`の一つ|
|`value_list: list[float]`|6つの数値スロットを固定します。`move/line`は`x,y`を使用し、`quadratic`は制御点と終点の4つの値を使用します。`cubic`は2つの制御点と終点の6つの値を使用し、`arc`は終点、半径、回転角の最初の5つの値を使用します。|
|`clockwise: bool`|円弧が時計回りか|
|`large_arc: bool`|円弧が大きな弧を選択しているか|

### 7.3.drawing_image

構築。`drawing_image(width: int, height: int, pixel_data)`。

`pixel_data`は連続するシングルバイトバッファを受け入れます。例えば`bytes/bytearray/memoryview`です。画像は行ごとに並べられ、各ピクセルはR、G、B、Aの4つのバイトで構成されます。長さは正確に`width * height * 4`でなければなりません。幅と高さは`0`以上でなければなりません。

|メンバー|用途|
|---|---|
|`width: int`|読み取り専用のピクセル幅|
|`height: int`|読み取り専用のピクセル高さ|
|`rgba_data: bytes`|読み取り専用のRGBAピクセルバイトコピー|
|`load_file(path: str) -> drawing_image`|静的なメソッドで、システムがサポートする画像ファイルを読み込み、ICOは最大の画像フレームを選択します。|
|`load_memory(data: bytes) -> drawing_image`|静的なメソッドで、完全にエンコードされた画像バイトから読み込みます。|
|`load_ico(data: bytes) -> drawing_image`|静的なメソッドで、ICOファイルヘッドをチェックし、メモリからアイコンを読み込みます。|
|`encode_ico() -> bytes`|RGBAピクセルを保持し、PNGシングルICOを無損失で生成します。幅と高さはそれぞれ1～256ピクセルです。|

### 7.4.派生コントロールの拡張ポイント

通常のコントロールはPythonで派生でき、状態は自身のメンバーに保存されます。Pythonのメソッド名は以下のオーバーライドシグネチャーと一致します。描画はフレームによって呼び出され、コールバックが返された後で一括して送信されます。

|オーバーライドシグネチャー|役割|
|---|---|
|`render(self, context)`|本体の描画。`super().render(context)`を使用してネイティブベースクラスの本体を描画できます。|
|`render_overlay(self, context)`|ポップアップレイヤーの描画；ベースクラスの同名の描画メソッドを呼び出すことができます。|
|`is_focusable(self) -> bool`|フォーカスナビゲーションに参加するかどうかを定義します。|
|`get_content_top(self) -> float`|コンテンツのトップオフセットを定義します。|
|`get_input_rectangle(self) -> rect`|コントロールのローカル入力エリアを返します。|
|`process_input(self, event)`|入力を処理し、対応するイベントルールに従って`event.handled`を設定します。`super().process_input(event)`を呼び出してベースクラスの処理を保持します。|

コンテナ派生クラスには3つのレイアウトヒールがあり、ネイティブフレームによって呼び出されます：

|オーバーライドシグネチャー|戻り値と機能|
|---|---|
|`get_active_control_list(self) -> list[control]`|現在レイアウト、描画、当たりに参加しているコントロールのリスト|
|`is_control_active(self, item: control) -> bool`|コントロールがアクティブ状態かどうかを指定します。|
|`get_managed_control_rectangle(self, item: control, rectangle: rect) -> rect \| None`|受容器管理の論理矩形を指定します。Noneは元の矩形を使用します。|

レイアウトフックはprotected拡張ポイントに属し、Python派生クラスでカバー可能であり、派生クラスのメソッド内でsuperを使用して対応するネイティブベースクラスの実装を呼び出します。デフォルトの集合の読み取りには`control_list`を使用し、Tabでは`page_list`を使用します。ウィンドウベースクラスの描画は、コンテキストの`render_control_list`によってコントロールの描画が配置されます。

```python
from easyvrui import control

class meter_control(control):
    def __init__(self, name):
        super().__init__(name)
        self.value = 0.5

    def render(self, context):
        left, top, width, height = context.rectangle
        context.fill((left, top, width, height), self.background_color)
        context.fill((left, top, width * self.value, height), 0x30B080FF)

    def set_value(self, value):
        self.value = max(0.0, min(1.0, value))
        self.invalidate()
```

`selection_control`派生クラスは`is_blank_at(local_left, local_top)`と`clear_selection()`をカバーできます。Grid派生クラスは`read_cell_value/write_cell_value/render_cell`をカバーでき、署名と書き込み結果の規定はgridセクションを参照してください。

## 8. ループの適用、接続、および入力インターフェース

### 8.1. 関数の実行

|署名|用途|
|---|---|
|`run(application_name: str) -> None`|`application_name`をセッション名として普通のウィンドウループを実行します。ロードされていない、または閉じられていないウィンドウがない場合、または実行環境が停止した場合に戻ります。|
|`set_application_name(application_name: str) -> None`|セッション名を登録します。必須であり、空でない文字列です。`run(application_name)`にはこのステップが含まれており、独立したメインループは最初の`pump()`の前に呼び出されます。|
|`pump(timeout_millisecond: int = 0) -> bool`|メッセージの配布とコールバック、タイミング状態の進行、更新待ちのウィンドウの送信。パラメータで指定されたミリ秒待ってから、ループが続行できる場合に`True`に戻ります。|
|`show_input_ui(window: window, rectangle: rect \| Sequence[int], completion = None) -> None`|関連するウィンドウで入力インターフェースを開きます。矩形の順序は`left, top, width, height`です。|
|`hide_input_ui(completion = None) -> None`|現在の入力インターフェースを収納する要求を出し、ドレインが完了した後に古い入力パスを終了します。|
|`get_application_directory() -> pathlib.Path`|アプリリソースディレクトリを特定します。|
|`measure_text(text: str, font: font) -> float`|指定されたフォントでテキストの幅を測定します。単位は論理ピクセルです。|

アプリループはUIスレッドでイベントを実行し、非同期完了通知とローカルでのコールバックを提供します。ネイティブ接続はサーバーイベントと非同期応答をそれぞれ保存し、メッセージポンプは受信順序で2つのキューを統合します。内部同期リクエストは自分自身の応答を待つだけで、その間に到着したイベントは後続のメッセージループで処理されます。実装は[IPC、TLS、および接続キュー](/ja/advanced/03_ipc_tls_protocol)を参照してください。

セッション名はエンジンアプリリスト内のこのプログラムを識別し、ウィンドウの所属を追跡するための基準です。名前は必須であり、空でない文字列です。接続が確立された後、名前は固定され、異なる名前を再度入力すると例外が発生します。明示的に名前が付けられていない場合、SDKは実行可能ファイル名をセッション名として使用します。

入力矩形はウィンドウの論理座標を使用し、テキスト編集領域を表します。関連するウィンドウは現在対話可能な普通のアプリウィンドウでなければなりません。layout/IMEセッションおよび補助ウィンドウはアプリの入力領域を開くことができません。`completion`は`Callable[[bool], None]`または`None`であり、操作が成功したかどうかを受け取ります。要求が発行された後、アプリループを続けて完了通知を処理します。表示されているウィンドウは隠されていても`run(application_name)`を続行できます。アプリが終了するとウィンドウは閉じられます。

編集可能なテキストコントロールのフォーカス変更は、コントロールフレームワークによって入力インターフェースで調整されます。カスタム入力エリアを使用する場合は、上記の関数を適用する必要があります。エンジンは現在のウィンドウでキーボードをルーティングし、ウィンドウ内のフォーカスはコントロールフレームワークによって配布されます。`Pause`は物理キーボードのインターセプトするモードを切り替え、編集エリアのみに仮想キーボードとIMEインターフェースを表示します。

編集コントロールをアクティブにした後、入力エリアの下に補助入力バーが表示され、言語、IME名、および「入力法切り替え」ボタンが表示されます。ボタンをクリックすると、まず入力インターフェースが隠れ、次にモーダル選択ダイアログが開きます。レイアウトリストは独立して選択され、言語リストはIMEリストのフィルタリングに使用されます。ダイアログは各言語の一時的な選択を保持し、「確定」をクリックすると選択が適用され、選択されたIMEをデフォルト項目に設定することもできます。キャンセルすると一時的な選択が放棄され、閉じた後元の編集コントロールに戻ります。物理キーボードモードで有効な現在のウィンドウがある場合、`Alt+Shift`は言語を切り替え、前回使用されたIMEを復元します。`Ctrl+Shift`は現在の言語内でIMEを切り替えます。

ウィンドウが表示されている間、SDKはこのプロセスのCtrl+Cをインターフェースのショートカットキーとして処理します。最後の表示ウィンドウが閉じた後、コンソール処理が回復します。Ctrl+Breakはコンソールの動作を継続します。

### 8.2.ローカルおよびリモート接続

ウィンドウや高層アプリケーションのインターフェースを使用する際には、必要に応じて接続を確立します。ローカルアプリケーションはローカルで情報を検出してエンジンに接続します。リモート接続パラメータは起動コマンドラインによって提供され、Python APIは同じパラメータセットを使用します：

|パラメータ|用途|
|---|---|
|`--easyvrui-host=値`|ホスト名、IPv4または裸のIPv6アドレス|
|`--easyvrui-port=値`|ポート、省略時は`49537`|
|`--easyvrui-access-credential=値`|アクセス証明|
|`--easyvrui-public-key-fingerprint=値`|サーバー側の公開鍵SHA-256フィンガープリント|

`--name=value`形式を使用します。アプリケーション自身のパラメータと同じコマンドラインに置きます。どのリモートパラメータが存在しても、リモート方式で検証されます。ホスト、証明書、フィンガープリントは必須であり、パラメータは重複したり空のりません。ポート範囲は`1`から`65535`です。例えば：

```cmd
python my_vr_app.py --easyvrui-host=192.0.2.10 --easyvrui-port=49537 --easyvrui-access-credential="my credential" --easyvrui-public-key-fingerprint=0000000000000000000000000000000000000000000000000000000000000000
```

接続と証明書の検証に失敗した場合は、エラーレポートを通じて報告されます。アプリケーション層はウィンドウ、グラフィック、入力インターフェースを使用して済みます。完全なメッセージフィールドの定義は[エンジンプロトコル参照](./engine_protocol)を参照してください。

### 8.3.アプリケーションリストと終了

`easyvrui`または`easyvrui.application_management`からアプリケーション管理インターフェースをインポートできます。リストの読取りとプロセスの起動は、呼び出し元のマシンで行われるため、アプリケーションとエンジンは異なるマシンに存在することができます。単一インスタンスはアプリケーション自身によって実装されます。アプリケーション管理のスナップショットには、検証されたエンジンのホストセッションとそのウィンドウが含まれ、Desktopと入力コンポーネントがフィルタリングされます。クエリと終了操作は検証されたエンジンのホストセッションを要求し、Desktopと入力コンポーネントは終了操作によって保護されます。

|署名|用途|
|---|---|
|`read_application_entry(manifest_path: str \| Path, language: str = "") -> application_entry`|リストを読み取り、指定された言語で名前を選択します。言語が空の場合はシステム言語を使用し、最終的には`en`に戻ります。|
|`launch_application(manifest_path: str, extra_argument_list: Sequence[str] \| None = None) -> int`|`.easyvrui`のリストを読み取り、本機でそのアプリケーションを起動し、新しいプロセスPIDを返します。`extra_argument_list`はリストで宣言されたパラメータの後に追加されます。リストが欠落しているか、起動に失敗した場合は例外を投げます。|
|`get_application_snapshot_list() -> list[application_snapshot]`|クエリエンジンが返すセッションスナップショットのリストを照会します。|
|`terminate_application(session_id: int) -> bool`|目標セッションに対応するプロセスを終了し、エンジンが与える操作結果を返します。|
|`close_application_window(session_id: int, window_id: int) -> bool`|目標セッションが指定されたウィンドウを正常に閉じるよう要求し、イベントが送信されたかを返します。|
|`request_application_snapshot_list(completion) -> None`|アプリケーションのスナップショットを非同期で照会します。|
|`request_terminate_application(session_id, completion) -> None`|アプリケーションを非同期で終了します。|
|`request_close_application_window(session_id, window_id, completion) -> None`|ウィンドウを正常に非同期で閉じます。|

コールバックがアプリケーションUIスレッドで実行され、`(result, error)`を受け取ります。スナップショットの照会結果はリストであり、アプリケーションを終了するかウィンドウを閉じる結果はブール値です。成功した場合`error`は`None`です。

#### `application_entry`

`read_application_entry()`は以下の読み取り/書き込み属性を設定します。パスはリストがあるディレクトリを基準にします。フィールドのルールは[アプリケーションリスト](./application_manifest)を参照してください。

|属性|用途|
|---|---|
|`id: str`、`name: str`|アプリケーションIDと完了言語が一致した後の表示名。|
|`icon_path: Path \| None`、`icon_data: bytes`|外部アイコンのパスと内蔵アイコンのファイルバイト。|
|`runtime: application_runtime`|デフォルト`native`は、ネイティブプログラムを起動することを意味します。`python`はPythonのメインスクリプトを起動することを意味します。|
|`executable: Path \| None`、`script: Path \| None`|解析されたネイティブプログラムのパスまたはPythonスクリプトのパス。|
|`argument_list: list[str]`|リストで宣言された起動パラメータ。|
|`type: application_type`|値は`application`、`desktop`、`layout`、または`ime`で、デフォルトは`application`です。|

#### `application_snapshot`

|属性|用途|
|---|---|
|`session_id: int`|エンジンが割り当てたセッションの識別子。|
|`process_id: int`|セッションに対応するプロセス番号。|
|`name: str`|セッション名。|
|`window_list: list[application_window]`|そのセッションで登録されたウィンドウのリスト。|
|`memory_bytes: int`|プロセスのメモリ使用量のバイト数。|
|`cpu_percent: float`|プロセスのCPU使用率のパーセンテージ。|
|`gpu_percent: float`|プロセスのGPU使用率のパーセンテージ。|

#### `application_window`

|属性|用途|
|---|---|
|`id: int`|ウィンドウの識別子。|
|`name: str`|ウィンドウを作成する際に提供されたアプリ内のウィンドウ名。|
|`title: str`|ウィンドウのタイトルバーのテキスト。|
|`visible: bool`|ウィンドウが現在見えるかどうか。|

### 8.4.フォーカスとTabキー。

デフォルトのボタン、テキストボックス、コンボボックス、リストはフォーカスを取得できます。通常のコンテナとラベルはTabナビゲーションには参加しません。ナビゲーションは隠されている、無効化されている、またはアクティブでないページ内のコントロールをスキップします。正の数`tab_index`はまず数値の昇順で並べられ、次に`tab_index = 0`の自動項目が並べられます。同じインデックスはウィンドウの絶対論理座標の`top`の昇順で、さらに`left`の昇順で並べられ、位置も同時にトラバース順序を保持します。したがって、自動ナビゲーションは上から下への行順で、同じ高さで左から右へと行われます。逆ナビゲーションは`Shift+Tab`を使用し、境界に達した後はループします。

テキストボックスのフォーカスが切り替わると、対応する入力領域も更新されます。現在のウィンドウを切り替える際には、以前の入力インターフェースを閉じます。カスタムコントロールは`focusable`を使用してフォーカスナビゲーションに参加するかどうかを宣言し、`process_input()`または`on_key_down/on_key_up`を使用してキー操作を処理します。

## 9.標準ダイアログボックス

`easyvrui`または`easyvrui.dialog`から以下の関数をインポートします。呼び出しはユーザーが完了するのを待って結果を返し、待機中はインターフェースのアクティビティを継続的に処理します。ownerは直接の親ウィンドウです。モーダル中はその親ウィンドウを無効にします。ダイアログボックスはそのphysical_scaleを継承し、Worldとcenterの位置を使用します。

|署名|戻り値|
|---|---|
|`color_dialog(color: int = 0x000000ff, title: str = "", default_color: int = 0x000000ff, owner: window \| None = None) -> int \| None`|確定すると`0xRRGGBBAA`が返され、キャンセルするとNoneが返されます。|
|`font_dialog(font: font = font(), title: str = "", default_font: font = font(), owner: window \| None = None) -> font \| None`|確定するとシステムフォントが返され、キャンセルするとNoneが返されます。|
|`messagebox(message: str, title: str = "", button_set = messagebox_button_set.ok, icon = messagebox_icon.none, default_button = dialog_result.none, owner: window \| None = None) -> dialog_result`|選択された標準ボタン|
|`messagebox(message: str, title: str, button_list: list[messagebox_button], icon = messagebox_icon.none, default_button_name: str = "", owner: window \| None = None) -> str`|選択されたボタンの名前|
|`inputbox(prompt: str, title: str = "", default_text: str = "", max_length: int = 0, owner: window \| None = None) -> str \| None`|確定すると文字が返され、キャンセルするとNoneが返されます。空の文字列と文字cancelは有効な入力です。|

`messagebox_button(name = "", text = "")`はボタンの識別と表示文字を保存します。メッセージボックスのエンハンスメントメンバーと数値はC++と一致します：

|エンハンスメント|メンバー|
|---|---|
|`messagebox_icon`|`none=0`、`error=0x10`、`question=0x20`、`warning=0x30`、`information=0x40`|
|`messagebox_button_set`|`ok=0`、`ok_cancel=1`、`abort_retry_ignore=2`、`yes_no_cancel=3`、`yes_no=4`、`retry_cancel=5`|
|`dialog_result`|`none=0`、`ok=1`、`cancel=2`、`abort=3`、`retry=4`、`ignore=5`、`yes=6`、`no=7`|

### 9.1.ファイルダイアログボックス

```python
file_open_dialog(title = "", initial_directory = None, initial_filename = "", filter_list = [], filter_index = 0, multi_select = False, confirm_text = "", owner = None, directory_changed = None, filter_changed = None)
file_save_dialog(title = "", initial_directory = None, initial_filename = "", filter_list = [], filter_index = 0, default_extension = "", confirm_overwrite = True, confirm_text = "", owner = None, directory_changed = None, filter_changed = None)
```

開くと`list[pathlib.Path]`が返され、キャンセルすると空のリストが返されます。保存すると`pathlib.Path`が返され、キャンセルすると`None`が返されます。`initial_directory=None`はメモリディレクトリを使用します。`directory_changed`はパスを受け取り、`filter_changed`は0から始まるフィルタリングインデックスを受け取ります。2つのコールバックは初期値と後続の変化を受け取ります。

`file_filter(name, pattern_list)`はフィルタリング名とファイルパターンを定義します。`confirm_text`は空の場合にはローカライズされたボタン文字を使用します。保存時には`default_extension`を使用して拡張子を補完し、`confirm_overwrite`を使用して確認のカットオーバーを制御します。

```python
import easyvrui

path = easyvrui.file_save_dialog(title = "保存", initial_filename = "window1", filter_list = [easyvrui.file_filter("EasyVRUI UI", ["*.easyvruifrm"])], default_extension = "easyvruifrm", owner = owner)
```

### 9.2.language_pack

`language_pack.current`はSDKの現在の言語パッケージを取得します。内蔵文字はSDKに組み込まれたPythonネイティブ拡張子に従い、デフォルトではシステム言語で選択されます。`language_pack.load_directory(path)`は指定されたディレクトリからカスタム言語パッケージを明示的にロードできます。このディレクトリは`en.json`で基本文字を提供し、他のファイルは言語コードで命名されます。

|プロパティまたは操作|用途|
|---|---|
|`locale: str`|現在の言語コードを読み取るまたは設定する|
|`available_locale_list: list[str]`|現在の言語パッケージが提供する言語コード|
|`key_list: list[str]`|`locale`でクエリ可能な言語キー|
|`len(pack)`、`key in pack`|言語キーの数とメンバークエリ|
|`pack[key]`|文字列を取得します。キーがなければ`KeyError`を送出します。|
|`pack.format(key, *args)`|パラメータを`{0}`、`{1}`などのプレースホルダーに代入|

## 10.独立なレイアウトとIMEアプリケーション

### 10.1.エンumerationとコンポーネント情報

|タイプ|メンバーのエンumeration|
|---|---|
|`input_role`|`layout`仮想キーボードレイアウト、`ime`入力法|
|`input_provider_state`|`stopped`起動していない、`starting`起動中、`running`実行中|

`provider_info()`デフォルト記録を構築可能、フィールドは読み取り専用：

|フィールド|タイプとデフォルト値|用途|
|---|---|---|
|`id`|`int = 0`|エンジン内のコンポーネント識別子|
|`name`|`str = ""`|表示名|
|`language`|`str = "en"`|IME言語コード、一般的にzh/en/ja、他の非空コードもサポート；レイアウト記録はデフォルト値を使用|
|`role`|`input_role.ime`|コンポーネントの役割|
|`state`|`input_provider_state.stopped`|起動状態|
|`configured`|`bool = False`|持続的な設定からのかどうか|
|`active`|`bool = False`|現在選択されているコンポーネントをクエリするかどうか|
|`default_provider`|`bool = False`|持続的なデフォルトIMEかどうか|
|`process_id`|`int = 0`|コンポーネントのプロセスID|
|`error`|`str = ""`|コンポーネントの最近のエラーメッセージ|

リスト記録はスナップショットです。コンポーネントが退出した後、記録は保持され、起動していない状態になります；動的に登録され、設定に書き込まれていないコンポーネントが退出した後、リストから削除されます。

IMEのlanguageは言語グループに使用され、レイアウトのプロトコル記録ではこのフィールドは省略されます。Pythonのprovider_info.languageは読み取り専用の文字列です；特定のIMEを選択すると、現在の入力言語も決定されます。

### 10.2.input_ui_state

構築。`input_ui_state()`。

|読み取り/書き込みフィールド|デフォルト値と用途|
|---|---|
|`active: bool`|`False`；コンポーネントが現在の活動的な入力パスにあるかどうか|
|`physical: bool`|`False`；現在が物理キーボードモードかどうか|
|`rectangle: render_rectangle \| None`|`None`；現在のコンポーネントの補助ウィンドウの位置矩形、順序は`left/top/width/height`|

物理キーボードモードではレイアウトインターフェースが折りたたまれ、レイアウト状態の`rectangle`は`None`になり得ます。IMEは状態に応じて自身のヒントウィンドウを表示するかどうかを決定します；英語の空のケースIMEはインターフェースが全くない場合もあります。

### 10.3.input_event

構築。`input_event()`。フィールドは書き込み可能：

|フィールド|デフォルト値と用途|
|---|---|
|`event_type: str`|`""`；キーイベントは`"key_down"/"key_up"`を使用し、テキストの送信は`"ime_submit"`を使用|
|`key: str`|`""`；論理キーノーマル|
|`text: str`|`""`；現在の入力に関連するテキスト|
|`shift: bool`|`False`；Shift状態|
|`ctrl: bool`|`False`；Ctrl状態|
|`alt: bool`|`False`；Alt状態|
|`meta: bool`|`False`；Windows/Metaキーの状態|
|`handled: bool`|`False`；IMEがイベントを消費するために`True`に設定|

読み取り専用属性`type`は`input_event_type`を返し、そのメンバーは`unknown`、`key_down`、`key_up`、`ime_submit`です。

### 10.4.input_provider

構築。`input_provider()`。通常のアプリケーションはコンポーネントをクエリでき、layoutとIMEアプリケーションはコンポーネントオブジェクトを作成し登録します。このクラスから派生し、処理関数をカバーすることを推奨します。

|属性|用途|
|---|---|
|`provider_list: list[provider_info]`|読み取り専用；コンポーネントが最近受け取ったリストのスナップショット|
|`role: input_role`|読み取り専用；現在登録されているロール、登録されていない場合は`ime`|
|`input_ui_state: input_ui_state`|読み取り専用；現在の入力パス状態のスナップショット|
|`session_id: int`|読み取り専用；現在のセッション番号、接続していない場合は0|
|`connected: bool`|読み取り専用；コンポーネントの接続状態|
|`draining: bool`|読み取り専用；コンポーネントが入力をドレインしているかどうか|
|`active: bool`|読み取り専用；現在の状態の`active`|
|`physical: bool`|読み取り専用；現在の状態の`physical`|

|署名|用途|
|---|---|
|`register_provider(role: input_role = input_role.ime, default_provider: bool = False, name: str = "", language: str = "en") -> None`|コンポーネントの登録を開始；後続のアプリケーションが登録結果をループ処理し、`default_provider`はデフォルトコンポーネントへの申請を意味します。languageはIMEにのみ使用され、空でない言語コードでなければなりません。デフォルトはenです。|
|`send_event(event: input_event) -> None`|現在の入力パスにイベントを送信|
|`commit_text(text: str, /) -> None`|IMEが最終テキストを送信；layoutがロールエラーを報告|
|`begin_input_task() -> None`|未完了の入力アサスチェムタスクを登録|
|`finish_input_task() -> None`|登録されたタスクを完了；開始とペアリングが必要|
|`run() -> None`|入力コンポーネントのループを実行；登録されていない場合はデフォルトIMEロールで登録を開始|
|`process_state(state: input_ui_state, /) -> None`|カバー可能；アクティブなパス、モード、および位置の変更を処理|
|`process_input(event: input_event, /) -> None`|カバー可能；IMEが受け取ったキーボード入力を処理|
|`process_drain() -> None`|カバー可能；ドレインに必要なアプリケーションの作業を完了|

登録後のセッションはlayoutまたはIMEロールに固定；コンポーネントウィンドウはフレームワークとEngineによって補助表面としてマークされ、Engineは関連する入力エリアに基づいて自動的に位置を決定し、スケーリングを継承します。設定された`reference_object`はEngineによって無視されます。これらのウィンドウはキーボード、候補、またはヒントインターフェースに使用されます。通常のアプリケーションは`show_input_ui()`を使用して入力エリアを開きます。

入力状態のコールバックは先に`process_state()`を実行し、その後`on_state_changed`をトリガーします。IMEキーは先に`process_input()`を実行し、その後`on_input`をトリガーします。最終的に`handled=False`の時にはキーがアプリケーションに転送され、`handled=True`の時にはIMEが消費します。テキストの送信は`commit_text()`を使用します。layoutはキーをIMEに送信し、その後IMEが処理または転送します。IMEの候補と組み合わせ状態はIMEアプリケーションが自ら維持します。

|イベント|コールバックの署名と用途|
|---|---|
|`on_state_changed`|`callback(state: input_ui_state) -> None`、入力パスの状態変化|
|`on_input`|`callback(event: input_event) -> None`、IMEがキーを受信。`handled`を変更可能|

入力インターフェースを停止、切り替え、収納する際、コンポーネントはドレイン通知を受け取る。非同期タスクは`begin_input_task()`で事前に登録し、出力送信後は`finish_input_task()`で完了する；ドレイン期間中は古いタスクと送信待ち結果の完了を待ち、その後コンポーネントインターフェースで確認を完了する。`process_drain()`は自身のバッファ作業を終了するのに適している。登録されていない、アクティブ化されていない、またはドレイン確認後に送信されたものは有効な入力パスには入らない。

```python
from easyvrui import input_provider, input_role

class english_ime(input_provider):
    def process_input(self, event):
        if ((((event.event_type == "key_down") and event.text) and (not event.ctrl)) and (not event.alt)) and (not event.meta):
            self.commit_text(event.text)
            event.handled = True

ime_english = english_ime()
ime_english.register_provider(input_role.ime, name = "EasyVRUI English", language = "en")
ime_english.run()
```

この例は処理と転送インターフェースの処理のみを演示している。実際の応用では、対応するキーの押下、離し、および修正状態の保持イベントを組み合わせ、必要なキーボードレイアウトに基づいてテキストマッピングを決定する必要がある。

## 11.言語と異常

|署名|用途|
|---|---|
|`get_error_language() -> str`|現在のエラーメッセージ言語を読み取る|
|`select_error_language(language: str, /) -> None`|メッセージ言語を切り替え、`zh/en/ja`をサポート|
|`get_localized_error(key: str, *argument_list) -> str`|言語キーを押してメッセージテキストを取得し、フォーマットパラメータを文字列に変換する|

これら3つの関数は`easyvrui`または`easyvrui.common.error`からインポート可能。初期言語はシステムの優先言語に基づいて選択される。

|タイプまたは関数|用途|
|---|---|
|`error_diagnostic(location = None, condition = "")`|呼び出し位置または指定された`error_diagnostic`に基づいて診断を構築する。`error_diagnostic(file, line, column, function, condition)`を使用して各フィールドを指定することもできる|
|`engine_error(key: error_key, argument_list = [], location = None, condition = "")`|エンジンエラー、`RuntimeError`を継承。読み取り専用の`key`は`error_key`の列挙値|
|`request_error(language_key: str, message: str, argument_list: list[str], diagnostic)`|リクエストエラー、`RuntimeError`を継承。`diagnostic`は既存の診断オブジェクトまたは診断フィールドを持つ異常を使用できる|
|`localized_invalid_argument(key: language_key, argument_list = [], location = None, expression = "")`|ローカライゼーションパラメータエラー、`ValueError`を継承。読み取り専用の`key`は`language_key`の列挙値|
|`localized_runtime_error(key: language_key, argument_list = [], location = None, expression = "")`|ローカライゼーション実行エラー、`RuntimeError`を継承。読み取り専用の`key`は`language_key`の列挙値|
|`get_error_diagnostic(error: BaseException) -> error_diagnostic`|異常が持つ診断を読み取る。通常の異常は呼び出し位置に基づいて診断を生成する|
|`get_error_message(error: BaseException) -> str`|診断情報を持つ単行異常テキストを読み取るまたは生成する|

`error_diagnostic`と上記の4種類の異常はすべて`get_message(key = "", detail = "")`を提供し、既存のソース、指定されたエラーチェックボタン、および説明に基づいて単行診断をフォーマットする。それらは以下の読み取り専用属性を共有する。

|属性|用途|
|---|---|
|`file: str`|診断ソースファイル|
|`line: int`|行番号|
|`column: int`|列番号|
|`function: str`|関数名|
|`condition: str`|失敗条件|

異常にはさらに`language_key: str`と`argument_list: list[str]`の読み取り専用属性があり、それぞれ言語キー文字列とフォーマットパラメータリストを記録する。`str(error)`は異常の完全なテキストを返し、`ファイル:行番号:列番号: error: 条件 [エラーキー] 説明`の形式で、エラーキーと説明が実際の情報に基づいて表示される。

## 12.コントロール属性索引

以下の属性は、それらを宣言したコントロールタイプに従って並べられている。派生物コントロールはベースクラスの属性を継承する。

|定義階層|属性|アクセス|
|---|---|---|
|`control`|`rect`|読み書き|
|`control`|`background_color`|読み書き|
|`control`|`visible`|読み書き|
|`control`|`enabled`|読み書き|
|`control`|`tab_index`|読み書き|
|`text_control`|`foreground_color`|読み書き|
|`text_control`|`font`|読み書き|
|`selection_control`|`clear_selection_on_blank_click`|読み書き|
|`item_control`|`selected_index`|読み書き|
|`item_control`|`selected_item`|読み取り専用|
|`item_control`|`row_height`|読み書き|
|`label`|`text`|読み書き|
|`button`|`text`|読み書き|
|`textbox`|`multiline`|読み書き|
|`textbox`|`max_length`|読み書き|
|`textbox`|`text`|読み書き|
|`textbox`|`read_only`|読み書き|
|`textbox`|`selectable`|読み書き|
|`textbox`|`horizontal_scrollbar_visible`|読み書き|
|`textbox`|`vertical_scrollbar_visible`|読み書き|
|`textbox`|`selection_start`|読み書き|
|`textbox`|`selection_length`|読み書き|
|`textbox`|`selected_text`|読み書き|
|`textbox`|`can_undo`、`can_redo`|読み取り専用|
|`combobox`|`dropdown_style`、`dropped_down`|読み書き|
|`combobox`|`text`|読み書き|
|`tabcontrol`|`selected_index`|読み書き|
|`tabcontrol`|`tab_position`|読み書き|
|`tabcontrol`|`tab_size`|読み書き|
|`tabcontrol`|`page_close_button_visible`|読み書き|
|`tabcontrol`|`tab_font`|読み書き|
|`tabcontrol`|`tab_foreground_color`|読み書き|
|`tabcontrol`|`tab_background_color`|読み書き|
|`tabcontrol`|`selected_tab_foreground_color`|読み書き|
|`tabcontrol`|`selected_tab_background_color`|読み書き|
|`window`|`title`|読み書き|
|`window`|`title_foreground_color`|読み書き|
|`window`|`title_background_color`|読み書き|
|`window`|`title_font`|読み書き|
|`window`|`physical_scale`|読み書き|
|`window`|`curvature`|読み書き|
|`window`|`startup_position`|読み書き|
|`window`|`curvature_adjustable`|読み書き|
|`window`|`position`|読み書き|
|`window`|`rotation`|読み書き|
|`window`|`reference_object`|読み書き|
|`window`|`show_title_bar`|読み書き|
|`window`|`tracking_mode_set`|読み書き|
|`window`|`show_close_button`|読み書き|
|`window`|`movable`|読み書き|
|`window`|`resizable`|読み書き|
|`checkbox`|`checked`|読み書き|
|`radiobutton`|`checked`|読み書き|
|`numericupdown`|`value`|読み書き|
|`numericupdown`|`minimum`|読み書き|
|`numericupdown`|`maximum`|読み書き|
|`numericupdown`|`step`|読み書き|
|`numericupdown`|`decimal_places`|読み書き|
|`slider`|`minimum`|読み書き|
|`slider`|`maximum`|読み書き|
|`slider`|`value`|読み書き|
|`slider`|`orientation`|読み書き|
|`progressbar`|`minimum`|読み書き|
|`progressbar`|`maximum`|読み書き|
|`progressbar`|`value`|読み書き|
|`treeview`|`selected_node`|読み書き|
|`scrollpanel`|`horizontal_scrollbar_visible`|読み書き|
|`scrollpanel`|`vertical_scrollbar_visible`|読み書き|
|`image`|`stretch_mode`|読み書き|
|`splitter`|`orientation`|読み書き|
|`splitter`|`split_position`|読み書き|
|`screen`|`screen_id`|読み書き|
|`grid`|`selection_mode`|読み書き|
|`grid`|`multi_select`|読み書き|
|`grid`|`row_height`|読み書き|
|`grid`|`header_height`|読み書き|
|`grid`|`read_only`|読み書き|
|`grid`|`selected_index`|読み書き|
|`grid`|`row_count`|読み書き|
|`menuitem`|`text`|読み書き|
|`menuitem`|`shortcut`|読み書き|
|`menuitem`|`checkable`|読み書き|
|`menuitem`|`checked`|読み書き|
|`menuitem`|`separator`|読み書き|
|`menubar`|`font`|読み書き|
|`menubar`|`row_height`|読み書き|
|`toolbar_button`|`separator`|読み書き|
|`toolbar_button`|`enabled`|読み書き|
|`toolbar_button`|`tooltip_text`|読み書き|
|`toolbar`|`tool_size`|読み書き|
|`toolbar`|`spacing`|読み書き|
|`item_control`|`item_list`|読み書き|
|`window`|`icon`|読み書き|
|`menuitem`|`icon`|読み書き|
|`toolbar_button`|`icon`|読み書き|
|`image`|`source`|読み書き|
|`listview`|`column_list`|読み書き|
|`listview`|`item_list`|読み書き|
|`grid`|`column_list`|読み書き|

## 13.Python演算子プロトコル索引

|プロトコルメソッド|使用入口|
|---|---|
|`__eq__`|`vec3/font/rect/color/reference_object`の同型値比較|
|`__add__`、`__sub__`|ベクトルの加算と減算|
|`__mul__`、`__rmul__`|ベクトルとスカラーの乗算；四元数、姿勢の組み合わせ|
|`__matmul__`|姿勢の`@`組み合わせ|
|`__int__`、`__index__`、`__str__`|色の整数、索引整数、テキスト変換|
|`__len__`、`__contains__`、`__getitem__`、`__delitem__`、`__iter__`|集合の長さ、含む、索引、削除、および巡回|
|`__setitem__`|文字列項目集合と`grid[row, column]`の下付き添字の割り当て|
|`__iadd__`、`__isub__`、`__bool__`|イベントコンテナの追加、削除、および購読の有無のチェック|

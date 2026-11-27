# C++APIインターフェースリファレンス

コントロールの使用方法と完全な例は[コントロールカタログ](/ja/guide/)を参照してください。ウィンドウインターフェースの例は[window](/ja/guide/controls/window-and-text/window)を、標準ダイアログの使用方法は[内蔵ダイアログ](/ja/guide/09_builtin_dialogs)を参照してください。

通常のコントロールのnameは`type_用途`を使用し、例えば`button_ok`です。デザイナーから出力されたパブリックコントロールメンバーのnameは同じ名前で、`button_ok`を通じて直接アクセスできます。ウィンドウクラスの名前はデザインファイルの名前に対応しています。

本文は`repo/sdk/api/cpp/include`のパブリックヘッダーファイルに対応しています。インストール後は`sdk/api/cpp/include/`の下のパブリックヘッダーを使用し、`#include <easyvrui.h>`を通じてすべてのパブリックインターフェースを導入できます。ライブラリとCMakeのエクスポートは`sdk/engine_interface/`にあります。

## 使用規則

### ネームスペースとリンク

ウィンドウ、コントロール、イベント、幾何学およびアプリケーションインターフェースは`easyvrui`ネームスペースにあり、`get_preferred_ui_language()`を含みます。`drawing_image`と`drawing_path`はグローバルネームスペースにあります。

C++20を使用し、APIヘッダーを同じビルドバージョンのライブラリと一緒に使用します。内蔵C++アプリケーションはデフォルトで`sdk/engine_interface/lib/engine_interface_static.lib`をリンクし、静的CRTを使用します。静的ライブラリ呼び出し者は`ENGINE_INTERFACE_STATIC`を定義します。DLLを選択する場合は、`lib/engine_interface.lib`を使用してライブラリをインポートし、同じSDKの`bin/engine_interface.dll`をデプロイします。消費者は互換性のある動的CRTを使用する必要があります。CMakeの補助設定は`sdk/engine_interface/lib/cmake/EngineInterface/`にあります。C++インターフェースは標準ライブラリの文字列、コンテナ、およびコールバックを使用し、呼び出しプログラムはコンパイラ、標準ライブラリ、ビルド設定、およびABIに合致する必要があります。

宣言中の`ENGINE_INTERFACE_API`はエクスポートマークであり、以下の署名ではそのマークを省略します。ヘッダーファイルでは使用の便宜のために`using std::...`が導入されていますが、これは標準ライブラリの元の意味で理解されます。

### タイプ、単位、および戻り値

|規則|意味|
|---|---|
|`u32string`、`std::u32string`、`U"..."`|Unicodeコードポイントシーケンスは、コントロール名、インターフェーステキスト、およびフォント名に使用されます。|
|`string`、`std::string`|このAPIでテキストを明確に指定する場合はUTF-8を使用します。プロトコルキー、診断、およびBase64は対応するインターフェースで別途説明されます。|
|`uint32_t color`|`0xRRGGBBAA`に従って並べられます。Alpha=0は完全に透明で、Alpha=255は不透明です。|
|`rectangle_t`|無符号整数の論理座標で、フィールドの順序は`left`、`top`、`width`、`height`です。|
|`render_rectangle_t`|doubleの論理座標で、描画に浮動小数点位置を使用できます。|
|`window.position`|参照対象に対するオフセットで、単位はメートルです。|
|`window.rotation`とオイラー角インターフェース|XYZ回転で、単位は度です。組み合わせの順序はRz×Ry×Rxです。|
|`physical_scale`|論理ピクセルの物理サイズのスケーリング倍率です。1倍の場合、各論理ピクセルは1ミリメートルに対応します。|
|`index`、`start`|通常0から始まりますが、具体的な内容は対応するインターフェースを参照してください。|
|テキストの選択位置|UTF-32コードポイントのオフセットです。実際の選択、移動、および削除は文字の境界を整列させます。|
|`optional<T>`|値がある場合はTを提供し、値がない場合は`nullopt`を使用します。|
|オブジェクトポインタ|インターフェース説明に`nullptr`の可能性がある状況をリストします。|
|`const T &`|読み取り専用の参照を借用し、その有効期間は元のオブジェクトとその後の変更に依存します。|
|`void`|オブジェクトの状態、イベント、または完了コールバックを通じて効果を提供します。|

`std::u32string`内の要素はコードポイントです。一つの可視文字素は複数のコードポイントで構成されることがあります。テキストセルの長さは依然としてコードポイントでカウントされます。

### スレッド、ライフサイクル、イベント

コントロールは作成時に現在のUIスレッドに属します。ウィンドウ、コンテナ、テキスト、メッセージのループ操作は所属するスレッドで実行されます。バックグラウンドワークが完了した後、`control_base::begin_invoke(callback)`を通じて更新が送信されます。通常のイベントはアプリケーションのメッセージループによって割り当てられ、`show_dialog()`は同じスレッドのネストされたループを通じて続けて割り当てられます。内部の同期リクエストは自身の応答を待つだけで、その間に到着したイベントはキューに残り、後のメッセージループによって処理されます。

コントロールの構築は`name`のみを要求します。名前は空であってはならず、U+0000を含まないこと、文字は有効なユニコードスカラで構成されていること、名前の構築後は読み取り専用であること、同じコントロールコンテナ内の名前は一意であり、異なるコンテナでは同じ名前を使用できます。コンテナは名前でオブジェクトを取得することができます。オブジェクトは一つの親を持つことができ、コントロールの階層は循環してはなりません。

`add(control &)`などの参照の重複は、呼び出し側がオブジェクトの生存を保証します。`add(shared_ptr<control>)`などの重複はコンテナが共有所有権を保持します。`remove`と`clear`はコンテナからの移動を表し、`dispose`はオブジェクトの解放を表します。`hide`はウィンドウを再表示用に保持し、`close`は閉じるおよびモダンパーニングプロセスを進みます。

コントロールイベントは`event_container<引数型>`を使用し、コールバックの署名は`void(control_base &source, 引数型 &event)`です。`add`を使用すると、取消登録のトークンを取得できます。`+=`を使用すると、直接登録できます。

```cpp
#include <easyvrui.h>
#include <memory>

using namespace std;

int main()
{
    easyvrui::set_application_name(U"demo");
    auto window_main = make_shared<easyvrui::window>(U"window_main");
    auto button_ok = make_shared<easyvrui::button>(U"button_ok");
    button_ok->set_rect(easyvrui::rectangle_t{24u, 80u, 200u, 44u});
    button_ok->set_text(U"确定");
    button_ok->on_click += [](easyvrui::control_base &source, easyvrui::event_args_t &)
    {
        source.invalidate();
    };

    window_main->get_control_list().add(button_ok);
    window_main->show();
    easyvrui::run(U"demo");
    return 0;
}
```

後続のコードセクションは上記のヘッドファイルとusing namespace stdを使用し、所属するアプリケーション関数内で実行されます。window_mainは呼び出し側が保持する`shared_ptr<window>`を表し、ownerは有効なウィンドウ参照を表します。

ウィンドウが表示中の間、SDKはこのプロセスのCtrl+Cをインターフェースのショートカットキーとして処理します。最後の表示ウィンドウが閉じた後、コンソール処理が回復します。Ctrl+Breakはコンソールの動作を継続します。

### 継承関係とプロパティの読み書き

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

派生物は祖先のすべてのpublicメンバーを継承します。後文では、各タイプが自身が宣言するpublicメンバーと重複をリストし、protectedメンバーは単独でリストされ、継承された同名のメソッドはC++のカバーと名前の隠蔽ルールに従って使用されます。`text_control`は文字の前景色とフォントを提供します。通常の`control`とコンテナは背景色を提供します。ウィンドウのタイトルとタブのタイトルはそれぞれ独立した文字の外観プロパティを持ちます。

プロパティは`get_xxx()`と`set_xxx(value)`を通じて読み取りと変更が可能です。各setterはプロパティをチェックし設定し、値が変更されると対応するイベントがトリガされます。

Tabナビゲーションは、現在のウィンドウ内でフォーカス可能で、表示され、有効で、アクティブなページ上のコントロールに対して使用されます。正のtab_indexは数値の昇順で並べられ、0はその後に並びます。同じグループはウィンドウの絶対的なtopから昇順で、次にleftから昇順で並べられ、位置が同じ場合は巡回順序が保持されます。Tabは前進し、Shift+Tabは後退し、始末と終わりの循環が可能です。Pauseは物理キーボードの入力を取り込むモードを切り替えます。テキストのフォーカスはIME/layoutの表示を制御し、他のフォーカス可能なコントロールは引き続きキー入力を受け付けます。

編集コントロールをアクティブにした後、入力エリアの下に補助入力バーが表示され、言語、IME名、および「入力法切り替え」ボタンが表示されます。ボタンをクリックすると、まず入力インターフェースが排空され、折りたたまれ、次にモーダルダイアログが開きます。layoutは独立して選択され、言語リストがIMEリストのフィルタリング範囲を決定します。各言語の一時的な選択は「確定」をクリックした後に適用され、キャンセルされると破棄されます。閉じた後は元の編集コントロールに戻ります。物理キーボードモードで現在のウィンドウが有効な場合、Alt+Shiftで言語を切り替え、前回使用されたIMEを復元します。Ctrl+Shiftで現在の言語内のIMEを切り替えます。

### 強制型イベント

コントロールは、第一引数でイベントのソースを提供し、第二引数の型はイベントメンバーの宣言によって決定されます。通常のイベントは`event_args_t`を使用し、他の18種類のコントロールイベントパラメータはこのベースクラスから公開継承されます。キャンセルまたは消費のマークがあるイベントは、`cancel`または`handled`でコールバックを更新することができ、配布プロセスは更新後の値を読み取ります。コンテナイベントは実際のオブジェクトを提供し、インデックスは0から始まります。

### リモート接続の起動パラメータ

接続エントリは現在のプロセスの起動パラメータを読み取り、すべてのリモートオプションは`--name=value`形式を使用します：

|パラメータ|用途とデフォルト値|
|---|---|
|`--easyvrui-host=アドレス`|リモートホスト名、IPv4または裸IPv6アドレス、例えば`::1`；リモートモードを使用する場合は必須|
|`--easyvrui-port=ポート番号`|十進数ポート、デフォルト49537、有効範囲は1から65535|
|`--easyvrui-access-credential=認証情報`|リモートアクセス証明書、必須|
|`--easyvrui-public-key-fingerprint=フィンガープリント`|サービス公開鍵SHA-256の16進フィンガープリント、必須|

アプリケーションは同じコマンドラインで自身の起動パラメータを提供できます。ローカルプログラムは自動検出を使用し、通常のコントロールは`run(application_name)`エントリを使用して現在の接続設定を使用します。プロトコルメッセージの定義は[Engineプロトコル参照](./engine_protocol)を参照してください。

### 設計ファイルのエクスポートレイアウト

生成されたC++レイアウトクラスは、設計ルートに対応するSDKタイプを継承し、すべての非ルートコントロールの参照はpublicメンバーであり、メンバー名は各control.nameと完全に一致します。ネストされたコンテナ、タブ、メニュー内のコントロールは、この生成クラスのメンバー名前空間を共同で使用するため、名前は設計全体で一意でなければならず、C++とPythonの識別子規則に従い、ルートSDKの公開エントリを避ける必要があります。

生成クラス自体はコンストラクタのみを定義します。通常のエクスポートでは、同名の`.h`と`.cpp`に宣言と実装をそれぞれ記述します。コンストラクタはコントロールを作成し、対応する集合に追加し、プロパティを初期化します。デフォルトでは、nameパラメータはデザインルートノードの名前を使用します。例えば`const std::u32string &name = U"sample_form"`です。ビジネスクラスは生成されたウィンドウインスタンスを保持し、同名のメンバーを通じてイベントをバインドし、コントロールのプロパティを読み取り、変更します。

画像とアイコンはSDKの`drawing_image::load_file()`などの描画リソースロードインターフェースを再利用します。値の記録はSDKタイプを通じて直接構築され、リソースファイルはエクスポート結果とともにデプロイされます。

## 公開ヘッダーファイルインデックス

|モジュール|ヘッダーファイル|
|---|---|
|描画|`drawing_image.h`、`drawing_path.h`、`easyvrui/render/render_context.h`、`easyvrui/render/render_style.h`|
|アプリケーションエントリ|`easyvrui/application.h`、`easyvrui/application_management.h`|
|モダルウィンドウ結果|`easyvrui/dialog/dialog_result.h`|
|基本値とテキストツール|`easyvrui/common/color.h`、`easyvrui/common/error.h`、`easyvrui/common/error_diagnostic.h`、`easyvrui/common/keyboard_key.h`、`easyvrui/common/u32string_hash.h`、`easyvrui/common/value.h`|
|標準ダイアログボックス|`easyvrui/dialog/color_dialog.h`、`easyvrui/dialog/file_open_dialog.h`、`easyvrui/dialog/file_save_dialog.h`、`easyvrui/dialog/font_dialog.h`、`easyvrui/dialog/inputbox.h`、`easyvrui/dialog/messagebox.h`|
|活動リストとツリーノード|`easyvrui/control/listview_column.h`、`easyvrui/control/listview_column_collection.h`、`easyvrui/control/listview_item.h`、`easyvrui/control/listview_item_collection.h`、`easyvrui/control/listview_cell_collection.h`、`easyvrui/control/tree_node.h`、`easyvrui/control/tree_node_collection.h`|
|イベント|`easyvrui/event/event_args.h`、`easyvrui/event/event_container.h`、`easyvrui/event/event_signal.h`|
|空間幾何学|`easyvrui/geometry/pose.h`、`easyvrui/geometry/quat.h`、`easyvrui/geometry/vec3.h`|
|入力コンポーネント|`easyvrui/input/input_provider.h`|
|エラーと言語|`easyvrui/localization/error.h`、`easyvrui/localization/language_pack.h`、`easyvrui/localization/request_error.h`|
|集約エントリ|`easyvrui.h`|
|エクスポート設定|`engine_interface_api.h`|

通常のアプリケーションはコントロールのpublicインターフェースを使用し、派生コントロールはこのファイルの各セクションにリストされたprotected拡張ポイントを使用します。

## アプリケーションエントリ

### `easyvrui.h`

一般的なコントロール、アプリケーション、イベント、および描画インターフェースの集約エントリ。通常のウィンドウアプリケーションはこのヘッダーファイルから始まります。

公開されているヘッダーファイルは76個あり、集約エントリは`easyvrui.h`あります。各インターフェースの宣言位置は以下を参照してください。

### `easyvrui/application.h`

ウィンドウアプリケーションのイベントループ、リソースクエリ、および入力エリア制御エントリ。

#### 自由関数とタイプ別名

|宣言|用途と戻り値|
|---|---|
|`void show_input_ui(window &item, const rectangle_t &rectangle, std::function<void(bool)> completion = {})`|itemウィンドウのロジック入力エリアrectangleを呼び出してIME/layoutを起動します。completionは操作が成功したかどうかのブール値を受け取ります。|
|`void hide_input_ui(std::function<void(bool)> completion = {})`|現在の入力エリアと関連するIME/layoutを収納します。completionは操作が成功したかどうかのブール値を受け取ります。|
|`void set_application_name(const std::u32string &application_name)`|非空セッション名を設定します。接続が確立された後、登録済みの名前を再設定できます。|
|`void run(const std::u32string &application_name)`|必須の非空名前でセッションを登録し、ウィンドウアプリケーションのイベントループを実行します。ウィンドウがすべて終了するか、実行環境が停止すると返します。|
|`bool pump(uint64_t timeout_millisecond = 0u)`|メッセージを配布し、コールバックを行い、更新されるウィンドウを提出し、指定されたミリ秒待ちします。falseを返すとループが終了します。|
|`std::filesystem::path get_application_directory()`|アプリケーションディレクトリを返し、これによりリソースを特定できます。|
|`double measure_text(const std::u32string &text, const font_t &font)`|指定されたフォントでテキストの幅を測定し、単位はロジックピクセルです。|

アプリケーションは、UIスレッドでサーバーイベントを割り当て、非同期完了通知とローカルでのコールバックを実行し、タイマー状態を進めて更新予定のウィンドウを提出します。接続は非同期応答とサーバーイベントをそれぞれ保存し、メッセージポンプが2つのキューを統合する際には受信順序を保持します。例えば、古い入力テキストが先に割り当てられ、その後に入力エリアの閉鎖完了コールバックが呼び出されます。内部の同期応答はリクエストIDごとに個別に提供されます。実装については[IPC、TLSおよび接続キュー](/ja/advanced/03_ipc_tls_protocol)を参照してください。

### `easyvrui/application_management.h`

`application_entry_t.name`はマッチング後の名前を保存し、`icon_path`はアイコンパスを保存し、`icon_data`は内蔵画像の原始ファイルバイトを保存します。`language`は空の場合はシステム言語を保存し、`en`に戻ります。リストフィールドについては[アプリケーションリスト](./application_manifest)を参照してください。

アプリケーションリストの読み取り、ローカル起動、アプリケーションスナップショットのクエリと終了の入口です。

#### 自由関数とタイプ別名

|宣言|用途と戻り値|
|---|---|
|`application_entry_t read_application_entry(const std::filesystem::path &manifest_path, const std::u32string &language = {})`|`.easyvrui`のリストを読み取り、起動説明に解析します。リストが欠落しているかフィールドが不正な場合は例外を投げます。|
|`uint32_t launch_application(const std::filesystem::path &manifest_path, const std::vector<std::u32string> &extra_argument_list = {})`|プロセスが存在するマシン上でマニフェストを読み取り、そのアプリケーションを起動し、新しいプロセスPIDを返します。extra_argument_listはマニフェストで宣言されたパラメータの後に追加されます。PythonエントリはPATH内のpython.exeを通じてマニフェストで指定されたスクリプトを実行します。起動に失敗した場合は例外を投げます。|
|`std::vector<application_snapshot_t> get_application_snapshot_list()`|クエリエンジンが返す、ローカルで検証されたアプリケーションスナップショットリストには、セッション名とウィンドウリストが含まれます。|
|`bool terminate_application(uint64_t session_id)`|終了対象のセッションに対応するプロセスを終了し、エンジンが与える操作結果を返します。|
|`bool close_application_window(uint64_t session_id, uint64_t window_id)`|リクエスト対象のセッションが指定されたウィンドウを正常に閉じるように要求し、イベントが送信されたかを返します。|
|`void request_application_snapshot_list(std::function<void(std::vector<application_snapshot_t>, std::exception_ptr)> completion)`|アプリケーションスナップショットの非同期クエリ。|
|`void request_terminate_application(uint64_t session_id, std::function<void(bool, std::exception_ptr)> completion)`|終了対象アプリケーションの非同期リクエリ。|
|`void request_close_application_window(uint64_t session_id, uint64_t window_id, std::function<void(bool, std::exception_ptr)> completion)`|対象ウィンドウの正常な非同期閉鎖リクエリ。|

リストの解析と起動はSDKのローカルで完了するため、プログラムとエンジンは異なるマシンに存在しても問題ありません。単一インスタンスはアプリケーション自身によって実装されます。インスタンスの調整は、対象アプリがプロセスインスタンスロックなどを使用して実行します。アプリケーションリストと終了操作は、検証されたエンジンのローカルセッションを要求します。リストにはDesktopが含まれ、入力コンポーネントがフィルタリングされます。Desktopと入力コンポーネントは終了操作によって保護されます。

非同期コールバックはアプリケーションUIスレッドで実行されます。スナップショットコールバックはスナップショットリストと`exception_ptr`を受け取り、操作コールバックはブール結果と`exception_ptr`を受け取ります。成功した場合は例外ポインタが空で、失敗した場合は再投げて診断を得ることができます。

#### `application_type_t`

声明。`enum class application_type_t`。

`application`は通常のアプリケーションを表し、`ime`と`layout`は入力コンポーネントを表し、`desktop`はデスクトップを表します。

|宣言|用途と呼び出しの意味|
|---|---|
|`application`|通常のアプリケーション。|
|`ime`|独立した入力法。|
|`layout`|独立したキーボードレイアウト。|
|`desktop`|デスクトップアプリケーション。|

#### `application_runtime_t`

声明。`enum class application_runtime_t`。

nativeは本機実行ファイルを使用し、PythonはPythonメインスクリプトを使用します。

|宣言|用途と呼び出しの意味|
|---|---|
|`native`|本機実行ファイルを起動します。|
|`python`|Pythonメインスクリプトを起動します。|

#### `application_entry_t`

声明。`struct application_entry_t`。

解析後のアプリケーションリスト、パスはリストがあるディレクトリに従って解析されます；nameは指定された言語またはシステム言語にマッチしており、マッチしない場合はenにリトライします。

|宣言|用途と呼び出しの意味|
|---|---|
|`std::u32string id`|リスト内のアプリケーションID。|
|`std::u32string name`|言語に応じてマッチしたアプリケーションの表示名。|
|`std::filesystem::path icon_path`|外部アイコンパス。|
|`std::vector<uint8_t> icon_data`|内蔵画像の原始ファイルバイト。|
|`std::filesystem::path executable`|本機プログラムまたはPythonインタプリタのパス。|
|`application_runtime_t runtime = application_runtime_t::native`|起動時のデフォルトはnativeです。|
|`std::filesystem::path script`|Pythonメインスクリプトのパス。|
|`std::vector<std::u32string> argument_list`|目標プログラムに追加されるパラメータリスト。|
|`application_type_t type = application_type_t::application`|アプリケーションタイプ、デフォルトは`application`です。|

#### `application_window_t`

声明。`struct application_window_t`。

アプリケーションスナップショット内のウィンドウ記録、idはグローバルウィンドウID、nameは固定内部名、titleは実際のウィンドウタイトル、visibleは表示状態です。

|宣言|用途と呼び出しの意味|
|---|---|
|`uint64_t id = 0u`|グローバルウィンドウID。|
|`std::u32string name`|ウィンドウ構築時の固定名。|
|`std::u32string title`|ユーザーが見る実際のウィンドウタイトル。|
|`bool visible = false`|ウィンドウが現在表示されているかどうか。|

#### `application_snapshot_t`

声明。`struct application_snapshot_t`。

Engineによって検証された本機アプリケーションセッションスナップショット、セッションID、プロセスID、名前、ウィンドウリスト、メモリバイト数、CPU/GPUパーセンテージを含みます。

|宣言|用途と呼び出しの意味|
|---|---|
|`uint64_t session_id = 0u`|EngineセッションID。|
|`uint32_t process_id = 0u`|本機プロセスID。|
|`std::u32string name`|セッション登録名。|
|`std::vector<application_window_t> window_list`|そのセッションのウィンドウリスト。|
|`uint64_t memory_bytes = 0u`|プロセスメモリ使用量、単位はバイト。|
|`double cpu_percent = 0.0`|プロセスCPU使用率パーセンテージ。|
|`double gpu_percent = 0.0`|プロセスGPU使用率パーセンテージ。|

## 基本値と空間幾何学

### `easyvrui/common/value.h`

フォント、コントロール矩形、方向の列挙。

#### 自由関数とタイプ別名

|宣言|用途と戻り値|
|---|---|

#### `font_t`

声明。`struct font_t`。

純粋なデータフォント値で、familyはシステムフォント名、sizeはuint64_tの論理フォントサイズで0以上でなければなりません。デフォルトではSegoe UI、18、bold=false、italic=falseです。operator==は各フィールドを比較します。

|宣言|用途と呼び出しの意味|
|---|---|
|`static constexpr uint64_t DEFAULT_SIZE = uint64_t{18u}`|font_tのデフォルト論理フォントサイズ。|
|`u32string family = U"Segoe UI"`|システムフォントのファミリー名。|
|`uint64_t size = DEFAULT_SIZE`|フォントの論理フォントサイズ。|
|`bool bold = false`|太字かどうか。|
|`bool italic = false`|斜体かどうか。|
|`bool operator==(const font_t &other) const = default`|対応するメンバー値を比較して等しいかどうかを返し、boolを返します。|

#### `rectangle_t`

声明。`struct rectangle_t`。

純粋なデータコントロールの矩形で、すべてのフィールドはuint64_tです。デフォルト値はleft=0、top=60、width=160、height=40です。コントロールのsetterは幅と高さが正であることを要求します。operator==は各フィールドを比較します。

|宣言|用途と呼び出しの意味|
|---|---|
|`uint64_t left = 0u`|矩形の左側の横座標。|
|`uint64_t top = 60u`|矩形の上側の縦座標。|
|`uint64_t width = 160u`|矩形の幅、単位は論理ピクセル。|
|`uint64_t height = 40u`|矩形の高さ、単位は論理ピクセル。|
|`bool operator==(const rectangle_t &other) const = default`|対応するメンバー値を比較して等しいかどうかを返し、boolを返します。|

### `easyvrui/common/color.h`

RRGGBBAA色値と成分、16進数および透明度の操作。

#### `color_t`

声明。`struct color_t`。

デフォルトのvalue=0は完全に透明な黒色です。32ビットの配列はRRGGBBAAで、最低8ビットは透明度、0は完全に透明、255は不透明です。

|宣言|用途と呼び出しの意味|
|---|---|
|`uint32_t value = 0u`|32ビットのRRGGBBAA色値。|
|`color_t() = default`|このタイプのインスタンスを構築します。パラメータの意味はこのタイプの説明と署名を参照してください。|
|`explicit color_t(uint32_t value)`|このタイプのインスタンスを構築します。パラメータの意味はこのタイプの説明と署名を参照してください。|
|`std::array<uint8_t, 4u> get_rgba() const`|R、G、B、Aの順序で4ビットの8ビット成分を返します。|
|`std::string get_hex() const`|0xで始まるRRGGBBAA16進数の色文字列を返します。|
|`color_t create_with_alpha(uint8_t alpha) const`|RGBを保持し、alphaを置き換えて新しい色値を返します。|
|`bool operator==(const color_t &other) const = default`|対応するメンバー値を比較して等しいかどうかを返し、boolを返します。|

### `easyvrui/geometry/vec3.h`

3次元ベクトル。

#### `vec3_t`

声明。`struct vec3_t`。

デフォルトではゼロベクトルです。operator==は各成分をdouble精度でスケーリングした近似比較を行い、有限値でない比較はfalseを返します。

|宣言|用途と呼び出しの意味|
|---|---|
|`double x = 0.0`|ベクトルのX成分。|
|`double y = 0.0`|ベクトルのY成分。|
|`double z = 0.0`|ベクトルのZ成分。|
|`static bool is_equal(double left, double right)`|double精度の閾値と数値スケールで有限浮動小数点数を比較する；非有限値はfalseを返す。|
|`bool operator==(const vec3_t &other) const`|3つのdouble成分で近似比較し、is_equalルールを使用する。|
|`vec3_t operator+(vec3_t b) const`|各成分を加算し、新しいvec3_tを返す。|
|`vec3_t operator-(vec3_t b) const`|各成分を減算し、新しいvec3_tを返す。|
|`vec3_t operator*(double scalar) const`|すべての成分にスカラーを乗じし、新しいベクトルを返す。|
|`double calculate_dot_product(vec3_t b) const`|bとの点積を返す。|
|`vec3_t calculate_cross_product(vec3_t b) const`|bとの外積を返す。|
|`double get_length() const`|3次元ベクトルの長さを返す。|
|`vec3_t get_normalized() const`|単位長さのベクトルを返す；ゼロ値、過小値、非有限入力は例外を投げる。|

### `easyvrui/geometry/quat.h`

四元数回転。

#### `quat_t`

声明。`struct quat_t`。

デフォルトの単位回転{x=0, y=0, z=0, w=1}。軸角とエウロー角のインターフェースは度で表される；create_from_eulerはRz×Ry×Rxの組み合わせである。get_inverse/rotateは現在の値を正規化して回転を解釈する。

|宣言|用途と呼び出しの意味|
|---|---|
|`double x = 0.0`|四元数のX成分。|
|`double y = 0.0`|四元数のY成分。|
|`double z = 0.0`|四元数のZ成分。|
|`double w = 1.0`|四元数の実数成分；単位回転は1である。|
|`quat_t operator*(quat_t b) const`|現在の四元数をbと組み合わせ、bに対応する回転が最初に適用される。|
|`quat_t get_normalized() const`|単位四元数を返す；ゼロ値、過小値、非有限入力は例外を投げる。|
|`quat_t get_inverse() const`|逆回転を表す四元数を返す。|
|`vec3_t rotate(vec3_t v) const`|現在の四元数でベクトルvを回転させ、回転結果を返す。|
|`static quat_t get_axis(vec3_t v, double angle)`|単位軸vとangle度で軸角四元数を作成する；呼び出し側が単位軸を提供する。|
|`static quat_t create_from_euler(vec3_t v)`|XYZ角度で回転を作成し、Rz×Ry×Rxの組み合わせとする。|
|`vec3_t get_euler_angle_vector() const`|現在の四元数に等価なXYZエウロー角を返す；単位度で；異なる角度の組み合わせが同じ姿勢を表すことがある。|
|`static quat_t create_from_axis_basis(vec3_t a, vec3_t b, vec3_t c)`|3つの軸ベクトルa/b/cで回転を作成し、正規化する。|
|`static quat_t blend(quat_t a, quat_t b, double t)`|a/bに対して最短の同方向の正規化線形補間を行い、tは通常0から1までとする。|

### `easyvrui/geometry/pose.h`

位置と四元数回転の組み合わせ姿勢。

#### `pose_t`

声明。`struct pose_t`。

デフォルトではpositionはゼロ、rotationは単位四元数である。a*bはbの局所姿勢をaに組み合わせることを表す；transform_pointは回転後に平行移動を実行する。

|宣言|用途と呼び出しの意味|
|---|---|
|`vec3_t position`|三次元平行移動。|
|`quat_t rotation`|四元数で姿勢回転を表現する。|
|`pose_t operator*(const pose_t &b) const`|現在の姿勢とbを組み合わせ、bが先に作用し、その後現在の姿勢が変換される。|
|`pose_t get_inverse() const`|逆姿勢を返す。|
|`vec3_t transform_point(vec3_t v) const`|局所点vを現在の姿勢の親参照系に変換する。|

### `easyvrui/control/reference_object.h`

オプションのウィンドウ参照対象は`world`、`body`、`head`、`left`、および`right`。Engineは関連する入力エリアに基づいてIME/layoutの補助表面を位置決めする。

#### 自由関数とタイプ別名

|宣言|用途と戻り値|
|---|---|
|`u32string get_reference_object_type_name(reference_object_type_t value)`|参照対象の列挙をUnicode名に変換する。|
|`reference_object_type_t parse_reference_object_type(const u32string &value)`|Unicode名を参照対象に解析する；無効な名前は例外を投げる。|

#### `reference_object_type_t`

声明。`enum class reference_object_type_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`world`|世界空間参照。|
|`body`|身体位置に従い、校正された方向を保持する参照。reset_body_centerを使用して再校正可能。|
|`head`|ヘッドマウント参照、位置と回転に従う。|
|`left`|左手ハンドル参照。|
|`right`|右手ハンドル参照。|

#### `reference_object_t`

声明。`struct reference_object_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`reference_object_type_t type = reference_object_type_t::world`|参照対象のカテゴリー。|
|`bool operator==(const reference_object_t &other) const = default`|対応するメンバー値を比較して等しいかどうかを返し、boolを返します。|

## イベントと値のコンテナ

### `easyvrui/event/event_signal.h`

登録順に呼び出されるジェネリックイベントチェーン。

#### `event_signal<source_type, argument_type_list...>`

声明。`class event_signal`。

テンプレートパラメータはsource_typeとargument_type_list...であり、処理関数の署名はvoid(source_type &, argument_type_list &...)。addは登録トークンを返す；removeとoperator-=はトークンを使用し、operator+=はイベントチェーンの参照を返す。callは登録順に呼び出される；現在の呼び出しは処理関数リストのスナップショットを使用し、この回の追加や削除は次回の呼び出しで反映される。コールバックの例外は呼び出し側に伝播する。イベントチェーンは所属オブジェクトのスレッドが使用する。

|宣言|用途と呼び出しの意味|
|---|---|
|`uint64_t add(std::function<void(source_type &, argument_type_list &...)> callback)`|登録された非空コールバックを返し、uint64_tトークンを使用して、後のremoveまたはoperator-=に使用する。|
|`event_signal &operator+=(std::function<void(source_type &, argument_type_list &...)> callback)`|コールバックを登録し、イベントチェーンの参照を返す。C#式の追加構文に適している；取り消しが必要な場合は、トークンを保持するためにaddを優先して呼び出す。|
|`bool remove(uint64_t token)`|tokenで指定された処理関数を削除する；trueを返す場合はtrue、そうでない場合はfalse。|
|`event_signal &operator-=(uint64_t token)`|tokenに対応する処理関数を削除し、イベントチェーンの参照を返す。|
|`void clear()`|すべての処理関数を削除する。|
|`bool is_empty() const`|イベントチェンルにゼロのサブスクリプションがあるかを検索する。|
|`void call(source_type &source, argument_type_list &...argument_list) const`|登録順に、sourceと参照パラメータで現在のイベントチェーンを呼び出す；コールバックはvoidを返す。|

### `easyvrui/event/event_container.h`

control_baseをイベントソースとするイベントチェーンタイプの別名。

#### 自由関数とタイプ別名

|宣言|用途と戻り値|
|---|---|
|`using event_container = event_signal<control_base, argument_type_list...>`|template<typename... argument_type_list>の別名で、イベントソースはcontrol_baseに固定される。|

### `easyvrui/event/event_args.h`

`event_args_t`は空ベースクラス。以下の表の残りの18種類の構造体はすべて`event_args_t`から公開継承される。各イベントは、その宣言された具体的なパラメータタイプでサブスクライバを呼び出す。

|パラメータタイプ|フィールド|用途|
|---|---|---|
|`event_args_t`|なし|クリック、フォーカス、ウィンドウのライフサイクルおよび各固有の属性の変化。|
|`cancel_event_args_t`|`bool cancel = false`|ウィンドウを閉じる前に`cancel`を設定すると、通常の閉じる操作をキャンセルできる。強制閉じる操作は常に実行される。|
|`key_event_args_t`|`std::u32string key`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`、`bool handled = false`|キーナンバー、マウスキー、消費状態。|
|`text_input_event_args_t`|`std::u32string text`、`bool handled = false`|送信されたテキストと消費状態。|
|`pointer_event_args_t`|`std::u32string hand`、`double left = 0.0`、`double top = 0.0`、`double x = 0.0`、`double y = 0.0`、`bool captured = false`、`bool cancelled = false`、`bool handled = false`、`bool has_position = false`、`bool has_local_position = false`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`|手の位置、ウィンドウ座標`left/top`、コントロールのローカル座標`x/y`、およびマウスキーを含む。`has_position`と`has_local_position`を使用して対応する座標が有効かどうかを判断する。|
|`scroll_event_args_t`|`std::u32string hand`、`double delta_x = 0.0`、`double delta_y = 0.0`、`bool handled = false`|手の位置、横スクロールと縦スクロール量、消費状態。|
|`interaction_end_event_args_t`|`bool cancelled = false`|移動、ズーム、カーブ調整、またはドラッグが終了する。`cancelled`は操作がキャンセルされたことを表す。|
|`property_changed_event_args_t`|`std::u32string property_name`|`property_name`は変化する属性名。`source`を使用して現在の値を読み取る。|
|`control_collection_event_args_t`|`control *item = nullptr`、`size_t index = 0u`|集合内のコントロールとインデックス。全体表通知の`item`は空である。|
|`menu_item_event_args_t`|`menuitem *item = nullptr`、`size_t index = 0u`|メニュー項目とインデックス。|
|`tabpage_event_args_t`|`tabpage *page = nullptr`、`size_t index = 0u`|タブオブジェクトとインデックス。|
|`listview_column_event_args_t`|`std::shared_ptr<listview_column> column`、`size_t index = 0u`|ListView列オブジェクトとインデックス。全体表通知の`column`は空である。|
|`listview_item_event_args_t`|`std::shared_ptr<listview_item> item`、`size_t index = 0u`|ListView項オブジェクトとインデックス。全体表通知の`item`は空である。|
|`grid_column_event_args_t`|`size_t index = 0u`、`uint64_t width = 0u`|Grid列のインデックスと幅。表ヘッダーをクリックすると`index`を使用して列インデックスを読み取る。|
|`grid_cell_event_args_t`|`uint64_t row = 0u`、`uint64_t column = 0u`、`std::u32string error`|Gridセル行列のインデックス。編集が失敗した場合、`error`にはエラー説明が含まれる。|
|`tree_node_event_args_t`|`tree_node *node = nullptr`|操作のツリーノード。選択がキャンセルされた場合、`node`は空である。|
|`render_error_event_args_t`|`std::string message`|レンダリングエラーのメッセージ。|
|`controller_event_args_t`|`std::u32string hand`、`bool trigger = false`、`bool grip = false`、`uint8_t joystick_x = 128u`、`uint8_t joystick_y = 128u`、`bool joystick_pressed = false`、`bool primary = false`、`bool secondary = false`|ハンドルキーとジョイスティックの状態。ジョイスティックの軸範囲は0から255までで、`primary`は左手Xまたは右手A、`secondary`は左手Yまたは右手Bである。|
|`control_input_event_args_t`|`control_input_type_t type = control_input_type_t::none`、`std::u32string hand`、`std::u32string key`、`std::u32string text`、`double left = 0.0`、`double top = 0.0`、`double x = 0.0`、`double y = 0.0`、`int64_t steps = 0`、`bool horizontal = false`、`bool shift = false`、`bool ctrl = false`、`bool alt = false`、`bool meta = false`、`bool captured = false`、`bool cancelled = false`、`bool handled = false`、`bool has_position = false`、`bool has_local_position = false`|派生コントロールの入力委任パラメータ。`type`を使用して入力を区別し、フィールドをタイプごとに読み取り、`handled`を設定すると消費済みとマークされます。|

`control_input_type_t`の値は`none`、`click`、`focus_in`、`focus_out`、`pointer_enter`、`pointer_leave`、`pointer_move`、`pointer_down`、`pointer_up`、`scroll`、`key_down`、`key_up`、`text_input`、`controller_input`です。

## コントロールの基底クラスとコンテナ

### `easyvrui/control/control_base.h`

コントロールの識別子、親クラス、ライフサイクル、プロパティアクセス、および基本イベント。

#### `control_base`

声明。`class control_base : public std::enable_shared_from_this<control_base>`。

アイデンティティとライフサイクル基底クラス、`std::enable_shared_from_this<control_base>`から継承。コンストラクタはprotectedで、派生クラスが呼び出します。nameとtypeは構築後に読み取り専用です；get_id()は実行時の番号です。コントロールは複製できません。オブジェクト操作は所属するUIスレッドの制約に従い、スレッド間の更新にはbegin_invokeを使用します。継承されたshared_from_this()とweak_from_this()は標準ライブラリの共有所有権規則に従います；参照方式で管理されるコントロールは通常、コンテナとコントロールインターフェースを使用してアクセスされます。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_disposed`|オブジェクトが解放されるときにトリガーされます。|
|`event_container<property_changed_event_args_t> on_property_changed`|プロパティ値が変更されるときにトリガーされます。property_nameは変更されるプロパティ名です。|
|`virtual ~control_base()`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`virtual uint64_t get_id() const`|実行時に割り当てられたオブジェクト番号を読み取ります。|
|`virtual control_base *get_parent() const`|親オブジェクトのポインタを読み取ります。トップレベルオブジェクトはnullptrです。|
|`virtual bool get_disposed() const`|オブジェクトが解放されたかどうかを読み取ります。|
|`virtual void invalidate()`|所属するウィンドウの再描画を要求します；カスタム状態の変更後に画面を更新する場合に適用されます。|
|`virtual void dispose()`|コントロールと関連する実行時リソースを解放します；解放後はそのオブジェクトの使用を停止します。|
|`virtual void begin_invoke(std::function<void()> callback)`|callbackを所属するUIスレッドにキューイングします；オブジェクトが実行前に解放される場合はコールバックをスキップします。|
|`virtual const u32string &get_name() const`|構築時に決定された名前を読み取ります。|
|`virtual const u32string &get_type() const`|オブジェクトのタイプ名を読み取ります。|
|`virtual const u32string &get_tag() const`|アプリケーションが保存した文字列マーカーを読み取ります。デフォルトでは空文字列です。|
|`virtual void set_tag(const u32string &value)`|マーカーを設定します。値が変更されると`on_tag_changed`がトリガーされます。|
|`event_container<event_args_t> on_tag_changed`|マーカーが変更されるとトリガーされ、コールバックはソースコントロールと追加データの`event_args_t`を受け取ります。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`virtual std::shared_ptr<control_base> get_retained_owner()`|操作期間中にオブジェクトのライフサイクルを保持するための共有参照を返します。|
|`virtual bool notify_property_changed(std::u32string_view name, bool changed, event_container<event_args_t> *specific = nullptr, bool redraw = true)`|プロパティが変更されると通知をトリガーし、trueを返します。redrawは再描画を要求するかどうかを制御します。|
|`control_base(const u32string &name, const u32string &type)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|
|`virtual void process_input(control_input_event_args_t &event)`|コントロールの入力イベントを処理する虚関数；派生拡張が可能で、event.typeによって入力タイプを区別します。|

### `easyvrui/control/control.h`

可視コントロールの共通属性と入力イベント。

#### `control`

声明。`class control : public control_base`。

直接構造化可能な可視クラスベース。デフォルトのrectは{0,60,160,40}、visible=true、enabled=true、tab_index=0です。デフォルトではフォーカスを受け付けません。背景色はデフォルトで0x162738FFです。容器内の座標は相対的な親レベルのロジック単位を使用します。

`control_base`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_background_color_changed`|背景色が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_visible_changed`|可視状態が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_enabled_changed`|利用可能状態が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_tab_index_changed`|Tabのフォーカス順序が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_moved`|論理位置またはウィンドウ空間位置が変更されたときにトリガーされます。元のオブジェクトの現在の属性に基づきます。|
|`event_container<event_args_t> on_size_changed`|rectの幅と高さが変更されたときにトリガーされます。|
|`event_container<pointer_event_args_t> on_pointer_enter`|レーザーがコントロールに入ったときにトリガーされます。|
|`event_container<pointer_event_args_t> on_pointer_leave`|レーザーがコントロールから出たときにトリガーされます。|
|`event_container<pointer_event_args_t> on_pointer_move`|レーザーがコントロール上で指し示す位置が変更されたときにトリガーされます。|
|`event_container<pointer_event_args_t> on_pointer_down`|レーザーレバーが押されたときにトリガーされます。|
|`event_container<pointer_event_args_t> on_pointer_up`|レーザーレバーが解放されたり、キャンセルされたときにトリガーされます。cancelledはキャンセルされたかどうかを示します。|
|`event_container<event_args_t> on_click`|コントロールのクリックが完了したり、デフォルトでアクティブになったときにトリガーされます。|
|`event_container<scroll_event_args_t> on_scroll`|スクロール入力がコントロールに到達したときにトリガーされます。|
|`event_container<event_args_t> on_viewport_changed`|スクロールビューの変更があったときにトリガーされます。|
|`event_container<event_args_t> on_focus_in`|コントロールがキーボードのフォーカスを得たときにトリガーされます。|
|`event_container<event_args_t> on_focus_out`|コントロールがキーボードのフォーカスを失ったときにトリガーされます。|
|`event_container<key_event_args_t> on_key_down`|キーが押されたときにトリガーされます。パラメータにはキーナンバー、マウスキー、消費状態が含まれます。|
|`event_container<key_event_args_t> on_key_up`|キーが解放されたときにトリガーされます。|
|`explicit control(const u32string &name)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|
|`virtual bool is_focusable() const`|コントロールタイプがフォーカスを受け入れるかどうかを検索します。実際のフォーカスはvisible、enabled、ウィンドウのモーダル状態にも影響されます。|
|`virtual const rectangle_t &get_rect() const`|相対的な親レベルのロジック矩形を読み取ります。|
|`virtual void set_rect(const rectangle_t &value)`|相対的な親レベルのロジック矩形を設定します。|
|`virtual uint32_t get_background_color() const`|背景色を読み取り、形式は0xRRGGBBAAです。|
|`virtual void set_background_color(uint32_t value)`|背景色を設定し、形式は0xRRGGBBAAです。|
|`virtual const u32string &get_tooltip_text() const`|ハイライトテキストを読み取り、デフォルトでは空文字列です。|
|`virtual void set_tooltip_text(const u32string &value)`|ハイライトテキストを設定します。|
|`event_container<event_args_t> on_tooltip_text_changed`|テキストが変更されたときにトリガーされます。|
|`virtual bool get_visible() const`|可視状態を読み取ります。|
|`virtual void set_visible(bool value)`|可視状態の設定。|
|`virtual bool get_enabled() const`|互換状態の読取り。|
|`virtual void set_enabled(bool value)`|互換状態の設定。|
|`virtual uint64_t get_tab_index() const`|Tabフォーカス順序の読取り、デフォルトは0。|
|`virtual void set_tab_index(uint64_t value)`|Tabフォーカス順序の設定、デフォルトは0。|
|`~control() override`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`virtual void show()`|コントロールまたはウィンドウを表示し、対応する可視性とウィンドウのライフサイクル動作をトリガーする。|
|`virtual void hide()`|コントロールまたはウィンドウを隠す。関連するフォーカス、キャプチャ、入力エリアはウィンドウ状態に応じて解放される。|
|`virtual void focus()`|このコントロールにキーボードフォーカスを移動する要求。|
|`virtual void activate()`|このオブジェクトが属するウィンドウをアクティブにする；ウィンドウの再読み込みが自身をアクティブにする。|
|`virtual rectangle_t get_absolute_rectangle() const`|ウィンドウ内のコントロールの論理矩形を返す。|
|`virtual bool get_focused() const`|コントロールにフォーカスがあるかを検索する。|
|`virtual std::shared_ptr<window> get_owning_window() const`|コントロールが属するウィンドウを返す、未属するウィンドウの場合は空指針を返す。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`rectangle_t rect`|派生物がアクセス可能な相対的な親クラスの論理矩形；通常の代入はsetterを使用して変更通知を生成する。|
|`uint32_t background_color = render_style::CONTROL_BACKGROUND_COLOR`|派生物がアクセス可能な背景色、形式は0xRRGGBBAA；通常の代入はsetterを使用して変更通知を生成する。|
|`bool visible = true`|派生物がアクセス可能な可視状態；通常の代入はsetterを使用して変更通知を生成する。|
|`bool enabled = true`|派生物がアクセス可能な互換状態；通常の代入はsetterを使用して変更通知を生成する。|
|`uint64_t tab_index = 0u`|派生物がアクセス可能なTabフォーカス順序、デフォルトは0；通常の代入はsetterを使用して変更通知を生成する。|
|`size_t focus_target_index = 0u`|現在の内部フォーカスエリアのインデックス、初期は0。|
|`virtual size_t get_focus_target_count() const`|コントロールの内部でフォーカス可能なエリアの数を返す、数字ボタンやタブアイコンなどの複合コントロールでカバーされる場合を除く。|
|`virtual size_t get_focus_target_index() const`|現在の内部フォーカスエリアのインデックスを読取る。|
|`virtual void set_focus_target_index(size_t value)`|現在の内部フォーカスエリアのインデックスを設定する。|
|`control(const u32string &name, const u32string &type)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|
|`virtual void refresh_layout()`|コントロールのレイアウトを更新する、派生物がカバーする場合は必要なベースクラスの処理を保持する。|
|`virtual rectangle_t get_input_rectangle() const`|コントロールのローカル座標内の入力エリアを返す；デフォルトではコントロール全体をカバーし、派生編集コントロールでは実際の編集エリアに縮小することができる。|
|`virtual double get_content_top() const`|本文の開始の論理的なtopオフセットを読取る。|
|`void notify_viewport_changed()`|再描画を要求し、`on_viewport_changed`イベントを発行する。|
|`virtual void render(render_context &context) const`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|
|`virtual void render_overlay(render_context &context) const`|コントロールのフルーリングを描画する、例えばコンボボックスのポップアップメニュー。|

### `easyvrui/control/blank.h`

#### `blank`

声明。`class blank : public control`。

命名矩形のプレースホルダオブジェクト。基本的な設定では、構築時には読み取り専用のnameと変更可能なrectが設定されます。幾何学的変化のイベント、属性変化の通知、およびオブジェクトのライフサイクルインターフェースは、基クラスを継承しています。get_control_list().add()を使用して通常のコンテナに追加できます。

|宣言|用途と呼び出しの意味|
|---|---|
|`explicit blank(const u32string &name)`|一意の名前でプレースホルダオブジェクトを構築し、nameはインスタンスが存在する間固定されます。|
|`~blank() override`|オブジェクトのライフサイクルを終了します。|
|`const u32string &get_name() const`|継承された名前の読み取りインターフェース。|
|`const rectangle_t &get_rect() const`、`void set_rect(const rectangle_t &value)`|継承された矩形の読み取りおよび設定インターフェース。|
|`on_moved`、`on_size_changed`|left/topおよびwidth/heightの変化をそれぞれ通知します。|
|`on_property_changed`|属性変化の通知。`event.property_name`を使用して名前を読み取り、元のコントロールから現在の値を読み取ります。|
|`on_disposed`、`get_disposed()`、`dispose()`|オブジェクトの解放通知、状態、および解放のポートルート。|
|`invalidate()`、`begin_invoke(callback)`|継承されたフラッシュリクエストおよび作成スレッドスケジューリングインターフェース。|

blankタイプを通じて直接visible、enabled、background_color、tab_indexおよび対応するアクセサー、表示/非表示、フォーカス、アクティブ化、およびインタラクティブイベントにアクセスしますが、これらはprivateアクセス制約の下にあります。描画と入力処理は、フレームが内部ハッカーを呼び出して行います。

コンテナとフレームは、通常のcontrol基クラス参照を保持できます。control参照を使用して仮想関数を呼び出す場合、get_visible()、get_enabled()、およびis_focusable()は常にfalseを返し、visibleとenabledのセッターはその状態を維持します。名前、矩形、幾何学的イベント、およびライフサイクルインターフェースは利用可能です。

### `easyvrui/control/text_control.h`

テキストコントロールのフォントと前景色。

#### `text_control`

声明。`class text_control : public control`。

フォントと前景色の基クラスで、コンストラクタはprotectedです。デフォルトの前景色は0xD1DEF0FF、フォントはSegoe UI、18、通常の文字の太さ、および非斜体です。テキスト内容は具体的なコントロールによって定義されます。

`control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_foreground_color_changed`|テキストの前景色が変更されるとトリガーされます。|
|`event_container<event_args_t> on_font_changed`|フォントが変更されるとトリガーされます。|
|`virtual uint32_t get_foreground_color() const`|テキストの前景色を読み取ります。フォーマットは0xRRGGBBAAです。|
|`virtual void set_foreground_color(uint32_t value)`|テキストの前景色を設定します。フォーマットは0xRRGGBBAAです。|
|`virtual const font_t &get_font() const`|テキストのフォントを読み取ります。|
|`virtual void set_font(const font_t &value)`|テキストのフォントを設定します。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`uint32_t foreground_color = render_style::TEXT_FOREGROUND_COLOR`|派生クラスがアクセス可能なテキストの前景色、フォーマット0xRRGGBBAA；通常の代入はsetterを使用して変化通知を生成します。|
|`font_t font`|派生クラスがアクセス可能なテキストのフォント；通常の代入はsetterを使用して変化通知を生成します。|
|`text_control(const u32string &name, const u32string &type)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|

### `easyvrui/control/container_control.h`

サブコントロールを収容できる基クラスおよび統一コンテナアクセスインターフェース。

#### `container_control`

声明。`class container_control : public control`。

コンテナ基クラス、コンストラクタはprotectedです。get_control_list()は活動中のcontrol_collectionを返し、要素の統一管理、名前のインデックス、所有権を管理します。通常のコンテナはこの集合を通じて操作します；tabcontrolはアプリケーションがページを管理するための独立したpage_listを公開します。

`control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<control_collection_event_args_t> on_control_added`|サブコントロールを追加する際にトリガーされ、コントロールオブジェクト`item`とインデックス`index`を含みます。|
|`event_container<control_collection_event_args_t> on_control_removed`|サブコントロールを削除する際にトリガーされ、コントロールオブジェクト`item`とインデックス`index`を含みます。|
|`virtual control_collection &get_control_list()`|そのコンテナに属する直接操作可能な集合を返します；クエリ、インデックス、追加、挿入、削除、クリアが可能です。constオーバーライドは読み取り専用集合アクセスを提供します。|
|`virtual const control_collection &get_control_list() const`|そのコンテナに属する直接操作可能な集合を返します；クエリ、インデックス、追加、挿入、削除、クリアが可能です。constオーバーライドは読み取り専用集合アクセスを提供します。|
|`virtual std::vector<control *> get_active_item_list() const`|現在表示とインタラクションに関与する直接コントロールのリストを返します。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`container_control(const std::u32string &name, const std::u32string &type)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|
|`virtual void validate_control(const control &item) const`|追加前に要素のタイプとこのコンテナの追加制約をチェックします；失敗した場合は例外を投げ、集合は元の状態を保持します。|
|`virtual void notify_control_added(control &item, size_t index)`|要素が追加された後、所属コンテナに通知します。indexは実際の集合インデックスです。|
|`virtual void notify_control_removed(control &item, size_t index)`|要素が削除された後、所属コンテナに通知します。indexは削除前の実際のインデックスです。|
|`virtual void notify_control_list_cleared()`|集合が完全にクリアされたときに所属コンテナに通知します。|
|`virtual std::vector<control *> get_active_control_list() const`|現在表示とインタラクションに関与する要素を返します；派生コンテナは非活動ページをフィルタリングできます。|
|`virtual bool is_control_active(const control &item) const`|指定された要素が現在のコンテナの表示およびインタラクションに参加しているかどうかを判断します。|
|`virtual std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const`|コンテナが配置した矩形を返します。nulloptは要素自身の矩形を継続することを意味します。|
|`virtual std::optional<int64_t> get_selection_index_at(double left, double top, const rectangle_t &rectangle) const`|ローカル位置とコンテナの矩形に基づいて選択インデックスを取得します。ヒットしない場合はnulloptを返します。|

### `easyvrui/control/control_collection.h`

名前で索引付けされた順序のコントロールコンテナです。

#### `control_collection`

声明。`class control_collection`。

順序のある子コントロールを持ち、名前は現在のコンテナ内で一意です。indexは0から始まります。insertは末尾を超えた場合に追加されます。nameで検索する場合は平均O(1)、位置で要素を取得する場合はO(1)です。中間での挿入や削除には順序の項目を移動する必要があります。参照のオーバーランドはオブジェクトの破棄を引き継ぎません。呼び出し側はオブジェクトがコンテナ内の参照よりも長く生きることを保証します。shared_ptrのオーバーランドは共有所有権を保持します。removeは親関係を解除し、オブジェクトを返します。参照の追加時には返される値がオブジェクトを所有していない可能性があります。共有ポインタが空である、重複名前である、既に親を持っている、またはループを形成している場合は失敗します。

|宣言|用途と呼び出しの意味|
|---|---|
|`explicit control_collection(container_control &owner)`|このタイプのインスタンスを構築します。パラメータの意味はこのタイプの説明と署名を参照してください。|
|`virtual ~control_collection()`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`size_t get_size() const`|集合の項目数を返します。|
|`bool is_empty() const`|コントロール集合が空かどうかを検索します。|
|`bool contains(const control &item) const`|インスタンスで指定されたコントロールを検索します。|
|`bool contains(const u32string &name) const`|名前でコントロールを検索します。|
|`control &get_control(size_t index) const`|indexまたはnameでコントロールの参照を返します。存在しない場合は例外を投げます。|
|`control &get_control(const u32string &name) const`|indexまたはnameでコントロールの参照を返します。存在しない場合は例外を投げます。|
|`size_t get_index(const control &item) const`|オブジェクトまたは文字が集合内の0からの位置を返します。存在しない場合は例外を投げます。|
|`const vector<control *> &get_item_list() const`|現在の集合の読み取り専用の順序リストを返します。この参照の有効性は所属コンテナのライフサイクルと後続の変更によって変わります。|
|`virtual void insert(size_t index, control &item)`|index位置に挿入します。indexが現在の数より小さい場合は追加されます。具体的な要素タイプ、所有権、重複名前の制約については、所属コンテナの説明を参照してください。|
|`virtual void insert(size_t index, std::shared_ptr<control> item)`|index位置に挿入します。indexが現在の数より小さい場合は追加されます。具体的な要素タイプ、所有権、重複名前の制約については、所属コンテナの説明を参照してください。|
|`void add(control &item)`|項目を追加します。オブジェクトの参照方法は呼び出し側が保証します。shared_ptrの方法はコンテナが共有所有権を保持します。|
|`void add(std::shared_ptr<control> item)`|項目を追加します。オブジェクトの参照方法は呼び出し側が保証します。shared_ptrの方法はコンテナが共有所有権を保持します。|
|`virtual std::shared_ptr<control> remove(size_t index)`|指定された要素を削除し、そのshared_ptrを返します。共有の追加時にはその参照を渡し、参照の追加時には破棄を引き継がない参照を返します。|
|`std::shared_ptr<control> remove(control &item)`|指定された要素を削除し、そのshared_ptrを返します。共有の追加時にはその参照を渡し、参照の追加時には破棄を引き継がない参照を返します。|
|`std::shared_ptr<control> remove(const u32string &name)`|指定された要素を削除し、そのshared_ptrを返します。共有の追加時にはその参照を渡し、参照の追加時には破棄を引き継がない参照を返します。|
|`virtual void clear()`|集合からすべてのコントロールを削除します。|
|`control &operator[](size_t index) const`|0の開始位置または名前でオブジェクト参照を取得します。この動作はget_control/get_pageと同じです。|
|`control &operator[](const u32string &name) const`|0の開始位置または名前でオブジェクト参照を取得します。この動作はget_control/get_pageと同じです。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`container_control &get_owner() const`|集合が属するコンテナの参照を返します。|
|`void release_control_list() noexcept`|集合が保持する参照を解放し、派生集合のデストラクターチェックで使用します。|
|`virtual void notify_control_added(control &item, size_t index)`|派生集合の追加通知。itemが追加されました。indexは実際のインデックスです。|
|`virtual void notify_control_removed(control &item, size_t index, bool clearing)`|派生集合の削除通知。clearingはこの操作がclearから来たことを意味します。|

### `easyvrui/control/panel.h`

通常のサブコントロールパネル。

#### `panel`

声明。`class panel : public container_control`。

通常のコンテンツパネル。名前の構造のみを追加し、container_controlの全ての共通インターフェースを継承します。

`container_control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`explicit panel(const u32string &name)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`panel(const u32string &name, const u32string &type)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|

### `easyvrui/control/selection_control.h`

#### `selection_control`

声明。`class selection_control : public text_control`。

集合で選択されるコントロールの抽象クラス。フォントと前景色を継承します。派生クラスは項目エリアの空白ヒットと選択のクリアを定義します。Listbox、TreeView、Grid、ListViewの項目の空白エリアは、この規則に従ってテキスト編集を終了し、IME/layoutを収納し、キーボードナビゲーションのフォーカスを保持します。`clear_selection_on_blank_click`を有効にすると、項目の選択も同時にクリアされます。表頭、列の幅調整エリア、スクロールバー、ポップアップオプションはそれぞれクリックを処理します。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_clear_selection_on_blank_click_changed`|空白クリック選択ルールが変更された時にトリガーされる。|
|`virtual bool get_clear_selection_on_blank_click() const`|読み取りクリック項目エリアの空白時に項目選択をクリアするかどうか、デフォルトはfalse。|
|`virtual void set_clear_selection_on_blank_click(bool value)`|読み取りクリック項目エリアの空白時に項目選択をクリアするかどうかを設定する、デフォルトはfalse。|
|`virtual bool is_blank_at(double local_left, double local_top) const`|コントロールのローカル位置が空白かどうかを判断する、具体的な項目エリアは派生クラスによって決定される。|
|`virtual void clear_selection() = 0`|純粋な虚関数で、具体的な集合コントロールが選択をクリアする実装を行う。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`selection_control(const std::u32string &name, const std::u32string &type)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|

## テキストと項目コントロール

### `easyvrui/control/label.h`

静的テキストラベル。

#### `label`

声明。`class label : public text_control`。

ラベルは`text_control`から継承され、テキストを表示するために使用され、デフォルトではテキストは空である。

`text_control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_text_changed`|テキストが変更された時にトリガーされる。|
|`explicit label(const u32string &name)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`virtual const u32string &get_text() const`|テキスト内容を読み取る。|
|`virtual void set_text(const u32string &value)`|テキスト内容を設定する。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|

### `easyvrui/control/button.h`

フォーカス可能でクリック可能なテキストボタン。

#### `button`

声明。`class button : public text_control`。

テキストボタンで、デフォルトではtextが空で、フォーカスとon_clickをサポートする；text_controlから継承される。

`text_control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_text_changed`|テキストが変更された時にトリガーされる。|
|`explicit button(const u32string &name)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`bool is_focusable() const override`|コントロールタイプがフォーカスを受け入れるかどうかを検索します。実際のフォーカスはvisible、enabled、ウィンドウのモーダル状態にも影響されます。|
|`virtual const u32string &get_text() const`|テキスト内容を読み取る。|
|`virtual void set_text(const u32string &value)`|テキスト内容を設定する。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`button(const u32string &name, const u32string &type)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`void render(render_context &context) const override`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|

### `easyvrui/control/textbox.h`

テキスト入力、選択範囲、マルチラインおよびスクロールバーコントロール。

#### `textbox`

声明。`class textbox : public text_control`。

テキスト入力コントロールでは、デフォルトでtextは空で、selectable=true、read_only=false、max_length=0、multiline=falseです。2つのスクロールバーの表示オプションはどちらもfalseで、選択範囲の開始点と長さはともに0です。multilineは改行を保持し、単行モードでは改行が削除されます。max_lengthを変更すると、既存のテキストが規格化されます。フォントサイズとレイアウトによって実際の行の高さが決まり、テキストのインデックスはコードポイントでカウントされ、文字の境界が整列されます。

`text_control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_text_changed`|テキストが変更された時にトリガーされる。|
|`event_container<event_args_t> on_read_only_changed`|読み取り専用状態が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_selectable_changed`|テキストの選択設定が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_selection_changed`|選択状態が変更されたときにトリガーされます。テキストエディターではstart/lengthを使用し、項目とタブではselectedを使用します。|
|`event_container<event_args_t> on_max_length_changed`|テキストの長さ上限が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_multiline_changed`|マルチラインオプションが変更されたときにトリガーされます。|
|`event_container<event_args_t> on_horizontal_scrollbar_visible_changed`|横向きスクロールバーの表示設定が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_vertical_scrollbar_visible_changed`|縦向きスクロールバーの表示設定が変更されたときにトリガーされます。|
|`explicit textbox(const u32string &name)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`bool is_focusable() const override`|コントロールタイプがフォーカスを受け入れるかどうかを検索します。実際のフォーカスはvisible、enabled、ウィンドウのモーダル状態にも影響されます。|
|`virtual const u32string &get_text() const`|テキスト内容を読み取る。|
|`virtual void set_text(const u32string &value)`|テキスト内容を設定する。|
|`virtual bool get_read_only() const`|ユーザー入力の読み取り専用状態；プログラムは依然としてテキストを設定できます。|
|`virtual void set_read_only(bool value)`|ユーザー入力の読み取り専用状態を設定；プログラムは依然としてテキストを設定できます。|
|`virtual bool get_selectable() const`|テキストの選択、カーソルの表示、入力インターフェースの呼び出しを許可するかどうか；falseの場合でもコントロールのフォーカスを受け取ることができます。|
|`virtual void set_selectable(bool value)`|テキストの選択オプションを設定；falseの場合、カーソルは隠され、入力インターフェースは閉じられ、ユーザーの編集は阻止されますが、プログラムのset_textは依然として使用できます。|
|`virtual bool get_multiline() const`|複数行読取りモード、デフォルトはfalse。|
|`virtual void set_multiline(bool value)`|複数行読取りモードの設定、デフォルトはfalse。|
|`virtual bool get_horizontal_scrollbar_visible() const`|横向きスクロールバー表示のオン/オフの読取り。|
|`virtual void set_horizontal_scrollbar_visible(bool value)`|横向きスクロールバー表示のオン/オフの設定。|
|`virtual bool get_vertical_scrollbar_visible() const`|縦向きスクロールバー表示の状態の読取り。|
|`virtual void set_vertical_scrollbar_visible(bool value)`|縦向きスクロールバー表示の状態の設定。|
|`virtual uint64_t get_selection_start() const`|選択範囲の小端のコードポイント位置の読取り。|
|`virtual uint64_t get_selection_length() const`|選択範囲に含まれるコードポイント数の読取り。|
|`virtual void set_selection_start(uint64_t value)`|選択範囲の小端のコードポイント位置の設定。|
|`virtual void set_selection_length(uint64_t value)`|選択範囲に含まれるコードポイント数の設定。|
|`virtual u32string get_selected_text() const`|選択範囲のテキストコピーの読取り。|
|`virtual bool get_can_undo() const`|テキスト編集の取消可能性の確認。|
|`virtual bool get_can_redo() const`|取消可能なテキスト編集記録の有無の確認。|
|`virtual bool undo()`|一度の編集取消、成功時はtrueを返す。|
|`virtual bool redo()`|再編集、成功時はtrueを返す。|
|`virtual void set_selected_text(const u32string &value)`|現在の選択範囲をvalueで置換する；プログラムの変更入力として、read_onlyコントロールで使用可能。|
|`virtual uint64_t get_max_length() const`|テキストの最大コードポイント数の読取り、0は無制限を意味する；完全な文字素を保持するために切り捨てる。|
|`virtual void set_max_length(uint64_t value)`|テキストの最大コードポイント数の設定、0は無制限を意味する；完全な文字素を保持するために切り捨てる。|
|`virtual void select(uint64_t start, uint64_t length = 0u)`|startからlength個のコードポイントを選択する；デフォルトのlengthは0で、即ち挿入点を設定する。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`virtual uint64_t get_selection_anchor() const`|選択範囲のアンカーポイントの読取り、選択方向を保持する。|
|`virtual uint64_t get_selection_active() const`|選択範囲の活動端、即ち現在の挿入端を読取り。|
|`virtual void set_selection(uint64_t anchor, uint64_t active)`|anchorとactiveで方向付きの選択範囲を指定する；位置はテキスト範囲内で文字素の境界に整列する。|
|`void render(render_context &context) const override`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|
|`void render_overlay(render_context &context) const override`|コントロールのフルーリングを描画する、例えばコンボボックスのポップアップメニュー。|

エディタにフォーカスがある場合、Ctrl+Zでテキスト変更を取消し、Ctrl+YまたはCtrl+Shift+Zで変更を復元する。これらのキーはアプリケーションメニューのショートカットより優先する。

### `easyvrui/control/item_control.h`

項目リスト、選択項目、行スクロールの共通基盤クラス。

#### `item_control`

声明。`class item_control : public selection_control`。

プロジェクトコントロールの基底クラスで、コンストラクタはprotectedで、selection_controlを継承しています。デフォルトではプロジェクトは空で、selected_index=-1、scroll_offset=0、row_height=32です。selected_itemは読み取り専用のu32stringで、選択項目がない場合は空文字列を返します。scroll_offsetのアクセスインターフェースはprotectedです。

`selection_control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`item_collection item_list`|テキストプロジェクトコンテナで、変更は所属するプロジェクトコントロールに通知されます。|
|`event_container<event_args_t> on_item_list_changed`|テキストプロジェクトリストが変更されるとトリガーされます。|
|`event_container<event_args_t> on_selection_changed`|選択状態が変更されたときにトリガーされます。テキストエディターではstart/lengthを使用し、項目とタブではselectedを使用します。|
|`event_container<event_args_t> on_selected_index_changed`|選択インデックスが変更されるとトリガーされます。|
|`event_container<event_args_t> on_row_height_changed`|行高が変更されるとトリガーされます。|
|`bool is_focusable() const override`|コントロールタイプがフォーカスを受け入れるかどうかを検索します。実際のフォーカスはvisible、enabled、ウィンドウのモーダル状態にも影響されます。|
|`const item_collection &get_item_list() const`|順序付けられた文字列集合を読み取ります。|
|`item_collection &get_item_list()`|変更可能な集合を取得し、`assign(value)`で内容を置き換えます。|
|`virtual int64_t get_selected_index() const`|現在の選択インデックスを読み取ります、-1は選択されていないことを表します。|
|`virtual void set_selected_index(int64_t value)`|現在の選択インデックスを設定します、-1は選択されていないことを表します。|
|`void clear_selection() override`|選択をクリアし、selected_indexは-1に変わり、selected_itemは空文字列を返します。|
|`virtual u32string get_selected_item() const`|選択された文字を読み取ります。選択項目がない場合は空文字列を返します。|
|`virtual uint64_t get_row_height() const`|プロジェクトの行高を読み取ります。論理単位で0以上でなければなりません。|
|`virtual void set_row_height(uint64_t value)`|プロジェクトの行高を設定します。論理単位で0以上でなければなりません。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`int64_t selected_index = NO_SELECTION_INDEX`|派生クラスがアクセス可能な現在の選択インデックスで、-1は選択されていないことを表します。通常の値設定ではsetterを使用して通知を生成します。|
|`uint64_t scroll_offset = 0u`|派生クラスがアクセスできる最初の表示項目のインデックスオフセット；通常の代入はsetterを使用して変化通知を生成します。|
|`uint64_t row_height = render_style::DEFAULT_ROW_HEIGHT`|派生クラスがアクセス可能なプロジェクトの行高で、論理単位で0以上でなければなりません。通常の値設定ではsetterを使用して通知を生成します。|
|`virtual bool get_vertical_scrollbar_visible() const`|派生クラスは縦スクロールバーが表示されているかをチェックし、デフォルトではfalseを返します。|
|`void refresh_layout() override`|コントロールのレイアウトを更新する、派生物がカバーする場合は必要なベースクラスの処理を保持する。|
|`virtual void refresh_item_list()`|項目内容の変更後の派生更新ポート。|
|`virtual void notify_selection_changed(int64_t previous_index, const u32string &previous_item, int64_t next_index, const u32string &next_item)`|選択変更通知を提供し、元の索引/文字と新しい索引/文字を提供する。|
|`virtual void notify_item_list_changed(const vector<u32string> &previous, int64_t previous_index, const u32string &previous_item, uint64_t previous_scroll)`|項目リストの変更通知を提供し、元のリスト、元の選択、元のスクロール位置を提供する。|
|`virtual uint64_t get_scroll_offset() const`|最初に表示される項目の索引オフセットを読み取る。|
|`virtual void set_scroll_offset(uint64_t value)`|最初に表示される項目の索引オフセットを設定する。|
|`item_control(const u32string &name, const u32string &type)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|
|`virtual uint64_t get_maximum_scroll_offset() const`|現在の項目コントロールが許可する最大の最初の行オフセットを返す。|
|`virtual uint64_t get_visible_item_count() const`|現在の視点の項目行容量を返す。|
|`void reveal_item(uint64_t index)`|指定された項目が表示可能な位置までスクロールし、その項目がまだ表示可能な既存の位置を保持する。|
|`virtual void handle_item_list_changed(const vector<u32string> &previous)`|項目リストの変更を処理し、現在の選択と表示を調整する。|
|`virtual void render_item_list(render_context &context, const render_rectangle_t &rectangle) const`|矩形内に現在表示可能な項目を描画する。|

### `easyvrui/control/item_collection.h`

順序付けられたテキスト項目コンテナ。

#### `item_collection`

声明。`class item_collection`。

順序付けられたUnicodeテキスト項目コンテナで、同じ文字が重複することが許可される。get_index/remove操作で最初の一致する項目を取得する。存在しない場合や位置が越境した場合は例外を投げる。insertが末尾を超える場合は追加する。リストの変更は、所属するitem_controlの選択と描画状態を同期する。

|宣言|用途と呼び出しの意味|
|---|---|
|`explicit item_collection(item_control &owner)`|このタイプのインスタンスを構築します。パラメータの意味はこのタイプの説明と署名を参照してください。|
|`void add(const u32string &item)`|項目を追加します。オブジェクトの参照方法は呼び出し側が保証します。shared_ptrの方法はコンテナが共有所有権を保持します。|
|`void insert(size_t index, const u32string &item)`|index位置に挿入します。indexが現在の数より小さい場合は追加されます。具体的な要素タイプ、所有権、重複名前の制約については、所属コンテナの説明を参照してください。|
|`u32string remove(size_t index)`|パラメータで指定された位置、オブジェクト、または名前で項目を削除する。削除されたオブジェクトや成功の有無を返す。具体的な返り値は署名を参照。|
|`u32string remove(const u32string &item)`|パラメータで指定された位置、オブジェクト、または名前で項目を削除する。削除されたオブジェクトや成功の有無を返す。具体的な返り値は署名を参照。|
|`void clear()`|集合からすべてのテキスト項目を削除する。|
|`void assign(const vector<u32string> &item_list)`|item_list全体でテキスト項目リストを置き換え、選択と表示状態を更新する。|
|`size_t get_size() const`|集合の項目数を返します。|
|`bool is_empty() const`|テキスト項目集合が空かどうかを検索する。|
|`bool contains(const u32string &item) const`|集合内に`item`と同じテキストが存在するかどうかを検索する。|
|`const u32string &get_item(size_t index) const`|indexで項目のテキストを読み取り専用の参照として返す。越境した場合は例外を投げる。|
|`const u32string &operator[](size_t index) const`|0の開始位置で項目のテキストconst参照として返す。越境した場合は例外を投げる。|
|`size_t get_index(const u32string &item) const`|オブジェクトまたは文字が集合内の0からの位置を返します。存在しない場合は例外を投げます。|
|`const vector<u32string> &get_item_list() const`|現在の集合の読み取り専用の順序リストを返します。この参照の有効性は所属コンテナのライフサイクルと後続の変更によって変わります。|

### `easyvrui/control/combobox.h`

リスト選択とオプションテキスト編集を組み合わせたコンボボックス。

#### `combobox`

声明。`class combobox : public item_control`。

`item_control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_dropdown_style_changed`|ドロップダウンスタイルの変更時にトリガーされる。|
|`event_container<event_args_t> on_text_changed`|テキストが変更された時にトリガーされる。|
|`explicit combobox(const u32string &name)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`virtual const u32string &get_text() const`|テキスト内容を読み取る。|
|`virtual void set_text(const u32string &value)`|テキスト内容を設定する。|
|`virtual combobox_dropdown_style_t get_dropdown_style() const`|ドロップダウンスタイルを読み取り、デフォルトはdropdown_list。|
|`virtual void set_dropdown_style(combobox_dropdown_style_t value)`|dropdownの自由入力を設定し、dropdown_listはリストから選択する。|
|`virtual bool get_dropped_down() const`|ドロップダウンリストが展開されているかを読み取り。|
|`virtual void set_dropped_down(bool value)`|ドロップダウンリストを展開または収納する。|
|`void set_selected_index(int64_t value) override`|現在の選択インデックスを設定します、-1は選択されていないことを表します。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void refresh_item_list() override`|選択文字、ドロップダウンリスト、およびレイアウトを同期する。|
|`void handle_item_list_changed(const vector<u32string> &previous) override`|項目リストの変更を処理し、現在の選択と表示を調整する。|
|`void render(render_context &context) const override`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|
|`void render_overlay(render_context &context) const override`|コントロールのフルーリングを描画する、例えばコンボボックスのポップアップメニュー。|

### `easyvrui/control/listbox.h`

スクロール可能なチェックリスト。

#### `listbox`

声明。`class listbox : public item_control`。

item_controlを継承し、デフォルトの行高は30；内容が表示可能な行数を超えた場合は縦スクロールバーを提供する。get_vertical_scrollbar_visible()は読み取り専用の計算状態です。レーザー対応ハンドルのジョイスティックでスクロール可能なリストで、スクロール量は反転の程度に応じて変化する。

`item_control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`explicit listbox(const u32string &name)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`bool is_blank_at(double local_left, double local_top) const override`|ローカル位置がリストの内容領域の空白かどうかを判断する。|
|`virtual bool get_vertical_scrollbar_visible() const`|表示領域を超える縦方向の項目が計算リストに存在するかを確認する；内容が不足している場合はfalseを返す。|
|`void set_visible(bool value) override`|表示状態を設定する；隠す場合は、このコントロールで進行中のインタラクションをクリアする。|
|`void set_enabled(bool value) override`|操作可能な状態を設定する；無効化する場合は、進行中のインタラクションをクリアする。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void refresh_layout() override`|コントロールのレイアウトを更新する、派生物がカバーする場合は必要なベースクラスの処理を保持する。|
|`uint64_t get_maximum_scroll_offset() const override`|現在の項目コントロールが許可する最大の最初の行オフセットを返す。|
|`void render(render_context &context) const override`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|

## コントロールの拡張

### `easyvrui/control/checkbox.h`

#### `checkbox`

声明。`class checkbox : public text_control`。

チェックボックス、デフォルトではtextは空で、checkedはfalse。クリックまたはSpace/Enterキーでcheckedを切り替える；文字の外観はtext_controlから継承される。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_text_changed`|テキストが変更された時にトリガーされる。|
|`event_container<event_args_t> on_checked_changed`|チェック状態が変更されるとトリガーされる。|
|`explicit checkbox(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`bool is_focusable() const override`|このコントロールがフォーカス能力を持っているかを検索する；実際のフォーカスはvisible、enabled、およびモダンな関係によって制限される。|
|`virtual const std::u32string &get_text() const`|表示される文字を読み取る。|
|`virtual void set_text(const std::u32string &value)`|表示される文字を設定する。|
|`virtual bool get_checked() const`|現在のチェック状態を読み取る。|
|`virtual void set_checked(bool value)`|現在のチェック状態を設定する。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|

### `easyvrui/control/radiobutton.h`

#### `radiobutton`

声明。`class radiobutton : public text_control`。

ラジオボタン、デフォルトではtextは空で、checkedはfalse。同じ直接コンテナ内のradiobuttonは相互に排他；set_checked(true)は同レベルの他のラジオボタンを無効にする。panelを使用して独立したグループを分割することができる。クリックまたはSpace/Enterキーで選択する。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_text_changed`|テキストが変更された時にトリガーされる。|
|`event_container<event_args_t> on_checked_changed`|チェック状態が変更されるとトリガーされる。|
|`explicit radiobutton(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`bool is_focusable() const override`|このコントロールがフォーカス能力を持っているかを検索する；実際のフォーカスはvisible、enabled、およびモダンな関係によって制限される。|
|`virtual const std::u32string &get_text() const`|表示される文字を読み取る。|
|`virtual void set_text(const std::u32string &value)`|表示される文字を設定する。|
|`virtual bool get_checked() const`|現在のチェック状態を読み取る。|
|`virtual void set_checked(bool value)`|現在のチェック状態を設定する。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|

### `easyvrui/control/numericupdown.h`

#### `numericupdown`

声明。`class numericupdown : public text_control`。

数値入力と上下調整ボタン。value/minimum/maximum/stepはdouble型で、デフォルトはそれぞれ0.0/0.0/100.0/1.0です。decimal_placesはuint32_t型で、デフォルトは0で、範囲は0から17までで、小数の桁数を制御します。境界は有限でなければならず、minimumはmaximumより小さく、stepは有限の正の数でなければなりません。valueは境界内に制限されます。上下ボタンにはそれぞれホバーとフォーカスがあり、これらをクリックすると数値編集エリアが閉じられます。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_value_changed`|現在の値が変動したときにトリガーされます。|
|`event_container<event_args_t> on_minimum_changed`|下限が変動したときにトリガーされます。|
|`event_container<event_args_t> on_maximum_changed`|上限が変動したときにトリガーされます。|
|`event_container<event_args_t> on_step_changed`|ステップ幅が変動したときにトリガーされます。|
|`event_container<event_args_t> on_decimal_places_changed`|小数の桁数が変動したときにトリガーされます。|
|`explicit numericupdown(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`bool is_focusable() const override`|このコントロールがフォーカス能力を持っているかを検索する；実際のフォーカスはvisible、enabled、およびモダンな関係によって制限される。|
|`virtual double get_value() const`|現在の数値を読み取ります。setterはこのタイプの境界で処理されます。|
|`virtual void set_value(double next)`|現在の数値を設定します。setterはこのタイプの境界で処理されます。|
|`virtual double get_minimum() const`|数値範囲の下界を読み取ります。|
|`virtual void set_minimum(double next)`|数値範囲の下界を設定します。|
|`virtual double get_maximum() const`|数値範囲の上界を読み取ります。|
|`virtual void set_maximum(double next)`|数値範囲の上界を設定します。|
|`virtual double get_step() const`|上下ボタンが調整するたびの有限の正のステップ幅を読み取ります。|
|`virtual void set_step(double next)`|上下ボタンが調整するたびの有限の正のステップ幅を設定します。|
|`virtual uint32_t get_decimal_places() const`|表示される小数の桁数を読み取ります。範囲は0から17までです。|
|`virtual void set_decimal_places(uint32_t next)`|表示される小数の桁数を設定します。範囲は0から17までです。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`size_t get_focus_target_count() const override`|複合コントロールのフォーカスナビゲーションに使用する、内部のフォーカス可能な領域の数を返す。|
|`virtual size_t get_focus_target_at(double left, double top) const`|コントロールのローカル座標に基づいて、内部のフォーカス領域のインデックスを取得する。|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|
|`void render_overlay(render_context &context) const override`|派生描画エントリポイント；contextを使用してフラップを描画する。|

### `easyvrui/control/slider.h`

#### `slider`

声明。`class slider : public control`。

スライダーをドラッグ可能。minimum、maximum、valueはすべてint64_tで、デフォルトは0、100、0で、minimum<maximumの条件が必要。set_valueは入力を範囲内に制限し、境界を変更すると現在の値が同時に修正される。方向は`orientation_t`で指定され、デフォルトは`orientation_t::horizontal`で、`orientation_t::vertical`に設定することもできる。方向キーは整数1で値を増減し、縦方向の上端はmaximumに対応する。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_minimum_changed`|下限が変動したときにトリガーされます。|
|`event_container<event_args_t> on_maximum_changed`|上限が変動したときにトリガーされます。|
|`event_container<event_args_t> on_value_changed`|現在の値が変動したときにトリガーされます。|
|`event_container<event_args_t> on_orientation_changed`|方向が変わるとトリガーされる。|
|`event_container<event_args_t> on_drag_start`|ドラッグを開始するとトリガーされる。|
|`event_container<interaction_end_event_args_t> on_drag_end`|ドラッグを終了またはキャンセルするとトリガーされる。|
|`explicit slider(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`bool is_focusable() const override`|このコントロールがフォーカス能力を持っているかを検索する；実際のフォーカスはvisible、enabled、およびモダンな関係によって制限される。|
|`virtual int64_t get_minimum() const`|数値範囲の下界を読み取ります。|
|`virtual void set_minimum(int64_t next)`|数値範囲の下界を設定します。|
|`virtual int64_t get_maximum() const`|数値範囲の上界を読み取ります。|
|`virtual void set_maximum(int64_t next)`|数値範囲の上界を設定します。|
|`virtual int64_t get_value() const`|現在の数値を読み取ります。setterはこのタイプの境界で処理されます。|
|`virtual void set_value(int64_t next)`|現在の数値を設定します。setterはこのタイプの境界で処理されます。|
|`virtual orientation_t get_orientation() const`|レイアウト方向を読み取り、許容される値と意味はこのタイプの説明を参照。|
|`virtual void set_orientation(orientation_t next)`|レイアウト方向を設定し、許容される値と意味はこのタイプの説明を参照。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|

### `easyvrui/control/progressbar.h`

#### `progressbar`

声明。`class progressbar : public control`。

整数進捗の表示。minimum、maximum、valueはすべてint64_tで、デフォルトは0、100、0。minimum<maximumの条件が必要。set_valueは入力を範囲内に制限し、境界を変更すると現在の値が同時に調整される。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_minimum_changed`|下限が変動したときにトリガーされます。|
|`event_container<event_args_t> on_maximum_changed`|上限が変動したときにトリガーされます。|
|`event_container<event_args_t> on_value_changed`|現在の値が変動したときにトリガーされます。|
|`explicit progressbar(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`virtual int64_t get_minimum() const`|数値範囲の下界を読み取ります。|
|`virtual void set_minimum(int64_t next)`|数値範囲の下界を設定します。|
|`virtual int64_t get_maximum() const`|数値範囲の上界を読み取ります。|
|`virtual void set_maximum(int64_t next)`|数値範囲の上界を設定します。|
|`virtual int64_t get_value() const`|現在の数値を読み取ります。setterはこのタイプの境界で処理されます。|
|`virtual void set_value(int64_t next)`|現在の数値を設定します。setterはこのタイプの境界で処理されます。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|

### `easyvrui/control/image.h`

#### `image`

声明。`class image : public control`。

画像コントロール。sourceは`shared_ptr<const drawing_image>`で保存され、デフォルトでは空です。`stretch_mode`では`image_stretch_mode_t`を使用し、デフォルトでは`contain`です。`fill`、`contain`、`cover`、`none`はそれぞれ、ストレッチで満たす、等倍で完全に表示する、等倍でカバーし切り取りする、画像ピクセルサイズを維持することを表します。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_source_changed`|画像ソースが変更されたときにトリガーされます。|
|`event_container<event_args_t> on_stretch_mode_changed`|ストレッチ方法が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_source_unavailable`|画像リソースが利用できなくなったときにトリガーされます。|
|`explicit image(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`virtual const std::shared_ptr<const drawing_image> &get_source() const`|画像リソースの共有参照を読み取ります。nullptrはクリアを表します。|
|`virtual void set_source(std::shared_ptr<const drawing_image> value)`|画像リソースの共有参照を設定します。nullptrはクリアを表します。|
|`virtual image_stretch_mode_t get_stretch_mode() const`|画像のストレッチモードを読み取ります：fill、contain、cover、またはnone。|
|`virtual void set_stretch_mode(image_stretch_mode_t value)`|画像のストレッチモードを設定します：fill、contain、cover、またはnone。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|

### `easyvrui/control/screen.h`

#### `screen`

声明。`class screen : public control`。

リアルタイムディスプレイ画面コントロール。screen_idはuint64_tで、デフォルトは0です。番号は現在のエンジンが提供するディスプレイの列挙に応じて決定され、画面切り替えにはset_screen_idを使用します。コントロールの矩形は論理的な表示サイズを決定し、画面ピクセルサイズに設定すると同じ論理的なサイズで表示されます。実際の空間サイズは、所属するウィンドウのphysical_scaleに影響されます。get_screen_availableは利用可能な状態を提供します。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_screen_id_changed`|ディスプレイが変更されたときにトリガーされます。|
|`event_container<event_args_t> on_screen_unavailable`|ディスプレイが利用できない状態でキャプチャされたときにトリガーされます。|
|`event_container<event_args_t> on_screen_restored`|ディスプレイが復旧したときにトリガーされます。|
|`explicit screen(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`virtual uint64_t get_screen_id() const`|ディスプレイの番号を読み取ります。|
|`virtual void set_screen_id(uint64_t value)`|ディスプレイの番号を設定します。|
|`virtual bool get_screen_available() const`|現在のディスプレイのキャプチャが利用可能かどうかを読み取ります。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|

### `easyvrui/control/scrollpanel.h`

#### `scrollpanel`

声明。`class scrollpanel : public container_control`。

スクロール可能なコンテナで、コンテンツはget_control_list()で追加されます。horizontal_scrollbar_visibleとvertical_scrollbar_visibleはデフォルトでtrueです。スクロールバーと視野はコンテンツの範囲に応じてレイアウトされます。スクロールオフセットのアクセスインターフェースはprotectedで、アプリケーションはコントロールのレイアウトとスクロール入力操作によって操作されます。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_horizontal_scrollbar_visible_changed`|横向きスクロールバーの表示設定が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_vertical_scrollbar_visible_changed`|縦向きスクロールバーの表示設定が変更されたときにトリガーされます。|
|`explicit scrollpanel(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`virtual bool get_horizontal_scrollbar_visible() const`|横向きのスクロールバーが表示されているかどうかを読み取ります。|
|`virtual void set_horizontal_scrollbar_visible(bool value)`|横向きのスクロールバーが表示されるように設定します。|
|`virtual bool get_vertical_scrollbar_visible() const`|縦向きのスクロールバーが表示されているかどうかを読み取ります。|
|`virtual void set_vertical_scrollbar_visible(bool value)`|縦向きのスクロールバーが表示されるように設定します。|
|`void set_visible(bool value) override`|表示状態を設定する；隠す場合は、このコントロールで進行中のインタラクションをクリアする。|
|`void set_enabled(bool value) override`|操作可能かどうかを設定します。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void refresh_layout() override`|コントロールのレイアウトを更新する、派生物がカバーする場合は必要なベースクラスの処理を保持する。|
|`void notify_control_added(control &child, size_t index) override`|挿入後のコンテナ通知、indexは要素の実際の集合インデックスです。|
|`void notify_control_removed(control &child, size_t index) override`|削除後のコンテナ通知、indexは削除前の実際の集合インデックスです。|
|`virtual uint64_t get_horizontal_scroll_offset() const`|派生クラスによる横方向のロジックスクロールオフセットの読み取り。|
|`virtual void set_horizontal_scroll_offset(uint64_t value)`|派生クラスによる横方向のロジックスクロールオフセットの設定、内容範囲内に制限されます。|
|`virtual uint64_t get_vertical_scroll_offset() const`|派生クラスによる縦方向のロジックスクロールオフセットの読み取り。|
|`virtual void set_vertical_scroll_offset(uint64_t value)`|派生クラスによる縦方向のロジックスクロールオフセットの設定、内容範囲内に制限されます。|
|`virtual uint64_t get_maximum_vertical_scroll_offset() const`|派生クラスによる縦方向のロジックスクロール上限の読み取り。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|要素にコンテナ管理用の矩形を提供します；nulloptは自身の矩形を継続することを意味します。|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|
|`void render_overlay(render_context &context) const override`|派生描画エントリポイント；contextを使用してフラップを描画する。|

### `easyvrui/control/splitter.h`

#### `splitter`

声明。`class splitter : public container_control`。

二つの領域でコンテナを分割し、get_control_list()の順序に従って最大2つのコントロールを配置します。方向はデフォルトで`orientation_t::vertical`で、垂直分割バーで左右の領域を分けます。`orientation_t::horizontal`では水平分割バーで上下の領域を分けます。split_positionは有限のdoubleで、範囲は0.0から1.0まで、デフォルトは0.5です。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_orientation_changed`|方向が変わるとトリガーされる。|
|`event_container<event_args_t> on_split_position_changed`|分割位置が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_split_start`|分割バーをドラッグし始めたときにトリガーされます。|
|`event_container<interaction_end_event_args_t> on_split_end`|分割バーをドラッグを終えたときにトリガーされます。|
|`explicit splitter(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`virtual orientation_t get_orientation() const`|レイアウト方向を読み取り、許容される値と意味はこのタイプの説明を参照。|
|`virtual void set_orientation(orientation_t value)`|レイアウト方向を設定し、許容される値と意味はこのタイプの説明を参照。|
|`virtual double get_split_position() const`|最初の領域が利用可能なスペースの割合を読み取ります、範囲は0.0から1.0までです。|
|`virtual void set_split_position(double value)`|最初の領域が利用可能なスペースの割合を設定します、範囲は0.0から1.0までです。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void validate_control(const control &child) const override`|通常のコンテナ条件を検証し、最大2つの領域のコントロールに制限します。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|要素にコンテナ管理用の矩形を提供します；nulloptは自身の矩形を継続することを意味します。|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|

## 複数列およびツリーコントロール

### `easyvrui/control/grid.h`

#### `grid_column_t`

声明。`struct grid_column_t`。

テーブル列の定義：textはタイトル、widthはデフォルト100、editableはデフォルトtrueです。列を追加するか、列の幅を変更する場合は正の値でなければなりません。全体の幅はint64_tで表現可能でなければなりません。失敗した場合は、元の列と幅を保持します。

|宣言|用途と呼び出しの意味|
|---|---|
|`static constexpr uint64_t DEFAULT_WIDTH = 100u`|デフォルトの列幅は100ロジックピクセルです。|
|`std::u32string text`|表頭のテキスト。|
|`uint64_t width = DEFAULT_WIDTH`|正の整数で表される列幅、デフォルトはDEFAULT_WIDTHです。|
|`bool editable = true`|この列がユーザーに編集可能かどうか、デフォルトはtrueです。|

#### `grid_cell_t`

声明。`struct grid_cell_t`。

rowとcolumnはuint64_tで記録され、どちらも0から始まります。等値比較は2つのフィールドで行われます。

|宣言|用途と呼び出しの意味|
|---|---|
|`uint64_t row = 0u`|0は開始行のインデックスです。|
|`uint64_t column = 0u`|0は開始列のインデックスです。|
|`bool operator==(const grid_cell_t &) const = default`|フィールドごとに列と行の位置を比較します。|

#### `grid_selection_mode_t`

声明。`enum class grid_selection_mode_t`。

cellはセル選択を表し、rowは全体行の選択を表します。

|宣言|用途と呼び出しの意味|
|---|---|
|`cell`|セルごとに選択します。|
|`row`|全体行を選択します。|

#### `grid_cell_render_t`

声明。`struct grid_cell_render_t`。

セルの描画コールバックに渡されるデータレコードには、セル位置、描画矩形、値、選択/ホバー/編集状態が含まれます。

|宣言|用途と呼び出しの意味|
|---|---|
|`grid_cell_t cell`|現在の行と列の位置です。|
|`render_rectangle_t rectangle`|現在のセルの描画矩形です。|
|`grid_value_t value`|セルの値です。|
|`bool selected = false`|選択されているかどうかです。|
|`bool hovered = false`|指摘されているかどうかです。|
|`bool editing = false`|編集中かどうかです。|

#### `grid`

声明。`class grid : public selection_control`。

編集可能な二次元テーブルです。デフォルトでは列が空で、行数は0、selection_mode=cell、multi_select=false、selected_index=-1、row_height=30、header_height=32、read_only=falseです。header_height=0は表頭を隠します。列幅はデフォルト100です。挿入または変更時にwidth=0、および全体幅のオーバーフローは例外を発生させ、元のデータと変更イベントは変わりません。publicインターフェースはセル、外部データコールバック、編集チェック操作を通じてテーブルを操作します。スクロールオフセットはprotected拡張インターフェースに属します。

表頭の背景は可視幅全体を覆い、長いタイトルの末尾には省略記号が表示されます。物理キーボードのキャプチャモードでは、Ctrlキーを押して項目を切り替え、Shiftキーを押して選択を拡張します。明示的なselect_cellのextend/toggleパラメータはアプリケーションによって選択が制御されます。begin_editとcommit_editは成功か失敗かを返し、失敗の説明はget_edit_errorから読み取れます。編集を終了する際、IME/layoutは現在のセルに対応する可視矩形を表示します。

grid_value_tはvariant<u32string, int64_t, double, bool>です。value_provider_tは指定された行と列を読み取ります。value_writer_tは書き込みを試み、errorを返して失敗の説明を提供します。cell_renderer_tはrender_contextとgrid_cell_render_tを受け取ります。edit_validator_tは送信前にセルと値をチェックします。

|宣言|用途と呼び出しの意味|
|---|---|
|`using value_provider_t = std::function<grid_value_t(uint64_t, uint64_t)>`|外部データの読み取りコールバックで、行と列をパラメータとしてgrid_value_tを返します。|
|`using value_writer_t = std::function<bool(uint64_t, uint64_t, const grid_value_t &, std::u32string &)>`|外部の書き込みコールバックで、行、列、書き込み対象値、およびエラーテキストをパラメータとしてboolを返します。|
|`using cell_renderer_t = std::function<void(render_context &, const grid_cell_render_t &)>`|可視セルの描画コールバックで、render_contextとセル描画レコードを受け取ります。|
|`using edit_validator_t = std::function<bool(grid_cell_t, const grid_value_t &, std::u32string &)>`|編集の送信チェックで、セル位置、値、およびエラーテキストをパラメータとしてboolを返します。|
|`event_container<event_args_t> on_column_list_changed`|列定義が変更されたときにトリガーされます。|
|`event_container<grid_column_event_args_t> on_column_width_changed`|列の幅が変更されたときにトリガーされます。|
|`event_container<grid_column_event_args_t> on_column_click`|列タイトルをクリックしたときにトリガーされます。|
|`event_container<event_args_t> on_selection_changed`|選択状態が変更されたときにトリガーされます。|
|`event_container<grid_cell_event_args_t> on_cell_double_click`|セルをダブルクリックしたときにトリガーされます。|
|`event_container<grid_cell_event_args_t> on_cell_value_changed`|セル値が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_row_height_changed`|行高が変更されるとトリガーされます。|
|`event_container<event_args_t> on_header_height_changed`|表頭の高さが変更されたときにトリガーされます。|
|`event_container<grid_cell_event_args_t> on_edit_started`|セルを編集し始めたときにトリガーされます。|
|`event_container<grid_cell_event_args_t> on_edit_committed`|セルの編集が成功して送信されたときにトリガーされます。|
|`event_container<grid_cell_event_args_t> on_edit_cancelled`|セルの編集をキャンセルしたときにトリガーされます。|
|`event_container<grid_cell_event_args_t> on_edit_failed`|セルの編集の送信に失敗したときにトリガーされます。|
|`explicit grid(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`~grid() override`|インスタンスをデストラクタリングし、そのオブジェクトが保持するリソースと参照を解放します。|
|`bool is_focusable() const override`|このコントロールがフォーカス能力を持っているかを検索する；実際のフォーカスはvisible、enabled、およびモダンな関係によって制限される。|
|`virtual const std::vector<grid_column_t> &get_column_list() const`|現在の列定義の読み取り専用参照を返します。|
|`virtual void set_column_list(std::vector<grid_column_t> value)`|列定義を全体として置換します。幅は正の数であり、総幅はint64_tで表現可能でなければなりません。チェックに失敗した場合は元の列を保持します。|
|`virtual uint64_t get_row_count() const`|最初の行数を読み取ります。初期値は0です。|
|`virtual void set_row_count(uint64_t value)`|行数を設定し、選択範囲を視口に合わせて有効範囲内にする。|
|`virtual grid_value_t get_cell_value(uint64_t row, uint64_t column) const`|指定された行列の値を読み取り、インデックスが範囲外の場合は例外を投げる。|
|`virtual void set_cell_value(uint64_t row, uint64_t column, grid_value_t value)`|現在のデータ書き込みエントリを呼び出して指定されたセルを更新し、失敗した場合はエラー説明を含む例外を投げる。|
|`virtual void set_data_provider(uint64_t row_count, value_provider_t reader, value_writer_t writer = {})`|外部データソースを関連付ける；readerは有効でなければならず、writerが空の場合はデータソースが読み取り専用であることを示し、row_countは現在の总行数である。|
|`virtual void set_cell_renderer(cell_renderer_t renderer)`|表示可能なセルの描画コールバックを設定する；空のコールバックはデフォルトの描画を復元する。|
|`virtual void set_edit_validator(edit_validator_t validator)`|ユーザー編集の送信チェックを設定する；falseを返した場合は編集状態を保持し、errorを提供する。|
|`virtual void refresh_data()`|外部データが変更された後、キャッシュ、レイアウト、表示を更新する。|
|`static std::u32string get_value_text(const grid_value_t &value)`|grid_value_tをセルの表示文字に変換する。|
|`virtual std::optional<grid_cell_t> get_cell_at(double local_left, double local_top) const`|コントロールのローカル座標をセルにマッピングする；表頭、スクロールバー、空白部分はnulloptを返す。|
|`virtual render_rectangle_t get_cell_rectangle(uint64_t row, uint64_t column) const`|指定されたセルの論理的な描画矩形を読み取る。|
|`virtual grid_selection_mode_t get_selection_mode() const`|セルまたは行全体の選択モードを読み取る。|
|`virtual void set_selection_mode(grid_selection_mode_t value)`|セルまたは行の選択モードを設定する。|
|`virtual bool get_multi_select() const`|複数選択スイッチを読み取り、デフォルトはfalseである。|
|`virtual void set_multi_select(bool value)`|複数選択を有効または無効にする。|
|`virtual const std::vector<grid_cell_t> &get_selected_cell_list() const`|現在選択されているセルの順序付き読み取り専用リストを返す。|
|`virtual bool get_cell_selected(uint64_t row, uint64_t column) const`|指定された行列が現在の選択に属しているかどうかを判断する。|
|`virtual void select_cell(uint64_t row, uint64_t column, bool extend = false, bool toggle = false)`|指定された行列を選択する；extendは範囲を拡張し、toggleはその選択を切り替える、デフォルトはどちらもfalseである。|
|`void clear_selection() override`|現在のセルまたは行全体の選択をクリアする。|
|`bool is_blank_at(double local_left, double local_top) const override`|ローカル座標が項目区の空白に属しているかどうかを判断し、空白のクリック選択ルールに使用する。|
|`virtual int64_t get_selected_index() const`|現在の行インデックスを返す、-1は選択されていないことを意味する。|
|`virtual void set_selected_index(int64_t value)`|指定された有効な行を選択する、-1は選択をクリアする。|
|`virtual uint64_t get_row_height() const`|正の整数行高を読み取り、デフォルトは30である。|
|`virtual void set_row_height(uint64_t value)`|正の整数行高を設定する。|
|`virtual uint64_t get_header_height() const`|表頭の高さを読み取り、デフォルトは32である。|
|`virtual void set_header_height(uint64_t value)`|表頭の高さを設定する；0は表頭を非表示にする。|
|`virtual uint64_t get_visible_row_count() const`|現在の視口で表示可能な行数を返す。|
|`virtual bool get_vertical_scrollbar_visible() const`|内容範囲に基づいて計算された縦スクロールバーの可視性を照会する。|
|`virtual bool get_horizontal_scrollbar_visible() const`|内容範囲に基づいて計算された横スクロールバーの可視性を照会する。|
|`virtual void set_column_width(uint64_t column, uint64_t value)`|既存の列の正の幅を設定する；インデックス、幅、または総幅が不正な場合は例外を投げる。元の値とイベント状態は変わらない。|
|`virtual bool get_read_only() const`|全表のユーザー編集読み取り専用スイッチを読み取り、デフォルトはfalseである。|
|`virtual void set_read_only(bool value)`|ユーザー編集を制御する；trueの場合は編集を終了し、セルの表示を保持する。|
|`virtual bool get_editing() const`|編集中のセルが存在するかどうかを返す。|
|`virtual std::optional<grid_cell_t> get_edit_cell() const`|現在の編集セルを返す；編集されていない場合はnulloptである。|
|`virtual const std::u32string &get_edit_text() const`|現在の編集エリアのテキストを読み取ります。|
|`virtual void set_edit_text(const std::u32string &value)`|現在の編集エリアのテキストを更新し、送信時にタイプとビジネス検証を実行します。|
|`virtual const std::u32string &get_edit_error() const`|最後に編集に失敗した説明を読み取ります。|
|`virtual bool begin_edit(uint64_t row, uint64_t column)`|指定されたセルを編集し始めます。コントロールと列の読み取り専用条件によって制限されます。成功した場合はtrueを返します。|
|`virtual bool commit_edit()`|現在の編集テキストまたは指定されたgrid_value_tを送信します。成功した場合はtrueを返し、失敗した場合はget_edit_errorを読み取ります。|
|`virtual bool commit_edit(const grid_value_t &value)`|現在の編集テキストまたは指定されたgrid_value_tを送信します。成功した場合はtrueを返し、失敗した場合はget_edit_errorを読み取ります。|
|`virtual void cancel_edit()`|現在の編集をキャンセルし、対応する入力インターフェースを閉じます。|
|`void set_visible(bool value) override`|表示状態を設定する；隠す場合は、このコントロールで進行中のインタラクションをクリアする。|
|`void set_enabled(bool value) override`|操作可能な状態を設定する；無効化する場合は、進行中のインタラクションをクリアする。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void refresh_layout() override`|コントロールのレイアウトを更新する、派生物がカバーする場合は必要なベースクラスの処理を保持する。|
|`virtual void notify_selection_changed(const vector<grid_cell_t> &previous, int64_t previous_index)`|更新された派生通知を選択し、元のセルリストと元の行インデックスを提供します。|
|`virtual uint64_t get_scroll_offset() const`|派生クラスは縦方向のスクロール行のオフセットを読み取ります。|
|`virtual void set_scroll_offset(uint64_t value)`|派生クラスは縦方向のスクロール行のオフセットを設定し、内容範囲内に制限します。|
|`virtual uint64_t get_horizontal_scroll_offset() const`|派生クラスによる横方向のロジックスクロールオフセットの読み取り。|
|`virtual void set_horizontal_scroll_offset(uint64_t value)`|派生クラスによる横方向のロジックスクロールオフセットの設定、内容範囲内に制限されます。|
|`virtual uint64_t get_maximum_scroll_offset() const`|派生クラスは最大縦方向行のオフセットを検索します。|
|`virtual uint64_t get_maximum_horizontal_scroll_offset() const`|派生クラスは最大横方向の論理オフセットを検索します。|
|`grid(const std::u32string &name, const std::u32string &type)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`virtual void set_horizontal_scrollbar_enabled(bool value)`|派生クラスは横方向のスクロールバーがレイアウトに参加するかどうかを制御します。|
|`virtual void remap_row_selection(uint64_t row_count, const std::function<std::optional<uint64_t>(uint64_t)> &mapper)`|データが再配置された後、マッパーによって元の選択を再マッピングします。nulloptを返すと、元の行が削除されたことを意味します。|
|`virtual grid_value_t read_cell_value(uint64_t row, uint64_t column) const`|派生データは入力ポイントを読み取り、指定された行と列のgrid_value_tを返します。|
|`virtual bool write_cell_value(uint64_t row, uint64_t column, const grid_value_t &value, std::u32string &error)`|派生データは入力ポイントを書き込みます。失敗した場合はfalseを返し、エラーを記載します。|
|`virtual bool get_cell_value_choice_list(uint64_t row, uint64_t column, std::vector<grid_value_t> &choice_list) const`|セルに選択可能な値を提供します。choice_listを通じて選択肢を提供する場合、trueを返します。|
|`virtual std::shared_ptr<const drawing_image> get_row_icon(uint64_t row) const`|その行の画像リソースを読み取ります。空のポインタはアイコンがないことを意味します。|
|`virtual void render_cell(render_context &context, const grid_cell_render_t &cell) const`|単一の可視セルを描画します。派生クラスによってカスタマイズ可能です。|
|`rectangle_t get_input_rectangle() const override`|現在のセルが実際に見えるローカル編集エリアを返し、入力インターフェースの位置決めに使用します。|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|
|`void render_overlay(render_context &context) const override`|派生描画エントリポイント；contextを使用してフラップを描画する。|

### `easyvrui/control/listview.h`

`listview`は`selection_control`を継承し、複数列のテキストを行全体で表示および選択できます。最初の列には項目のアイコンを表示できます。表頭をクリックすると`on_column_click`がトリガーされ、分割線をドラッグして列の幅を調整できます。ユーザーはレーザー、スクロールバー、キーボードを使用して各行を閲覧できます。

|メンバー|用途|
|---|---|
|`explicit listview(const std::u32string &name)`|リストビューを作成します。|
|`get_column_list()`|有効な`listview_column_collection`参照を返し、constオーバーロードを提供します。|
|`get_item_list()`|有効な`listview_item_collection`参照を返し、constオーバーロードを提供します。|
|`get_selected_index() / set_selected_index(value)`|主要な選択項目の位置を読み取りまたは設定します。`-1`は空の選択範囲を表します。|
|`get_selected_item() / set_selected_item(item)`|集合内の行オブジェクトを読み取りまたは選択します。`nullptr`は空の選択範囲を表します。|
|`select_item(index, extend = false, toggle = false)`|行のサブスカラに基づいて選択します。複数選択モードではアンカープオートまたは現在の行を切り替えることができます。|
|`get_selected_item_list()`|現在の選択範囲内の行オブジェクトを読み取ります。|
|`get_multi_select() / set_multi_select(value)`|単選または複数選択を切り替えます。|
|`get_row_height() / set_row_height(value)`|正の行の高さを設定します。デフォルトは30ロジックピクセルです。|
|`get_header_height() / set_header_height(value)`|表頭の高さを設定します。デフォルトは32で、0は表頭を非表示にします。|
|`get_visible_row_count()`|一画面に収容可能なロジック行数を読み取ります。|
|`get_vertical_scrollbar_visible() / get_horizontal_scrollbar_visible()`|スクロールバーの表示状態を読み取ります。|
|`on_item_list_changed`、`on_column_list_changed`|項目または列集合が変更されたときにトリガーされます。|
|`on_column_width_changed`、`on_column_click`|列の幅が変更されたり、表頭をクリックしたときにトリガーされます。パラメータは`listview_column_event_args_t`で、列オブジェクト`column`とそのインデックス`index`を提供します。|
|`on_selection_changed`、`on_row_double_click`|選択範囲の変更または行のアクティブ化時にトリガーされます。行ダブルクリックのパラメータは`listview_item_event_args_t`で、行オブジェクト`item`とそのインデックス`index`を提供します。|
|`on_row_height_changed`、`on_header_height_changed`|行の高さまたは表頭の高さが変更されたときにトリガーされます。|

ソートにより、元の行オブジェクトを新しい順序で`get_item_list().assign(...)`に渡すことができます。集合はオブジェクトのアイデンティティに基づいて選択が維持されます。

### `easyvrui/control/listview_column.h`

`listview_column(text, width)`は表頭のテキストとロジック幅を保存します。デフォルトではテキストは空で、幅は`DEFAULT_WIDTH`です（100）。`get_text()/set_text()`と`get_width()/set_width()`を使用してアクセスします。列の幅は0より大きく、同じリストの列の幅の合計は`int64_t`の正の範囲内でなければなりません。マウントされた列の変更はビューを更新します。

### `easyvrui/control/listview_item.h`

`listview_item(cell_list, icon, tag)`は一行のテキスト、オプションのアイコン、およびアプリケーションタグを保存します。デフォルトでは各項目は空で、`get_icon()/set_icon()`と`get_tag()/set_tag()`を使用してアクセスできます。`get_cell_list()`を読み取りまたは書き込みしてリストを更新できます。

### `easyvrui/control/listview_column_collection.h`

`listview_column_collection`はリストビューによって保持されます。`get_size()`を使用して数を読み取り、`contains(item)`と`get_index(item)`を使用して列オブジェクトで検索し、`operator[]`を使用して共有参照を返します。`add/insert`を使用して列を挿入し、`remove`を使用してオブジェクトまたは位置に基づいて列を取り出し、共有ポインタを返します。`assign`を使用してすべての内容を置き換え、`clear`を使用して集合をクリアします。挿入前に所有権と幅をチェックします。

### `easyvrui/control/listview_item_collection.h`

`listview_item_collection`は列集合と同じメンバー名を使用し、要素は`std::shared_ptr<listview_item>`です。各行オブジェクトは一つのリストに属しており、取り出した後には別のリストに追加できます。

### `easyvrui/control/listview_cell_collection.h`

`listview_cell_collection`列位置でUTF-32セルテキストを保存します。`operator[]`でテキストを読み取り、`set_cell(index, text)`で既存の位置を変更します。`add/insert/remove/assign/clear`で集合を調整し、`get_size/contains/get_index`でクエリを実行します。マウントされたプロジェクトの更新は自動的に再描画されます。

### `easyvrui/control/treeview.h`

`treeview`は`selection_control`を継承します。`get_node_list()`を通じてルートノード集合にアクセスし、constオーバーライドを提供します。`get_selected_node()/set_selected_node(tree_node *)`ではオブジェクトを通じて選択し、`nullptr`では選択を解除します。`get_row_height()`と`get_vertical_scrollbar_visible()`ではレイアウト状態を読み取ります。

`on_node_list_changed`はノードの追加や削除時にトリガーされ、`on_selection_changed`は選択範囲が変更された時にトリガーされ、`on_node_expanded/on_node_collapsed`は展開と折りたたみに対応し、`on_node_activated`はダブルクリックまたはEnterに対応します。`tree_node_event_args_t::node`はイベントに関連するノードを指します。

### `easyvrui/control/tree_node.h`

`tree_node(text, expanded, tag)`はノードを作成し、デフォルトではテキストとタグが空で、ノードは折りたたまれます。`get_text/set_text`、`get_tag/set_tag`、`get_expanded/set_expanded`では各属性にアクセスします。`expand()`と`collapse()`では展開状態を切り替えます。`get_parent()`は親ノードポインタを返し、ルートノードと親から離れたノードは`nullptr`を返します。`get_node_list()`は子ノードの直接操作可能な集合を返し、constオーバーライドを提供します。

### `easyvrui/control/tree_node_collection.h`

ルートノードと子ノード集合は`get_size/contains/get_index`を使用してクエリを行い、`operator[]`を通じて共有参照を取得します。`add/insert/assign`ではオブジェクトを設定し、`remove`ではオブジェクトまたは位置に応じて除外し、`clear`では空にします。ノードはオブジェクトのアイデンティティによって区別され、各ノードは同時に一つの集合に属します。ノードを移動する際は、まず元の集合から除外し、次に目標集合に加えます。

### `easyvrui/control/menu_container.h`

#### `menu_container`

声明。`class menu_container : public container_control`。

メニューコンテナの共通ベースクラスで、コンストラクタはprotectedです。get_control_list()は通常のcontrol_collectionを返し、要素はmenuitemでなければならず、名前はこの層内で一意です。get_menubar()は所属するメニューバーを見つけます；on_control_added/on_control_removedはメニュー固有のon_item_added/on_item_removedと同様にサブスクライブできます。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<menu_item_event_args_t> on_item_added`|メニューアイテムが集合に追加される際にトリガーされ、項目IDと実際のインデックスが含まれます。|
|`event_container<menu_item_event_args_t> on_item_removed`|メニューアイテムが集合から除外される際にトリガーされ、項目IDと除外前のインデックスが含まれます。|
|`virtual menubar *get_menubar() const`|所属するメニューバーを返し、まだメニューバーに関連していない場合はnullptrを返します。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`menu_container(const std::u32string &name, const std::u32string &type)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`void validate_control(const control &child) const override`|挿入前に要素が該当するコンテナの制約を満たしているかをチェックし、失敗した場合は例外を投げます。|
|`void notify_control_added(control &child, size_t index) override`|挿入後のコンテナ通知、indexは要素の実際の集合インデックスです。|
|`void notify_control_removed(control &child, size_t index) override`|削除後のコンテナ通知、indexは削除前の実際の集合インデックスです。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &child, const rectangle_t &rectangle) const override`|要素にコンテナ管理用の矩形を提供します；nulloptは自身の矩形を継続することを意味します。|
|`std::vector<control *> get_active_control_list() const override`|現在の表示とインタラクションに直接関与する要素を返す。|
|`bool is_control_active(const control &item) const override`|指定された要素が現在の表示とインタラクションに関与しているかを判断する。|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|
|`void render_overlay(render_context &context) const override`|派生描画エントリポイント；contextを使用してフラップを描画する。|

ウィンドウメニューは実際のcontrol_listに属する。set_menuを使用して追加する；control_listから直接menubarを追加すると、get_menuも同期して変更される。削除またはclearは同期の関連を解除し、on_control_added/on_control_removed内のindexはその要素の実際の集合インデックスである。各ウィンドウには一つのmenubarが関連しており、新しいメニューは置き換えられたメニューの同じ名前を使用することができる。

```cpp
auto menubar_main = make_shared<easyvrui::menubar>(U"menubar_main");
auto menuitem_file = make_shared<easyvrui::menuitem>(U"menuitem_file");
menuitem_file->set_text(U"文件(&F)");
auto menuitem_open = make_shared<easyvrui::menuitem>(U"menuitem_open");
menuitem_open->set_text(U"打开(&O)");
menuitem_open->set_shortcut(U"Ctrl+O");
menuitem_file->get_control_list().add(menuitem_open);
menubar_main->get_control_list().add(menuitem_file);
window_main->set_menu(menubar_main);
```

### `easyvrui/control/menuitem.h`

#### `menuitem`

声明。`class menuitem : public menu_container`。

メニュー項目とサブメニューコンテナ。デフォルトではtext/shortcutは空で、iconは空で、checkable/checked/separatorはすべてfalseである。サブ項目はget_control_list().add()を使用して追加され、階層的にさらに内包することができる。separator=trueは分割線を描画する；テキスト内の&Aまたは(&A)はニーモニックキーを指定する。shortcutはCtrl+Cなどのキーボードコマンドの文字を保存する；選択された項目を実行すると、継承されたon_clickがトリガーされる。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_text_changed`|テキストが変更された時にトリガーされる。|
|`event_container<event_args_t> on_icon_changed`|アイコンが変更されるとトリガーされる。|
|`event_container<event_args_t> on_shortcut_changed`|キーボードコマンドが変更されるとトリガーされる。|
|`event_container<event_args_t> on_checkable_changed`|チェックを設定するかどうかが変更されるとトリガーされる。|
|`event_container<event_args_t> on_checked_changed`|チェック状態が変更されるとトリガーされる。|
|`event_container<event_args_t> on_separator_changed`|分割線の設定が変更されるとトリガーされる。|
|`event_container<event_args_t> on_opening`|サブメニューを展開する準備が整うとトリガーされる。|
|`event_container<event_args_t> on_closed`|サブメニューが収納されるとトリガーされる。|
|`explicit menuitem(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`virtual const std::u32string &get_text() const`|表示される文字を読み取る。|
|`virtual void set_text(const std::u32string &value)`|表示される文字を設定する。|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|選択可能な画像リソースの共有参照を読み取り、nullptrはクリアを表す。|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|選択可能な画像リソースの共有参照を設定し、nullptrはクリアを表す。|
|`virtual const std::u32string &get_shortcut() const`|メニューキーボードコマンドの文字を読み取り。|
|`virtual void set_shortcut(const std::u32string &value)`|メニューキーボードコマンドの文字を設定する。|
|`virtual bool get_checkable() const`|チェックを許可するかどうかを読み取り。|
|`virtual void set_checkable(bool value)`|チェックを許可するかどうかを設定する。|
|`virtual bool get_checked() const`|現在のチェック状態を読み取る。|
|`virtual void set_checked(bool value)`|現在のチェック状態を設定する。|
|`virtual bool get_separator() const`|読み取りがセパレーターとして表示されるかどうか。|
|`virtual void set_separator(bool value)`|設定がセパレーターとして表示されるかどうか。|

### `easyvrui/control/menubar.h`

#### `menubar`

声明。`class menubar : public menu_container`。

メニューバー、デフォルトのフォントはfont_t{}、行高さ=32。メインメニューおよび各層のサブメニューはget_control_list()で維持される。open/closeでメニューのインタラクションを管理し、繰り返しクリックで展開されたメインメニューは収納される。レーザーで展開時には初期にサブアイテムのハイライトはなく、具体的なアイテムを指すとハイライトが付く。ウィンドウはset_menuで関連メニューを設定し、menubarをウィンドウのcontrol_listに実際の要素として追加することもできる。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_font_changed`|フォントが変更されるとトリガーされます。|
|`event_container<event_args_t> on_row_height_changed`|行高が変更されるとトリガーされます。|
|`event_container<event_args_t> on_opening`|メニューバーを展開する準備が整ったときにトリガーされる。|
|`event_container<event_args_t> on_closed`|メニューバーが収納されたときにトリガーされる。|
|`explicit menubar(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`bool is_focusable() const override`|このコントロールがフォーカス能力を持っているかを検索する；実際のフォーカスはvisible、enabled、およびモダンな関係によって制限される。|
|`virtual const font_t &get_font() const`|メニューのフォントを読み取り、デフォルトはfont_t{}。|
|`virtual void set_font(const font_t &value)`|メニューのフォントを設定し、フォント名は空でなければならず、サイズは正しい。|
|`virtual uint64_t get_row_height() const`|論理行高さを読み取り。|
|`virtual void set_row_height(uint64_t value)`|論理行高さを設定する。|
|`virtual bool get_is_open() const`|現在メニューのインタラクションモードにいるかどうかを検索する。|
|`virtual bool get_is_submenu_open(const menuitem &item) const`|指定されたメニューアイテムの次の層のポップアップリストが展開されているかどうかを検索する。|
|`virtual void open()`|メニューのインタラクションモードに入る。|
|`virtual void close(bool restore_focus = true)`|すべてのサブメニューを収納する；restore_focusはデフォルトでtrueで、メニューに入る前のフォーカスを復元するために使用される。|
|`void set_visible(bool value) override`|表示状態を設定する；隠す場合は、このコントロールで進行中のインタラクションをクリアする。|
|`void set_enabled(bool value) override`|操作可能な状態を設定する；無効化する場合は、進行中のインタラクションをクリアする。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|
|`void render_overlay(render_context &context) const override`|派生描画エントリポイント；contextを使用してフラップを描画する。|

### `easyvrui/control/toolbar.h`

#### `toolbar`

声明。`class toolbar : public container_control`。

アイコンツールバー。tool_sizeはデフォルトで40であり、0より大きく。spacingはデフォルトで6.0であり、有限かつ非負でなければなりません。`get_button_list()`を使用してボタン、アイコン、ヒント、およびセパレーターを設定します。ボタンは横に並んで配置され、ツールバー自体には背景が提供されます。利用可能な領域を超える完全なボタンセットは、描画とヒットを停止します。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_spacing_changed`|ツールバーセル間の間隔が変更されるとトリガーされます。|
|`event_container<event_args_t> on_tool_size_changed`|ツールバーセルの辺の長さが変更されるとトリガーされます。|
|`toolbar_button_collection &get_button_list()`およびconstのオーバーライド|アクセスボタンおよびセパレーターの集合を取得します。|
|`explicit toolbar(const u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`void dispose() override`|button_listをクリアし、そのツールバーを解放します。|
|`virtual size_t get_tool_size() const`|ツールバーボタンの正の整数辺の長さを読み取ります。|
|`virtual void set_tool_size(size_t value)`|ツールバーボタンの正の整数辺の長さを設定します。|
|`virtual double get_spacing() const`|ツールバー間の有限かつ非負の論理間隔を読み取ります。|
|`virtual void set_spacing(double value)`|ツールバー間の有限かつ非負の論理間隔を設定します。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|派生描画エントリー；contextを使用して本文を描画する。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|ツールバーのサイズ、間隔、および現在の順序に基づいてボタンの表示矩形を配置します。|
|`bool is_control_active(const control &item) const override`|指定された要素が現在の表示とインタラクションに関与しているかを判断する。|
|`std::vector<control *> get_active_control_list() const override`|現在の表示とインタラクションに直接関与する要素を返す。|

`get_button_list()`を使用してボタンとセパレーターを設定します：

```cpp
auto toolbar_main = make_shared<easyvrui::toolbar>(U"toolbar_main");
auto &button_save = toolbar_main->get_button_list().add(U"save");
button_save.set_tooltip_text(U"保存");
auto &separator_main = toolbar_main->get_button_list().add(U"separator");
separator_main.set_separator(true);
window_main->get_control_list().add(toolbar_main);
```

### `easyvrui/control/toolbar_button.h`

#### `toolbar_button`

声明。`class toolbar_button : public button`。

ツールバーボタンは`button`を継承し、構築後の名前は読み取り専用です。iconはデフォルトで空で、separatorはfalse、enabledはtrue、tooltip_textは空です。アイコンは比率を維持し、指し示されるときにヒントが表示されます。separatorがtrueの場合、狭いセパレーターが表示されます。toolbar.get_button_list()を追加した後、get_parentは所属するツールバーを返します。通常のボタンはon_clickを受け取ります。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_click`|ツールバーボタンの操作が実行されるとトリガーされます。|
|`event_container<event_args_t> on_icon_changed`|アイコンが変更されるとトリガーされる。|
|`explicit toolbar_button(const std::u32string &name)`|インスタンスの構築；パラメータと制約はこのタイプの説明を参照。|
|`control_base *get_parent() const override`|所属するツールバーを返します。どのツールバーにも属していない場合はnullptrを返します。|
|`void dispose() override`|所属するボタン集合からボタンを削除し、解放します。|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|選択可能な画像リソースの共有参照を読み取り、nullptrはクリアを表す。|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|選択可能な画像リソースの共有参照を設定し、nullptrはクリアを表す。|
|`virtual bool get_separator() const`|読み取りがセパレーターとして表示されるかどうか。|
|`virtual void set_separator(bool value)`|設定がセパレーターとして表示されるかどうか。|
|`virtual bool get_enabled() const`|操作可能かどうかを読み取ります。|
|`virtual void set_enabled(bool value)`|操作可能かどうかを設定します。|

### `easyvrui/control/toolbar_button_collection.h`

#### `toolbar_button_collection`

声明。`class toolbar_button_collection`。

toolbarに属するボタンコンテナで、コンストラクタはprivateで、toolbar.get_button_list()によって提供されます。インデックスまたは名前で検索し、名前は栏内で一意です。add/insertは`shared_ptr<toolbar_button>`を受け入れることも、名前に基づいてボタン参照を作成して返すこともできます。insertは末尾を超えて追加され、removeは`shared_ptr<toolbar_button>`を返し、get_item_listはポインタリストのコピーを返します。

|宣言|用途と呼び出しの意味|
|---|---|
|`toolbar_button_collection(const toolbar_button_collection &) = delete`|コピー構築を禁止します。|
|`~toolbar_button_collection()`|インスタンスをデストラクタリングし、そのオブジェクトが保持するリソースと参照を解放します。|
|`toolbar_button_collection &operator=(const toolbar_button_collection &) = delete`|このコピーまたは代入操作を禁止します。|
|`size_t get_size() const`|ボタンとセパレーターの総数を返します。|
|`bool is_empty() const`|集合が空かどうかを検索します。|
|`bool contains(const toolbar_button &item) const`|指定されたインスタンスまたは名前がこの集合に属するかどうかを検索します。|
|`bool contains(const std::u32string &name) const`|指定されたインスタンスまたは名前がこの集合に属するかどうかを検索します。|
|`toolbar_button &get_item(size_t index) const`|インデックスまたは名前でtoolbar_buttonの参照を取得します。欠如した場合は例外を投げます。|
|`toolbar_button &get_item(const std::u32string &name) const`|インデックスまたは名前でtoolbar_buttonの参照を取得します。欠如した場合は例外を投げます。|
|`size_t get_index(const toolbar_button &item) const`|集合内でのボタンの0開始位置を取得します。未加入の場合は例外を投げます。|
|`std::vector<toolbar_button *> get_item_list() const`|表示順に並んだtoolbar_buttonポインタリストのコピーを返します。|
|`void insert(size_t index, std::shared_ptr<toolbar_button> item)`|インデックスで共有ボタンを挿入するか、名前に基づいて新しいボタンを作成します。末尾を超えて追加されます。|
|`toolbar_button &insert(size_t index, const std::u32string &name)`|インデックスで共有ボタンを挿入するか、名前に基づいて新しいボタンを作成します。末尾を超えて追加されます。|
|`void add(std::shared_ptr<toolbar_button> item)`|共有ボタンを追加するか、名前に基づいて新しいボタン参照を作成して返します。|
|`toolbar_button &add(const std::u32string &name)`|共有ボタンを追加するか、名前に基づいて新しいボタン参照を作成して返します。|
|`std::shared_ptr<toolbar_button> remove(size_t index)`|対応するボタンのshared_ptrを削除して返します。別のtoolbarに再追加できます。|
|`std::shared_ptr<toolbar_button> remove(toolbar_button &item)`|対応するボタンのshared_ptrを削除して返します。別のtoolbarに再追加できます。|
|`std::shared_ptr<toolbar_button> remove(const std::u32string &name)`|対応するボタンのshared_ptrを削除して返します。別のtoolbarに再追加できます。|
|`void clear()`|すべてのボタンとセパレータを削除し、所属関係を解除する。|
|`toolbar_button &operator[](size_t index) const`|インデックスまたは名前でボタン参照を取得する。|
|`toolbar_button &operator[](const std::u32string &name) const`|インデックスまたは名前でボタン参照を取得する。|

### `easyvrui/control/tabpage.h`

タブ内容コンテナ。

#### `tabpage`

声明。`class tabpage : public panel`。

`tabpage`は継承されたコントロール集合を通じてページ内容を収容する。タブタイトルは`tabpage`自身によって保存され、ページの有効表示領域は所属する`tabcontrol`によって管理される。

`panel`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

|宣言|用途と呼び出しの意味|
|---|---|
|`explicit tabpage(const u32string &name)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`~tabpage() override`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`virtual const u32string &get_text() const`|タブタイトルを読み取り、デフォルトでは空とする。|
|`virtual void set_text(const u32string &value)`|タイトルを変更し、所属する`tabcontrol`のタブを更新する。|
|`event_container<event_args_t> on_text_changed`|タブタイトルが変更されるとトリガーされる。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void render(render_context &context) const override`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|

### `easyvrui/control/tabpage_collection.h`

位置または名前でページ集合を検索する機能をサポートする。

#### `tabpage_collection`

声明。`class tabpage_collection : public control_collection`。

ページ集合のインデックス、名前の一意性、ライフサイクル規則は`control_collection`と一致する。`get_page()`と`operator[]`はページ参照を返す。`insert()`は末尾を超えた場合に追加され、ページが削除されると自動的に現在の選択を調整する。

|宣言|用途と呼び出しの意味|
|---|---|
|`explicit tabpage_collection(tabcontrol &owner)`|このタイプのインスタンスを構築します。パラメータの意味はこのタイプの説明と署名を参照してください。|
|`~tabpage_collection() override`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`tabpage &get_page(size_t index) const`|インデックスまたは名前でページ参照を返す；存在しない場合は例外を投げる。|
|`tabpage &get_page(const u32string &name) const`|インデックスまたは名前でページ参照を返す；存在しない場合は例外を投げる。|
|`void insert(size_t index, control &page) override`|index位置に挿入します。indexが現在の数より小さい場合は追加されます。具体的な要素タイプ、所有権、重複名前の制約については、所属コンテナの説明を参照してください。|
|`void insert(size_t index, std::shared_ptr<control> page) override`|index位置に挿入します。indexが現在の数より小さい場合は追加されます。具体的な要素タイプ、所有権、重複名前の制約については、所属コンテナの説明を参照してください。|
|`using control_collection::add`|項目を追加します。オブジェクトの参照方法は呼び出し側が保証します。shared_ptrの方法はコンテナが共有所有権を保持します。|
|`using control_collection::remove`|ページを削除して`shared_ptr<control>`に戻り、他の適切なコレクションに直接追加できます。|
|`std::shared_ptr<control> remove(size_t index) override`|ページを削除して`shared_ptr<control>`に戻り、他の適切なコレクションに直接追加できます。|
|`void clear() override`|すべてのページを削除します。|
|`tabpage &operator[](size_t index) const`|0の開始位置または名前でオブジェクト参照を取得します。この動作はget_control/get_pageと同じです。|
|`tabpage &operator[](const u32string &name) const`|0の開始位置または名前でオブジェクト参照を取得します。この動作はget_control/get_pageと同じです。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`void notify_control_added(control &item, size_t index) override`|ページを追加した後、ページ選択とon_page_addedイベントを同期します。|
|`void notify_control_removed(control &item, size_t index, bool clearing) override`|ページが削除された後、`on_page_removed`がトリガーされます。|

`page_list`は`control_collection`を継承し、そのページ保存、名前インデックス、所有権規則を使用します。`tabpage::set_text()`を使用してタイトルを設定し、タイトルはページと共に保持されます。

```cpp
auto tabcontrol_main = make_shared<easyvrui::tabcontrol>(U"tabcontrol_main");
auto tabpage_general = make_shared<easyvrui::tabpage>(U"tabpage_general");
auto textbox_value = make_shared<easyvrui::textbox>(U"textbox_value");
textbox_value->set_text(U"配置");
tabpage_general->get_control_list().add(textbox_value);
tabpage_general->set_text(U"常规");
tabcontrol_main->get_page_list().add(tabpage_general);
window_main->get_control_list().add(tabcontrol_main);
```

### `easyvrui/control/tabcontrol.h`

タブの選択、タイトルの外観、ページのレイアウト。

#### `tab_position_t`

声明。`enum class tab_position_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`top`|タブは上にあります。|
|`bottom`|タブは下にあります。|
|`left`|タブは左側にあります。|
|`right`|タブは右側にあります。|

#### `tabcontrol`

声明。`class tabcontrol : public container_control`。

container_controlを継承します。page_listはページとタイトルを管理します。デフォルトのタブはtopにあり、tab_size=36、ページが追加されていない場合selected_index=-1；最初のページを追加した後、有効なページが選択されます。現在のページの内容のみ表示され、タブの選択エリアにハイライトが表示されます。tab_fontはデフォルトでSegoe UI、18です。ウィンドウの本文とtabpageはそれぞれの背景を保持します。

アプリケーションは`get_page_list()`を使用してページを管理します。その他のpublicメンバーは継承規則に従って使用されます。

|宣言|用途と呼び出しの意味|
|---|---|
|`tabpage_collection &get_page_list()`およびconstのオーバーライド|タブコレクションにアクセスし、要素は`tabpage`です。|
|`event_container<event_args_t> on_selected_index_changed`|選択インデックスが変更されるとトリガーされます。|
|`event_container<event_args_t> on_tab_position_changed`|タブの位置が変更されるとトリガーされます。|
|`event_container<event_args_t> on_tab_size_changed`|タブバーの厚さが変更されるとトリガーされます。|
|`event_container<event_args_t> on_tab_font_changed`|タブのフォントが変更されるとトリガーされます。|
|`event_container<event_args_t> on_tab_foreground_color_changed`|通常のタブの前景色が変更されるとトリガーされます。|
|`event_container<event_args_t> on_tab_background_color_changed`|通常のタブの背景色が変更されるとトリガーされます。|
|`event_container<event_args_t> on_selected_tab_foreground_color_changed`|選択されたタブの前景色が変更されるとトリガーされます。|
|`event_container<event_args_t> on_selected_tab_background_color_changed`|選択されたタブの背景色が変更されるとトリガーされます。|
|`event_container<tabpage_event_args_t> on_page_added`|ページを追加する際にトリガーされ、タブ`page`とインデックス`index`を含む。|
|`event_container<tabpage_event_args_t> on_page_removed`|ページを削除する際にトリガーされ、タブ`page`とインデックス`index`を含む。|
|`event_container<tabpage_event_args_t> on_page_text_changed`|タブのタイトルが変更された際にトリガーされ、`event.page->get_text()`を通じてタブのタイトルを読み取る。|
|`event_container<tabpage_event_args_t> on_page_close`|閉じるアイコンをクリックするか、タブがフォーカスされた時にDeleteキーを押すことでトリガーされる。アプリケーションが保存を確認した後、`page_list`から`event.page`を削除する。|
|`event_container<event_args_t> on_page_close_button_visible_changed`|タブの閉じるボタンの設定が変更された際にトリガーされる。|
|`event_container<event_args_t> on_selection_changed`|選択状態が変更されたときにトリガーされます。テキストエディターではstart/lengthを使用し、項目とタブではselectedを使用します。|
|`explicit tabcontrol(const u32string &name)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`bool is_focusable() const override`|このコントロールがフォーカス能力を持っているかを検索する；実際のフォーカスはvisible、enabled、およびモダンな関係によって制限される。|
|`virtual int64_t get_selected_index() const`|現在の選択インデックスを読み取ります、-1は選択されていないことを表します。|
|`virtual void set_selected_index(int64_t value)`|現在の選択インデックスを設定します、-1は選択されていないことを表します。|
|`virtual tabpage *get_selected_page() const`|現在のtabpageポインタを読み取る；選択されていない場合はnullptr。|
|`virtual tab_position_t get_tab_position() const`|タブがtop、bottom、left、またはrightに位置しているかを読み取る。|
|`virtual void set_tab_position(tab_position_t value)`|タブをtop、bottom、left、またはrightに位置させる。|
|`virtual uint64_t get_tab_size() const`|タブの条の厚さを読み取る。0よりも大きくなければならない。|
|`virtual void set_tab_size(uint64_t value)`|タブの条の厚さを設定する。0よりも大きくなければならない。|
|`virtual bool get_page_close_button_visible() const`|タブの閉じるボタンが表示されているかを読み取る。デフォルトはfalse。|
|`virtual void set_page_close_button_visible(bool value)`|タブの閉じるボタンを設定する；クリック時にはon_page_closeのリクエストのみを発行し、アプリケーションがページを削除するかどうかを決定する。|
|`virtual const font_t &get_tab_font() const`|タブのフォントを読み取る。|
|`virtual void set_tab_font(const font_t &value)`|タブのフォントを設定する。|
|`virtual uint32_t get_tab_foreground_color() const`|選択されていないタブの前景色を読み取る。|
|`virtual void set_tab_foreground_color(uint32_t value)`|選択されていないタブの前景色を設定する。|
|`virtual uint32_t get_tab_background_color() const`|選択されていないタブの背景色を読み取る。|
|`virtual void set_tab_background_color(uint32_t value)`|選択されていないタブの背景色を設定する。|
|`virtual uint32_t get_selected_tab_foreground_color() const`|選択されているタブの前景色を読み取る。|
|`virtual void set_selected_tab_foreground_color(uint32_t value)`|選択されているタブの前景色を設定する。|
|`virtual uint32_t get_selected_tab_background_color() const`|選択されているタブの背景色を読み取る。|
|`virtual void set_selected_tab_background_color(uint32_t value)`|選択されているタブの背景色を設定する。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`tabpage_collection &get_control_list() override`|保護されたコヴァリーンカバレッジで、page_listを返す；アプリケーションは`get_page_list()`を通じてアクセスする。|
|`const tabpage_collection &get_control_list() const override`|保護されたコヴァリーンカバレッジで、page_listを返す；アプリケーションは`get_page_list()`を通じてアクセスする。|
|`void validate_control(const control &item) const override`|要素がtabpageであることを検証する；他のコントロールタイプはページ集合に追加できない。|
|`vector<control *> get_active_control_list() const override`|現在選択されているページを返す。選択されていない場合は空のリストを返す。|
|`bool is_control_active(const control &item) const override`|要素が現在選択されているページであるかを判断する。|
|`virtual void notify_selected_index(int64_t previous)`|現在のページインデックスの変化に関する通知。|
|`void refresh_layout() override`|コントロールのレイアウトを更新する、派生物がカバーする場合は必要なベースクラスの処理を保持する。|
|`size_t get_focus_target_count() const override`|複合コントロールのフォーカスナビゲーションに使用する、内部のフォーカス可能な領域の数を返す。|
|`virtual size_t get_focus_target_at(double left, double top) const`|コントロールのローカル座標に基づいて、内部のフォーカス領域のインデックスを取得する。|
|`optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|要素にコンテナ管理用の矩形を提供します；nulloptは自身の矩形を継続することを意味します。|
|`optional<int64_t> get_selection_index_at(double left, double top, const rectangle_t &rectangle) const override`|指定された論理座標に対応する選択可能なサブアイテムのインデックスを検索する；マッチしない場合はnulloptとする。|
|`void render(render_context &context) const override`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|

### `easyvrui/control/window.h`

VRトップレベルのコンテナ、空間参照、表示、モダルおよびウィンドウのインタラクション。

#### `startup_position_t`

宣言。`enum class startup_position_t`、メンバーは`none`および`center`である。

`none`は設定された初期位置と姿勢を使用する。`center`は初めて表示される際に、ソースウィンドウ面と平行で中央に整列し、ヘッドマウントの側面の法線に沿って前進する。モダルウィンドウは直接の親ウィンドウを厳格に使用する。SDKが提供する同じセッションのソースを優先する；ソースを省略した場合、Engineは現在選択されている可視の普通の表面を使用し、セッション間でDesktopから他のアプリを起動することができる。有効なソースがない場合は、現在のヘッドマウントの姿勢に基づいて中央に配置し、初期距離は`max(1.2, max(physical_width, physical_height))`メートルとする。Engineは各セッションウィンドウと組み合わせて初期深度を設定し、presentの完了コールバックで最終的なposition/rotationを同期する。位置決めは一度だけ適用され、その後、隠し、表示、およびソースウィンドウの移動は、そのウィンドウが確定した姿勢を保持する；補助入力ウィンドウはEngineが入力エリアと関連して位置決めする。

`startup_position_t::none`であり、positionとrotationが共にゼロの場合、世界ウィンドウの左上角は初期の正面を基準にする。デフォルトのcenterは上記のソース優先とヘッドマウントの後退規則に従う。

#### `window`

声明。`class window : public container_control`。

container_controlを継承します。デフォルトではrect={0,0,640,360}、visible=false、title=name、タイトルフォントSegoe UI/20、物理スケール=1.0倍、positionとrotationは全0、reference_objectはworldです。タイトルバー、閉じるボタン、移動とスケーリングは全て有効で、トラッキングメニューにはデフォルトでworld/body/left/right/headが含まれます。トップレベルのウィンドウの空間位置は`position`と参照対象によって決定されます。ウィンドウの展開幅は`rect.width * physical_scale / 1000`メートル、高さは`rect.height * physical_scale / 1000`メートルです。移動可能でサイズが十分な場合、本文の外側に制御リングが予約されています。派生的ウィンドウは、保護されたget_content_top()を通じて本文を配置できます。通常は片手で遠距離移動と回転を行い、両手で2つの制御リングブロックを握って制限された回転を行います。`get_closed()`を通じてウィンドウが閉じているかを確認します。

初回表示時は、`set_physical_scale()`を明示的に呼び出さない場合にのみ、SDKが決定した同じセッションのソースウィンドウのスケーリングを継承します。明示的な設定が優先され、1.0を含みます。モーダルウィンドウはworld参照対象を使用し、独立してドラッグ可能です。

`show_dialog(owner_window)`のownerには、同じUIランタイムに属する別の操作可能なウィンドウを渡します。ダイアログは非表示で、閉じられておらず、モーダル状態に入っていないことが必要です。呼び出し中は直接のownerが一時的に操作できなくなります。ボタンやメニューのイベントから同期的に開けます。また、現在操作できるダイアログを次のダイアログのownerにできます。描画の送信中に呼び出すとエラーになります。処理順は[セッションと入れ子のメッセージループ](/ja/advanced/04_session_and_context)を参照してください。

モーダルに入ると、結果が`dialog_result_t::none`にリセットされます。`none`以外の結果を設定すると、閉じる処理を要求します。ハンドラーが閉じる操作を取り消した場合は、ダイアログが開いたままになり、結果は設定前の値に戻ります。結果が`none`のままタイトルバーの閉じるボタンまたは`close()`で正常に閉じると、`dialog_result_t::cancel`を返します。呼び出し元はウィンドウオブジェクトを保持し、戻った後でコントロールの値を読めます。

`container_control`の全てのpublic属性アクセス、メソッド、イベントを継承します。以下の表は、このタイプ自身の宣言またはカバーするメンバーをリストしています。

曲率kは有限の非負数で、単位はm⁻¹です。k=0は平面を表し、非ゼロの場合は常に弧度数θ=k×get_physical_width()で、属性とEngineのチェックはθ<2πを要求します。get_physical_width()は展開された弧長で、rect.width×physical_scale/1000で計算されます。ウィンドウの左下角のインタラクティブハンドルと対応するスティックの安全調整上限は160°です。この上限はUI操作規則に属し、set_curvature()は依然として前述の合法範囲を使用します。rectやphysical_scaleを変更する場合も曲率が合法であることを保証する必要があります。

左下角の曲率調整ノブと右下角の拡大縮小ノブはtriggerを使用し、押した状態で選択状態を維持し、レーザーの端をロックします。曲率は横スティックで左右に、拡大縮小は上下に調整します。左下角をダブルクリックすると平面に戻ります。curvature_adjustableとresizableはそれぞれ2種類の調整インターフェースを制御します。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_container<event_args_t> on_menu_changed`|メニューバーの関連変化がトリガーされます。|
|`event_container<event_args_t> on_title_changed`|タイトルの変化がトリガーされます。|
|`event_container<event_args_t> on_title_foreground_color_changed`|タイトルの文字の前景色が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_title_background_color_changed`|タイトルバーの背景色が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_title_font_changed`|タイトルのフォントが変更されたときにトリガーされます。|
|`event_container<event_args_t> on_icon_changed`|タイトルのアイコンオブジェクトが変更されたりクリアされたときにトリガーされます。|
|`event_container<event_args_t> on_rotation_changed`|ウィンドウの回転角度が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_curvature_changed`|曲率が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_startup_position_changed`|起動位置方式が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_curvature_adjustable_changed`|曲率のインタラクティブ調整スイッチが変更されたときにトリガーされます。|
|`event_container<event_args_t> on_reference_object_changed`|空間参照対象が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_show_title_bar_changed`|タイトルバーの表示設定が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_tracking_mode_set_changed`|トラッキングモードのオプションが変更されたときにトリガーされます。|
|`event_container<event_args_t> on_show_close_button_changed`|閉じるボタンの表示設定が変更されたときにトリガーされます。|
|`event_container<event_args_t> on_movable_changed`|移動スイッチが変更されたときにトリガーされます。|
|`event_container<event_args_t> on_resizable_changed`|拡大縮小スイッチが変更されたときにトリガーされます。|
|`event_container<event_args_t> on_load`|ウィンドウが初めて表示される際に一度トリガーされます。|
|`event_container<event_args_t> on_shown`|ウィンドウが表示される際にトリガーされます。|
|`event_container<event_args_t> on_hidden`|ウィンドウが隠される際にトリガーされます。|
|`event_container<cancel_event_args_t> on_closing`|通常の閉じる前にトリガーされます。`event.cancel = true`を使用するとこの閉じる操作を中止できます。|
|`event_container<event_args_t> on_closed`|ウィンドウが閉じる際にトリガーされます。|
|`event_container<render_error_event_args_t> on_render_failed`|ウィンドウが送信またはレンダリングに失敗したときにトリガーされ、エラーデータが付随します。|
|`event_container<event_args_t> on_tracking_lost`|ウィンドウの空間参照トラッキングが失われたときにトリガーされます。|
|`event_container<event_args_t> on_tracking_restored`|ウィンドウの空間参照トラッキングが回復したときにトリガーされます。|
|`event_container<event_args_t> on_activated`|ウィンドウが現在のアクティブウィンドウになったときにトリガーされます。|
|`event_container<event_args_t> on_deactivated`|ウィンドウがアクティブ状態を失ったときにトリガーされます。|
|`event_container<event_args_t> on_move_start`|ウィンドウがインタラクティブに移動または回転を開始したときにトリガーされます。|
|`event_container<interaction_end_event_args_t> on_move_end`|ウィンドウがインタラクティブに移動または回転を終了したときにトリガーされ、cancelledは終了の理由を説明します。|
|`event_container<event_args_t> on_resize_start`|ウィンドウがインタラクティブに拡大縮小を開始したときにトリガーされます。|
|`event_container<interaction_end_event_args_t> on_resize_end`|ウィンドウがインタラクティブに拡大縮小を終了したときにトリガーされます。|
|`event_container<event_args_t> on_curvature_adjust_start`|ウィンドウの曲率を調整し始めたときにトリガーされます。|
|`event_container<interaction_end_event_args_t> on_curvature_adjust_end`|ウィンドウの曲率調整を終了したときにトリガーされます。|
|`explicit window(const u32string &name)`|不変のUnicode名nameでインスタンスを作成する；その他の属性はそれぞれのsetterで設定する。|
|`virtual const std::shared_ptr<menubar> &get_menu() const`|現在のメニューに戻る`const shared_ptr<menubar> &`；空引用はメニューが設定されていないことを意味します。|
|`virtual void set_menu(std::shared_ptr<menubar> value)`|固有メニューの設定または解除；メニューはcontrol_list内の実際の要素です。新しいメニューを追加するには、まず元のメニューを削除し、その後新しいメニューを集合に追加します。元のメニューの同名の新しいインスタンスを使用することができます。|
|`void set_visible(bool value) override`|可視状態の設定。|
|`virtual const u32string &get_title() const`|ウィンドウのタイトル文字を読み取り、デフォルトではnameと同じです。|
|`virtual void set_title(const u32string &value)`|ウィンドウのタイトル文字を設定、デフォルトではnameと同じです。|
|`virtual uint32_t get_title_foreground_color() const`|ウィンドウのタイトル文字の前景色を読み取ります。|
|`virtual void set_title_foreground_color(uint32_t value)`|ウィンドウのタイトル文字の前景色を設定します。|
|`virtual uint32_t get_title_background_color() const`|ウィンドウのタイトルバーの背景色を読み取ります。|
|`virtual void set_title_background_color(uint32_t value)`|ウィンドウのタイトルバーの背景色を設定します。|
|`virtual const font_t &get_title_font() const`|ウィンドウのタイトル文字のフォントを読み取ります。|
|`virtual void set_title_font(const font_t &value)`|ウィンドウのタイトル文字のフォントを設定します。|
|`virtual const std::shared_ptr<const drawing_image> &get_icon() const`|タイトルバーの左側のアイコンオブジェクトを読み取ります。デフォルトではネイティブアイコンを使用します。|
|`static std::shared_ptr<const drawing_image> get_default_icon()`|ネイティブデフォルトアイコンを読み取ります。set_iconを通じてデフォルト値に戻します。|
|`virtual void set_icon(std::shared_ptr<const drawing_image> value)`|アイコンを設定します。画像を等比例縮小し、垂直中央に配置し、タイトル文字の後ろの領域を保持します。nullptrを渡すとアイコンをクリアし、タイトルの左側のレイアウトを復元します。|
|`virtual double get_physical_scale() const`|スケーリング倍率を読み取ります。有限の正の数でなければなりません。|
|`virtual void set_physical_scale(double value)`|有限の正のスケーリング倍率を設定します。新しい物理幅は依然として曲率の合法範囲を満たす必要があります。|
|`virtual double get_curvature() const`|柱面の曲率kを読み取ります。単位はm⁻¹です。0は平面を表します。|
|`virtual void set_curvature(double value)`|有限の曲率kを設定します。k>=0かつk×get_physical_width()<2πが必要です。160°はインタラクティブハンドルの安全調整上限です。|
|`virtual startup_position_t get_startup_position() const`|起動位置方式を読み取ります。デフォルトではcenterです。|
|`virtual void set_startup_position(startup_position_t value)`|起動位置方式を設定します。noneまたはcenterを受け入れます。|
|`virtual const vec3_t &get_position() const`|相対参照対象の位置オフセットを読み取ります。単位はメートルです。|
|`virtual void set_position(const vec3_t &value)`|相対参照対象の位置オフセットを設定します。単位はメートルです。|
|`virtual const vec3_t &get_rotation() const`|相対参照対象のXYZオイラー回転を読み取ります。単位は度です。|
|`virtual void set_rotation(const vec3_t &value)`|相対参照対象のXYZオイラー回転を設定します。単位は度です。|
|`virtual const reference_object_t &get_reference_object() const`|空間参照目標を読み取ります。|
|`virtual void set_reference_object(const reference_object_t &value)`|空間参照目標を設定します。|
|`virtual bool get_show_title_bar() const`|ウィンドウタイトルバーを表示するかどうかを読み取ります。|
|`virtual void set_show_title_bar(bool value)`|ウィンドウタイトルバーを表示するかどうかを設定します。|
|`virtual const std::set<reference_object_type_t> &get_tracking_mode_set() const`|タイトルバーのトラッキングメニューのパターン集合を読み取ります。空集合の場合はスイッチボタンを隠します。|
|`virtual void set_tracking_mode_set(const std::set<reference_object_type_t> &value)`|タイトルバーのトラッキングメニューのパターン集合を設定します。空集合の場合はスイッチボタンを隠します。|
|`virtual bool get_show_close_button() const`|タイトルバーの閉じるボタンを表示するかどうかを読み取ります。|
|`virtual void set_show_close_button(bool value)`|タイトルバーの閉じるボタンを表示するかどうかを設定します。|
|`virtual bool get_movable() const`|インタラクティブな移動と制御リングの回転を許可するかどうかを読み取ります。|
|`virtual void set_movable(bool value)`|インタラクティブな移動と回転の制御を許可するかどうかを設定します。|
|`virtual bool get_resizable() const`|論理サイズのインタラクティブな変更を許可するかどうかを読み取ります。|
|`virtual void set_resizable(bool value)`|論理サイズのインタラクティブな変更を許可するかどうかを設定します。|
|`virtual bool get_curvature_adjustable() const`|曲率のインタラクティブスイッチを読み取ります。デフォルトはtrueです。|
|`virtual void set_curvature_adjustable(bool value)`|左下角の曲率ボタンの表示とインタラクションを設定します。オフの状態では、現在の曲率のドラッグやスティック調整を即座にキャンセルし、再起動後にtriggerを離してから再調整を開始できます。|
|`virtual double get_physical_width() const`|展開幅を返します。単位はメートル：rect.width×physical_scale/1000。|
|`virtual double get_physical_height() const`|高さを返します。単位はメートル：rect.height×physical_scale/1000。|
|`~window() override`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`virtual void show()`|ウィンドウを表示します。最初の表示はloadをトリガーし、状態変化はshownをトリガーします。|
|`virtual void hide()`|ウィンドウを隠し、関連するキャプチャ、フォーカス、入力インターフェースを解放します。コントロールオブジェクトは再表示のために保持されます。|
|`virtual bool close(bool force = false)`|閉じる要求を送信します。成功した場合はtrueを返します。force=trueの場合は、閉じるキャンセルコールバックをスキップします。|
|`virtual void activate()`|このオブジェクトが属するウィンドウをアクティブにする；ウィンドウの再読み込みが自身をアクティブにする。|
|`virtual dialog_result_t show_dialog(window &owner_window)`|モーダルウィンドウの表示をブロックし、直接所有者を無効にしてUIイベントの配布を続けます。閉じた後、結果の列挙を返し、呼び出し側はウィンドウの属性を読み取ることができます。|
|`virtual bool get_loaded() const`|ウィンドウが最初にロードされたかどうかを読み取ります。|
|`virtual bool get_closed() const`|ウィンドウが閉じられたかどうかを読み取ります。|
|`virtual dialog_result_t get_dialog_result() const`|現在のモーダル結果を読み取ります。モーダル状態に入った場合はnoneにリセットされます。|
|`virtual void set_dialog_result(dialog_result_t value)`|モーダル結果を設定します。モーダル期間中、`none`以外の値は閉じる要求をします。閉じる要求がキャンセルされた場合は元の値に戻ります。|
|`void set_rect(const rectangle_t &value) override`|論理矩形を設定します。幅と高さは正の値でなければならず、設定後の物理幅は曲率の合法範囲を満たす必要があります。|
|`virtual void set_size(uint64_t width, uint64_t height)`|ウィンドウのrect.widthとrect.heightを設定します。単位は論理単位で、0より大きくなければなりません。|
|`virtual void reparent(const reference_object_t &reference, bool keep_world = false)`|world、body、head、left、rightの参照対象に変更します。keep_world=trueを入力した場合は、世界の姿勢を保持します。|
|`bool get_is_tracking_available(reference_object_type_t mode) const`|指定された参照モードが現在追跡可能かどうかを問い合わせます。|
|`virtual std::optional<pose_t> get_world_transform() const`|ウィンドウの中心の世界姿勢を返します。参照姿勢が使用できない場合はnulloptです。position属性で定義されたアンカーポイントは左上角にあり、両者は幅と高さの半分の差があります。|
|`virtual bool center_at_view(double distance)`|視線前方の指定されたメートル数でウィンドウを中央に配置します。追跡が可能で位置決めが成功した場合はtrueを返します。|
|`virtual bool get_auxiliary() const`|そのウィンドウが関連する入力領域の補助表面であるかどうかを問い合わせます。|
|`virtual void set_auxiliary(bool value)`|補助入力表面をマークします。実際の位置決めとスケーリングは、現在の入力領域に基づいてEngineが維持します。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`u32string title`|派生クラスがアクセス可能なウィンドウタイトルの文字、デフォルトはnameに等しい；通常の設定ではsetterを使用して変更通知を生成する。|
|`uint32_t title_foreground_color = render_style::SELECTED_TEXT_FOREGROUND_COLOR`|派生クラスがアクセス可能なウィンドウタイトルの前景色；通常の設定ではsetterを使用して変更通知を生成する。|
|`uint32_t title_background_color = render_style::WINDOW_TITLE_BACKGROUND_COLOR`|派生クラスがアクセス可能なウィンドウタイトルの背景色；通常の設定ではsetterを使用して変更通知を生成する。|
|`font_t title_font`|派生クラスがアクセス可能なウィンドウタイトルのフォント；通常の設定ではsetterを使用して変更通知を生成する。|
|`std::shared_ptr<const drawing_image> icon`|タイトルアイコン、デフォルトではネイティブアイコンを使用；派生クラスはset_iconを使用して描画を更新し、イベントをトリガーする。|
|`double physical_scale = render_style::DEFAULT_PHYSICAL_SCALE`|派生クラスがアクセス可能なスケーリング倍率；有限の正の数でなければならない；通常の設定ではsetterを使用して変更通知を生成する。|
|`double curvature = 0.0`|柱面の曲率、デフォルトは0.0、平面を表す。|
|`startup_position_t startup_position = startup_position_t::center`|初回表示の位置戦略、デフォルトはcenter。|
|`vec3_t position`|派生クラスがアクセス可能な相対参照対象の位置オフセット、単位はメートル；通常の設定ではsetterを使用して変更通知を生成する。|
|`vec3_t rotation`|派生クラスがアクセス可能な相対参照対象のXYZオールエル回転、単位は度；通常の設定ではsetterを使用して変更通知を生成する。|
|`reference_object_t reference_object`|派生クラスがアクセス可能な空間参照目標；通常の設定ではsetterを使用して変更通知を生成する。|
|`bool show_title_bar = true`|派生クラスがアクセス可能なウィンドウタイトルバーの表示有無；通常の設定ではsetterを使用して変更通知を生成する。|
|`std::set<reference_object_type_t> tracking_mode_set{reference_object_type_t::world, reference_object_type_t::body, reference_object_type_t::left, reference_object_type_t::right, reference_object_type_t::head}`|派生クラスがアクセス可能なタイトルバートラッキングメニューのパターン集合；空の集合はトラッキングボタンを隠す；通常の設定ではsetterを使用して変更通知を生成する。|
|`bool show_close_button = true`|派生クラスがアクセス可能なタイトルバー閉じるボタンの表示有無；通常の設定ではsetterを使用して変更通知を生成する。|
|`bool movable = true`|派生クラスがアクセス可能なインタラクティブな移動とコントロールリングの回転の許可有無；通常の設定ではsetterを使用して変更通知を生成する。|
|`bool resizable = true`|派生クラスがアクセス可能なロジックサイズのインタラクティブ変更の許可有無；通常の設定ではsetterを使用して変更通知を生成する。|
|`bool curvature_adjustable = true`|曲率のインタラクティブスイッチ；派生クラスはset_curvature_adjustableを使用して同期してキャプチャをキャンセルし、イベントをトリガーする。|
|`void refresh_layout() override`|コントロールのレイアウトを更新する、派生物がカバーする場合は必要なベースクラスの処理を保持する。|
|`void validate_control(const control &item) const override`|チェックウィンドウが受け取ることができる要素；同一ウィンドウは同時に1つのメニューバーに関連している。|
|`void notify_control_added(control &item, size_t index) override`|要素が実際に追加された後、menuの関連性を同期し、実際のインデックスに基づいてコンテナイベントを発行します。|
|`void notify_control_removed(control &item, size_t index) override`|要素が実際に削除された後、menuの関連性を同期し、元の実際のインデックスに基づいてコンテナイベントを発行します。|
|`void notify_control_list_cleared() override`|集合がクリアされた後、ウィンドウのmenuの関連性を同期します。|
|`virtual render_rectangle_t get_menu_rectangle() const`|現在のウィンドウ内のメニューバーの実際のロジック矩形を読み取ります。|
|`virtual void render_window_frame(render_context &context, bool spatial_handle) const`|ウィンドウのフレーム、タイトルを描画し、spatial_handleで制御される空間の操作ハンドルを操作します。|
|`std::optional<rectangle_t> get_managed_control_rectangle(const control &item, const rectangle_t &rectangle) const override`|メニューバーの下に矩形を配置します。通常のコントロールは自身の矩形を使用します。|
|`double get_content_top() const override`|本文の開始の論理的なtopオフセットを読取る。|
|`void render(render_context &context) const override`|contextを使用してコントロールの本文を描画する。派生物はカスタムの外観を実現するためにオーバーライドすることができる。|

参照対象はworld、body、head、left、rightの5種類です。tracking_mode_setでタイトルバーの選択可能な対象を設定します。world/bodyでは通常のウィンドウのキャプチャが実行できます。派生ウィンドウのレイアウトは、保護されたget_content_top()を使用してタイトルバー、メニュー、コントロールリングに適応できます。

### `easyvrui/dialog/dialog_result.h`

`dialog_result_t`は、モダンウィンドウと標準メッセージボックスが共有する結果の列挙です。メンバー`none/ok/cancel/abort/retry/ignore/yes/no`は順に`0`から`7`に対応します。

## カスタム描画

### `easyvrui/render/render_context.h`

カスタムコントロールが使用する描画とインタラクション状態のクエリインターフェース。

#### `render_rectangle_t`

声明。`struct render_rectangle_t`。

浮動小数点ロジック矩形で、left/top/width/heightはすべてdouble型で、デフォルトは0です。描画とカットオフに使用されます。

|宣言|用途と呼び出しの意味|
|---|---|
|`double left = 0.0`|矩形の左側の横座標。|
|`double top = 0.0`|矩形の上側の縦座標。|
|`double width = 0.0`|矩形の幅、単位は論理ピクセル。|
|`double height = 0.0`|矩形の高さ、単位は論理ピクセル。|

#### `render_context`

声明。`class render_context`。

カスタムコントロールのrender/render_overlayが受け取る抽象的な描画コンテキストです。矩形、座標、半径、線の太さはロジック単位を使用します。色は0xRRGGBBAAです。純粋な虚関数は具体的なコンテキストによって提供され、通常のコントロールは直接呼び出します。静的型呼び出し時、デフォルトパラメータはその型の宣言に従います。

|宣言|用途と呼び出しの意味|
|---|---|
|`virtual ~render_context() = default`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`virtual render_rectangle_t get_rectangle(const control &item) const = 0`|コントロールが現在のウィンドウ内で実行しているロジック描画矩形を取得します。|
|`virtual render_rectangle_t get_popup_rectangle(const item_control &item) const = 0`|項目コントロールのポップアップ領域の矩形を取得します。|
|`virtual bool is_hovered(const control &item) const = 0`|レーザーがコントロールまたは指定された矩形内にハイライトされているかを検索します。|
|`virtual bool is_hovered(const control &item, const render_rectangle_t &rectangle) const = 0`|レーザーがコントロールまたは指定された矩形内にハイライトされているかを検索します。|
|`virtual bool is_focused(const control &item) const = 0`|コントロールの視覚的フォーカスを検索する；入力ドレイン待ちの間はfalseになり、その場合でも論理的フォーカスは保持される可能性がある。|
|`virtual bool is_blinking() const = 0`|このフレームの挿入ポイントが表示周期内にあるかを検索する。|
|`virtual bool is_active(const window &item) const = 0`|ウィンドウが現在アクティブなウィンドウであるかを検索する。|
|`virtual bool is_blocked(const window &item) const = 0`|ウィンドウがモダンな関係によってブロックされているかを検索する。|
|`virtual bool is_close_button_hovered(const window &item) const = 0`|ウィンドウの閉じるボタンがホバー状態にあるかを検索する。|
|`virtual int64_t get_hovered_item(const item_control &item) const = 0`|レーザー指向の項目のインデックスを取得する；ヒットしない場合は-1となる。|
|`virtual double measure(const u32string &text, const font_t &font) = 0`|指定されたフォントでのUnicodeテキストの論理的な幅を測定する。|
|`virtual void fill(const render_rectangle_t &rectangle, uint32_t color) = 0`|colorで矩形を塗りつぶす；座標は論理単位である。|
|`virtual void outline(const render_rectangle_t &rectangle, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|矩形の輪郭を描画し、thicknessは正の線幅である。|
|`virtual void draw_line(double x1, double y1, double x2, double y2, uint32_t color, double thickness = render_style::FOCUSED_OUTLINE_THICKNESS) = 0`|(x1,y1)から(x2,y2)までの線を描画し、colorと正の線幅thicknessを使用する。|
|`virtual void draw_text(const u32string &value, const font_t &font, const render_rectangle_t &rectangle, uint32_t color, bool center = false) = 0`|指定された矩形内にテキストを描画する；centerがtrueの場合は中央に配置し、フォント、サイズ、スタイルは対応するパラメータで指定される。|
|`virtual void push_clip(const render_rectangle_t &rectangle) = 0`|矩形のクリップ範囲に圧入する；後の描画は現在のクリップ範囲によって制限される。|
|`virtual void pop_clip() = 0`|最近圧入されたクリップ範囲をポップする；push_clipと一緒に使用する必要がある。|
|`virtual void render_control_list(const window &item) = 0`|ウィンドウの現在の集合順序に従ってコントロールを描画する。|
|`virtual void render_overlay_list(const window &item) = 0`|ウィンドウ内のコントロールのフローテーションを描画する。|
|`virtual void fill_ellipse(double center_x, double center_y, double radius_x, double radius_y, uint32_t color) = 0`|(center_x,center_y)を中心に、半径がradius_x/radius_yの楕円を塗りつぶす。|
|`virtual void outline_ellipse(double center_x, double center_y, double radius_x, double radius_y, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|楕円の輪郭を描画する；半径と線幅は描画パラメータの制約を満たす必要がある。|
|`virtual void fill_rounded_rectangle(const render_rectangle_t &rectangle, double radius_x, double radius_y, uint32_t color) = 0`|矩形を塗りつぶし、radius_x/radius_yは丸みの半径を指定する。|
|`virtual void outline_rounded_rectangle(const render_rectangle_t &rectangle, double radius_x, double radius_y, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|丸みを帯びた矩形の輪郭を描画する。|
|`virtual void draw_image(const drawing_image &image, const render_rectangle_t &rectangle, double opacity = 1.0) = 0`|RGBA画像を目的の矩形にスケールして描画し、opacityの範囲は0から1までである。|
|`virtual void draw_screen(uint64_t screen_id, const render_rectangle_t &rectangle) = 0`|screen_idで指定されたリアルタイムディスプレイの画面を描画する。|
|`virtual void fill_path(const drawing_path &path, uint32_t color) = 0`|パスに沿った塗りつぶし規則に従ってパスを塗りつぶす。|
|`virtual void outline_path(const drawing_path &path, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS) = 0`|thicknessに従ってパスの輪郭を描画する。|
|`virtual void render_control(const control &item)`|指定されたコントロールの保護されたテキスト描画エントリを呼び出し、カスタム組み合わせ描画に使用する。|
|`virtual void render_control_overlay(const control &item)`|指定されたコントロールの保護されたフローテーション描画エントリを呼び出す。|
|`void fill_circle(double center_x, double center_y, double radius, uint32_t color)`|円を塗りつぶす；radiusは半径である。|
|`void draw_circle(double center_x, double center_y, double radius, uint32_t color, double thickness = render_style::NORMAL_OUTLINE_THICKNESS)`|円の輪郭を描画する；radiusは半径、thicknessは線幅である。|
|`static render_rectangle_t get_inset_rectangle(render_rectangle_t rectangle, double left_padding, double right_padding, double top_padding = 0.0, double bottom_padding = 0.0)`|指定された四辺の内側のピッチまたはコントロールと左右のピッチに従って内側に縮小した矩形を返す。|
|`render_rectangle_t get_inset_rectangle(const control &item, double left_padding, double right_padding) const`|指定された四辺の内側のピッチまたはコントロールと左右のピッチに従って内側に縮小した矩形を返す。|
|`void draw_control(const control &item, bool highlight = true)`|コントロールの背景とフレームを描画する；highlightはインタラクティブな強調表示を有効にするかどうかを制御する。|
|`uint32_t get_foreground(const text_control &item) const`|文字コントロールの現在の状態に適用される前景色を返す。|

### `drawing_image.h`

変更不可能なRGBA画像値。

#### `drawing_image`

声明。`class drawing_image`。

グローバル名前空間内の変更不可能な画像。width、height、RGBAバイト配列を受け取り、各ピクセル4バイトで行ごとに並べ、バイト数は幅と高さに一致する必要がある。getterを使用して各フィールドを読み取る。

|宣言|用途と呼び出しの意味|
|---|---|
|`drawing_image(uint64_t width, uint64_t height, std::vector<uint8_t> pixel_data)`|構造オブジェクト；パラメータ、デフォルト状態、制約はこのタイプの説明を参照してください。|
|`static std::shared_ptr<drawing_image> load_file(const std::filesystem::path &path)`|システムがサポートする画像ファイルを読み込み、ICOでは最大の画像フレームを選択する。|
|`static std::shared_ptr<drawing_image> load_memory(std::span<const uint8_t> data)`|完全にエンコードされた画像バイトから読み込む。|
|`static std::shared_ptr<drawing_image> load_ico(std::span<const uint8_t> data)`|ICOファイルヘッダをチェックし、メモリからアイコンを読み込む。|
|`std::vector<uint8_t> encode_ico() const`|無損失PNGエンコードを行い、単一のICOファイルに封入し、RGBAピクセルを保持する。幅と高さは1～256ピクセルである。|
|`uint64_t get_width() const`|画像ピクセルの幅を読み取る。|
|`uint64_t get_height() const`|画像ピクセルの高さを読み取る。|
|`const std::vector<uint8_t> &get_pixel_data() const`|RGBAピクセルバイト配列を読み取る。|

### `drawing_path.h`

パスフラグメント、フィルタリングルール、および連鎖的に構築可能な二次元パス。

#### `drawing_path_operation_t`

声明。`enum class drawing_path_operation_t : uint8_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`move = 0u`|起点に移動し、value_list[0..1]はx/yである。|
|`line = 1u`|直線で終点に移動し、value_list[0..1]はx/yである。|
|`quadratic = 2u`|二次曲線で、value_list[0..3]は制御点と終点である。|
|`cubic = 3u`|三次曲線で、value_list[0..5]は2つの制御点と終点である。|
|`arc = 4u`|楕円弧で、value_list[0..4]は終点x/y、半径x/y、回転角度であり、さらにclockwise/large_arcを使用する。|
|`close = 5u`|現在のサブパスを閉じる。|

#### `drawing_fill_rule_t`

声明。`enum class drawing_fill_rule_t : uint8_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`even_odd = 0u`|奇数と偶数フィルタリングルール。|
|`non_zero = 1u`|非ゼロの回転フィルタリングルール。|

#### `drawing_path_segment_t`

声明。`struct drawing_path_segment_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`drawing_path_operation_t operation = drawing_path_operation_t::move`|このパスフラグメントの操作タイプ。|
|`std::array<double, 6u> value_list{}`|パスフラグメントの座標とパラメータ配列、容量は6である。|
|`bool clockwise = true`|円弧が時計回りかどうか。|
|`bool large_arc = false`|円弧が半回転以上のパスを使用しているかどうか。|

value_listの実際の使用位置はoperationによって決定されます。move/lineは使用前に2項を使用し、quadraticは使用前に4項を使用し、cubicは6項を使用し、arcは使用前に5項を使用します。使用されていない項目はデフォルト値を保持します。

#### `drawing_path`

声明。`class drawing_path`。

グローバル名前空間内のパス構築器。move_to/line_to/曲線/arc_to/closeはすべてdrawing_path &を返し、連鎖呼び出しが可能です。デフォルトの充填規則はeven_oddです。clearはセグメントをクリアします。座標は有限でなければならず、半径は非負で、パスは有効な開始点から始まる必要があります。

|宣言|用途と呼び出しの意味|
|---|---|
|`drawing_path()`|このタイプのインスタンスを構築します。パラメータの意味はこのタイプの説明と署名を参照してください。|
|`const std::vector<drawing_path_segment_t> &get_segment_list() const`|パスセグメントの読み取りは読み取り専用リストです。|
|`drawing_fill_rule_t get_fill_rule() const`|パス充填規則の読み取り。|
|`void set_fill_rule(drawing_fill_rule_t value)`|パス充填規則の設定。|
|`void clear()`|パスセグメントをクリアし、現在の充填規則を保持します。|
|`drawing_path &move_to(double x, double y)`|(x,y)の新しいパス開始点に移動または開始し、現在のパス参照を返して連鎖呼び出しを行います。|
|`drawing_path &line_to(double x, double y)`|現在の点から直線を(x,y)に接続し、現在のパス参照を返します。|
|`drawing_path &quadratic_to(double control_x, double control_y, double end_x, double end_y)`|二次ベジェ曲線を追加し、controlは制御点、endは終点です。現在のパス参照を返します。|
|`drawing_path &cubic_to(double control1_x, double control1_y, double control2_x, double control2_y, double end_x, double end_y)`|三次ベジェ曲線を追加し、control1/control2は制御点、endは終点です。現在のパス参照を返します。|
|`drawing_path &arc_to(double end_x, double end_y, double radius_x, double radius_y, double rotation_degree = 0.0, bool clockwise = true, bool large_arc = false)`|(end_x,end_y)に接続する楕円弧を追加します。radiusは半径、rotation_degreeは角度、clockwiseとlarge_arcは弧の方向と大きさを選択します。|
|`drawing_path &close()`|現在のサブパスを閉じ、現在のdrawing_path参照を返します。|

### `easyvrui/render/render_style.h`

デフォルトの色、サイズ、線の太さ、およびレイアウトの定数。

#### `render_style`

声明。`class render_style`。

|宣言|用途と呼び出しの意味|
|---|---|
|`static constexpr uint32_t CONTROL_BACKGROUND_COLOR = 0x162738ffu`|通常のコントロールのデフォルト背景色。|
|`static constexpr uint32_t TEXT_FOREGROUND_COLOR = 0xd1def0ffu`|デフォルトのテキストの前景色。|
|`static constexpr uint32_t SELECTED_TEXT_FOREGROUND_COLOR = 0xffffffffu`|選択されたコンテンツのテキスト色。|
|`static constexpr uint32_t WINDOW_BACKGROUND_COLOR = 0x0d1624ffu`|ウィンドウのデフォルト背景色。|
|`static constexpr uint32_t WINDOW_TITLE_BACKGROUND_COLOR = 0x244565ffu`|ウィンドウのタイトルバーのデフォルト背景色。|
|`static constexpr uint32_t HOVER_OVERLAY_COLOR = 0x469eff55u`|ハイライトのオーバーレイ色。|
|`static constexpr uint32_t FOCUSED_OUTLINE_COLOR = 0x7bc9ffffu`|フォーカスのフレーム色。|
|`static constexpr uint32_t HOVERED_OUTLINE_COLOR = 0x63b4ffffu`|ハイライトのフレーム色。|
|`static constexpr uint32_t NORMAL_OUTLINE_COLOR = 0x45617dffu`|通常のフレーム色。|
|`static constexpr uint32_t SELECTED_ITEM_BACKGROUND_COLOR = 0x316b9affu`|選択された項目の背景色。|
|`static constexpr uint32_t HOVERED_ITEM_BACKGROUND_COLOR = 0x5eacff66u`|ハイライトされた項目の背景色。|
|`static constexpr uint32_t ITEM_LIST_OUTLINE_COLOR = 0x567a9cffu`|項目リストのプロファイル色。|
|`static constexpr uint32_t TEXT_SELECTION_BACKGROUND_COLOR = 0x3679bcddu`|テキスト選択範囲の背景色。|
|`static constexpr uint32_t CLOSE_BUTTON_HOVER_COLOR = 0xc84e64ffu`|閉じるボタンのハイライト色。|
|`static constexpr uint32_t WINDOW_OUTLINE_COLOR = 0x5f87a9ffu`|ウィンドウの輪郭色。|
|`static constexpr uint32_t BLOCKED_WINDOW_OVERLAY_COLOR = 0x00000088u`|モーダルブロックのマスク色。|
|`static constexpr uint32_t COLOR_RGB_MASK = 0xffffff00u`|高24位のRGBのビットマスクを抽出する。|
|`static constexpr uint32_t COLOR_ALPHA_MASK = 0x000000ffu`|低8位のAlphaのビットマスクを抽出する。|
|`static constexpr uint32_t DISABLED_ALPHA_DIVISOR = 2u`|無効状態の透明度の分母。|
|`static constexpr uint64_t DEFAULT_TAB_SIZE = 36u`|デフォルトのタブの幅。|
|`static constexpr uint64_t DEFAULT_ROW_HEIGHT = 32u`|デフォルトの項目の行の高さ。|
|`static constexpr uint64_t DEFAULT_WINDOW_WIDTH = 640u`|デフォルトのウィンドウの論理幅。|
|`static constexpr uint64_t DEFAULT_WINDOW_HEIGHT = 360u`|デフォルトのウィンドウの論理高さ。|
|`static constexpr uint64_t WINDOW_TITLE_FONT_SIZE = uint64_t{20u}`|デフォルトのタイトルの論理フォントサイズ。|
|`static constexpr double LOGICAL_PIXELS_PER_METER = 1000.0`|1倍の縮小時の1メートルあたりの論理ピクセル数。|
|`static constexpr double DEFAULT_PHYSICAL_SCALE = 1.0`|デフォルトのウィンドウの物理スケール倍率。|
|`static constexpr double NORMAL_OUTLINE_THICKNESS = 1.0`|通常の輪郭線の幅。|
|`static constexpr double FOCUSED_OUTLINE_THICKNESS = 2.0`|フォーカス輪郭線の幅。|
|`static constexpr double TEXT_HORIZONTAL_PADDING = 10.0`|テキストの水平内側のマージン。|
|`static constexpr double BUTTON_HORIZONTAL_PADDING = 6.0`|ボタンのテキストの水平内側のマージン。|
|`static constexpr double COMBOBOX_BUTTON_WIDTH = 48.0`|コンボボックスのドロップダウンボタンの幅。|
|`static constexpr uint64_t INPUT_BAR_HEIGHT = 48u`|補助入力バーの高さ。|
|`static constexpr uint64_t INPUT_BAR_MINIMUM_WIDTH = 480u`|補助入力バーの最小幅。|
|`static constexpr uint64_t INPUT_BAR_PADDING = 8u`|補助入力バーの内側のマージン。|
|`static constexpr uint64_t INPUT_BAR_COLUMN_GAP = 12u`|補助入力バーの列間隔。|
|`static constexpr uint64_t INPUT_BAR_FONT_SIZE = 20u`|補助入力バーのフォントサイズ。|
|`static constexpr uint64_t INPUT_BAR_SWITCH_MINIMUM_WIDTH = 144u`|入力法の切り替えボタンの最小幅。|
|`static constexpr double COMBOBOX_ARROW_CENTER_OFFSET = 24.0`|ドロップアレイアーの中心のオフセット。|
|`static constexpr double COMBOBOX_ARROW_HORIZONTAL_RADIUS = 8.0`|ドロップアレイアーの水平半径。|
|`static constexpr double COMBOBOX_ARROW_VERTICAL_RADIUS = 4.0`|ドロップアレイアーの垂直半径。|
|`static constexpr double COMBOBOX_ARROW_THICKNESS = 3.0`|ドロップアレイアーの線の幅。|
|`static constexpr double TEXTBOX_SCROLL_PADDING = 4.0`|テキストボックスのスクロール内側のマージン。|
|`static constexpr double TEXTBOX_SELECTION_VERTICAL_PADDING = 5.0`|テキストの選択範囲の垂直の余白。|
|`static constexpr double TEXTBOX_TEXT_TRAILING_PADDING = 2.0`|テキスト行の末尾の余白。|
|`static constexpr double TEXTBOX_CARET_VERTICAL_PADDING = 7.0`|挿入点の垂直の余白。|
|`static constexpr double TEXTBOX_CARET_THICKNESS = 2.0`|挿入点の線の幅。|
|`static constexpr double TEXTBOX_LINE_HEIGHT_RATIO = 1.4`|テキスト行の高さの相対フォントサイズの比率。|
|`static constexpr double SCROLLBAR_WIDTH = 12.0`|テキスト編集スクロールバーの幅。|
|`static constexpr double SCROLLBAR_MINIMUM_THUMB_SIZE = 18.0`|スクロールバーのスライダーの最小長さ。|
|`static constexpr uint32_t SCROLLBAR_TRACK_COLOR = 0x0d1624ffu`|スクロールバーのトラックの色。|
|`static constexpr uint32_t SCROLLBAR_THUMB_COLOR = 0x5f87a9ffu`|スクロールバーのスライダーの色。|
|`static constexpr double WINDOW_TITLE_HEIGHT = 48.0`|タイトルバーの論理高さ。|
|`static constexpr double WINDOW_TITLE_LEFT_PADDING = 16.0`|タイトルのテキストの左側の余白。|
|`static constexpr double WINDOW_TITLE_ICON_SIZE = 28.0`|タイトルバーのアイコンの辺の長さ。|
|`static constexpr double WINDOW_TITLE_ICON_GAP = 10.0`|タイトルアイコンとテキストの間隔。|
|`static constexpr double WINDOW_TITLE_RIGHT_PADDING = 56.0`|タイトルのテキストの右側の余白。|
|`static constexpr double WINDOW_CLOSE_BUTTON_WIDTH = 48.0`|閉じるボタンの幅。|
|`static constexpr double WINDOW_TRACKING_BUTTON_WIDTH = 48.0`|トラッキングの切り替えボタンの幅。|
|`static constexpr double WINDOW_TRACKING_POPUP_WIDTH = 160.0`|トラッキングの選択メニューの幅。|
|`static constexpr double WINDOW_TRACKING_ROW_HEIGHT = 32.0`|トラッキングの選択メニューの行の高さ。|
|`static constexpr double WINDOW_CLOSE_ICON_NEAR_OFFSET = 15.0`|閉じるアイコンの近い端のオフセット。|
|`static constexpr double WINDOW_CLOSE_ICON_FAR_OFFSET = 33.0`|閉じるアイコンの遠い端のオフセット。|
|`static constexpr double WINDOW_CLOSE_ICON_THICKNESS = 3.0`|閉じるアイコンの線の幅。|
|`static constexpr double WINDOW_RESIZE_OUTER_OFFSET = 6.0`|スケールアイコンの外側のオフセット。|
|`static constexpr double WINDOW_RESIZE_LONG_INNER_OFFSET = 22.0`|スケールアイコンの長い線の内側のオフセット。|
|`static constexpr double WINDOW_RESIZE_SHORT_INNER_OFFSET = 14.0`|スケールアイコンの短い線の内側のオフセット。|
|`static constexpr double WINDOW_OUTLINE_INSET = 1.0`|ウィンドウの輪郭の内側への縮小距離。|
|`static constexpr double WINDOW_OUTLINE_THICKNESS = 2.0`|ウィンドウの輪郭線の幅。|
|`static constexpr uint64_t POPUP_BOTTOM_MARGIN = 24u`|ポップアップメニューの下部のスペース。|
|`static constexpr uint64_t POPUP_MAXIMUM_VISIBLE_ITEM_COUNT = 8u`|ポップアップメニューに一度に表示できる最大項目数。|
|`static constexpr double WINDOW_RESIZE_HIT_SIZE = 30.0`|ウィンドウの縮小時の入力ヒット領域のサイズ。|
|`static uint32_t get_disabled_color(uint32_t color)`|透明度を下げるための無効化色の戻り値。|

## 入力コンポーネント

### `easyvrui/input/input_provider.h`

独立したlayoutとIMEアプリケーションの登録、入力、状態、およびドレインのインターフェース。

#### `input_role_t`

声明。`enum class input_role_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`layout`|仮想キーボードのキーを生成するレイアウトプログラム。|
|`ime`|キーを処理し、未使用のイベントを転送し、最終的な文字を送信する入力法プログラム。|

#### `input_provider_state_t`

声明。`enum class input_provider_state_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`stopped`|現在実行していない。|
|`starting`|起動が開始され、登録を待っている。|
|`running`|登録され、実行状態にある。|

#### `provider_info_t`

声明。`struct provider_info_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`uint64_t id = 0u`|入力コンポーネントの番号。|
|`std::u32string name`|コンポーネントの表示名。UTF-32を使用します。|
|`std::u32string language = U"en"`|IMEの言語コード、一般的にはzh/en/ja；他の言語コードもサポート。layoutは記録されたデフォルト値を使用し、プロトコル内のlayout項目からlanguageを省略する。|
|`input_role_t role = input_role_t::ime`|layoutまたはIMEのロール。|
|`input_provider_state_t state = input_provider_state_t::stopped`|コンポーネントのstopped、starting、またはrunning状態。|
|`bool configured = false`|エンジンの固定設定からのかどうか。|
|`bool active = false`|コンポーネントがクエリセッションの対応するロールの現在の選択されたアクティブ項目かどうか；入力パスがinput_ui_state_t::activeで表示されるかどうか。|
|`bool default_provider = false`|そのIMEが持続的なデフォルト項目かどうか。|
|`uint32_t process_id = 0u`|コンポーネントのプロセス番号。|
|`std::string error`|コンポーネントの最近のエラー説明。|
|`bool operator==(const provider_info_t &other) const = default`|対応するメンバー値を比較して等しいかどうかを返し、boolを返します。|

#### `input_ui_state_t`

声明。`struct input_ui_state_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`bool active = false`|コンポーネントが現在選択されているか、または入力エリアがアクティブ状態にあるかどうか。|
|`bool physical = false`|現在物理キーボードモードかどうか。|
|`std::optional<render_rectangle_t> rectangle`|ウィンドウ内の入力エリアの論理矩形；関連する入力エリアがない場合はnullopt。|

#### `input_event_type_t`

|列挙値|意味|
|---|---|
|`unknown`|識別できないイベント。|
|`key_down`|キーの押下または繰り返し。|
|`key_up`|キーの解放。|
|`ime_submit`|IMEが最終文字を送信する。|

#### `input_event_t`

声明。`struct input_event_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`std::string event_type`|イベント名、例えばkey_downやkey_upなど。|
|`std::u32string key`|論理的なキー名。|
|`std::u32string text`|表示される文字やIMEによる入力文字、UTF-32を使用。|
|`bool shift = false`|Shiftキーが押されているかどうか。|
|`bool ctrl = false`|Ctrlキーが押されているかどうか。|
|`bool alt = false`|Altキーが押されているかどうか。|
|`bool meta = false`|Windows/Metaキーが押されているかどうか。|
|`bool handled = false`|コンポーネントが現在のキーを処理しているかどうか；IMEは未処理のキーを引き続き転送することができる。|
|`input_event_type_t get_type() const`|`event_type`をイベントの列挙として解釈し、識別できない場合は`unknown`を返す。|

#### `input_provider`

声明。`class input_provider`。

独立したlayout/IMEアプリケーション用。登録後、セッションはコンポーネントのロールに固定され、コンポーネントは補助面でインターフェースを表示する。IMEはキーを処理し、`commit_text`を呼び出して文字を送信する。layoutは仮想キーを送信する。通常のアプリケーションは、入力法の切り替えダイアログで選択されたIMEをデフォルト設定にすることができる。入力エリアの状態はget_stateとon_state_changedによって提供される。非同期タスクはbegin_input_task/finish_input_taskのペアでなければならず、ドレインにはこれらのタスクと発送予定の出力が含まれる。

on_inputのコールバックの署名はvoid(input_provider &source, input_event_t &event)である。process_inputとon_inputが実行された後、event.handledがまだfalseのキーは自動的に転送される；キーを処理するときはhandledをtrueに設定する。同じキーをsend_eventで自分で転送する場合も、重複を避けるためにhandled=trueに設定する必要がある。IMEが文字を送信した後は通常、対応するキーを処理する。登録は非同期プロセスであり、runまたはメッセージループを通じて登録応答を続行する；同じスレッドには現在の入力コンポーネントが1つだけ許可され、登録後はロールが固定される。

|宣言|用途と呼び出しの意味|
|---|---|
|`event_signal<input_provider, input_ui_state_t> on_state_changed`|入力コンポーネントの活動的な入力エリア、モード、または矩形の状態が変わったときにトリガーされる。|
|`event_signal<input_provider, input_event_t> on_input`|入力コンポーネントがキーまたは文字イベントを受け取ったときにトリガーされる；処理可能または転送可能。|
|`input_provider()`|入力コンポーネントのインスタンスを作成する。|
|`virtual ~input_provider()`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`input_provider(const input_provider &) = delete`|複製または代入を禁止する；オブジェクトはその元のインスタンスとライフサイクルによって管理される。|
|`input_provider &operator=(const input_provider &) = delete`|複製または代入を禁止する；オブジェクトはその元のインスタンスとライフサイクルによって管理される。|
|`const input_ui_state_t &get_state() const`|入力インターフェースの状態を読み取る。|
|`input_role_t get_role() const`|入力コンポーネントのロールを読み取る。|
|`bool get_draining() const`|入力コンポーネントがドレインされているかを読み取ります。|
|`bool get_connected() const`|現在の入力コンポーネントの接続状態を読み取ります。|
|`uint64_t get_session_id() const`|現在の入力コンポーネントのセッション番号を読み取ります。接続されていない場合は0を返します。|
|`const std::vector<provider_info_t> &get_provider_list() const`|既知の入力コンポーネントのリストを読み取ります。|
|`void register_provider(input_role_t role = input_role_t::ime, bool default_provider = false, const std::u32string &name = U"", const std::u32string &language = U"en")`|現在の独立プログラムをlayoutまたはIMEとして登録します。default_providerはデフォルトの選択肢を表し、nameは表示名です。languageはIMEにのみ使用され、空でないコードでなければなりません。省略された場合はenです。一つのセッションロールは固定であり、排他的です。|
|`void begin_input_task()`|未完了の非同期入力タスクを登録します。ドレイン完了の確認を遅らせるために使用されます。|
|`void finish_input_task()`|begin_input_taskの登録を一度完了します。各登録は一度の完了に対応します。|
|`void send_event(const input_event_t &event)`|コンポーネントの出力としてキーボードイベントを送信します。|
|`void commit_text(const std::u32string &text)`|IMEに最終文字を提出し、エンジンによって現在の入力ウィンドウに転送します。|
|`void run()`|入力コンポーネントのイベントループを実行します。登録されていない場合はデフォルトのIMEロールで登録を開始し、登録に成功しないかコンポーネントがログアウトした後に返します。|

##### 派生拡張メンバー（protected）

以下のメンバーは派生クラスが使用します；通常のアプリケーションは上記のpublicインターフェースを通じてオブジェクトを操作します。

|宣言|用途と呼び出しの意味|
|---|---|
|`virtual void process_state(input_ui_state_t &state)`|コンポーネントの入力エリアの状態を処理し、派生クラスが拡張するためのものです。|
|`virtual void process_input(input_event_t &event)`|IMEが受け取ったキーを処理します。派生クラスはイベントを変更したり、handledを設定したりし、その後on_inputイベントチェーンを呼び出します。|
|`virtual void process_drain()`|入力をドレインする準備をします。派生実装は非同期タスクを完了し、古いパスからの出力を停止する必要があります。|

## 文字と環境ツール

### `easyvrui/common/u32string_hash.h`

u32string_viewクエリをサポートする透明なハッシュエンジンです。

#### `u32string_hash`

声明。`class u32string_hash`。

|宣言|用途と呼び出しの意味|
|---|---|
|`using is_transparent = void`|透明なハッシュマークにより、ハッシュコンテナが異なる文字列ビュータイプのクエリをサポートします。|
|`size_t operator()(u32string_view value) const noexcept`|Unicode文字列ビューのsize_tハッシュ値を計算し、例外を発生させないようにします。|

## エラーと言語

### `easyvrui/common/error_diagnostic.h`

ソースコードの位置、条件式、および単行エラーディアグノスティクスです。

#### 自由関数とタイプ別名

|宣言|用途と戻り値|
|---|---|
|`error_diagnostic get_error_diagnostic(const std::exception &error, const std::source_location &location = std::source_location::current())`|例外から既存の診断を取得します。例外に診断がない場合は、呼び出し位置から構築します。|
|`std::string get_error_message(const std::exception &error, const std::source_location &location = std::source_location::current())`|単行の、ソースコードの位置を含む例外診断テキストを返します。|

#### `error_diagnostic`

声明。`class error_diagnostic`。

診断値の記録ファイル、行列、関数、条件；source_locationはデフォルトでインターフェース呼び出し位置をキャプチャします。get_messageはVSCodeが認識できる診断形式の単行式を出力します。

|宣言|用途と呼び出しの意味|
|---|---|
|`explicit error_diagnostic(const std::source_location &location = std::source_location::current(), std::string_view condition = {})`|このタイプのインスタンスを構築します。パラメータの意味はこのタイプの説明と署名を参照してください。|
|`error_diagnostic(std::string file, uint64_t line, uint64_t column, std::string function, std::string condition)`|このタイプのインスタンスを構築します。パラメータの意味はこのタイプの説明と署名を参照してください。|
|`virtual ~error_diagnostic()`|オブジェクトをデストラクタして、そのリソースや参照のライフサイクルを終了します。|
|`const std::string &get_file() const`|診断ソースファイル名を読み取ります。|
|`uint64_t get_line() const`|診断行番号を読み取ります。|
|`uint64_t get_column() const`|診断列番号を読み取ります。|
|`const std::string &get_function() const`|診断関数名を読み取ります。|
|`const std::string &get_condition() const`|失敗条件式を読み取ります。|
|`std::string get_message(std::string_view key = {}, std::string_view detail = {}) const`|file:line:column: error: condition [key] detail形式の単行文字を返します。|

### `easyvrui/common/error.h`

コントロールと描画エラーのキー、構造的エラー、アサスペル式条件チェック。

#### 自由関数とタイプ別名

|宣言|用途と戻り値|
|---|---|
|`string_view get_language_key(error_key_t key)`|エラーを言語キーに変換します。|

#### `error_key_t`

声明。`enum class error_key_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`unknown`|未知のエラー。|
|`owning_thread_required`|begin_invoke()を使用してワークスレッドからコントロールにアクセスしてください。|
|`callable_required`|フィールドには呼び出し可能なオブジェクトが必要です。|
|`candidate_string_sequence`|候補は文字列シーケンスでなければなりません。|
|`candidate_index_invalid`|候補インデックスは整数でなければなりません。|
|`operation_failed`|UIサービスの操作が失敗しました。|
|`service_disconnected`|UIサービスの接続が切断されました。|
|`service_request_timeout`|UIサービスの要求がタイムアウトしました。|
|`number_required`|フィールドは数値でなければなりません。|
|`finite_number_required`|フィールドは有限の数値でなければなりません。|
|`unsigned_integer_required`|フィールドは符号付き整数でなければなりません。|
|`three_component_required`|フィールドには3つの成分が必要です。|
|`name_invalid`|名前は空でない文字列でなければなりません。|
|`duplicate_property`|属性が重複しています：指定値。|
|`unknown_property`|未知の属性：指定値。|
|`property_type_mismatch`|属性のタイプが一致しません：指定値。|
|`duplicate_control_name`|コントロール名が重複しています：指定値。|
|`duplicate_tabpage_name`|タブページ名が重複しています：指定値。|
|`event_data_object_required`|イベントデータはオブジェクトでなければなりません。|
|`object_disposed`|オブジェクトが解放されました。|
|`window_activation_failed`|ウィンドウがアクティブになりません。|
|`control_focus_failed`|コントロールがフォーカスを取得できません。|
|`client_mismatch`|コントロールは異なるUI実行環境に属しています。|
|`control_has_parent`|コントロールは既に何らかのコンテナに属しています。|
|`cyclic_control_hierarchy`|コントロールは自身またはその祖先コントロールを含むことができません。|
|`cyclic_reference_object`|ウィンドウの参照対象は循環してはならない。|
|`cyclic_json_container`|JSONコンテナには自身またはその祖先を含んではならない。|
|`control_not_in_container`|コントロールはこのコンテナに属していない。|
|`item_not_in_collection`|オプションはこの集合に属していない。|
|`item_index_out_of_range`|オプションのインデックスは範囲を超えている。|
|`selected_item_index_out_of_range`|選択されたオプションのインデックスは範囲を超えている。|
|`selected_tab_index_out_of_range`|選択されたタブのインデックスは範囲を超えている。|
|`positive_rect_required`|コントロールの幅と高さは正の数でなければならない。|
|`positive_row_height_required`|行の高さはゼロを超えていなければならない。|
|`positive_tab_size_required`|タブのサイズはゼロを超えていなければならない。|
|`font_family_invalid`|フォント名は空でないこと、またはNULを含まないこと。|
|`font_size_invalid`|フォントのサイズは正の整数でなければならない。|
|`title_font_family_invalid`|タイトルのフォント名は有効でない。|
|`title_font_size_invalid`|タイトルのサイズはゼロを超えていなければならない。|
|`tab_font_family_invalid`|タブのフォント名は有効でない。|
|`tab_font_size_invalid`|タブのサイズはゼロを超えていなければならない。|
|`physical_scale_invalid`|physical_scaleは有限の正の倍率でなければならない。|
|`curvature_invalid`|曲率は非負でなければならず、ウィンドウの総弧度は1回転を超えてはならない。|
|`position_invalid`|位置は有限の数値でなければならない。|
|`rotation_invalid`|回転は有限の数値でなければならない。|
|`combobox_item_required`|テキストはコンボボックス内の利用可能なオプションと一致しなければならない。|
|`invalid_dialog_owner`|ダイアログボックスの所有者はインタラクティブなウィンドウでなければならない。|
|`invalid_reference_object_type`|参照対象のタイプは有効でない。|
|`reference_not_tracked`|ウィンドウの参照対象は現在追跡されていない。|
|`unknown_reference_object`|未知のウィンドウ参照対象。|
|`invalid_reference_owner`|参照は現在のUI実行環境で閉じていないウィンドウを指し示さなければならない。|
|`control_required`|controlインスタンスが必要です。|
|`tabpage_required`|tabpageインスタンスが必要です。|
|`page_list_required`|get_page_list()を使用してタブを管理してください。|
|`invalid_rotation`|回転値は有効でない。|
|`zero_direction`|方向ベクトルはゼロではありません。|
|`invalid_utf8_leading_byte`|UTF-8の開始バイトは有効でない。|
|`invalid_utf8_continuation_byte`|UTF-8の後続バイトは有効でない。|
|`truncated_utf8`|UTF-8のシーケンスは不完全です。|
|`overlong_utf8`|UTF-8のシーケンスには超長いエンコーディングが存在します。|
|`invalid_utf8_scalar`|UTF-8の文字値は範囲を超えています。|
|`invalid_utf32_scalar`|UTF-32の文字値は範囲を超えています。|
|`truncated_utf16_surrogate`|UTF-16のエージェントペアは不完全です。|
|`invalid_utf16_surrogate`|UTF-16のエージェントペアは有効でない。|
|`invalid_utf16_low_surrogate`|UTF-16の低い位のエージェント項目は有効でない。|
|`event_handler_null`|イベント処理関数は空でない必要があります。|
|`window_render_failed`|ウィンドウのレンダリングに失敗しました。|
|`service_stopped`|サービスが停止しました。|
|`window_closing`|ウィンドウが閉じられています。|
|`window_closed`|ウィンドウが閉じられました。|
|`invalid_drawing_coordinate`|描画座標は有限の数値でなければなりません。|
|`invalid_drawing_radius`|描画半径は有限の非負の値でなければなりません。|
|`invalid_drawing_thickness`|線の太さは有限の正の値でなければなりません。|
|`invalid_drawing_opacity`|描画の透明度は0から1の間の有限の値でなければなりません。|
|`invalid_drawing_rectangle`|描画の矩形の幅と高さは非負の値でなければなりません。|
|`invalid_drawing_image`|描画の画像サイズは正で、RGBA8バイト数と一致していなければなりません。|
|`drawing_image_size_overflow`|描画の画像のバイト数が整数またはアドレス可能なサイズ範囲を超えています。|
|`invalid_drawing_path`|描画のパス充填規則、線分の値、または図形の順序が有効ではありません。|
|`invalid_input_provider_role`|入力プロバイダーのロールはlayoutまたはimeでなければなりません。|
|`language_pack_unavailable`|言語パックが利用できません：指定値。|
|`language_pack_object_required`|言語パックはオブジェクトでなければなりません：指定値。|
|`language_value_text_required`|言語値はテキストでなければなりません：指定値。|
|`language_key_unavailable`|言語キーが利用できません：指定値。|
|`invalid_base64`|有効でない標準的なBase64エンコーディング。|
|`base64_size_overflow`|Base64データがコンテナのアドレス可能なサイズを超えています。|
|`desktop_open_failed`|デスクトップアプリケーションを呼び出すことができません：指定値。|
|`grid_value_required`|セル値は空でなければなりません。|
|`grid_boolean_required`|セル値はtrueまたはfalseでなければなりません。|
|`grid_integer_required`|セル値は64の符号付き整数でなければなりません。|
|`grid_finite_number_required`|セル値は有限の浮動小数点数でなければなりません。|
|`grid_cell_type_mismatch`|セル値は元のタイプを保持しなければなりません。|
|`grid_provider_read_only`|セルデータプロバイダーは読み取り専用です。|
|`grid_value_rejected`|セル値が拒否されました。|
|`grid_value_type_required`|セル値はテキスト、64の符号付き整数、有限の浮動小数点数、またはブール値でなければなりません。|
|`grid_write_result_invalid`|セルへの書き込みコールバックはbool、None、エラーテキスト、または(bool, エラーテキスト)を返さなければなりません。|
|`process_launch_failed`|アプリケーションの起動に失敗し、診断情報にはWindowsのエラーコードが含まれています。|

#### `engine_error`

声明。`class engine_error : public error_diagnostic, public runtime_error`。

コントロールと描画に異常があり、error_diagnosticとstd::runtime_errorを同時に継承しています；get_keyはerror_key_tを返し、what()は単行の診断を返します。

|宣言|用途と呼び出しの意味|
|---|---|
|`engine_error(error_key_t key, vector<string> argument_list = {}, const source_location &location = source_location::current(), string_view condition = {})`|keyを押すと異常が発生し、argument_listはローカライズされた説明に代入されます；locationはデフォルトで呼び出し位置をキャプチャし、conditionは失敗条件を保存します。|
|`error_key_t get_key() const`|構造化されたエラーキーを読み取ります。|
|`const vector<string> &get_argument_list() const`|エラーのフォーマットパラメータを読み取ります。|

### `easyvrui/localization/error.h`

接続層のエラーキーとローカライズされた異常を接続します。

#### 自由関数とタイプ別名

|宣言|用途と戻り値|
|---|---|
|`using localized_invalid_argument = localized_exception<invalid_argument>`|`localized_exception<invalid_argument>`別名。|
|`using localized_runtime_error = localized_exception<runtime_error>`|`localized_exception<runtime_error>`別名。|
|`string_view get_language_key(language_key_t key)`|エラーを言語キーに変換します。|
|`string get_localized_error(language_key_t key, const vector<string> &argument_list = {})`|language_key_tとargument_listに基づいてローカライズされたエラーテキストを生成します。|
|`void select_error_language(const string &language)`|接続エラーの言語を選択します。|
|`string get_error_language()`|現在の接続エラー言語コードを返します。|

#### `language_key_t`

声明。`enum class language_key_t`。

|宣言|用途と呼び出しの意味|
|---|---|
|`unknown`|未分類のエラー。|
|`service_disconnected`|サービス接続が切断されました。|
|`operation_failed`|操作に失敗しました。|
|`invalid_utf32_scalar`|UTF-32に不正なUnicodeスカラが含まれています。|
|`winsock_initialization_failed`|ネットワーク運用環境の初期化に失敗しました。|
|`service_connection_failed`|サービスへの接続に失敗しました。|
|`invalid_frame_length`|受信フレームの長さが有効ではありません。|
|`json_object_required`|メッセージはJSONオブジェクトでなければなりません。|
|`invalid_outgoing_frame_size`|送信フレームのサイズが有効ではありません。|
|`socket_wait_failed`|ソケットの待ち受けに失敗しました。|
|`accepted_connection_configuration_failed`|接続設定に失敗しました。|
|`service_connection_cancelled`|接続操作がキャンセルされました。|
|`service_identity_mismatch`|サービスアイデンティティまたは起動パラメータが一致しません。|
|`tls_operation_failed`|TLS操作に失敗しました。|
|`authentication_failed`|アクセス認証に失敗しました。|
|`invalid_session`|セッションが無効です。|
|`heartbeat_timeout`|ハートビートタイムアウトしました。|
|`remote_service_unavailable`|リモートサービスが利用できません。|
|`service_startup_timeout`|サービスの起動タイムアウトしました。|
|`executable_location_failed`|実行ファイルの位置を検索するに失敗しました。|
|`native_service_required`|ネイティブサービスプログラムが必要です。|
|`native_service_start_failed`|ネイティブサービスの起動に失敗しました。|

#### `localized_exception<base_type>`

声明。`class localized_exception : public error_diagnostic, public base_type`。

テンプレートエラーで、error_diagnosticとbase_typeを同時に継承します。localized_invalid_argumentはlocalized_runtime_errorに対応し、invalid_argumentとruntime_errorに対応します。get_language_key()メンバーはlanguage_key_tの列挙を返します。

|宣言|用途と呼び出しの意味|
|---|---|
|`localized_exception(language_key_t key, vector<string> argument_list = {}, const source_location &location = source_location::current(), string_view expression = {})`|接続エラーのkeyとargument_listに基づいてローカライズされたエラーを生成します。locationは呼び出し位置を記録し、expressionは失敗条件を保存します。|
|`language_key_t get_language_key() const`|このエラーのエラーハンドル列挙を返します。|
|`const vector<string> &get_argument_list() const`|エラーのフォーマットパラメータを読み取ります。|

### `easyvrui/localization/request_error.h`

リモートリクエストに失敗したエラータイプ。

#### `request_error`

声明。`class request_error : public error_diagnostic, public std::runtime_error`。

リクエスト失敗エラーが発生し、std::runtime_error::what()およびerror_diagnosticのソース位置インターフェースを提供します。language_keyとargument_listには、サービスが提供するエラー情報が保持されます。

|宣言|用途と呼び出しの意味|
|---|---|
|`request_error(std::string language_key, std::string message, std::vector<std::string> argument_list, error_diagnostic diagnostic)`|UTF-8言語キー、サービスエラー説明、フォーマットされたパラメータ、および既存のソースコード診断からリクエストエラーを構築します。|
|`const std::string &get_language_key() const`|このエラーのエラーキー文字列を返します。|
|`const std::vector<std::string> &get_argument_list() const`|エラーのフォーマットパラメータを読み取ります。|

### `easyvrui/localization/language_pack.h`

インターフェース言語の選択と言語テキストの検索。

#### `language_pack`

声明。`class language_pack`。

`get_current()`でSDKの現在の言語パッケージを取得します。内蔵文字は静的ライブラリおよびDLLに組み込まれ、デフォルトではシステム言語に基づいて選択されます。`load_directory(path)`では、指定されたディレクトリからカスタム言語パッケージを明示的にロードでき、`en.json`では基本文字を提供します。

|宣言|用途と呼び出しの意味|
|---|---|
|`static language_pack &get_current()`|SDKが管理する現在の言語パッケージを返します。|
|`void select_language(const std::u32string &language)`|インターフェース言語を選択し、zh、ja、enおよびその地域形式を統一します。|
|`std::string get_code() const`|現在の言語コードを読み取ります。|
|`static std::unique_ptr<language_pack> load_directory(const std::filesystem::path &path)`|指定されたディレクトリの言語パッケージを読み込みます。|
|`std::vector<std::u32string> get_available_locale_list() const`|ディレクトリ内の言語コードを読み取ります。|
|`std::vector<std::u32string> get_key_list() const`|現在の言語パッケージのキーをリストアップします。|
|`size_t get_size() const`|言語キーの数を読み取ります。|
|`std::optional<std::u32string> find_text(const std::u32string &key) const`|キーを押して翻訳テキストを検索し、不足の場合は空値を返します。|
|`std::u32string get_text(const std::u32string &key) const`|Unicode言語キーを押して翻訳テキストを返します。キーが存在しない場合は、キー自体を返します。|
|`std::string get_message(const std::string &key, const std::vector<std::string> &argument_list) const`|UTF-8言語キーを読み取り、{0}、{1}などのプレースホルダをUTF-8パラメータに代入し、UTF-8説明を返します。|

## 一般的な入力と検証

### `easyvrui/common/keyboard_key.h`

特殊キーの列挙とテキストキーナンバーの解析。`keyboard_key_t`には`unknown`、`backquote`、`backspace`、`tab`、`enter`、`escape`、`space`、方向キー`left/right/up/down`、`home/end/page_up/page_down/insert/delete_key`、`caps_lock/num_lock/scroll_lock/menu/pause`、`f1`から`f24`、および`control/shift/alt/meta`の各々の一般的な、左側、右側の列挙項目が含まれます。例えば`control/left_control/right_control`です。

|宣言|用途と戻り値|
|---|---|
|`keyboard_key_t parse_keyboard_key(std::string_view text)`|UTF-8特殊キーナンバーを解析し、識別できない場合はunknownを返します。|
|`keyboard_key_t parse_keyboard_key(std::u32string_view text)`|UTF-32特殊キーナンバーを解析し、識別できない場合はunknownを返します。|

キーナンバーは大文字と小文字でマッチし、`Ctrl/Control`、`Enter/Return`、`Meta/Win`およびそれに応じた左右の修飾キー別名をサポートします。通常の文字はイベントのkey/textで読み取ります。unknownは特殊キーにマッチしないことを示します。

#### `keyboard_modifier_t`

声明。`struct keyboard_modifier_t`。

キー変更状態、ctrl、shift、alt、metaはデフォルトでfalseです。

|宣言|用途と呼び出しの意味|
|---|---|
|`bool ctrl = false`|Control修飾キーの状態、デフォルトでfalseです。|
|`bool shift = false`|Shift修飾キーの状態、デフォルトでfalseです。|
|`bool alt = false`|Alt修飾キーの状態、デフォルトでfalseです。|
|`bool meta = false`|Windows/Meta修飾キーの状態、デフォルトでfalseです。|

#### `keyboard_key_t`

声明。`enum class keyboard_key_t`。

特殊キーの列挙型です。parse_keyboard_keyはUTF-8またはUTF-32のキー名を受け取ります。認識できない名前にはunknownを返します。

|宣言|用途と呼び出しの意味|
|---|---|
|`unknown`|認識できない特殊キー。|
|`backquote`|`backquote`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`backspace`|`backspace`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`tab`|`tab`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`enter`|`enter`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`control`|`control`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`left_control`|`left_control`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`right_control`|`right_control`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`shift`|`shift`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`left_shift`|`left_shift`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`right_shift`|`right_shift`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`alt`|`alt`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`left_alt`|`left_alt`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`right_alt`|`right_alt`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`meta`|`meta`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`left_meta`|`left_meta`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`right_meta`|`right_meta`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`pause`|`pause`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`escape`|`escape`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`space`|`space`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`left`|`left`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`right`|`right`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`up`|`up`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`down`|`down`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`home`|`home`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`end`|`end`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`page_up`|`page_up`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`page_down`|`page_down`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`insert`|`insert`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`delete_key`|`delete_key`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`caps_lock`|`caps_lock`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`num_lock`|`num_lock`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`scroll_lock`|`scroll_lock`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`menu`|`menu`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f1`|`f1`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f2`|`f2`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f3`|`f3`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f4`|`f4`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f5`|`f5`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f6`|`f6`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f7`|`f7`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f8`|`f8`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f9`|`f9`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f10`|`f10`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f11`|`f11`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f12`|`f12`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f13`|`f13`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f14`|`f14`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f15`|`f15`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f16`|`f16`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f17`|`f17`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f18`|`f18`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f19`|`f19`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f20`|`f20`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f21`|`f21`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f22`|`f22`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f23`|`f23`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|
|`f24`|`f24`特殊キー；文字列名前はparse_keyboard_keyによって解析されます。|

## リンクマクロ

### `engine_interface_api.h`

静的ライブラリとDLLの宣言マクロは、ビルド設定によってリンク形式で設定されます。

|マクロまたはコンパイル定義|用途|
|---|---|
|`ENGINE_INTERFACE_BUILD`|DLLをビルドする際に、ENGINE_INTERFACE_APIを__declspec(dllexport)で展開します。|
|`ENGINE_INTERFACE_STATIC`|静的ライブラリとその呼び出し側が使用し、ENGINE_INTERFACE_APIは空に展開されます。|
|`ENGINE_INTERFACE_API`|前述のビルドマクロが定義されていない場合は__declspec(dllimport)に展開され、DLLのインポートインターフェースが宣言されます。|

## 標準ダイアログボックス

以下の関数は呼び出しが完了した時点で結果を返し、待機中はインターフェースの活動を継続的に処理します。ownerは直接の親ウィンドウを指定します。モーダル状態中はその親ウィンドウを無効にし、他のウィンドウは相互作用を続けます。ダイアログはWorldとcenterの位置を採用し、親ウィンドウのphysical_scaleを継承します。

### 色とフォント

|ヘッダーファイル|関数|結果|
|---|---|---|
|`easyvrui/dialog/color_dialog.h`|`std::optional<uint32_t> color_dialog(uint32_t color = 0x000000ffu, const std::u32string &title = U"", uint32_t default_color = 0x000000ffu, window *owner = nullptr)`|確定すると`0xRRGGBBAA`を返し、キャンセルすると`std::nullopt`を返します。|
|`easyvrui/dialog/font_dialog.h`|`std::optional<font_t> font_dialog(const font_t &font = font_t{}, const std::u32string &title = U"", const font_t &default_font = font_t{}, window *owner = nullptr)`|確定するとシステムフォントを返し、キャンセルすると`std::nullopt`を返します。|

色インターフェースには色域、色相、透明度、RGB／HSV入力が含まれます。フォントインターフェースにはシステムフォント、数字のサイズ、太字、斜体、およびプレビューが提供されます。default_colorとdefault_fontはデフォルトの値のボタンの復元目標を指定します。

### メッセージボックスと入力ボックス

`easyvrui/dialog/messagebox.h`には2つの重载が提供されます：

```cpp
dialog_result_t messagebox(const std::u32string &message, const std::u32string &title = U"", messagebox_button_set_t button_set = messagebox_button_set_t::ok, messagebox_icon_t icon = messagebox_icon_t::none, dialog_result_t default_button = dialog_result_t::none, window *owner = nullptr);
std::u32string messagebox(const std::u32string &message, const std::u32string &title, const std::vector<messagebox_button_t> &button_list, messagebox_icon_t icon = messagebox_icon_t::none, const std::u32string &default_button_name = U"", window *owner = nullptr);
```

`messagebox_button_t`はnameとtextを保存します。標準の重载は`dialog_result_t`を返し、カスタムボタンの重载は選択されたボタンのnameを返します。

|列挙型|メンバーと数値|
|---|---|
|`messagebox_icon_t`|`none=0`、`error=0x10`、`question=0x20`、`warning=0x30`、`information=0x40`|
|`messagebox_button_set_t`|`ok=0`、`ok_cancel=1`、`abort_retry_ignore=2`、`yes_no_cancel=3`、`yes_no=4`、`retry_cancel=5`|
|`dialog_result_t`|`none=0`、`ok=1`、`cancel=2`、`abort=3`、`retry=4`、`ignore=5`、`yes=6`、`no=7`|

`easyvrui/dialog/inputbox.h`は以下を宣言します：

```cpp
std::optional<std::u32string> inputbox(const std::u32string &prompt, const std::u32string &title = U"", const std::u32string &default_text = U"", uint64_t max_length = 0u, window *owner = nullptr);
```

確定すると入力文字を返し、空の文字列と文字列のキャンセルを許可します。キャンセルすると`std::nullopt`を返します。max_lengthが0の場合は長さに制限はありません。

### ファイルの開くと保存

`easyvrui/dialog/file_open_dialog.h`はフィルター`file_filter_t`と開く関数を宣言します。`easyvrui/dialog/file_save_dialog.h`は保存関数を宣言します。

```cpp
std::vector<std::filesystem::path> file_open_dialog(const std::u32string &title = U"", const std::filesystem::path &initial_directory = {}, const std::u32string &initial_filename = U"", const std::vector<file_filter_t> &filter_list = {}, std::size_t filter_index = 0u, bool multi_select = false, const std::u32string &confirm_text = U"", window *owner = nullptr, std::function<void(const std::filesystem::path &)> directory_changed = {}, std::function<void(std::size_t)> filter_changed = {});
std::optional<std::filesystem::path> file_save_dialog(const std::u32string &title = U"", const std::filesystem::path &initial_directory = {}, const std::u32string &initial_filename = U"", const std::vector<file_filter_t> &filter_list = {}, std::size_t filter_index = 0u, const std::u32string &default_extension = U"", bool confirm_overwrite = true, const std::u32string &confirm_text = U"", window *owner = nullptr, std::function<void(const std::filesystem::path &)> directory_changed = {}, std::function<void(std::size_t)> filter_changed = {});
```

`initial_directory`が空の場合はメモリディレクトリを使用します。`initial_filename`はファイル名を事前に設定します。フィルターリストが空の場合はデフォルトのフィルターを使用し、`filter_index`は0から始まります。`file_filter_t`の`pattern_list`は`*`と`?`をサポートします。`confirm_text`が空の場合はローカライズされた確認ボタンを使用します。ディレクトリとフィルターのコールバックは、UIスレッドが初期値とその後の変化を受け取る際に行われます。

開くと選択されたパスリストを返し、キャンセルすると空のリストを返します。`multi_select`を有効にすると複数のファイルを選択できます。保存すると目標パスを返し、キャンセルすると`std::nullopt`を返します。`default_extension`が空の場合は現在のフィルターに基づいて推論し、`confirm_overwrite`はカバー確認を制御します。

## 一般的な呼び出し組み合わせ

|シナリオ|呼び出しエントリ|
|---|---|
|通常のウィンドウの作成|windowの構築→属性の設定→get_control_list().add→show→easyvrui::run|
|フォントの設定|get_font()から返されるfont_tをコピー→フィールドを修正→set_font|
|バックグラウンドからインターフェースを更新|begin_invoke(callback)→callback内でsetterを呼び出す|
|モーダルウィンドウを開く|独立したウィンドウを構築→show_dialog(owner)→結果の列挙。イベント処理関数はset_dialog_resultで結果を設定する|
|カスタムコントロール|controlまたはtext_controlを派生→render/render_overlayをオーバーライド→状態が変わった後にinvalidate|
|タブを作成|`tabcontrol`と`tabpage`を構築→`tabpage::set_text()`を呼び出してタイトルを設定→`page_list.add(page)`→ページに子コントロールを追加|
|テキストセルを修正|select(start,length)→get_selected_text/set_selected_text|
|イベントコールバックを削除|on_click.add(callbackから返されるtokenを保存→on_click.remove(token)|
|カスタムIME|register_provider(input_role_t::ime)→on_inputを実行→textを消費してcommit_text、またはhandled=falseのまま自動的に転送|
|カスタムレイアウト|input_provider.register_provider(input_role_t::layout)→stateに応じて補助ウィンドウを表示→send_eventでキーを送信→run|
|手動でアプリケーションループを統合|easyvrui::pumpを周期的に呼び出す；ホストが呼び出しのタイミングと他の作業を調整する|

サンプルアプリケーションのディレクトリは`repo/app/demo/cpp`；アプリケーションはAPIヘッダファイルとコンパイルされたengine_interfaceライブラリを組み合わせて実行可能なプログラムにする。Pythonのサンプルは`repo/app/demo/python`にあります。

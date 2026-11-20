# 組み込みダイアログ

EasyVRUIには`messagebox`、`inputbox`、`file_open_dialog`、`file_save_dialog`、`color_dialog`、`font_dialog`があります。結果は同期的に返ります。待機中も、同じUIスレッドでメッセージの処理を続けます。現在の`window`を`owner`として渡すと、確認操作をその直接のownerに関連付けられます。

## モーダル呼び出しと結果

`dialog.show_dialog(owner)`を呼ぶと、SDKはまだ表示されておらず閉じられていない`window`を表示します。直接のownerの操作を制限し、このUIスレッドでメッセージループを入れ子にして実行します。呼び出し元はダイアログが終わるまで待ちます。待機中もキュー内のメッセージや`begin_invoke()`のコールバックが実行されるため、アプリの処理に再入する場合があります。処理順は[型付きイベントとマルチスレッド実行](/ja/guide/07_events_dialogs_threading)を参照してください。

`dialog_result_t`の値は`none`、`ok`、`cancel`、`abort`、`retry`、`ignore`、`yes`、`no`です。Pythonでは`dialog_result`を使います。モーダルに入ると、結果が`none`にリセットされます。`dialog_result`に有効な結果を設定すると、閉じる処理を開始します。通常、タイトルバーから閉じると`cancel`を返します。アプリは結果を確認してから変更を確定します。

```cpp
auto dialog = make_shared<easyvrui::window>(U"window_confirm");
auto button_accept = make_shared<easyvrui::button>(U"button_accept");
button_accept->set_rect({40u, 96u, 180u, 46u});
button_accept->set_text(U"确定");
button_accept->on_click += [owner = dialog.get()](easyvrui::control_base &, easyvrui::event_args_t &)
{
    owner->set_dialog_result(easyvrui::dialog_result_t::ok);
};
dialog->get_control_list().add(button_accept);
auto result = dialog->show_dialog(*window_main);
```

```python
dialog = window("window_confirm")
button_accept = button("button_accept")
button_accept.rect = rect(40, 96, 180, 46)
button_accept.text = "确定"

def button_accept_click(source, event):
    dialog.dialog_result = dialog_result.ok

button_accept.on_click += button_accept_click
dialog.control_list.add(button_accept)
result = dialog.show_dialog(window_main)
```

上のコードは、`window_main`を保持するイベントハンドラー内で実行します。開き直すときは新しいダイアログのインスタンスを作成します。

## messagebox

確認、通知、エラーを表示します。標準のオーバーロードは`message`、`title`、`button_set`、`icon`、`default_button`、`owner`を受け取り、`dialog_result_t`またはPythonの`dialog_result`を返します。カスタムボタンのオーバーロードは`messagebox_button_t`または`messagebox_button`の一覧を受け取ります。各ボタンには識別用の安定した`name`と表示用の`text`を指定します。結果は選んだボタンの名前です。そのままキャンセルした場合は空文字列を返します。

ボタンの組み合わせは`ok`、`ok_cancel`、`abort_retry_ignore`、`yes_no_cancel`、`yes_no`、`retry_cancel`から選びます。既定のボタンには、指定した組み合わせに含まれる有効な結果を設定します。

![messagebox保存確認](/images/ja/dialog_messagebox.png)

## inputbox

短いテキストを受け取ります。引数の順序は`prompt`、`title`、`default_text`、`max_length`、`owner`です。`max_length = 0`はUnicodeコードポイント数を制限しません。確定時はテキストを返します。キャンセル時はC++で空の`optional`、Pythonで`None`を返します。ユーザーが確定した空文字列も有効です。結果の有無でキャンセルを判別します。

![inputbox報告命名](/images/ja/dialog_inputbox.png)

## file_open_dialog

既存ファイルのパスを選びます。`initial_directory`と`initial_filename`で初期ディレクトリとファイル名を設定します。`filter_list`には`file_filter_t`またはPythonの`file_filter`を指定します。メンバーは`name`と`pattern_list`です。フィルターのインデックスは0から数えます。`multi_select`を有効にすると複数のパスを返し、キャンセル時は空のコレクションを返します。

`confirm_text`で確定ボタンの表示を変更できます。任意の`directory_changed`コールバックはディレクトリのパス、`filter_changed`はインデックスを受け取ります。次に開くときの初期値を保存する場合に使えます。

![file_open_dialogで既存のファイルを選択](/images/ja/dialog_file_open.png)

## file_save_dialog

保存先のパスを選びます。ディレクトリ、ファイル名、フィルター、変更通知は`file_open_dialog`と対応します。`default_extension`と`confirm_overwrite`も設定できます。結果は省略可能なパスで、キャンセル時はC++で空の`optional`、Pythonで`None`になります。ユーザーが確定したパスに対し、アプリ側で書き込みを行い、エラーを処理します。

![file_save_dialogで報告用のパスを選択](/images/ja/dialog_file_save.png)

## color_dialog

`0xRRGGBBAA`形式の色を選びます。引数は現在の`color`、`title`、リセット先の`default_color`、`owner`です。確定時は選んだ色、キャンセル時は空の`optional`または`None`を返します。ダイアログの「既定値」を押すと、呼び出し元が設定したリセット先をプレビューします。

![color_dialogで色相と透明度を表示](/images/ja/dialog_color.png)

## font_dialog

フォントファミリー、サイズ、太字、斜体を選びます。引数は`font`、`title`、`default_font`、`owner`です。確定時はC++で`font_t`を格納した`optional`、Pythonで`font`を返します。キャンセル時は結果が空になります。アプリは結果を受け取った後、フォントサイズに合わせてコントロールの矩形を更新できます。

![font_dialogでフォントリストとプレビューを表示](/images/ja/dialog_font.png)

## 送信とキャンセル

|エントリー|確定時|キャンセル時|
|---|---|---|
|`show_dialog`|アプリケーション設定の結果一覧|`cancel`|
|`messagebox`|結果一覧またはカスタムボタン名|ボタン集に基づいて結果を返し、カスタムキャンセルは空文字列|
|`inputbox`|テキスト、空文字列を含む|空の選択可能値|
|`file_open_dialog`|パス集合|空の集合|
|`file_save_dialog`、`color_dialog`、`font_dialog`|選択されたパス、色、またはフォント|空の選択可能値|

ダイアログはUIイベントから開き、待機時にはアプリ側のロックを解放しておきます。削除、上書き、ウィンドウの終了などは、ユーザーが確定した分岐で実行します。シグネチャーと既定値は[C++ API](/ja/reference/cpp_api)または[Python API](/ja/reference/python_api)を参照してください。

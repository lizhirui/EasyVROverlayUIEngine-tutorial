# button

`button`はユーザーの操作を明確なコマンドにマッピングします。例えば、設定の適用、確認、または再編集などです。操作結果を簡潔に表現する文字を使用し、コマンドが一時的に実行できない場合は`enabled`を更新します。

[公共コントロールインターフェース](/ja/guide/controls/common-api#control)および[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を継承します。

## 既定の外観

デフォルトではフォーカス可能、可視、有効です。`text`は初期値で空です。設定された文字はコントロールの矩形の中央に配置されます。スクリーンショットでは文字と矩形のみを記入してください。

![buttonのデフォルト外観](/images/ja/button_default.png)

## プロパティの比較

4行にわたってデフォルト、フォントと色、無効化とフォーカスの境界線を順に表示します。同じ文字を保持することで状態の違いを比較できます。アラインメントはコントロールの固定描画規則に従います。

![buttonの属性比較](/images/ja/button_comparison.png)

## APIリファレンス

C++の属性は表内のアクセスメソッドを通じて読み書きされ、Pythonは同名の属性を通じてアクセスされます。表内のイベントパラメータはC++の型名を使用し、Pythonの対応する型には`_t`の接尾辞を省略します。公共メンバーは[基本インターフェース](/ja/guide/controls/common-api)を参照してください。

### プロパティ

|プロパティ|C++|用途と既定値|
|---|---|---|
|`text`|`get_text`、`set_text`|表示される文字を読み書きし、デフォルトでは空の文字列です。|
|`focusable`、`enabled`、`tab_index`|`is_focusable`、`get_enabled`、`set_enabled`、`get_tab_index`、`set_tab_index`|フォーカス可能で、デフォルトでは有効化されています。`tab_index`は`window`のTab順序に関与します。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`button(name)`|`button(name)`|一つの`button`を作成します。|
|`focus()`、`activate()`|`focus()`、`activate()`|インターフェースを継承します。前者はフォーカスを要求し、後者はプログラム的にアクティブ化のパスをトリガーします。|

### イベント

|イベント|発生条件と引数|
|---|---|
|`on_text_changed`|タイトルの文字が実際に変更され、パラメータは`event_args_t`です。|
|`on_click`|継承されたアクティブ化イベントのパラメータは`event_args_t`です。|
|`on_focus_in`、`on_focus_out`、`on_enabled_changed`|継承されたイベントは、フォーカスと利用可能な状態を観察するのに適しています。|

## 実行できるサンプル

「設定を提出」をクリックすると、状態文字が更新され、提出入口が無効化され、「再編集」が利用可能になります。「再編集」をクリックすると初期状態に戻ります。

まず[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルのリポジトリのルートディレクトリで、MSVCが設定されたx64 CMDを開き、実際にインストールされたSDKのパスを使用します。

### C++

```bat
cmake -S examples/guide/controls/window-and-text/button/cpp -B .work/example_button -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_button --config Release
.work\example_button\Release\tutorial_button.exe
```

上記の実行ファイルのパスはVisual Studioジェネレーターに対応しています。単一コンフィギレーションのNinjaを使用する場合、実行ファイルは直接ビルドディレクトリにあります。

<<< ../../../../../examples/guide/controls/window-and-text/button/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\button\python\run.cmd
```

<<< ../../../../../examples/guide/controls/window-and-text/button/python/button_demo.py

### 実行結果

![buttonの独立した例の実行結果](/images/ja/button_demo.png)

## よくある問題と実装上の注意

- ネットワークまたはディスクのタスクを送信する際には、まず利用可能な状態を更新し、完了後は`begin_invoke()`を通じてUIを更新して、イベントコールバックの処理時間を節約します。
- ビジネス呼び出しを`on_click`に置くことで、クリックとプログラム的なアクティブ化が同じパスを共有します。複数の`button`を連続して有効にする場合は、明確な`tab_index`を設定してください。
- 一時的な無効化と永久的な削除は、それぞれ`enabled`とコンテナ集合操作を使用して行い、無効化状態に読みやすいヒントを表示します。

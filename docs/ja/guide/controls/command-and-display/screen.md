# screen

`screen`はEngine側で指定された表示出力のキャプチャ画面を空間インターフェースに描画します。`screen_id`を選択し、ソース状態を購読することで、レンダリングバックエンドがキャプチャとテクスチャの送信を担当します。典型的な用途には、ヘッドセット内でデスクトップ出力を並列に表示したり、アプリケーションの状態を監視したり、一時的な参照画面を観察したりすることが含まれます。継承メンバーについては[公共コントロールインターフェース](/ja/guide/controls/common-api#control)を参照してください。

## 既定の外観

`screen_id`のデフォルトは0で、`screen_available`は初期値として偽です。下の図は、デフォルトの外観を保持するために無効なキャプチャ番号を使用しており、最初に画面がない時の背景と境界線を示しています。

![screenデフォルト外観](/images/ja/screen_default.png)

## プロパティの比較

異なるサイズのキャプチャエリアと利用可能/利用不可能な状態を比較します。左側はテストホストからの復元イベントを送信し、右側は利用不可能な状態を保持しています。両側にはWARPが実際に描画したコントロールとプレースホルダーテキストがあります。

![screen属性比較](/images/ja/screen_comparison.png)

## APIリファレンス

C++の表のメソッドは属性を読み書きし、Pythonは同名の属性をアクセスします。コールバックは`source`と`event`を受け取ります。表の各型付きイベント引数は`event_args_t`を継承し、基本パラメータ自体には追加のフィールドがありません。Pythonの型名は`_t`を省略しています。

### プロパティ

|プロパティ|C++でのメソッドアクセス|型、デフォルト値、および用途|
|---|---|---|
|`screen_id`|`get_screen_id`、`set_screen_id`|`uint64_t`、デフォルトは0で、Engineが識別する表示出力番号を選択します。|
|`screen_available`|`get_screen_available`|読み取り専用で、初期値は偽であり、現在のウィンドウと表示出力の状態メッセージに従います。|
|`rect`、`background_color`|`get_rect`、`set_rect`、`get_background_color`、`set_background_color`|継承される目標矩形と背景色。画面が利用不可能な場合でもコントロールの背景は描画されます。|

### メソッド

|メソッド|用途|
|---|---|
|`screen(name)`|コントロールを構築し、`window`またはコンテナに追加します。|
|`set_screen_id(value)`|C++では収集番号を切り替えます。Pythonでは`screen_id`に値を割り当てます。|

### イベント

|イベント|パラメータの型|トリガー条件|
|---|---|---|
|`on_screen_id_changed`|`event_args_t`|番号の実際の変化。|
|`on_screen_unavailable`|`event_args_t`|利用可能から利用不可能に変わる。番号を切り替えると、既存の利用可能な状態もリセットされます。|
|`on_screen_restored`|`event_args_t`|利用不可能から利用可能に変わる。|

## ヘッドなしのスクリーンショットと実際の収集

WARPのテストホストは無効な表示番号を使用してデスクトップ入力を無効化して収集バックエンドを維持し、SDKにテスト状態を送信します。状態テキストはルーチンの実際のイベント処理関数によって更新されます。スクリーンショットのプレースホルダーエリアには実際のデスクトップフレームは含まれていません。実際のEngineに接続し、有効な表示番号を選択すると、収集画面はEngineによって`screen`矩形にレンダリングされます。

## 実行できるサンプル

「表示出力監視」を実行すると、コントロールはデフォルトで0を選択します。状態エリアは収集の復元または中断に応じて更新されます。デモ画像では、復元イベントが到達した後、状態テキストが更新され、ヘッドなし環境で描画エリアが保持されます。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)をクリックしてEngineを起動します。チュートリアルのルートディレクトリにあるx64 Developer CMDでコマンドを実行し、サンプルでのSDKインストールパスを変更してください。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/screen/cpp -B .work/example_screen -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_screen --config Release
.work\example_screen\Release\tutorial_screen.exe
```

シングルコンフィギネーションのNinjaを使用する場合は、ビルドディレクトリから直接実行ファイルを実行します。

<<< ../../../../../examples/guide/controls/command-and-display/screen/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\screen\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/screen/python/screen_demo.py

### 実行結果

![screen独立例程運用効果](/images/ja/screen_demo.png)

## よくある質問とレイアウト実践

- ユーザーが見るのはEngine側のキャプチャソースの画面です。リモートEngineを選択する場合は、そのホストの表示出力番号を基準にします。
- `screen_available`と2つの状態イベントを使用してプロンプトを維持します。初期状態で使用できない場合は、まず待機状態を提供します。
- レイアウト時には、表示出力の比率に基づいて`rect`を設計し、プロンプトテキストをキャプチャエリアの下に配置できます。

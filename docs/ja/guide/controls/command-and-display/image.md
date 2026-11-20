# image

`image`は矩形内に`drawing_image`を表示し、アイコン、アルバムプレビュー、状態グラフィックに適しています。SDKは`stretch_mode`に基づいて、ソース画像とターゲット矩形間のスケーリングとトリミングを計算します。継承メンバーについては[公共コントロールインターフェース](/ja/guide/controls/common-api#control)を参照してください。

## 既定の外観

デフォルトのソースは空で、`stretch_mode = contain`です。スクリーンショットはターゲット矩形の背景と境界のみを表示します。

![imageデフォルト外観](/images/ja/image_default.png)

## プロパティの比較

4つの同じターゲット矩形はそれぞれ`contain`、`cover`、`fill`、`none`を使用しています。元の画像は2:1です。余白、トリミング、伸長、および元のサイズを観察できます。

![image属性比較](/images/ja/image_comparison.png)

## APIリファレンス

C++の表のメソッドは属性を読み書きし、Pythonは同名の属性をアクセスします。コールバックは`source`と`event`を受け取ります。表の各型付きイベント引数は`event_args_t`を継承し、基本パラメータには追加のフィールドがありません。Pythonの型名は`_t`を省略します。

### プロパティ

|プロパティ|C++でのメソッドアクセス|タイプ、デフォルト値、および用途|
|---|---|---|
|`source`|`get_source`、`set_source`|`drawing_image`リソースは空の場合があり、デフォルトでは空です。C++では`shared_ptr<const drawing_image>`を使用します。|
|`stretch_mode`|`get_stretch_mode`、`set_stretch_mode`|`image_stretch_mode_t`、デフォルトは`contain`です。Pythonの列挙名は`image_stretch_mode`です。|

### メソッド

|メソッド|用途|
|---|---|
|`image(name)`|コントロールの構築。|
|`drawing_image(width,height,rgba)`|指定されたサイズのRGBAバイトでリソースを構築し、バッファ長は幅×高さ×4です。|
|`drawing_image.load_file(path)`|ファイルリソースが必要な場合は、対応する画像形式をロードできます。|

### イベント

|イベント|パラメータタイプ|トリガー条件|
|---|---|---|
|`on_source_changed`、`on_stretch_mode_changed`|`event_args_t`|ソースリソースまたはスケーリングモードの変化。|
|`on_source_unavailable`|`event_args_t`|ソースリソースが利用できない場合に通知を受け取る。|

## 伸縮ルール

|モード|表示ルール|
|---|---|
|`contain`|等倍スケーリングで、元の画像を完全に表示し、残りの領域に背景を表示します。|
|`cover`|ターゲット矩形を等倍で満たし、超過部分はトリミングします。|
|`fill`|ターゲットの幅と高さをそれぞれマッチングし、縦横比を変更できます。|
|`none`|ターゲットの左上角から元の画像の論理サイズで描画し、表示範囲を超えた場合はトリミングします。|

## 実行できるサンプル

“素材プレビュー”では二重色のパターンを生成し、「等比充填を切り替える」をクリックして`contain`と`cover`の間を切り替えます。図では`cover`を示しています。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)に従ってEngineを起動します。チュートリアルのルートディレクトリのx64デベロッパCMDでコマンドを実行し、サンプルでのSDKインストールパスを置き換えます。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/image/cpp -B .work/example_image -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_image --config Release
.work\example_image\Release\tutorial_image.exe
```

シングルコンフィギュレーションのNinjaを使用する場合は、ビルドディレクトリから直接実行ファイルを実行します。

<<< ../../../../../examples/guide/controls/command-and-display/image/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\image\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/image/python/image_demo.py

### 実行結果

![image独立例程実行効果](/images/ja/image_demo.png)

## よくある問題とレイアウト実践

- すべての内容を保持する場合は`contain`を使用し、サムネイルカードが対象領域を完全に占める場合は`cover`を使用します。
- RGBAバイトを準備する際は行ごとに並べ、サイズとチャンネルの順序を確認します。純粋なグラフィックは同じ共有リソースを再利用できます。
- 画像外のテキストや操作項目のための矩形を予約します。画像モードの変更は画像自体にのみ影響します。

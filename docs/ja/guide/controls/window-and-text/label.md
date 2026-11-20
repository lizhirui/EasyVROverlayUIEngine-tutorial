# label

`label`はページの説明、状態、フィールドのタイトルを表示するために使用されます。デフォルトでは透明な背景で、文字は左揃えされ、Tabのフォーカス順序には含まれません。状態の色は明確なテキストと組み合わせ、接続中、成功、失敗をユーザーが区別できるようにします。

[公共コントロールインターフェース](/ja/guide/controls/common-api#control)および[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を継承します。

## 既定の外観

デフォルトでは`text`は空です。下の図は例示的な文字と矩形のみを設定しており、SDKのフォント、色、透明な背景は保持されています。

![labelのデフォルト外観](/images/ja/label_default.png)

## プロパティの比較

上から下へ同じ文字を保持し、デフォルト外観、大文字太字、緑色の文字と実色の背景、無効化後の文字色を順に表示します。`label`には独立した整列属性がなく、配置を変更する場合は`rect`を調整する必要があります。正確な整列が必要な場合は、カスタムの描画を使用します。

![label属性の比較](/images/ja/label_comparison.png)

## APIリファレンス

C++属性は表内のアクセスメソッドを通じて読み書きされ、Pythonは同名の属性を通じてアクセスされます。表内のイベントパラメータはC++の型名を使用し、Pythonの対応する型は`_t`接尾辞を省略します。公共メンバーは[基本インターフェース](/ja/guide/controls/common-api)を参照してください。

### プロパティ

|プロパティ|C++|用途と既定値|
|---|---|---|
|`text`|`get_text`、`set_text`|読み書きで文字を表示し、デフォルトでは空の文字列です。|
|`font`、`foreground_color`、`background_color`|`get_font`、`set_font`、`get_foreground_color`、`set_foreground_color`、`get_background_color`、`set_background_color`|スタイル属性を継承します。デフォルトのフォントサイズは18、背景は透明です。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`label(name)`|`label(name)`|一つの`label`を作成します。|

### イベント

|イベント|発生条件と引数|
|---|---|
|`on_text_changed`|文字が実際に変更され、パラメータは`event_args_t`です。|

## 実行できるサンプル

例程では接続ページのタイトル、前景色と背景色の接続結果、および次のステップのヒントを表示します。3つの`label`はそれぞれ第一級のタイトル、状態、補足説明を担当します。

まず[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルのリポジトリのルートディレクトリで、MSVCが設定されたx64 CMDを開き、実際にインストールされたSDKのパスを使用します。

### C++

```bat
cmake -S examples/guide/controls/window-and-text/label/cpp -B .work/example_label -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_label --config Release
.work\example_label\Release\tutorial_label.exe
```

上記の実行ファイルのパスはVisual Studioジェネレーターに対応しています。単一コンフィギレーションのNinjaを使用する場合、実行ファイルはビルドディレクトリに直接あります。

<<< ../../../../../examples/guide/controls/window-and-text/label/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\label\python\run.cmd
```

<<< ../../../../../examples/guide/controls/window-and-text/label/python/label_demo.py

### 実行結果

![labelの独立した例程の実行結果](/images/ja/label_demo.png)

## よくある問題と実装上の注意

- 長くなる可能性のある文字やローカライズされた文字に余裕を持たせるために幅を確保します。`font`を拡大した後、矩形の高さと上下の内側の余白を同時に確認します。
- 状態がリアルタイムで変更されると`text`を更新し、コントロールの繰り返し作成を避けます。バックグラウンドタスクでは、`begin_invoke()`を使用して更新をUIスレッドにディスパッチします。
- ユーザーが長いテキストをコピーする必要がある場合は、`read_only`の[textbox](./textbox)を使用します。

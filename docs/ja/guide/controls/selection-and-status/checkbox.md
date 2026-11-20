# checkbox

`checkbox`は、通知音の再生有無など、独立して切り替え可能なブールオプションを表示します。複数の`checkbox`を同時に選択することも、それぞれ選択解除することもできます。

[公共コントロールインターフェース](/ja/guide/controls/common-api#control)および[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を継承します。

## 既定の外観

デフォルトは`checked = False`で、フォーカス可能かつ有効です。空白のボックスは未選択のマークで、スクリーンショットは文字が入力された状態です。

![checkboxデフォルト外観](/images/ja/checkbox_default.png)

## プロパティの比較

未選択、選択、選択後に無効、フォントと色の順に4行で表示します。無効と選択は同時に成立し、チェックマークと文字の明るさはそれぞれの状態を示します。

![checkbox属性比較](/images/ja/checkbox_comparison.png)

## APIリファレンス

C++属性は表内のアクセスメソッドで読み書きされ、Pythonは同名の属性でアクセスします。表内のイベントパラメータはC++の型名を使用し、Pythonの対応する型には`_t`の接尾辞を省略します。公共メンバーは[基本インターフェース](/ja/guide/controls/common-api)を参照してください。

### プロパティ

|プロパティ|C++|用途と既定値|
|---|---|---|
|`text`|`get_text`、`set_text`|オプションの説明で、デフォルトは空の文字列です。|
|`checked`|`get_checked`、`set_checked`|ブール選択状態で、初期は偽です。|
|`focusable`|`is_focusable`|フォーカスへの入力順序が可能です。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`checkbox(name)`|`checkbox(name)`|独立した二値オプションを作成します。|

### イベント

|イベント|発生条件と引数|
|---|---|
|`on_text_changed`|文字の実際の変化を表示し、パラメータは`event_args_t`です。|
|`on_checked_changed`|`checked`の実際の変化で、ユーザーインタラクションとプログラムの値設定が含まれます。パラメータは`event_args_t`です。|
|`on_click`|継承されたアクティブイベント。持続的な選択状態を使用する際には`on_checked_changed`を使用します。|

## 実行できるサンプル

初期は「未読状態を表示」のみ選択されます。「通知音を再生」にチェックを入れると、別の項目は選択されたまま、状態文字が更新されます。再切り替えると通知音をオフにできます。

まず[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルリポジトリのルートディレクトリで、MSVCが設定されたx64 CMDを開き、実際にインストールされたSDKのパスを使用します。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/checkbox/cpp -B .work/example_checkbox -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_checkbox --config Release
.work\example_checkbox\Release\tutorial_checkbox.exe
```

上記の実行ファイルのパスはVisual Studioジェネレーターに対応しています。シングルコンフィギュレーションのNinjaを使用する場合、実行ファイルは直接ビルドディレクトリにあります。

<<< ../../../../../examples/guide/controls/selection-and-status/checkbox/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\checkbox\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/checkbox/python/checkbox_demo.py

### 実行結果

![checkbox独立例程実行効果](/images/ja/checkbox_demo.png)

## よくある問題と実装上の注意

- 初期化時にはまず`checked`を復元し、次に`on_checked_changed`を購読して、復元状態を新しい操作として扱わないようにします。
- 持続的な状態処理は状態イベントを統一して行います。複数のオプションを一括で復元する場合、ビジネス層で複数回の変化を一度の保存にまとめることができます。
- 現在のインターフェースは2つのブール状態を提供します。明確な排他的なオプションには[radiobutton](./radiobutton)を使用します。

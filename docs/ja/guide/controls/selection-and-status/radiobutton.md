# radiobutton

`radiobutton`は、通知戦略など、同じグループのオプションから一つを選択するのに適しています。同じ直接親コンテナ内の`radiobutton`は一つのグループを構成します。複数の独立したグループに対して別々に`panel`を作成します。

[公共コントロールインターフェース](/ja/guide/controls/common-api#control)および[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を継承します。

## 既定の外観

初期は選択されておらず、フォーカス可能で、中空の円で表示されます。デフォルトの文字は空で、スクリーンショットには例文と矩形のみを記入します。

![radiobuttonのデフォルト外観](/images/ja/radiobutton_default.png)

## プロパティの比較

第一行と第二行は中空の円と実心の選択点を示します。第三行は選択されていない文字と円印を示し、第四行はフォント、前景色、背景色を変更します。

![radiobuttonの属性比較](/images/ja/radiobutton_comparison.png)

## APIリファレンス

C++の属性は表のアクセスメソッドを通じて読み書きされ、Pythonは同名の属性を通じてアクセスします。表のイベントパラメータはC++の型名を使用し、Pythonの対応する型には`_t`の接尾辞を省略します。公共メンバーは[基本インターフェース](/ja/guide/controls/common-api)を参照してください。

### プロパティ

|プロパティ|C++|用途と既定値|
|---|---|---|
|`text`|`get_text`、`set_text`|オプションの説明は、デフォルトで空の文字列です。|
|`checked`|`get_checked`、`set_checked`|ブールの選択状態で、デフォルトは偽です。真の場合、同じ直接親コンテナ内で既に選択されている他の`radiobutton`を解除します。|
|`focusable`|`is_focusable`|フォーカスに入る順序が可能です。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`radiobutton(name)`|`radiobutton(name)`|相互排他のオプションを作成します。親コンテナに追加した後、デフォルトの項目を設定します。|

### イベント

|イベント|発生条件と引数|
|---|---|
|`on_checked_changed`|選択または取消し時にトリガーされ、パラメータは`event_args_t`です。グループ内の切り替えでは、旧項目の取消しのイベントを受け取ることができます。|
|`on_text_changed`|実際の文字の変化を表示し、パラメータは`event_args_t`です。|
|`on_click`|継承されたアクティブイベントです。グループの現在の値を追跡するには`on_checked_changed`を使用することが適切です。|

## 実行できるサンプル

2つの`radiobutton`は同じ`panel`に属します。初期は「重要な通知のみ受信」で、 「すべての通知を受信」を選択すると、旧項目の取消しと状態文字の更新が観察できます。

まず[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルのリポジトリのルートディレクトリで、MSVCを設定したx64 CMDを開き、実際にインストールされたSDKのパスを使用します。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/radiobutton/cpp -B .work/example_radiobutton -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_radiobutton --config Release
.work\example_radiobutton\Release\tutorial_radiobutton.exe
```

上記の実行ファイルのパスはVisual Studioジェネレーターに対応しています。単一コンフィギレーションのNinjaを使用する場合、実行ファイルは直接ビルドディレクトリにあります。

<<< ../../../../../examples/guide/controls/selection-and-status/radiobutton/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\radiobutton\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/radiobutton/python/radiobutton_demo.py

### 実行結果

![radiobuttonの独立した例の実行結果](/images/ja/radiobutton_demo.png)

## よくある問題と実装上の注意

- まずすべてのオプションを共通の親コンテナに追加し、デフォルトの選択項目を設定します。これにより、グループのルールが他のオプションをチェックできるようになります。
- 状態の変化を処理する際には、出所の`checked`をチェックします。選択イベントはビジネスエンデミングに適しており、取消イベントは旧項目の状態をクリアするのに適しています。
- 業務上常にオプションが必要な場合は、初期化時にデフォルト項目を明確に設定し、現在の項目をプログラム的に偽の状態に設定することを避けましょう。

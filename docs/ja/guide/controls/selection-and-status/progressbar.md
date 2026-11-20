# progressbar

`progressbar`は、ファイル処理数や同期エントリ数などの既知の範囲内の完了量を充填比率で表示します。数値とタスク名は、隣の`label`で表示できます。

コントロール[公共コントロールインターフェース](/ja/guide/controls/common-api#control)を継承します。

## 既定の外観

デフォルトの範囲は0から100で、現在の値は0です。左端からの充填比率は0で、トラックとフレームが依然として表示されます。

![progressbarのデフォルト外観](/images/ja/progressbar_default.png)

## プロパティの比較

4行にわたって、デフォルト値、42%の完了、範囲20から80、現在の値65（充填75%）、および無効な色とカスタム背景を表示します。充填色はSDKスタイルによって決定され、`background_color`でトラックが変更されます。現在のSDKは確定した進捗のみを提供し、未確定の総量の場合は`label`で現在の段階を表示し、総量が確定した後は`progressbar`を表示します。

![progressbarの属性比較](/images/ja/progressbar_comparison.png)

## APIリファレンス

C++属性は表内のアクセスメソッドで読み書きされ、Pythonは同名の属性でアクセスされます。表内のイベントパラメータはC++の型名を使用し、Pythonに対応する型は`_t`サフィックスを省略します。公共メンバーは[基本インターフェース](/ja/guide/controls/common-api)を参照してください。

### プロパティ

|プロパティ|C++|用途と既定値|
|---|---|---|
|`minimum`|`get_minimum`、`set_minimum`|符号付き64ビット整数の下限はデフォルト0で、現在の上限より小さくなければなりません。|
|`maximum`|`get_maximum`、`set_maximum`|符号付き64ビット整数の上限はデフォルト100で、現在の下限より大きくなければなりません。|
|`value`|`get_value`、`set_value`|現在の値はデフォルト0です。範囲を超えると最も近い端にクランプされ、範囲を狭めると現在の値も調整されます。|
|`background_color`、`enabled`|`get_background_color`、`set_background_color`、`get_enabled`、`set_enabled`|属性を継承します。背景色はトラックに使用され、無効状態では充填色が変更されます。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`progressbar(name)`|`progressbar(name)`|確定した進捗を示すためのプログレスバーを作成します。|

### イベント

|イベント|発生条件と引数|
|---|---|
|`on_minimum_changed`、`on_maximum_changed`|下限または上限が変更される場合、パラメータは`event_args_t`です。|
|`on_value_changed`|現在の値が実際に変更される場合、境界の調整による挟み込みも含まれ、パラメータは`event_args_t`です。|

## 実行できるサンプル

総量は8項で、初期完了は2項です。毎回「次の項目を完了」をクリックすると、充填と完了数が更新されます。効果図では5項の完了状態を示し、8項に達した後は操作の入口が無効になります。

まず[環境準備、構築とインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルリポジトリのルートディレクトリで、MSVCを設定したx64 CMDを開き、実際にインストールされたSDKのパスを使用します。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/progressbar/cpp -B .work/example_progressbar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_progressbar --config Release
.work\example_progressbar\Release\tutorial_progressbar.exe
```

上記の実行ファイルのパスはVisual Studioジェネレーターに対応しています。単一コンフィギレーションのNinjaを使用する場合、実行ファイルは直接ビルドディレクトリにあります。

<<< ../../../../../examples/guide/controls/selection-and-status/progressbar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\progressbar\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/progressbar/python/progressbar_demo.py

### 実行結果

![progressbarの独立した実行例の効果](/images/ja/progressbar_demo.png)

## よくある問題と実装上の注意

- 全体の範囲を変更する際は、適切な設定順序を選択してください。例えば`[0, 100]`から`[200, 500]`に切り替える場合は、まず`maximum = 500`を設定し、次に`minimum = 200`を設定します。
- 表示される比率は`(value - minimum) / (maximum - minimum)`です。元の計量単位と状態文字をフィルタリングと共に表示します。
- UIスレッドで進捗状況を更新し、頻繁に発生する進捗の変化はまとめて`begin_invoke()`で更新します。

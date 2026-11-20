# slider

`slider`は有限の整数範囲内で連続的なドラッグ操作を提供し、音量のパーセンテージ、明るさのレベル、速度のギアなどの即時設定に適しています。SDKはポインタの位置を範囲比率に変換し、整数に切り捨てます。横方向は左から右へ、縦方向は下から上へ増加します。キーボードのフォーカスが`slider`内の場合、方向キー→と↑は1を増加させ、←と↓は1を減少させます。

継承された一般的なメンバーについては[公共コントロールインターフェース](/ja/guide/controls/common-api#control)を参照してください。

## 既定の外観

デフォルトの範囲は`[0, 100]`で、初期値は0、方向は`horizontal`です。ポインタスライダーは左端に表示され、トラックはコントロールの横軸に沿って配置されます。

![sliderのデフォルト外観](/images/ja/slider_default.png)

## プロパティの比較

左上は`horizontal`で値は65です。右側は同じ値で`vertical`を表示し、上端は最大値を表します。左下の範囲は`[-20, 20]`に設定され、値10は75%の位置に対応し、無効な場合はトラックとスライダーが弱い色合いで表示されます。

![sliderの属性比較](/images/ja/slider_comparison.png)

## APIリファレンス

Pythonでは表の属性名を使用します。C++では対応するメソッドを使用して読み書きし、`control_base &source`と表の型の参照を使用してイベントをサブスクライブします。追加フィールドのない`event_args_t`は状態が更新されたことを意味し、コールバックは`source`を通じて新しい値を読み取ります。Pythonの対応するイベントタイプ名は`_t`を省略します。

### プロパティ

|プロパティ|C++|タイプ、デフォルト値、および用途|
|---|---|---|
|`minimum`|`get_minimum`、`set_minimum`|`int64_t`、デフォルトは0です。新しい下限は現在の上限より小さくなければなりません。|
|`maximum`|`get_maximum`、`set_maximum`|`int64_t`、デフォルトは100です。新しい上限は現在の下限より大きくなければなりません。|
|`value`|`get_value`、`set_value`|`int64_t`、デフォルトは0です。値が範囲を超えると端に引き込まれ、境界の調整によって現在の値が修正されます。|
|`orientation`|`get_orientation`、`set_orientation`|デフォルトは`orientation_t::horizontal`です。Pythonでは`orientation.horizontal`または`orientation.vertical`を使用します。|
|`focusable`|`is_focusable`|継承された読み取り専用の能力で、真を返します。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`slider(name)`|`slider(name)`|コントロールを構築します。継承された`focus()`を使用してフォーカスを要求します。|

### イベント

|イベント|パラメータのタイプ|トリガー条件|
|---|---|---|
|`on_minimum_changed`、`on_maximum_changed`|`event_args_t`|範囲の端の実際の変更。|
|`on_value_changed`|`event_args_t`|整数値の実際の変更、指標、方向キー、プログラムの値付け、または境界の引き込みを含みます。|
|`on_orientation_changed`|`event_args_t`|トラックの方向の変更。|
|`on_drag_start`|`event_args_t`|指標を押してドラッグを開始します。|
|`on_drag_end`|`interaction_end_event_args_t`|ドラッグが終了します。`cancelled`を使用してキャンセルされたドラッグを識別できます。|

## 実行できるサンプル

音量の監視は35から開始します。`slider`でドラッグすると、`on_value_changed`は`progressbar`と説明テキストを同期して更新します。スクリーンショットはスライダーを高音量領域にドラッグした後の状態を示しています。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)をクリックしてEngineを起動します。以下のコマンドはチュートリアルリポジトリのルートディレクトリのx64開発者CMDで実行します。サンプルSDKのパスを実際のインストール場所に変更してください。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/slider/cpp -B .work/example_slider -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_slider --config Release
.work\example_slider\Release\tutorial_slider.exe
```

Visual Studioジェネレーターは実行可能ファイルを`Release`サブディレクトリに配置します。シングルコンフィギュレーションのNinja生成器は直接ビルドディレクトリに出力します。

<<< ../../../../../examples/guide/controls/selection-and-status/slider/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\slider\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/slider/python/slider_demo.py

### 実行結果

![slider独立例程効果](/images/ja/slider_demo.png)

## よくある質問とレイアウト実践

- 縦向きレイアウトでは、高さはトラックに、幅はスライダーとレーザーヒットエリアに割り当てるべきです。`orientation`のみを切り替える場合、元の`rect`のサイズはそのまま保持されます。
- `on_value_changed`を使用して即時フィードバックを更新し、`on_drag_end`をポインターのドラッグ完了のシグナルとして使用します。キーボード調整をカバーする必要がある場合は、数値変化のパスでビジネス状態を統一して処理します。
- 正確な小数入力が必要な場合は[numericupdown](./numericupdown)を使用できます。[progressbar](./progressbar)と連動する際は、両者の値範囲を先に整列させます。

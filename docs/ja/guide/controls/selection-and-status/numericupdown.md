# numericupdown

`numericupdown`は有限小数值を受け入れ、ゲイン、倍率、時間間隔、その他正確な入力や固定ステップが必要なパラメータに適しています。内部編集エリアは数字を受け取り、Enterキーを押すか編集焦点を外すと入力が送信されます。右側の上下エリアは`step`で数値を調整し、操作前に編集中の内容が送信されます。

継承された一般的なメンバーは[文字スタイルインターフェース](/ja/guide/controls/common-api#text-control)を参照してください。

## 既定の外観

デフォルトは`value = 0.0`、`minimum = 0.0`、`maximum = 100.0`、`step = 1.0`、`decimal_places = 0`です。表示エリアは整数形式で0を描画し、右側には上下の操作エリアが描画されます。

![numericupdownデフォルト外観](/images/ja/numericupdown_default.png)

## プロパティの比較

第一行はデフォルト値0を表示します。第二行には負の範囲が追加され、下限−2.00が表示されます。第三行は1.00から0.25のステップを加えて1.25を表示し、第四行は同じ数値を保持し、コントロールを無効にします。`decimal_places`は表示される小数の桁数を決定します。

![numericupdown属性比較](/images/ja/numericupdown_comparison.png)

## APIリファレンス

Pythonでは表の属性名を使用します。C++では対応するメソッドを使用して読み書きし、`control_base &source`と表の型の参照を使用してイベントをサブスクライブします。追加フィールドのない`event_args_t`は状態が更新されたことを意味し、コールバックは`source`を使用して新しい値を読み取ります。Pythonの対応するイベントタイプ名は`_t`を省略します。

### プロパティ

|プロパティ|C++|タイプ、デフォルト値、および用途|
|---|---|---|
|`value`|`get_value`、`set_value`|`double`、デフォルトは0.0です。有限の数でなければならず、越境値は現在の範囲に収まります。|
|`minimum`|`get_minimum`、`set_minimum`|`double`、デフォルトは0.0です。有限であり、現在の上限より小さいです。|
|`maximum`|`get_maximum`、`set_maximum`|`double`、デフォルトは100.0です。有限であり、現在の下限より大きいです。|
|`step`|`get_step`、`set_step`|`double`、デフォルトは1.0です。正の有限数で、上下の調整に使用されます。|
|`decimal_places`|`get_decimal_places`、`set_decimal_places`|`uint32_t`、デフォルトは0で、0から17までをサポートします。固定小数点の表示を制御し、小数点を有効にすると英数字の小数点を受け入れます。|
|`focusable`|`is_focusable`|読み取り専用です。編集エリア、増加エリア、減少エリアは同じコントロールの異なるフォーカス位置です。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`numericupdown(name)`|`numericupdown(name)`|コントロールを構築します。`value`または`set_value()`を使用して初期数値を設定します。|

### イベント

|イベント|パラメータタイプ|トリガー条件|
|---|---|---|
|`on_value_changed`|`event_args_t`|送信された値が実際に変更されます。編集バッファの毎回の入力は必ずしも数値の変化を引き起こすわけではありません。|
|`on_minimum_changed`、`on_maximum_changed`|`event_args_t`|範囲の端が実際に変更されます。範囲の変更はトリガー値の変化に直ちに続く可能性があります。|
|`on_step_changed`、`on_decimal_places_changed`|`event_args_t`|ステップまたは小数点の桁数が実際に変更されます。|

## 実行できるサンプル

この例ではゲインを0.00から2.00に制限し、初期値は0.75です。上の調整エリアをクリックすると1.00が表示され、状態テキストが更新されます。編集エリアをアクティブにすると、直接数値を入力してEnterキーを押して送信できます。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)をに従いEngineを起動します。以下のコマンドは、チュートリアルリポジトリのルートディレクトリにあるx64デベロッパーCMDで実行します。サンプルSDKのパスを実際のインストール場所に変更してください。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/numericupdown/cpp -B .work/example_numericupdown -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_numericupdown --config Release
.work\example_numericupdown\Release\tutorial_numericupdown.exe
```

Visual Studioジェネレーターは実行可能ファイルを`Release`サブディレクトリに配置します。シングルコンフィギネーションのNinjaジェネレーターは直接ビルドディレクトリに出力します。

<<< ../../../../../examples/guide/controls/selection-and-status/numericupdown/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\numericupdown\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/numericupdown/python/numericupdown_demo.py

### 実行結果

![numericupdown独立例程効果](/images/ja/numericupdown_demo.png)

## よくある質問とレイアウト実践

- 負号、小数点、必要な数字の桁数、および右側の調整エリアの幅を予約してください。`font`のサイズを増やすと、同時に`rect.height`も増加します。
- `decimal_places`は形式と文字フィルタリングを制御し、ビジネス精度は個別に定義する必要があります。`value`を直接設定することで、`step`のシーケンス上にない有限値の入力も許可されます。
- 調整範囲を設定する際は、`minimum < maximum`の一方を保持できるように設定してください。データを保存する際に`value`を読み出し、無効な入力は現在の値のフォーマット表示を復元します。
- 編集エリアのフォーカス内ではUpまたはDownを使用して調整でき、フォーカスが増加または減少エリアにある場合はEnterまたはSpaceを使用できます。

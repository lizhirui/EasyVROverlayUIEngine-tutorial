# splitter

`splitter`ドラッグ可能な分割バーを使用して、2つの直接子コントロールを配置します。これはナビゲーションや詳細表示、編集エリアやプレビュー、上下の出力エリアに適しています。方向は分割バー自体を表し、`vertical`は内容を左右の2つのエリアに分け、`horizontal`は上下の2つのエリアに分けます。

継承された一般的なメンバーについては[コンテナインターフェース](/ja/guide/controls/common-api#container-control)を参照してください。

## 既定の外観

デフォルトは`orientation = vertical`、`split_position = 0.5`です。スクリーンショットには、エリアを区別するために2つの異なる色の`panel`を追加します。分割バーと比率はデフォルトのままです。

![splitterデフォルト外観](/images/ja/splitter_default.png)

## プロパティの比較

左側は`vertical`で、2つのエリアは使用可能な幅を均等に分けます。右側は`horizontal`で、最初の`panel`は分割バーを除いた使用可能な高さの38％を占めます。方向と比率は独立して設定できます。

![splitter属性比較](/images/ja/splitter_comparison.png)

## APIリファレンス

Pythonでは表の属性名を使用します。C++では対応するメソッドを使用して読み書きし、`control_base &source`と表の型の参照を使用してイベントをサブスクライブします。追加フィールドのない`event_args_t`は状態が更新されたことを意味し、コールバックは`source`を通じて新しい値を読み取ります。Pythonの対応するイベントタイプ名は`_t`を省略します。

### プロパティ

|プロパティ|C++|タイプ、デフォルト値、および用途|
|---|---|---|
|`orientation`|`get_orientation`、`set_orientation`|デフォルトは`vertical`です。C++では`orientation_t`を使用し、Pythonでは`orientation`を使用します。|
|`split_position`|`get_split_position`、`set_split_position`|デフォルトは0.5です。有効範囲は`[0.0, 1.0]`で、必ず有限でなければなりません。計算時には軸方向の全長から分割バーを差し引きます。|
|`control_list`|`get_control_list`|最大2つの直接子コントロールです。集合の順序は第一、第二のエリアに対応します。|
|`active_item_list`|`get_active_item_list`|継承された読み取り専用のアクティブな子コントロールのリストです。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`splitter(name)`|`splitter(name)`|2つのエリアを持つコンテナを構築します。|
|`control_list.add(item)`|`get_control_list().add(item)`|エリアの順序に従ってコントロールを追加します。|
|`control_list.remove(item)`|`get_control_list().remove(item)`|エリア内のコントロールを削除します。|

### イベント

|イベント|パラメータのタイプ|トリガー条件|
|---|---|---|
|`on_orientation_changed`、`on_split_position_changed`|`event_args_t`|方向または比率の実際の変化。比率イベントは1回のドラッグで複数回トリガーできます。|
|`on_split_start`|`event_args_t`|分割バーのドラッグ操作を開始します。|
|`on_split_end`|`interaction_end_event_args_t`|ドラッグを終了します。現在の実装ではデフォルトのイベント値が送信され、`cancelled`は偽です。|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|エリア内のコントロールの追加または削除。|

## 実行できるサンプル

2エリアワークステーションは42％の第一エリアの幅から開始します。分割バーを右にドラッグすると、左右の`panel`が再配置され、底部の状態は「レイアウト比率が更新されました」となります。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)に従ってEngineを起動します。以下のコマンドはチュートリアルリポジトリのルートディレクトリのx64開発者CMDで実行します。サンプルSDKのパスを実際のインストール場所に変更してください。

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/splitter/cpp -B .work/example_splitter -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_splitter --config Release
.work\example_splitter\Release\tutorial_splitter.exe
```

Visual Studioジェネレーターは実行可能ファイルを`Release`サブディレクトリに配置します。シングルコンフィギネーションのNinjaジェネレーターは直接ビルドディレクトリに出力します。

<<< ../../../../../examples/guide/controls/layout-and-container/splitter/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\splitter\python\run.cmd
```

<<< ../../../../../examples/guide/controls/layout-and-container/splitter/python/splitter_demo.py

### 実行結果

![splitter独立例程効果](/images/ja/splitter_demo.png)

## よくある質問とレイアウト実践

- `panel`を使用して各セクション内の複数のコントロールを包装します。`splitter`は2つの直接子コントロールの矩形を管理し、内部レイアウトはそれぞれのローカル座標を使用します。
- 分割バーはデフォルトで8の論理ピクセルを占め、比率は分割バーを除いた長さに基づいています。0または1の近くに配置されると、セクションが文字を表示できないほど縮小する可能性があります。
- 連続フィードバックには`on_split_position_changed`を使用し、ドラッグが完了した後はユーザーのレイアウトを`on_split_end`で保存できます。
- 方向を切り替えることが許可される場合は、左右と上下の2つのレイアウトでの最小読み取り可能サイズを確認してください。

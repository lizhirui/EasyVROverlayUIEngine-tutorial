# panel

`panel`は、親子関係を使ってコントロールを1つのまとまりにします。接続状態、特定の領域に関する設定、操作領域、または互いに排他的な選択肢をまとめるときに使えます。`control_list`に追加した子の座標は`panel`を基準にするため、`panel`を移動するとグループ全体が移動します。

継承された一般的なメンバーは[コンテナインターフェース](/ja/guide/controls/common-api#container-control)を参照してください。

## 既定の外観

デフォルトでコントロールの背景とフレームを描画します。空の`panel`はその矩形の輪郭のみを表示し、子コントロールを追加した後はそのグループの局部座標を使用して描画します。

![panelデフォルト外観](/images/ja/panel_default.png)

## プロパティの比較

左側はデフォルトのフレーム、背景、タイトルを保持します。右側は`background_color`を変更し、内部に背景付きの別の`panel`を追加します。デフォルトのフレームはSDKのレンダリングスタイルに依存し、カスタムフレームは派生コントロールのレンダリングで描画できます。

![panel属性比較](/images/ja/panel_comparison.png)

## APIリファレンス

Pythonでは表の属性名を使用します。C++では対応するメソッドを使用して読み書きし、`control_base &source`と表の型の参照を使用してイベントをサブスクライブします。追加フィールドのない`event_args_t`は状態が更新されたことを意味し、コールバックは`source`を使用して新しい値を読み取ります。Pythonの対応するイベントタイプ名は`_t`を省略します。

### プロパティ

|プロパティ|C++|タイプ、デフォルト値、および用途|
|---|---|---|
|`rect`|`get_rect`、`set_rect`|継承された論理的な矩形で、子コントロールの位置はその矩形に基づいています。|
|`background_color`|`get_background_color`、`set_background_color`|継承されたRGBA背景色で、デフォルトではSDKのコントロール背景色を使用します。|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|継承された表示とインタラクティブなオン/オフのスイッチ。一組のコントロールを制御するために使用できます。|
|`control_list`|`get_control_list`|読み取り専用のコレクションエントリで、追加、削除、ソート、および直接の子コントロールのインデックスに使用されます。|
|`active_item_list`|`get_active_item_list`|読み取り専用で、現在活動中の子コントロールのリストです。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`panel(name)`|`panel(name)`|通常のコンテナを構築します。|
|`control_list.add(item)`|`get_control_list().add(item)`|子コントロールをその親層に追加します。|
|`control_list.remove(item)`|`get_control_list().remove(item)`|子コントロールをコレクションから除外し、オブジェクトを返します。|
|`show()`、`hide()`|`show()`、`hide()`|この一組のコンテンツを表示または非表示にします。|

### イベント

|イベント|パラメータタイプ|トリガー条件|
|---|---|---|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|直接の子コントロールの追加または削除。`item`はコントロール、`index`はコレクションの位置です。|
|`on_background_color_changed`、`on_visible_changed`、`on_enabled_changed`|`event_args_t`|継承された背景または状態の変化。|
|`on_moved`、`on_size_changed`|`event_args_t`|継承された位置またはサイズの変化。|

## 実行できるサンプル

メインの`panel`は同期サービスをグループ化して表示します。内層の`panel`は接続の詳細を表示し、「接続の詳細を非表示に」をクリックすると全体が非表示になり、再クリックすると復元します。復元後のインターフェースが表示されます。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)に従ってEngineを起動します。以下のコマンドはチュートリアルリポジトリのルートディレクトリのx64開発者CMDで実行されます。サンプルSDKのパスを実際のインストール場所に変更してください。

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/panel/cpp -B .work/example_panel -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_panel --config Release
.work\example_panel\Release\tutorial_panel.exe
```

Visual Studioジェネレーターは実行可能ファイルを`Release`サブディレクトリに配置します。シングルコンフィギネーションのNinja生成器は直接ビルドディレクトリに出力します。

<<< ../../../../../examples/guide/controls/layout-and-container/panel/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\panel\python\run.cmd
```

<<< ../../../../../examples/guide/controls/layout-and-container/panel/python/panel_demo.py

### 実行結果

![panel独立例程効果](/images/ja/panel_demo.png)

## よくある質問とレイアウト実践

- ネストする際は、層ごとに親座標を使用します。最終的な表面矩形をクエリすると`absolute_rectangle`を読み取ることができ、レイアウト設定では`rect`を引き続き使用します。
- `panel`は固定サイズのグループに適しています。内容が視覚領域を超えてスクロールが必要な場合は[scrollpanel](./scrollpanel)を使用します。
- 同じ直接親コンテナ内の[radiobutton](../selection-and-status/radiobutton)は一組にまとめます。異なる`panel`を使用して独立したオプショングループを隔離します。

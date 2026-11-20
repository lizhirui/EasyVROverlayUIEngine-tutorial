# scrollpanel

`scrollpanel`はクリッピングビューポートのコンテナで、ログや設定、および単一スクリーンを超える他のコントロールをスクロールして表示するのに適しています。サブコントロールのローカル矩形がコンテンツの範囲を決定し、スクロールオフセットがビューポート内の位置を変更します。ビューポート外の領域はSDKによってクリッピングされます。

継承された一般的なメンバーについては[コンテナインターフェース](/ja/guide/controls/common-api#container-control)を参照してください。

## 既定の外観

デフォルトでは水平および垂直スクロールバーのオン/オフが両方とも真となり、オフセットは0から始まります。空のビューポートでは標準の背景とフレームが使用され、オン/オフが真の場合は対応するスクロールバーに領域が確保されます。

![scrollpanelのデフォルト外観](/images/ja/scrollpanel_default.png)

## プロパティの比較

両側は同じ6行の記録と同じビューポートを使用します。左側は上部に位置し、前3行を表示します。右側は下にスクロールして、後の記録を表示します。両側のコンテンツの超過部分はビューポートの端でクリッピングされます。

![scrollpanelの属性比較](/images/ja/scrollpanel_comparison.png)

## APIリファレンス

Pythonでは表の属性名を使用します。C++では対応するメソッドを使用して読み書きし、`control_base &source`と表の型の参照を使用してイベントをサブスクライブします。追加フィールドの`event_args_t`は状態が更新されたことを意味し、コールバックは`source`を使用して新しい値を読み取ります。Pythonの対応するイベントタイプ名は`_t`を省略します。

### プロパティ

|プロパティ|C++|タイプ、デフォルト値、および用途|
|---|---|---|
|`horizontal_scrollbar_visible`|`get_horizontal_scrollbar_visible`、`set_horizontal_scrollbar_visible`|無効。横向きスクロールバーとその占めるビューの面積を制御します。|
|`vertical_scrollbar_visible`|`get_vertical_scrollbar_visible`、`set_vertical_scrollbar_visible`|無効。縦向きスクロールバーと縦方向のスティックスクロールを制御します。|
|`control_list`|`get_control_list`|読み取り専用のサブコントロールの集合のエントリポイント。直接のサブコントロールの矩形がコンテンツの範囲の計算に参加します。|
|`visible`、`enabled`|`set_visible`、`set_enabled`|継承された読み書きオン/オフ。隠すか無効にするとスクロールバーのドラッグが停止します。|

### メソッド

|Python|C++|用途|
|---|---|---|
|`scrollpanel(name)`|`scrollpanel(name)`|クリッピング可能でスクロール可能なコンテナを構築します。日常的なアプリケーションでは、スクロールバーとハンドルを使用してビューを制御します。|
|`control_list.add(item)`|`get_control_list().add(item)`|コンテンツ座標を使用するサブコントロールを追加します。|

### イベント

|イベント|パラメータタイプ|トリガー条件|
|---|---|---|
|`on_horizontal_scrollbar_visible_changed`、`on_vertical_scrollbar_visible_changed`|`event_args_t`|対応するスクロールバーのオン/オフが実際に変更されます。|
|`on_viewport_changed`|`event_args_t`|継承されたビューの変化通知。スクロールまたはコンテンツの変化がビューに影響を与える場合にトリガーされます。|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|サブコントロールの追加または削除、パラメータには`item`および`index`が含まれます。|

## 実行できるサンプル

“同期ログ”は局部の縦座標に沿って6件のログを並べます。縦方向のスクロールを有効にし、横向きのスクロールバーを無効にします。ログエリアにレーザーを向けてスティックを下に動かすか、縦方向のスクロールバーをドラッグします。スクロール後の記録が表示されます。

[環境準備、構築とインストール](/ja/basics/01_install_and_setup)に従ってEngineを起動します。以下のコマンドはチュートリアルリポジトリのルートディレクトリのx64デベロッパCMDで実行します。サンプルSDKのパスを実際のインストール場所に変更してください。

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/scrollpanel/cpp -B .work/example_scrollpanel -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_scrollpanel --config Release
.work\example_scrollpanel\Release\tutorial_scrollpanel.exe
```

Visual Studioジェネレーターは実行可能ファイルを`Release`サブディレクトリに配置します。シングルコンフィギネーションのNinja生成器は直接ビルドディレクトリに出力します。

<<< ../../../../../examples/guide/controls/layout-and-container/scrollpanel/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\scrollpanel\python\run.cmd
```

<<< ../../../../../examples/guide/controls/layout-and-container/scrollpanel/python/scrollpanel_demo.py

### 実行結果

![scrollpanel独立例程効果](/images/ja/scrollpanel_demo.png)

## よくある質問とレイアウト実践

- 可視スクロールバーとコントロールの内容にスペースを確保します。上下にスクロールするだけの場合は横スクロールバーを閉じて、下部の視野領域を解放します。
- スクロールによって視野外の内容が隠れることがあります。子コントロールの実際の位置とサイズを確認し、特に内容の端が可視範囲を超えているかをチェックします。
- 子コントロールを隠した後でも、その矩形は内容範囲の計算に参加します。スクロール領域を短縮する必要がある場合は、子コントロールの矩形を更新するか、集合から対応するコントロールを削除します。
- オフセットは保護された実装インターフェースに属します。通常のアプリケーションではユーザーのインタラクションによるスクロールが行われ、`on_viewport_changed`で変化を観察します。図はWARPテストホストでオフセットを完全な行の境界に設定し、カットオフ効果を示しています。

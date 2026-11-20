# blank

`blank`は、名前、矩形および集合位置を保存できる、矩形および集合位置のプレースホルダコントロールです。デザイナーは、将来挿入されるカスタムコントロールの位置をこれで予約できます。アプリケーションがコンテンツを読み込む際に、そのローカル`rect`を読み取り、その集合項目を実際のコントロールで置き換えます。継承メンバーについては[公共コントロールインターフェース](/ja/guide/controls/common-api#control)をご覧ください。

## 既定の外観

`blank`自体は透明で描画されません。図に見える境界線は、親レベルの`panel`から来ており、プレースホルダ矩形が位置するコンテンツエリアを示しています。

![blankデフォルト外観](/images/ja/blank_default.png)

## プロパティの比較

左側の`panel`には`blank`が含まれ、右側の同じローカル位置には`label`が使用されます。実際のテキストとインタラクティブな機能は、置き換えられたコントロールから提供されます。

![blank属性比較](/images/ja/blank_comparison.png)

## APIリファレンス

C++の表のメソッドは属性を読み書きしますが、Pythonでは同名の属性を介してアクセスします。コールバックは`source`と`event`を受け取ります。表の各型付きイベント引数は`event_args_t`を継承し、基本パラメータ自体には追加フィールドがありません。Pythonの型名は`_t`を省略します。

### プロパティ

|プロパティ|C++でのメソッドアクセス|型、デフォルト値、および用途|
|---|---|---|
|`name`、`type`、`id`、`parent`、`disposed`|`get_name`、`get_type`、`get_id`、`get_parent`、`get_disposed`|読み書き規則は`control_base`と一致し、`type`は`blank`です。|
|`rect`、`tag`|`get_rect`、`set_rect`、`get_tag`、`set_tag`|継承されたローカル矩形とアプリケーションマーク。|
|`absolute_rectangle`、`owning_window`|`get_absolute_rectangle`、`get_owning_window`|継承された表面矩形と所属ウィンドウのクエリ。|
|`focused`|`get_focused`|読み取り専用で、`blank`はフォーカスを取得できません。|

### メソッド

|メソッド|用途|
|---|---|
|`blank(name)`|プレースホルダ項目を作成し、コンテナの`control_list`を使用して追加、削除、または置き換えます。|
|`dispose()`、`invalidate()`、`begin_invoke(callback)`|継承されたライフサイクルと所属スレッドスケジューリングメソッド。|

### イベント

|イベント|パラメータタイプ|トリガー条件|
|---|---|---|
|`on_moved`、`on_size_changed`、`on_viewport_changed`|`event_args_t`|継承されたジオメトリと視点通知。|
|`on_tag_changed`、`on_disposed`|`event_args_t`|継承されたマークと解放イベント。|
|`on_property_changed`|`property_changed_event_args_t`|公開可能な属性変更は`property_name`を介して行われます。|

## 公開メンバーの制限

`blank`はレイアウトと所有権機能を保持します。可視性、有効化、フォーカス、入力、背景、ツールチップ、およびTab属性は、このタイプの公開インターフェースには含まれていません。Pythonでアクセスされる隠されたメンバーにアクセスすると`AttributeError`が発生します。アプリケーションは、可視効果とインタラクティブイベントを置き換えられたコントロールに任せるべきです。

## 実行できるサンプル

「コンテンツの読み込み」をクリックすると、プログラムはプレースホルダ矩形を複製し、元のインデックスで`label`を挿入し、読み込み操作を無効にします。図は置き換えられた状態を示しています。

[環境準備、ビルド、およびインストール](/ja/basics/01_install_and_setup)でEngineを起動します。チュートリアルのルートディレクトリのx64デベロッパCMDでコマンドを実行し、サンプルでのSDKインストールパスを置き換えます。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/blank/cpp -B .work/example_blank -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_blank --config Release
.work\example_blank\Release\tutorial_blank.exe
```

シングルコンフィギネーションのNinjaを使用する場合は、ビルドディレクトリから直接実行ファイルを実行します。

<<< ../../../../../examples/guide/controls/command-and-display/blank/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\blank\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/blank/python/blank_demo.py

### 実行結果

![blank独立した例の実行効果](/images/ja/blank_demo.png)

## よくある質問とレイアウト実践

- まず`rect`と集合位置を記録し、その後元のプレースホルダ項目を削除します。置換作業は所属するUIスレッドで行います。
- 安定した識別子を保持する場合は、設計ファイル内の名称を使用して位置を検索できますが、集合内の名称は一意でなければなりません。
- 予約されたサイズは、最終的なコントロールのフォント、内側の余白、およびフォーカススタイルを考慮する必要があります。

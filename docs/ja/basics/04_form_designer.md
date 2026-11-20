# フォームの設計・プレビュー・コード出力

Form Designerでは、コントロールの配置、プロパティの編集、フォームのプレビュー、SDKコードのエクスポートができます。

![Form Designerの作業領域](/images/ja/vr_designer_annotated.png)

---

## Form Designerの作業領域

SteamVRとEngineを起動したら、DesktopでForm Designerを開くか、`D:\Tools\EasyVRUI\app\form_designer\easyvrui_form_designer.exe`を実行します。Desktopは`app/desktop/config.json`の登録を使って、インストール済みの`app/form_designer/easyvrui_form_designer.easyvrui`を参照します。デザイナーの画面は4つの領域に分かれています。

1. **上部の`menubar`と`toolbar`**
   - **ファイル／表示／レイアウト／実行／エクスポート**。`.easyvruifrm`の新規作成と読み込み、グリッドへのスナップ、キャンバスの拡大縮小、整列・幅と高さの統一・重なり順の調整に対応します。**VRプレビューの開始・停止**、**PythonやC++へのエクスポート**もここから操作します。
2. **左側のツールボックスとオブジェクトツリー**
   - **コントロールバー**。`label`、`button`、`textbox`、`combobox`、`listbox`、`listview`、`grid`、`checkbox`、`radiobutton`、`numericupdown`、`slider`、`progressbar`、`panel`、`scrollpanel`、`tabcontrol`、`treeview`、`image`、`screen`、`splitter`、`menubar`などのすべての内蔵コントロールを提供します。
   - **オブジェクトツリー**はコントロールの親子階層を表示します。コントロールが重なっていても、ツリーから目的のコントロールを選択できます。
3. **中央のデザインキャンバス**
   - VRウィンドウのレイアウトを画面上で編集します。グリッドへのスナップ、範囲選択による複数選択、ドラッグでのサイズ変更、変更の取り消しとやり直し（`Ctrl+Z`／`Ctrl+Y`）に対応します。
4. **右側のプロパティ欄**
   - `name`は一番上に固定され、残りの項目は名前順に並びます。テキスト、色、フォント、曲率、`tooltip_text`、`tag`などを編集できます。

---

## メッセージを送信するフォームを作る

この例では、`label`が案内を表示し、`textbox`がメッセージを受け取り、`button`で送信します。

### 1. 新規作成してデザインファイルを保存する

**ファイル → 新規**でフォームを作成します。起動時の空のフォームも使えます。**ファイル → 保存**を選び、`quick_shout_window.easyvruifrm`として保存します。

::: tip フォームのクラス名
プロパティ欄にあるフォームの`name`は**読み取り専用**で、`.easyvruifrm`の拡張子を除いたファイル名に対応します。`quick_shout_window.easyvruifrm`として保存すると、エクスポートされるクラス名は`quick_shout_window`になります。名前を変える場合はファイルメニューのデザインファイルを移動する機能を使います。フォーム名も自動的に更新されます。
:::

### 2. コントロールをキャンバスに追加する

左側の**ツールボックス**から、次の3つのコントロールを中央のキャンバスへ順にドラッグします。
1. 上部に`label`を配置します。
2. 中央に`textbox`を配置します。
3. 下部に`button`を配置します。

コントロールの枠をドラッグするとサイズを変更できます。`Ctrl`を押しながら複数のコントロールを選ぶと、上部の**レイアウト**メニューから左揃えや幅の統一を行えます。

### 3. コントロールのプロパティを設定する

フォームと各コントロールを順に選択し、右側の**プロパティ欄**で次の値を設定します。

|対象|プロパティ|設定値|用途|
|---|---|---|---|
|**フォーム本体**（キャンバスの空白をクリック）|`title`|`静音快捷喊话条`|タイトルバーに表示する名前|
|**`label`**|`name`|`label_hint`|エクスポートしたコードでのメンバー名。`型_用途`のように型名と用途を組み合わせます。|
|**`label`**|`text`|`输入想说的话：`|入力欄に添える案内|
|**`textbox`**|`name`|`textbox_message`|アプリ側のコードでは`self.ui.textbox_message`または`ui->textbox_message`で参照します。|
|**`textbox`**|`tag`|`chatbox_input`|アプリが識別に使う任意の文字列|
|**`button`**|`name`|`button_send`|ボタンに対応するメンバー名|
|**`button`**|`text`|`发送`|ボタンに表示するテキスト|
|**`button`**|`tooltip_text`|`把文本框里的内容发出去`|ボタンにレーザーを合わせたときの説明|

### 4. VRでリアルタイムプレビュー

図は、この章の`quick_shout_window.easyvruifrm`をForm Designerで開いた状態です。オブジェクトツリー、キャンバス、プロパティ欄は、すべて同じフォームを参照しています。画面は日本語表示の撮影例です。

![この章のデザインファイルのキャンバスレイアウト](/images/ja/basics_form_design.png)

`easyvrui_engine.exe`が実行中であることを確認し、ツールバーで**実行 → 開始**を選びます。
- 未保存の変更がある場合は、保存してから開始するよう促されます。
- フォームがSteamVRで動作します。`textbox`をクリックできることや、`button`にレーザーを合わせると`tooltip_text`が表示されることをその場で確認できます。
- プレビューを終えたら**停止**を選び、編集に戻ります。

---

## コードのエクスポートとアプリ側の処理

レイアウトができたら、**エクスポート → Pythonをエクスポート**または**エクスポート → C++をエクスポート**を選択します。
- Pythonでは、`.easyvruifrm`と同じディレクトリに`quick_shout_window.py`を生成します。
- C++では、同じディレクトリに`quick_shout_window.h`と`quick_shout_window.cpp`を生成します。各コントロールの初期化はコンストラクターに含まれます。

### アプリ側でイベント処理を実装する

エクスポートしたファイルには**UIの構築コード**が含まれます。ここでコントロールを作成し、プロパティを設定し、`control_list`に追加します。すべての子コントロールは`name`と同じ名前の公開メンバーになります。

**コンポジションで組み合わせます**。アプリ側のクラス（例は`my_shout_app`）で`quick_shout_window`をインスタンス化して保持します。`ui`メンバーからボタンのクリックイベントを登録します。クリック時には、アプリ側のメソッドが`textbox`の入力を読み、`label`を更新します。

::: code-group
```python [Python（my_shout_app.py）]
from easyvrui import run
from quick_shout_window import quick_shout_window

class my_shout_app:
    def __init__(self):
        self.ui = quick_shout_window()
        self.ui.button_send.on_click += self.button_send_click

    def button_send_click(self, source, event):
        message = self.ui.textbox_message.text
        self.ui.label_hint.text = f"已发送：{message}"

    def show(self):
        self.ui.show()

def main():
    app_main = my_shout_app()
    app_main.show()
    run("quick_shout_app")

if __name__ == "__main__":
    main()
```

<<< ../../../examples/basics/04_form_designer/cpp/main.cpp
:::

コンポジションを使うと、**フォームをエクスポートし直してもアプリ側のコードは保持されます**。`.easyvruifrm`でコントロールのサイズや色を変更したり、コントロールを追加したりして再出力すると、`quick_shout_window.py`、または`quick_shout_window.h`と`quick_shout_window.cpp`だけが更新されます。`my_shout_app`のイベント登録と処理はそのまま使えます。

---

## エクスポート前後の動作を確認する

C++アプリは、生成コードの`quick_shout_window`インスタンスを保持し、公開されている`on_click`に処理を登録します。Pythonでは`my_shout_app.ui`が同じ役割を担います。レイアウトのエクスポート後も、アプリは公開メンバーとイベントを介してウィンドウを操作できます。

![エクスポートしたコードを起動した直後のwindow](/images/ja/basics_form_initial.png)

テストホストが`textbox_message`に`Ready for sync`と入力します。`button_send`を押すと、アプリ側のコールバックが入力を読み取って`label_hint`を更新します。

![送信したテキストを表示するlabel](/images/ja/basics_form_sent.png)

[コントロール一覧](/ja/guide/)で各コントロールのプロパティ、イベント、サンプルを参照できます。エクスポート後にコードで描画要素を追加する場合は、[blank](/ja/guide/controls/command-and-display/blank)のプレースホルダーを差し替える例を参照してください。

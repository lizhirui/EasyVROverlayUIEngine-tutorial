# アプリマニフェスト

`.easyvrui`はUTF-8のJSON形式を使うアプリマニフェストです。DesktopとFile ManagerはSDKでマニフェストを読み取り、呼び出し元のコンピューターでアプリを起動します。相対パスと子プロセスの作業ディレクトリは、マニフェストが置かれたディレクトリを基準にします。付属の一般アプリでは、対応するプログラムとマニフェストがインストール先の`app/...`で同じディレクトリに置かれます。たとえば`app/demo/python/easyvrui_demo_python.easyvrui`では、`launch.script`は`main.py`です。

## マニフェストの構成

```json
{
    "id": "example",
    "name":
    {
        "en": "Example",
        "zh": "示例",
        "ja": "サンプル"
    },
    "type": "application",
    "icon":
    {
        "path": "example.ico"
    },
    "launch":
    {
        "runtime": "native",
        "executable": "example.exe",
        "argument_list": []
    }
}
```

|フィールド|ルール|
|---|---|
|`id`|アプリID。省略すると、拡張子を除いたマニフェストのファイル名を使います。|
|`name`|言語ごとの表示名を設定するオブジェクト。空でない`en`が必須です。|
|`type`|任意。`application`、`desktop`、`layout`、`ime`のいずれかを指定します。既定値は`application`です。|
|`icon`|任意のアイコンオブジェクト。`path`または`base64`のいずれかを指定します。|
|`launch`|必須の起動設定オブジェクト|

表は、有効なトップレベルフィールドのすべてです。単一インスタンスの制御はアプリ自身が行います。

システム言語の完全なタグを最初に照合し、見つからないと地域や用字系のサブタグを順に除き、最後に`en`へフォールバックします。たとえば`zh-Hant-TW`では、`zh-hant-tw`、`zh-hant`、`zh`、`en`の順に探します。タグの大文字と小文字は区別せず、アンダースコアはハイフンとして扱います。正規化後にタグが重複するとエラーになります。

`icon.path`には外部画像ファイルを指定します。`icon.base64`には、Windowsの画像デコーダーで読み込めるPNGやICOなどのファイルを、標準のBase64文字列として埋め込めます。

```json
{
    "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScLttAAAAABJRU5ErkJggg=="
}
```

## ネイティブプログラム

`launch.runtime`が`native`の場合は、次のフィールドを指定します。

|フィールド|ルール|
|---|---|
|`runtime`|必須、固定値は`native`です|
|`executable`|必須。実行ファイルのパス。相対パスはマニフェストのディレクトリを基準にします。|
|`argument_list`|任意。文字列引数の配列。既定値は`[]`です。|

## Pythonプログラム

`launch.runtime`が`python`の場合は、次のフィールドを指定します。

|フィールド|ルール|
|---|---|
|`runtime`|必須、固定値は`python`です|
|`script`|必須。Pythonのメインスクリプトのパス。相対パスはマニフェストのディレクトリを基準にします。|
|`argument_list`|任意。文字列引数の配列。既定値は`[]`です。|

```json
{
    "id": "python_example",
    "name":
    {
        "en": "Python Example",
        "zh": "Python示例",
        "ja": "Pythonサンプル"
    },
    "launch":
    {
        "runtime": "python",
        "script": "main.py",
        "argument_list": []
    }
}
```

SDKはPATHから`python.exe`を探し、`python.exe -B <メインスクリプト> <引数リスト>`を実行します。指定したメインスクリプトは実在する必要があります。SDKは、まずマニフェストのディレクトリから親の方向へインストールルートを探し、見つからなければ起動元が使うフレームワークのディレクトリを調べます。インストール先が見つかると、子プロセスの`PYTHONPATH`の先頭に`sdk/api/python/`を追加して元の値を保持し、`EASYVRUI_NATIVE_DIR`にも同じディレクトリを設定します。さらに`PYTHONDONTWRITEBYTECODE=1`を設定します。アプリのスクリプトは`import easyvrui`を直接実行できます。Pythonインタープリターは、インストール済みのx64ネイティブ拡張と同じCPythonバージョンを使用します。

## パラメータと接続情報

`argument_list`の引数は項目ごとにそのまま渡します。空文字列、空白、引用符、バックスラッシュ、Unicode文字も保持します。`launch_application(manifest_path, extra_argument_list)`を呼び出すと、追加引数はマニフェストの引数の後ろに追加されます。名前、識別子、パス、引数にNUL文字は指定できません。

マニフェストと追加引数のどちらにもリモート接続オプションがない場合、SDKは呼び出し元プロセスの`--easyvrui-host=`、`--easyvrui-port=`、`--easyvrui-access-credential=`、`--easyvrui-public-key-fingerprint=`を子プロセスに引き継ぎます。明示的に指定するときは、[リモートSDKの接続規則](./engine_protocol)に従ってすべての項目を設定します。

## Desktopのアプリ一覧 {#desktop-application-list}

Desktopは2つの設定を読み取ります。インストーラーは`app/desktop/config.json`に内蔵アプリを登録します。ユーザー設定は`%USERPROFILE%\easyvrui\desktop\config.json`にあり、`USERPROFILE`が設定されていない場合は`HOME`を使用します。

どちらの設定も`application_list`にマニフェストのパスを記録します。相対パスは、そのパスを記載した設定ファイルのディレクトリを基準にします。次はシステム設定の例です。

```json
{
    "application_list":
    [
        "../demo/cpp/easyvrui_demo_cpp.easyvrui",
        "../form_designer/easyvrui_form_designer.easyvrui"
    ]
}
```

Desktopは一般アプリの有効なマニフェストを読み取り、アプリ`id`で照合してメモリ内で統合します。IDのASCII英字は大文字と小文字を区別しません。システム設定が優先され、同じファイル内の重複には最初の有効な登録を使います。マニフェストや起動先が無効な項目は一覧から除外します。更新すると両方の設定を読み直します。

アプリを追加する際、DesktopはそのIDが統合後のリストに既に存在するかをチェックします。追加と削除はユーザー設定のみを更新します。システム設定はインストーラーによって生成され、内蔵アプリの登録パスはこのファイルによって管理されます。

## File Managerの拡張子の関連付け

File Managerは`app/file_manager/file_manager.json`から`association_map`を読み取ります。キーは先頭に`.`を付けた拡張子で、大文字と小文字を区別しません。値は`.easyvrui`マニフェストのパスです。相対パスはFile Managerの実行ファイルのディレクトリを基準にします。フォームのデザインファイルをインストール済みのForm Designerに関連付けるには、次のエントリーを追加します。

```json
{
    "association_map":
    {
        ".easyvruifrm": "../form_designer/easyvrui_form_designer.easyvrui"
    }
}
```

File Managerで`.easyvrui`をダブルクリックすると、対応するアプリが起動します。関連付けられた拡張子のファイルをダブルクリックすると、SDKはそのファイルの絶対パスを追加パラメータとして目標アプリに渡します。

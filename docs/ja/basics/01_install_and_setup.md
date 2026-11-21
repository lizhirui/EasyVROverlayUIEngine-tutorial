# 環境構築・ビルド・インストール

この章では、WindowsでEasyVROverlayUIEngineをソースからビルドし、実行環境をインストールします。

::: tip 説明
ルートの`build.bat`でコンポーネントをビルドし、`install.bat`で実行環境をインストールします。**Python**でVRアプリを開発する場合は、インストール済みのネイティブ拡張を使用できます。
:::

---

## 手順1　必要な環境

ビルドを始める前に、次の要件を確認します。

|項目|最低要件|補足|
|---|---|---|
|**OS**|Windows 10または11（64ビット）|EngineはWindowsとDirect3D 11を使用します。現在の対応OSはWindowsです。|
|**GPUとVR環境**|Direct3D 11対応のGPU、SteamVR、VRヘッドセット|一般的なSteamVRの動作要件を満たしてください。|
|**Python**|CPython 3.11以降の64ビット版|インストール時に**Add python.exe to PATH**を選択し、CMDで`python`を直接実行できるようにします。|
|**C++ビルドツール**|C++20に対応するMSVC x64、Windows SDK、CMake 3.24以降、Ninja|Visual Studioの「C++によるデスクトップ開発」ワークロードと、CMakeおよびNinjaのコンポーネントをインストールします。|

::: warning CMDのみを使用し、PowerShellは使用しないでください。
ビルドやスクリプトの実行には、Windowsの**コマンドプロンプト（CMD）**を使用します。`Win+R`を押して`cmd`を入力すると起動できます。PowerShellでは引用符、引数、環境変数の扱いがCMDと異なり、ビルドやインストールのスクリプトが正しく動かない場合があります。
:::

---

## 手順2　Engine、SDK、付属アプリをビルドする

CMDでソースリポジトリのルートに移動し、`build.bat`を実行します。

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
build.bat
```

既定の構成はRelease、並列ジョブ数は8です。構成は`--configuration`、ジョブ数は`--parallel`で指定できます。

```cmd
build.bat --configuration Release --parallel 8
```

### コンポーネントごとのビルドディレクトリ

ルートの`build.bat`はCMDでMSVC x64環境を一度初期化し、12個のコンポーネントの`build.bat`を順に呼び出します。各コンポーネントは自身の`build/`で設定とコンパイルを実行します。表の出力先は各コンポーネントからの相対パスです。

|コンポーネントのディレクトリ|ビルドの出力|
|---|---|
|`sdk/engine_interface`|`build/lib/`に静的ライブラリ、DLLのインポートライブラリ、CMakeパッケージ。`build/bin/`にDLL、`build/include/`に公開ヘッダー。|
|`sdk/api/python`|`build/bin/`にPython SDKパッケージと`engine_interface_native*.pyd`。|
|`engine`|`build/bin/`に`easyvrui_engine.exe`とSteamVRのアクションリソース。|
|`app/desktop`、`app/form_designer`、`app/file_manager`、`app/task_manager`、`app/demo/cpp`|それぞれの`build/bin/`に実行ファイルとビルドで生成したリソース。|
|`app/layout/standard_104`、`app/ime/cn/easyvrui_pinyin`、`app/ime/en/easyvrui_english`、`app/ime/jp/easyvrui_japanese`|それぞれの`build/bin/`に実行ファイル。中国語ピンインと日本語のIMEは`build/bin/rime/`にコンパイル済み辞書も生成します。|

### コンポーネントを個別にビルドする

各コンポーネントのディレクトリから`build.bat`を直接実行できます。Pythonのネイティブ拡張やC++アプリを個別にビルドする場合は、先に`sdk/engine_interface`を同じ構成でビルドします。続くビルドは`sdk/engine_interface/build/`のSDKを使います。次の例ではSDKをビルドしてからDesktopを個別にビルドします。

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo\sdk\engine_interface"
build.bat --configuration Release
cd /d "D:\program\project\EasyVROverlayUIEngine\repo\app\desktop"
build.bat --configuration Release
```

ビルドが成功すると、各コンポーネントの`build/configuration.txt`に構成を記録します。依存ソース、Rimeのスキーマと辞書はリポジトリに含まれています。ツールチェーンをインストールすれば、オフラインでビルドできます。

---

## 手順3　実行環境をインストールする

12個のコンポーネントをビルドしたら、ソースリポジトリのルートから`install.bat`を実行します。CMDのインストーラーは各コンポーネントの`build/`を参照し、すべてのビルドが完了し、構成がそろっていることを確認します。Python DemoとC++ APIヘッダーは各ソースディレクトリからコピーします。インストール先にはソースリポジトリと分離したディレクトリを選びます。

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
install.bat "D:\Tools\EasyVRUI"
```

インストール先の引数を省略すると、`install.bat`が入力を求めます。


新規インストールでは次の構成になります。アプリの相対パスは`repo/app/`のディレクトリ構成に対応します。

```text
D:\Tools\EasyVRUI\
├── installation.json
├── bin\
│   ├── easyvrui_engine.exe
│   ├── actions\                    # SteamVRアクションマニフェストと既定バインディングJSON（actions.json、bindings_*.json）
│   └── config.json
├── app\
│   ├── desktop\
│   │   ├── easyvrui_desktop.exe
│   │   └── config.json
│   ├── form_designer\
│   │   ├── easyvrui_form_designer.exe
│   │   ├── easyvrui_form_designer.easyvrui
│   │   └── resources\             # Form Designerのリソース
│   ├── file_manager\
│   │   ├── easyvrui_file_manager.exe
│   │   ├── easyvrui_file_manager.easyvrui
│   │   ├── easyvrui_volume_query.exe # ボリューム照会用の補助プログラム
│   │   └── file_manager.json         # ファイルの関連付け
│   ├── task_manager\
│   │   ├── easyvrui_task_manager.exe
│   │   └── easyvrui_task_manager.easyvrui
│   ├── demo\
│   │   ├── cpp\
│   │   │   ├── easyvrui_demo_cpp.exe
│   │   │   ├── easyvrui_demo_cpp.easyvrui
│   │   │   └── resources\          # C++ Demoのリソース
│   │   └── python\
│   │       ├── main.py
│   │       ├── demo\               # Python Demoの内部UIモジュールと画像リソース
│   │       ├── requirements.txt
│   │       └── easyvrui_demo_python.easyvrui
│   ├── layout\standard_104\easyvrui_layout_standard_104.exe
│   └── ime\
│       ├── cn\easyvrui_pinyin\
│       │   ├── easyvrui_ime_chinese_pinyin.exe
│       │   └── rime\chinese_pinyin\ # ピンインIME専用のRime辞書・スキーマデータ
│       ├── en\easyvrui_english\easyvrui_ime_english.exe
│       └── jp\easyvrui_japanese\
│           ├── easyvrui_ime_japanese.exe
│           └── rime\japanese\      # 日本語IME専用のRime辞書・スキーマデータ
└── sdk\
    ├── api\
    │   ├── cpp\
    │   │   ├── include\            # C++公開ヘッダ
    │   │   └── third_party\json\    # C++ API付属のJSONヘッダー
    │   └── python\
    │       ├── easyvrui\           # Python SDKラッパーパッケージ
    │       ├── engine_interface_native*.pyd
    │       ├── engine_interface_native.json
    │       └── requirements.txt
    └── engine_interface\
        ├── include\                # ネイティブAPI公開ヘッダとjson.hpp
        ├── lib\
        │   ├── engine_interface_static.lib
        │   ├── engine_interface.lib
        │   └── cmake\EngineInterface\ # CMake find_packageエクスポート設定
        └── bin\engine_interface.dll
```

新規インストール時に`install.bat`が`bin/config.json`を作成し、Engineが初回起動時に接続用の認証情報を生成します。`installation.json`はインストール先のルートを識別し、ビルド構成、Pythonのバージョン、アプリマニフェストのパスを記録します。`bin/config.json`の`desktop`と`provider_list`では、`bin/`からの相対パス`../app/...`で実行ファイルを指定します。`app/desktop/config.json`には、Desktopのディレクトリからの相対パスで付属アプリを登録します。例は`../demo/cpp/easyvrui_demo_cpp.easyvrui`です。各[アプリマニフェスト](/ja/reference/application_manifest)の`launch.executable`、`launch.script`、子プロセスの作業ディレクトリは、そのマニフェストが置かれた場所を基準に決まります。

付属のC++アプリとPythonのネイティブ拡張は、既定で`engine_interface_static`を静的リンクします。`engine_interface.lib`はDLLのインポートライブラリで、共有リンクを選んだアプリが`engine_interface.dll`を使用します。Engine、SDK、アプリの組み込み言語パックは各バイナリに組み込まれます。アプリではSDKの`language_pack.load_directory()`で独自の言語パックを読み込めます。

Desktopは、システム設定と`%USERPROFILE%\easyvrui\desktop\config.json`のユーザー設定を、アプリIDを基準にメモリ内で統合します。再インストール時はシステム設定を再生成し、既存のEngine設定と接続用の認証情報を保持します。Desktopでの追加・削除はユーザー設定にだけ反映されます。

インストール先のPython SDKは`sdk/api/python/`にまとまっています。DesktopやFile ManagerがSDK経由でPythonアプリを起動すると、このディレクトリが子プロセスの`PYTHONPATH`の先頭に追加されます。元の値も保持されます。

---

## 手順4　起動を確認する

**SteamVR**を起動し、ヘッドセットとコントローラーの準備ができていることを確認します。CMDでEngine、C++ Demoの順に起動します。

```cmd
start "" "D:\Tools\EasyVRUI\bin\easyvrui_engine.exe"
start "" /D "D:\Tools\EasyVRUI\app\demo\cpp" "D:\Tools\EasyVRUI\app\demo\cpp\easyvrui_demo_cpp.exe"
```

SteamVRにサンプルの`window`が表示されれば、EngineとSDKが接続できています。

Python DemoはDesktopから起動できます。CMDから直接起動する場合は、インストール済みのネイティブ拡張とバージョン、アーキテクチャが一致するCPythonを使います。次のコマンドでDemoの依存関係をインストールし、共有SDKのディレクトリを検索パスの先頭に追加してから、アプリのディレクトリでメインスクリプトを実行します。

```cmd
python -m pip install -r "D:\Tools\EasyVRUI\app\demo\python\requirements.txt"
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
cd /d "D:\Tools\EasyVRUI\app\demo\python"
python -B main.py
```

### 起動後にVRでウィンドウが見つからない場合

視野内にウィンドウが表示されないときは、次の2点を確認します。

1. **起動時と現在でヘッドセットの向きが異なる**。ウィンドウは既定で起動時のヘッドセットの正面に作成されます。**`Ctrl + Alt + Pause`**を押すと、Engineは`body`の参照中心と`world`の空間オフセットを、現在のヘッドセットの正面にリセットします。
2. **SteamVRの準備ができていない**。SteamVRを起動し、ヘッドセットを認識していることを確認します。実行中にSteamVRが終了またはクラッシュした場合は、Engineとアプリを動かしたまま、旧SteamVRプロセスの完全な終了を待ってSteamVRを起動し直します。Engineが自動で再接続し、ウィンドウを再表示します。

次章では、VR空間でウィンドウを操作し、付属アプリを使用します。

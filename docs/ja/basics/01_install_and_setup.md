# 環境構築・ビルド・インストール

この章では、WindowsでEasyVROverlayUIEngineをソースからビルドし、実行環境をインストールします。

::: tip 説明
リポジトリにある`build.bat`と`install.bat`でビルドとインストールを実行できます。CMakeやコンパイラのコマンドを手書きする必要はありません。**Python**だけでVRアプリを開発する場合は、初回だけビルドとインストールを済ませれば、その後はC++コンパイラを設定したり実行したりせずに開発できます。
:::

---

## 手順1　必要な環境

ビルドを始める前に、次の要件を確認します。

|項目|最低要件|補足|
|---|---|---|
|**OS**|Windows 10または11（64ビット）|EngineはWindowsとDirect3D 11を使用します。現在の対応OSはWindowsです。|
|**GPUとVR環境**|Direct3D 11対応のGPU、SteamVR、VRヘッドセット|一般的なSteamVRの動作要件を満たしてください。|
|**Python**|CPython 3.11以降の64ビット版|インストール時に**Add python.exe to PATH**を選択し、CMDで`python`を直接実行できるようにします。|
|**C++ビルドツール**|Visual Studioの「C++によるデスクトップ開発」ワークロードとWindows SDK|Engine、ネイティブSDK、付属アプリをコンパイルします。Visual Studio付属のCMakeとNinjaを使用できます。|

::: warning CMDのみを使用し、PowerShellは使用しないでください。
ビルドやスクリプトの実行には、Windowsの**コマンドプロンプト（CMD）**を使用します。`Win+R`を押して`cmd`を入力すると起動できます。PowerShellでは引用符、引数、環境変数の扱いがCMDと異なり、ビルドやインストールのスクリプトが正しく動かない場合があります。
:::

---

## 手順2　ソースの取得とビルド

ここでは、リポジトリが`D:\program\project\EasyVROverlayUIEngine\repo`にあるものとします。別の場所にも配置できます。パスに中国語や空白を含められます。

**CMD**でリポジトリのディレクトリに移動し、`build.bat`を実行します。

```cmd
cd /d D:\program\project\EasyVROverlayUIEngine\repo
build.bat
```

コンパイルを高速化する場合は、Release設定と並列ジョブ数を指定できます。次は8ジョブの例です。

```cmd
build.bat --configuration Release --parallel 8
```

### ビルドスクリプトが行う処理

`build.bat`は次の処理を自動で行います。
1. Visual Studioのx64ツールチェーン、CMake、Ninjaを探します。
2. **Engine**をコンパイルします。`easyvrui_engine.exe`はGPU描画とSteamVRとの連携を担当するサービスプロセスです。
3. **ネイティブSDK**をコンパイルします。静的ライブラリ`engine_interface_static.lib`、DLLの`engine_interface.dll`、Pythonのネイティブ拡張`engine_interface_native*.pyd`を生成します。
4. Desktop、Form Designer、File Manager、Task Manager、C++ Demo、標準104キーの仮想キーボード、中国語・英語・日本語のIMEをコンパイルし、Python Demoと各アプリのリソースを用意します。

::: info オフラインビルド
サードパーティーの依存ソースはすべてリポジトリに含まれています。中国語ピンインと日本語のIMEが使うRimeエンジンと辞書も含むため、**オフラインでビルド**できます。初回のフルビルドは通常数分かかり、その後の差分ビルドは数秒で終わります。
:::

::: tip ビルドエラーの切り分け
Windows SDKの不足、PATHの競合、Visual Studioワークロードの選択漏れなどで`build.bat`が失敗することがあります。CMDの出力末尾にあるエラーメッセージを確認します。Gemini、GPT、Claudeなどの支援ツールにエラーの内容を渡し、不足するコンポーネントを調べることもできます。
:::

既定の出力先は、ソースリポジトリの外にある`../build/easyvrui_distribution`です。ビルド時に`--build-directory`で別の場所を指定した場合は、インストール時にも同じディレクトリを指定します。

---

## 手順3　実行環境をインストールする

ビルドが完了したら、`install.bat`を実行してプログラムとSDKを指定のディレクトリに配置します。以下では`D:\Tools\EasyVRUI`にインストールします。

```cmd
install.bat "D:\Tools\EasyVRUI"
```

パス引数を省略して`install.bat`を実行すると、CMDでインストール先の入力を求められます。

新規インストールでは次の構成になります。アプリの相対パスは`repo/app/`のディレクトリ構成に対応します。

```text
D:\Tools\EasyVRUI\
├── installation.json
├── bin\
│   ├── easyvrui_engine.exe
│   ├── actions\
│   └── config.json
├── app\
│   ├── desktop\
│   │   ├── easyvrui_desktop.exe
│   │   └── config.json
│   ├── form_designer\
│   │   ├── easyvrui_form_designer.exe
│   │   └── easyvrui_form_designer.easyvrui
│   ├── file_manager\
│   │   ├── easyvrui_file_manager.exe
│   │   └── easyvrui_file_manager.easyvrui
│   ├── task_manager\
│   │   ├── easyvrui_task_manager.exe
│   │   └── easyvrui_task_manager.easyvrui
│   ├── demo\
│   │   ├── cpp\
│   │   │   ├── easyvrui_demo_cpp.exe
│   │   │   └── easyvrui_demo_cpp.easyvrui
│   │   └── python\
│   │       ├── main.py
│   │       ├── demo\
│   │       ├── requirements.txt
│   │       └── easyvrui_demo_python.easyvrui
│   ├── layout\standard_104\easyvrui_layout_standard_104.exe
│   └── ime\
│       ├── cn\easyvrui_pinyin\
│       │   ├── easyvrui_ime_chinese_pinyin.exe
│       │   └── rime\chinese_pinyin\
│       ├── en\easyvrui_english\easyvrui_ime_english.exe
│       └── jp\easyvrui_japanese\
│           ├── easyvrui_ime_japanese.exe
│           └── rime\japanese\
└── sdk\
    ├── api\
    │   ├── cpp\include\
    │   └── python\
    │       ├── easyvrui\
    │       ├── engine_interface_native*.pyd
    │       ├── engine_interface_native.json
    │       └── requirements.txt
    └── engine_interface\
        ├── include\
        ├── lib\
        │   ├── engine_interface_static.lib
        │   ├── engine_interface.lib
        │   └── cmake\EngineInterface\
        └── bin\engine_interface.dll
```

`installation.json`はインストール先のルートを識別し、ビルド構成、Pythonのバージョン、アプリマニフェストのパスを記録します。`bin/config.json`の`desktop`と`provider_list`では、`bin/`からの相対パス`../app/...`で実行ファイルを指定します。`app/desktop/config.json`には、Desktopのディレクトリからの相対パスで付属アプリを登録します。例は`../demo/cpp/easyvrui_demo_cpp.easyvrui`です。各[アプリマニフェスト](/ja/reference/application_manifest)の`launch.executable`、`launch.script`、子プロセスの作業ディレクトリは、そのマニフェストが置かれた場所を基準に決まります。

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

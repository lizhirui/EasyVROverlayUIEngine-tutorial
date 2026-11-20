---
layout: home

hero:
  name: EasyVROverlayUIEngine
  text: SteamVR向けのネイティブ空間UIエンジン
  tagline: C++またはPythonでSteamVR上の空間UIを開発できます。ビジュアルレイアウト、複数ウィンドウ、中国語・英語・日本語のテキスト入力に対応します。
  actions:
    - theme: brand
      text: Engineの概要
      link: /ja/basics/00_why_easyvrui
    - theme: alt
      text: 環境構築
      link: /ja/basics/01_install_and_setup
    - theme: alt
      text: コントロール一覧
      link: /ja/guide/

features:
  - title: ビジュアルフォーム設計
    details: Form Designerで.easyvruifrmを編集し、レイアウトをプレビューしてC++またはPythonのUIコードを出力できます。
    link: /ja/basics/04_form_designer
  - title: テキスト入力
    details: 中国語、英語、日本語でテキストを入力できます。入力バー、IME候補ウィンドウ、仮想キーボードは、現在の入力領域に合わせて配置されます。
    link: /ja/advanced/06_input_routing_and_drain
  - title: 空間ウィンドウ
    details: windowの参照対象にはworld、body、head、left、rightを選択できます。各ウィンドウの位置・姿勢、縮尺、曲率は個別に設定できます。
    link: /ja/guide/controls/window-and-text/window
  - title: 共有レンダリング
    details: 複数のアプリを同じEngineに接続できます。EngineはGPUテクスチャ、SteamVRのウィンドウ面、ウィンドウ単位の入力をまとめて管理します。
    link: /ja/advanced/05_rendering_pipeline
---

## チュートリアルの構成

|編|学習内容|
|---|---|
|[基礎編](/ja/basics/00_why_easyvrui)|[インストール先と起動](/ja/basics/01_install_and_setup)、SteamVRの操作、`window`の作成、フォーム設計とコード出力|
|[コントロール編](/ja/guide/)|コントロールごとにプロパティ、メソッド、イベントを調べ、付属のC++とPythonのサンプルを実行します。|
|[実践編](/ja/projects/01_vrc_chatbox)|VRChatのOSCチャットツール、ログと写真の管理、アバターパラメーターのパネル、手首HUD、リモートアプリを作成します。|
|[応用編](/ja/advanced/01_architecture)|EngineとSDKの役割を起点に、TLS、セッション、描画、入力のドレイン、空間を扱う数学を解説します。|
|リファレンス|[C++ API](/ja/reference/cpp_api)、[Python API](/ja/reference/python_api)、[Engineプロトコル](/ja/reference/engine_protocol)、[アプリマニフェスト](/ja/reference/application_manifest)|

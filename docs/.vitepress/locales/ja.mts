import type { DefaultTheme, LocaleSpecificConfig } from 'vitepress'

export const ja: LocaleSpecificConfig<DefaultTheme.Config> & { label: string; link?: string } = {
  label: '日本語',
  lang: 'ja-JP',
  link: '/ja/',
  title: 'EasyVROverlayUIEngine',
  description: 'SteamVR向け空間UIの開発ガイドとAPIリファレンス',
  themeConfig: {
    nav: [
      { text: '基礎編', link: '/ja/basics/00_why_easyvrui' },
      { text: 'コントロール編', link: '/ja/guide/' },
      { text: '実践編', link: '/ja/projects/01_vrc_chatbox' },
      { text: '応用編', link: '/ja/advanced/01_architecture' },
      { text: 'リファレンス', link: '/ja/reference/python_api' }
    ],
    sidebar: {
      '/ja/basics/': [
        {
          text: '基礎編',
          items: [
            { text: 'Engineの概要とユースケース', link: '/ja/basics/00_why_easyvrui' },
            { text: '環境構築・ビルド・インストール', link: '/ja/basics/01_install_and_setup' },
            { text: 'SteamVRの操作と付属アプリ', link: '/ja/basics/02_vr_operations_and_apps' },
            { text: '初めてのwindowを作成して実行する', link: '/ja/basics/03_first_window' },
            { text: 'フォームの設計・プレビュー・コード出力', link: '/ja/basics/04_form_designer' }
          ]
        }
      ],
      '/ja/guide/': [
        {
          text: 'コントロール編',
          items: [
            { text: 'コントロール一覧', link: '/ja/guide/' },
            { text: '共通インターフェース', link: '/ja/guide/controls/common-api' }
          ]
        },
        {
          text: 'フォームとテキスト',
          items: [
            { text: 'window', link: '/ja/guide/controls/window-and-text/window' },
            { text: 'label', link: '/ja/guide/controls/window-and-text/label' },
            { text: 'rich_label', link: '/ja/guide/controls/window-and-text/rich_label' },
            { text: 'button', link: '/ja/guide/controls/window-and-text/button' },
            { text: 'textbox', link: '/ja/guide/controls/window-and-text/textbox' }
          ]
        },
        {
          text: '選択と状態',
          items: [
            { text: 'checkbox', link: '/ja/guide/controls/selection-and-status/checkbox' },
            { text: 'radiobutton', link: '/ja/guide/controls/selection-and-status/radiobutton' },
            { text: 'progressbar', link: '/ja/guide/controls/selection-and-status/progressbar' },
            { text: 'slider', link: '/ja/guide/controls/selection-and-status/slider' },
            { text: 'numericupdown', link: '/ja/guide/controls/selection-and-status/numericupdown' },
            { text: 'datetime_selector', link: '/ja/guide/controls/selection-and-status/datetime_selector' }
          ]
        },
        {
          text: 'コレクションとデータ',
          items: [
            { text: 'combobox', link: '/ja/guide/controls/collection-and-data/combobox' },
            { text: 'listbox', link: '/ja/guide/controls/collection-and-data/listbox' },
            { text: 'treeview', link: '/ja/guide/controls/collection-and-data/treeview' },
            { text: 'listview', link: '/ja/guide/controls/collection-and-data/listview' },
            { text: 'grid', link: '/ja/guide/controls/collection-and-data/grid' }
          ]
        },
        {
          text: 'レイアウトとコンテナー',
          items: [
            { text: 'panel', link: '/ja/guide/controls/layout-and-container/panel' },
            { text: 'scrollpanel', link: '/ja/guide/controls/layout-and-container/scrollpanel' },
            { text: 'splitter', link: '/ja/guide/controls/layout-and-container/splitter' },
            { text: 'tabcontrol', link: '/ja/guide/controls/layout-and-container/tabcontrol' }
          ]
        },
        {
          text: 'コマンドと表示',
          items: [
            { text: 'menubar', link: '/ja/guide/controls/command-and-display/menubar' },
            { text: 'toolbar', link: '/ja/guide/controls/command-and-display/toolbar' },
            { text: 'image', link: '/ja/guide/controls/command-and-display/image' },
            { text: 'screen', link: '/ja/guide/controls/command-and-display/screen' },
            { text: 'blank', link: '/ja/guide/controls/command-and-display/blank' }
          ]
        },
        {
          text: '実装トピック',
          items: [
            { text: '組み込みダイアログ', link: '/ja/guide/09_builtin_dialogs' },
            { text: '型付きイベントとマルチスレッド実行', link: '/ja/guide/07_events_dialogs_threading' },
            { text: '空間配置・カスタム描画・Desktopへの登録', link: '/ja/guide/08_spatial_drawing_deploy' }
          ]
        }
      ],
      '/ja/projects/': [
        {
          text: '実践編',
          items: [
            { text: 'VRChatのOSCチャットツール', link: '/ja/projects/01_vrc_chatbox' },
            { text: 'VRChatのインスタンスログと写真管理', link: '/ja/projects/02_vrc_log_and_gallery' },
            { text: 'VRChatアバターのOSCパラメーター調整とプリセット', link: '/ja/projects/03_vrc_avatar_osc' },
            { text: '手首HUD、screen、レベルメーターの描画', link: '/ja/projects/04_vrc_wrist_hud' },
            { text: 'リモート配置と顔文字入力', link: '/ja/projects/05_remote_and_kaomoji_pad' }
          ]
        }
      ],
      '/ja/advanced/': [
        {
          text: '応用編',
          items: [
            { text: 'Engine・SDK・アプリのアーキテクチャ', link: '/ja/advanced/01_architecture' },
            { text: '言語別APIとengine_interface', link: '/ja/advanced/02_sdk_and_engine_interface' },
            { text: 'IPCトランスポート・TLS・メッセージプロトコル', link: '/ja/advanced/03_ipc_tls_protocol' },
            { text: 'Engineのセッションとコンテキスト管理', link: '/ja/advanced/04_session_and_context' },
            { text: 'コントロールツリー・描画パイプライン・SteamVRへの送信', link: '/ja/advanced/05_rendering_pipeline' },
            { text: '入力ルーティングと順次ドレイン', link: '/ja/advanced/06_input_routing_and_drain' },
            { text: '空間変換とSteamVRの座標系', link: '/ja/advanced/07_spatial_math' }
          ]
        }
      ],
      '/ja/reference/': [
        {
          text: 'リファレンス',
          items: [
            { text: 'Python APIリファレンス', link: '/ja/reference/python_api' },
            { text: 'C++ APIリファレンス', link: '/ja/reference/cpp_api' },
            { text: 'Engineプロトコルリファレンス', link: '/ja/reference/engine_protocol' },
            { text: 'アプリマニフェスト（.easyvrui）リファレンス', link: '/ja/reference/application_manifest' }
          ]
        }
      ]
    },
    outline: { label: 'このページの目次', level: [2, 3] },
    docFooter: { prev: '前のページ', next: '次のページ' },
    lastUpdated: { text: '最終更新' },
    returnToTopLabel: 'ページの先頭へ',
    sidebarMenuLabel: '目次',
    darkModeSwitchLabel: 'テーマ'
  }
}

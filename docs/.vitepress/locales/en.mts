import type { DefaultTheme, LocaleSpecificConfig } from 'vitepress'

export const en: LocaleSpecificConfig<DefaultTheme.Config> & { label: string; link?: string } = {
  label: 'English',
  lang: 'en-US',
  link: '/en/',
  title: 'EasyVROverlayUIEngine',
  description: 'SteamVR spatial UI development tutorial and API reference',
  themeConfig: {
    nav: [
      { text: 'Basics', link: '/en/basics/00_why_easyvrui' },
      { text: 'Guides', link: '/en/guide/' },
      { text: 'Projects', link: '/en/projects/01_vrc_chatbox' },
      { text: 'Advanced', link: '/en/advanced/01_architecture' },
      { text: 'Reference', link: '/en/reference/python_api' }
    ],
    sidebar: {
      '/en/basics/': [
        {
          text: 'Basics',
          items: [
            { text: 'Engine overview and use cases', link: '/en/basics/00_why_easyvrui' },
            { text: 'Prerequisites, build, and installation', link: '/en/basics/01_install_and_setup' },
            { text: 'SteamVR controls and built-in applications', link: '/en/basics/02_vr_operations_and_apps' },
            { text: 'Create and run your first window', link: '/en/basics/03_first_window' },
            { text: 'Form design, preview, and code export', link: '/en/basics/04_form_designer' }
          ]
        }
      ],
      '/en/guide/': [
        {
          text: 'Guides',
          items: [
            { text: 'Control index', link: '/en/guide/' },
            { text: 'Common APIs', link: '/en/guide/controls/common-api' }
          ]
        },
        {
          text: 'Windows and text',
          items: [
            { text: 'window', link: '/en/guide/controls/window-and-text/window' },
            { text: 'label', link: '/en/guide/controls/window-and-text/label' },
            { text: 'rich_label', link: '/en/guide/controls/window-and-text/rich_label' },
            { text: 'button', link: '/en/guide/controls/window-and-text/button' },
            { text: 'textbox', link: '/en/guide/controls/window-and-text/textbox' }
          ]
        },
        {
          text: 'Selection and status',
          items: [
            { text: 'checkbox', link: '/en/guide/controls/selection-and-status/checkbox' },
            { text: 'radiobutton', link: '/en/guide/controls/selection-and-status/radiobutton' },
            { text: 'progressbar', link: '/en/guide/controls/selection-and-status/progressbar' },
            { text: 'slider', link: '/en/guide/controls/selection-and-status/slider' },
            { text: 'numericupdown', link: '/en/guide/controls/selection-and-status/numericupdown' },
            { text: 'datetime_selector', link: '/en/guide/controls/selection-and-status/datetime_selector' }
          ]
        },
        {
          text: 'Collections and data',
          items: [
            { text: 'combobox', link: '/en/guide/controls/collection-and-data/combobox' },
            { text: 'listbox', link: '/en/guide/controls/collection-and-data/listbox' },
            { text: 'treeview', link: '/en/guide/controls/collection-and-data/treeview' },
            { text: 'listview', link: '/en/guide/controls/collection-and-data/listview' },
            { text: 'grid', link: '/en/guide/controls/collection-and-data/grid' }
          ]
        },
        {
          text: 'Layout and containers',
          items: [
            { text: 'panel', link: '/en/guide/controls/layout-and-container/panel' },
            { text: 'scrollpanel', link: '/en/guide/controls/layout-and-container/scrollpanel' },
            { text: 'splitter', link: '/en/guide/controls/layout-and-container/splitter' },
            { text: 'tabcontrol', link: '/en/guide/controls/layout-and-container/tabcontrol' }
          ]
        },
        {
          text: 'Commands and display',
          items: [
            { text: 'menubar', link: '/en/guide/controls/command-and-display/menubar' },
            { text: 'toolbar', link: '/en/guide/controls/command-and-display/toolbar' },
            { text: 'image', link: '/en/guide/controls/command-and-display/image' },
            { text: 'screen', link: '/en/guide/controls/command-and-display/screen' },
            { text: 'blank', link: '/en/guide/controls/command-and-display/blank' }
          ]
        },
        {
          text: 'Application topics',
          items: [
            { text: 'Built-in dialogs', link: '/en/guide/09_builtin_dialogs' },
            { text: 'Typed events and thread dispatch', link: '/en/guide/07_events_dialogs_threading' },
            { text: 'Spatial positioning, custom drawing, and Desktop registration', link: '/en/guide/08_spatial_drawing_deploy' }
          ]
        }
      ],
      '/en/projects/': [
        {
          text: 'Projects',
          items: [
            { text: 'VRChat OSC chat tool', link: '/en/projects/01_vrc_chatbox' },
            { text: 'VRChat instance logs and photo gallery', link: '/en/projects/02_vrc_log_and_gallery' },
            { text: 'VRChat Avatar OSC parameters and presets', link: '/en/projects/03_vrc_avatar_osc' },
            { text: 'Wrist HUD, screen, and level meter', link: '/en/projects/04_vrc_wrist_hud' },
            { text: 'Remote deployment and kaomoji input', link: '/en/projects/05_remote_and_kaomoji_pad' }
          ]
        }
      ],
      '/en/advanced/': [
        {
          text: 'Advanced',
          items: [
            { text: 'Engine, SDK, and application architecture', link: '/en/advanced/01_architecture' },
            { text: 'Language APIs and engine_interface', link: '/en/advanced/02_sdk_and_engine_interface' },
            { text: 'IPC transport, TLS, and the wire protocol', link: '/en/advanced/03_ipc_tls_protocol' },
            { text: 'Engine sessions and context management', link: '/en/advanced/04_session_and_context' },
            { text: 'Control tree, rendering pipeline, and SteamVR submission', link: '/en/advanced/05_rendering_pipeline' },
            { text: 'Input routing and serial draining', link: '/en/advanced/06_input_routing_and_drain' },
            { text: 'Spatial transforms and SteamVR coordinates', link: '/en/advanced/07_spatial_math' }
          ]
        }
      ],
      '/en/reference/': [
        {
          text: 'Reference',
          items: [
            { text: 'Python API reference', link: '/en/reference/python_api' },
            { text: 'C++ API reference', link: '/en/reference/cpp_api' },
            { text: 'Engine protocol reference', link: '/en/reference/engine_protocol' },
            { text: 'Application manifest (.easyvrui) reference', link: '/en/reference/application_manifest' }
          ]
        }
      ]
    },
    outline: { label: 'On this page', level: [2, 3] },
    docFooter: { prev: 'Previous page', next: 'Next page' },
    lastUpdated: { text: 'Last updated' },
    returnToTopLabel: 'Return to top',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Appearance'
  }
}

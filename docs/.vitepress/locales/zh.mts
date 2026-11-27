import type { DefaultTheme, LocaleSpecificConfig } from 'vitepress'

export const zh: LocaleSpecificConfig<DefaultTheme.Config> & { label: string; link?: string } = {
  label: '简体中文',
  lang: 'zh-CN',
  title: 'EasyVROverlayUIEngine',
  description: 'SteamVR空间UI开发教程与API参考',
  themeConfig: {
    nav: [
      { text: '基础篇', link: '/basics/00_why_easyvrui' },
      { text: '应用篇', link: '/guide/' },
      { text: '综合篇', link: '/projects/01_vrc_chatbox' },
      { text: '高级篇', link: '/advanced/01_architecture' },
      { text: '参考手册', link: '/reference/python_api' }
    ],
    sidebar: {
      '/basics/': [
        {
          text: '基础篇',
          items: [
            { text: '引擎概览与适用场景', link: '/basics/00_why_easyvrui' },
            { text: '环境准备、构建与安装', link: '/basics/01_install_and_setup' },
            { text: 'SteamVR操作与应用导览', link: '/basics/02_vr_operations_and_apps' },
            { text: '创建并运行第一个window', link: '/basics/03_first_window' },
            { text: '窗体设计、预览与代码导出', link: '/basics/04_form_designer' }
          ]
        }
      ],
      '/guide/': [
        {
          text: '应用篇',
          items: [
            { text: '控件目录', link: '/guide/' },
            { text: '基础接口', link: '/guide/controls/common-api' }
          ]
        },
        {
          text: '窗体与文本',
          items: [
            { text: 'window', link: '/guide/controls/window-and-text/window' },
            { text: 'label', link: '/guide/controls/window-and-text/label' },
            { text: 'rich_label', link: '/guide/controls/window-and-text/rich_label' },
            { text: 'button', link: '/guide/controls/window-and-text/button' },
            { text: 'textbox', link: '/guide/controls/window-and-text/textbox' }
          ]
        },
        {
          text: '选择与状态',
          items: [
            { text: 'checkbox', link: '/guide/controls/selection-and-status/checkbox' },
            { text: 'radiobutton', link: '/guide/controls/selection-and-status/radiobutton' },
            { text: 'progressbar', link: '/guide/controls/selection-and-status/progressbar' },
            { text: 'slider', link: '/guide/controls/selection-and-status/slider' },
            { text: 'numericupdown', link: '/guide/controls/selection-and-status/numericupdown' },
            { text: 'datetime_selector', link: '/guide/controls/selection-and-status/datetime_selector' }
          ]
        },
        {
          text: '集合与数据',
          items: [
            { text: 'combobox', link: '/guide/controls/collection-and-data/combobox' },
            { text: 'listbox', link: '/guide/controls/collection-and-data/listbox' },
            { text: 'treeview', link: '/guide/controls/collection-and-data/treeview' },
            { text: 'listview', link: '/guide/controls/collection-and-data/listview' },
            { text: 'grid', link: '/guide/controls/collection-and-data/grid' }
          ]
        },
        {
          text: '布局与容器',
          items: [
            { text: 'panel', link: '/guide/controls/layout-and-container/panel' },
            { text: 'scrollpanel', link: '/guide/controls/layout-and-container/scrollpanel' },
            { text: 'splitter', link: '/guide/controls/layout-and-container/splitter' },
            { text: 'tabcontrol', link: '/guide/controls/layout-and-container/tabcontrol' }
          ]
        },
        {
          text: '命令与显示',
          items: [
            { text: 'menubar', link: '/guide/controls/command-and-display/menubar' },
            { text: 'toolbar', link: '/guide/controls/command-and-display/toolbar' },
            { text: 'image', link: '/guide/controls/command-and-display/image' },
            { text: 'screen', link: '/guide/controls/command-and-display/screen' },
            { text: 'blank', link: '/guide/controls/command-and-display/blank' }
          ]
        },
        {
          text: '应用专题',
          items: [
            { text: '内建对话框', link: '/guide/09_builtin_dialogs' },
            { text: '强类型事件与多线程调度', link: '/guide/07_events_dialogs_threading' },
            { text: '空间定位、自定义绘图与Desktop登记', link: '/guide/08_spatial_drawing_deploy' }
          ]
        }
      ],
      '/projects/': [
        {
          text: '综合篇',
          items: [
            { text: 'VRChat OSC聊天工具', link: '/projects/01_vrc_chatbox' },
            { text: 'VRChat实例日志与相册管理', link: '/projects/02_vrc_log_and_gallery' },
            { text: 'VRChat Avatar OSC参数调试与预设', link: '/projects/03_vrc_avatar_osc' },
            { text: '腕部HUD、screen与电平绘制', link: '/projects/04_vrc_wrist_hud' },
            { text: '远程部署与颜文字输入', link: '/projects/05_remote_and_kaomoji_pad' }
          ]
        }
      ],
      '/advanced/': [
        {
          text: '高级篇',
          items: [
            { text: '引擎、SDK与应用架构', link: '/advanced/01_architecture' },
            { text: '语言API与engine_interface', link: '/advanced/02_sdk_and_engine_interface' },
            { text: 'IPC传输、TLS与消息协议', link: '/advanced/03_ipc_tls_protocol' },
            { text: 'Engine会话与上下文管理', link: '/advanced/04_session_and_context' },
            { text: '控件树、渲染管线与SteamVR提交', link: '/advanced/05_rendering_pipeline' },
            { text: '输入路由与串行排空', link: '/advanced/06_input_routing_and_drain' },
            { text: '空间变换与SteamVR坐标系', link: '/advanced/07_spatial_math' }
          ]
        }
      ],
      '/reference/': [
        {
          text: '参考手册',
          items: [
            { text: 'Python API参考', link: '/reference/python_api' },
            { text: 'C++ API参考', link: '/reference/cpp_api' },
            { text: 'Engine协议参考', link: '/reference/engine_protocol' },
            { text: '应用清单（.easyvrui）参考', link: '/reference/application_manifest' }
          ]
        }
      ]
    },
    outline: { label: '本页目录', level: [2, 3] },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: { text: '最后更新' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '目录',
    darkModeSwitchLabel: '主题'
  }
}

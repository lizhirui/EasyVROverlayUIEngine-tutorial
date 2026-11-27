---
layout: home

hero:
  name: EasyVROverlayUIEngine
  text: 面向SteamVR的原生空间UI引擎
  tagline: 使用C++或Python开发SteamVR空间界面，支持可视化布局、多窗口和中英日文本输入。
  actions:
    - theme: brand
      text: 引擎概览
      link: /basics/00_why_easyvrui
    - theme: alt
      text: 环境配置
      link: /basics/01_install_and_setup
    - theme: alt
      text: 控件目录
      link: /guide/

features:
  - title: 可视化窗体设计
    details: 在Form Designer中编辑.easyvruifrm，预览布局并导出C++或Python界面代码。
    link: /basics/04_form_designer
  - title: 文本输入
    details: 文本编辑支持中文、英文、日文输入。输入条、IME候选窗和虚拟键盘跟随当前输入区定位。
    link: /advanced/06_input_routing_and_drain
  - title: 空间窗口
    details: window支持world、body、head、left和right参考对象，每扇窗口可独立设置位姿、缩放与曲率。
    link: /guide/controls/window-and-text/window
  - title: 共享渲染
    details: 多个应用可连接同一个Engine。Engine统一处理GPU纹理、SteamVR窗面与窗口级输入。
    link: /advanced/05_rendering_pipeline
---

## 教程结构

|部分|学习内容|
|---|---|
|[基础篇](/basics/00_why_easyvrui)|[安装目录与服务配置](/basics/01_install_and_setup)、[SteamVR操作与内置应用（含EasyVRScreen）](/basics/02_vr_operations_and_apps)、创建`window`、窗体设计与代码导出|
|[应用篇](/guide/)|按控件查阅属性、方法和事件，运行配套的C++与Python示例|
|[综合篇](/projects/01_vrc_chatbox)|完成VRChat OSC聊天工具、日志与相册、Avatar参数面板、腕部HUD和远程应用|
|[高级篇](/advanced/01_architecture)|从Engine与SDK的职责讲到TLS、会话、渲染、输入排空和空间数学|
|参考手册|[C++API](/reference/cpp_api)、[Python API](/reference/python_api)、[Engine协议](/reference/engine_protocol)、[应用清单](/reference/application_manifest)|

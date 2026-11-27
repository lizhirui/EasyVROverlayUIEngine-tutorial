---
layout: home

hero:
  name: EasyVROverlayUIEngine
  text: A native spatial UI engine for SteamVR
  tagline: Build SteamVR spatial interfaces in C++ or Python with visual layout tools, multiple windows, and Chinese, English, and Japanese text input.
  actions:
    - theme: brand
      text: Engine overview
      link: /en/basics/00_why_easyvrui
    - theme: alt
      text: Set up your environment
      link: /en/basics/01_install_and_setup
    - theme: alt
      text: Control index
      link: /en/guide/

features:
  - title: Visual form design
    details: Edit .easyvruifrm files in Form Designer, preview layouts, and export C++ or Python UI code.
    link: /en/basics/04_form_designer
  - title: Text input
    details: Text editors support Chinese, English, and Japanese. The input bar, IME candidate window, and virtual keyboard follow the active input area.
    link: /en/advanced/06_input_routing_and_drain
  - title: Spatial windows
    details: A window supports world, body, head, left, and right references. Set the pose, scale, and curvature of each window independently.
    link: /en/guide/controls/window-and-text/window
  - title: Shared rendering
    details: Multiple applications can connect to the same Engine, which manages GPU textures, SteamVR window surfaces, and window-level input.
    link: /en/advanced/05_rendering_pipeline
---

## Tutorial structure

|Section|What you will learn|
|---|---|
|[Basics](/en/basics/00_why_easyvrui)|[Installation layout and service setup](/en/basics/01_install_and_setup), [SteamVR controls and built-in apps (including EasyVRScreen)](/en/basics/02_vr_operations_and_apps), creating a `window`, form design, and code export|
|[Guides](/en/guide/)|Look up properties, methods, and events by control. Run the accompanying C++ and Python examples.|
|[Projects](/en/projects/01_vrc_chatbox)|Build a VRChat OSC chat tool, an instance log and gallery, an Avatar parameter panel, a wrist HUD, and a remote application.|
|[Advanced](/en/advanced/01_architecture)|Study Engine and SDK responsibilities, TLS, sessions, rendering, input draining, and spatial math.|
|Reference|[C++ API](/en/reference/cpp_api), [Python API](/en/reference/python_api), [Engine protocol](/en/reference/engine_protocol), and [application manifest](/en/reference/application_manifest)|
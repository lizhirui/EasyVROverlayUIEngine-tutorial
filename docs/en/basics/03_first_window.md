# Create and Run Your First window

After completing the environment installation and understanding basic VR operations, this article will create the first `window` using approximately 20 lines of code. It will implement a window containing a title, `label` prompt text, and `button`. The text content will be updated when the button is clicked. The following text provides complete implementations in both Python and C++.

---

## SDK path configuration.

Before writing the code, configure the project or environment variables to locate the installed SDK. The following command assumes that the installation root directory is `D:\Tools\EasyVRUI`.

::: code-group
```cmd [Python：配置已安装的SDK]
python -m pip install -r "D:\Tools\EasyVRUI\sdk\api\python\requirements.txt"
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
```

```cmake [C++：最小CMakeLists.txt]
cmake_minimum_required(VERSION 3.24)
project(my_first_vr_window LANGUAGES CXX)

set(EASYVRUI_ENGINE_INTERFACE_ROOT "D:/Tools/EasyVRUI/sdk" CACHE PATH "Installed SDK or EngineInterface directory")
if(EXISTS "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")
    set(EASYVRUI_ENGINE_INTERFACE_ROOT "${EASYVRUI_ENGINE_INTERFACE_ROOT}/engine_interface")
endif()
include("${EASYVRUI_ENGINE_INTERFACE_ROOT}/lib/cmake/EngineInterface/EngineInterfaceApplication.cmake")

add_executable(my_first_vr_window main.cpp)
target_compile_options(my_first_vr_window PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/utf-8>)
easyvrui_link_selected_api(my_first_vr_window)
easyvrui_deploy_runtime(my_first_vr_window "${EASYVRUI_API_LINK_SHARED}")
```
:::

### Linking and running C++.

By default, `easyvrui_link_selected_api()` links `sdk/engine_interface/lib/engine_interface_static.lib` into `my_first_vr_window.exe` and uses static CRT. The built-in SDK language packages are included in the executable file. When selecting a DLL, pass `-DEASYVRUI_API_LINK_SHARED=ON` in the CMake configuration to use the corresponding import library and dynamic CRT. `easyvrui_deploy_runtime()` will copy `engine_interface.dll` from `sdk/engine_interface/bin/` to the program output directory.

::: tip Python version requirement
`sdk/api/python/` includes both the `easyvrui` package and the statically linked `engine_interface_native*.pyd`. When running directly, just prepend this directory for the interpreter to locate the package and the SDK to locate the extension. The version and architecture of the interpreter must match the version and x64 extension recorded in `installation.json`. When using `python/run.cmd` from the tutorial, `EASYVRUI_SDK_ROOT` can point to another installed `sdk/` directory.
:::

---

## First `window` example.

First, start SteamVR and the `bin/easyvrui_engine.exe` in the installation directory. Then save the following code as `first_window.py` or `main.cpp`:

::: code-group
```python [Python（first_window.py）]
from easyvrui import button, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "My First VR Window"
    window_main.rect = rect(0, 0, 520, 260)
    label_status = label("label_status")
    label_status.rect = rect(36, 76, 448, 48)
    label_status.text = "Click the button below to try it!"
    button_hello = button("button_hello")
    button_hello.rect = rect(36, 150, 200, 48)
    button_hello.text = "Say hello"

    def button_hello_click(source, event):
        label_status.text = "Hello, VR world!"

    button_hello.on_click += button_hello_click
    window_main.control_list.add(label_status)
    window_main.control_list.add(button_hello)
    window_main.show()
    run("my_first_vr_app")

if __name__ == "__main__":
    main()
```

<<< ../../../examples/basics/03_first_window/cpp/main.cpp
:::

### Run the program.

::: code-group
```cmd [运行 Python 版]
python first_window.py
```

```cmd [构建并运行 C++ 版]
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
build\my_first_vr_window.exe
```
:::

In SteamVR, find the item titled “My First VR Window”. It’s labeled with the code `window`. Use the controller laser to activate the “Point Me” option for `button` and `label`. The text for those options will be updated accordingly.

---

## Initial appearance and click feedback.

The following image was obtained by WARP's window construction function for executing this chapter's C++ routine. The initial state shows the `label` prompt and `button`.

Initial state of !['s first window:](/images/en/basics_first_initial.png).

Test the host to distribute clicks to `button_hello`, and the same `on_click` callback changes `label_status.text` to "Hello, VR World!".

The label of ![is updated to](/images/en/basics_first_clicked.png) after clicking the button.

## Initialization and event distribution.

The above example includes 5 core steps of the EasyVROverlayUIEngine application:

### 1. Specify the control name (Z`name`)

```python
window_main = window("window_main")
label_status = label("label_status")
```

Each control requires a non-empty and unique `name` when constructed (read-only after construction). It is recommended to use the naming style of `控件类型_用途` (e.g., `button_hello`), consistent with the member names exported by Form Designer.

### 2. Set the position and size (Z`rect`)

- The `rect(left, top, width, height)` of child controls uses logical pixel coordinates relative to the **upper left corner of the parent container**.
- The `rect.left` and `rect.top` of `window` themselves are not used to determine 3D spatial positions. Only `width` and `height` take effect (the window title bar height is approximately 44~56px, so the first child control is usually placed near `top = 76`).
- Under the default zoom level (`physical_scale = 1.0`), **1000 logical pixels correspond to 1 meter** (i.e., 1 logical pixel is approximately 1 millimeter). The physical width of the window with `520 × 260` is about 0.52 meters.

### 3. Binding strong-type events (`on_click += ...`)

```python
def button_hello_click(source, event):
    label_status.text = "Hello, VR world!"

button_hello.on_click += button_hello_click
```

All event callbacks use a unified two-parameter signature: **`(source, event)`**.
- `source`: The control instance that triggers the event (here it is `button_hello`);
- `event`: The strong-type event parameter object. For regular click events, it is `event_args` (C++ is for `easyvrui::event_args_t`); events such as keyboard input and window closure will involve event parameter types with specialized fields like `key` and `cancel`.

### 4. Adding controls to the window (`control_list.add`)

Newly created `label` and `button` must be added to the control collection of `window` through `window_main.control_list.add(...)` (C++ is for `window_main->get_control_list().add(...)`) before they can participate in layout, rendering, and laser hit detection.

### 5. `show()` and `run("my_first_vr_app")`

- `window_main.show()`: Submit a display request to the Engine, defaulting to being placed in the center in front of the user and automatically staggering with the depth of existing windows.
- `run("my_first_vr_app")`: Register the session name and enter the main message loop, continuously processing laser events, keyboard input, and incremental rendering until all windows close, then exit.

::: info The C++ string prefix `U"..."`
The C++ SDK uniformly uses `std::u32string` (UTF-32 encoding) to represent interface text and control names, accurately handling multi-language characters and Unicode code points. Using the literal `U"..."` allows for direct construction of `std::u32string`.
:::

The next chapter will introduce how to quickly build the interface and export code using the visual **Form Designer** through dragging and dropping.
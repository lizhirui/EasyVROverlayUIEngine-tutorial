# 创建并运行第一个window

完成环境安装并了解VR基本操作后，本篇将通过约20行代码创建第一个`window`，实现一个包含标题、`label`提示文本与`button`的窗口，点击按钮后更新文本内容。下文同时提供Python与C++两种语言的完整实现。

---

## SDK路径配置

编写代码前，配置工程或环境变量来定位已安装的SDK。以下命令假设安装根目录为`D:\Tools\EasyVRUI`。

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

### C++链接与运行

`easyvrui_link_selected_api()`默认将`sdk/engine_interface/lib/engine_interface_static.lib`链接进`my_first_vr_window.exe`，并使用静态CRT。SDK内置语言包随实现进入可执行文件。选择DLL时，在CMake配置中传入`-DEASYVRUI_API_LINK_SHARED=ON`，使用对应的导入库与动态CRT。`easyvrui_deploy_runtime()`会从`sdk/engine_interface/bin/`复制`engine_interface.dll`到程序输出目录。

::: tip Python版本要求
`sdk/api/python/`同时包含`easyvrui`包和静态链接的`engine_interface_native*.pyd`。直接运行时，前置这一个目录即可由解释器定位包，由SDK定位扩展。解释器的版本和架构须匹配`installation.json`记录的版本及x64扩展。使用教程中的`python/run.cmd`时，`EASYVRUI_SDK_ROOT`可指向其它安装的`sdk/`目录。
:::

---

## 第一个`window`示例

先启动SteamVR和安装目录中的`bin/easyvrui_engine.exe`。然后将以下代码保存为`first_window.py`或`main.cpp`：

::: code-group
```python [Python（first_window.py）]
from easyvrui import button, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "我的第一个VR窗口"
    window_main.rect = rect(0, 0, 520, 260)
    label_status = label("label_status")
    label_status.rect = rect(36, 76, 448, 48)
    label_status.text = "点一下下面的按钮试试看！"
    button_hello = button("button_hello")
    button_hello.rect = rect(36, 150, 200, 48)
    button_hello.text = "点我打招呼"

    def button_hello_click(source, event):
        label_status.text = "你好，VR世界！"

    button_hello.on_click += button_hello_click
    window_main.control_list.add(label_status)
    window_main.control_list.add(button_hello)
    window_main.show()
    run("my_first_vr_app")

if __name__ == "__main__":
    main()
```

<<< ../../examples/basics/03_first_window/cpp/main.cpp
:::

### 运行程序

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

在SteamVR中找到标题为“我的第一个VR窗口”的`window`。用手柄激光激活“点我打招呼”`button`，`label`的文本会更新。

---

## 初始外观与点击反馈

下图由WARP执行本章C++例程的窗口构建函数取得。初始状态先显示`label`提示及`button`。

![第一个window的初始状态](/images/zh/basics_first_initial.png)

测试宿主把点击派发到`button_hello`，同一个`on_click`回调将`label_status.text`改为“你好，VR世界！”。

![点击button后label更新](/images/zh/basics_first_clicked.png)

## 初始化与事件分发

以上示例包含EasyVROverlayUIEngine应用的5个核心步骤：

### 1. 指定控件名称（`name`）

```python
window_main = window("window_main")
label_status = label("label_status")
```

每个控件在构造时都需要传入非空且在同一容器内唯一的`name`（构造后只读）。建议采用`控件类型_用途`的命名风格（例如`button_hello`），与Form Designer导出的成员命名保持一致。

### 2. 设置位置与尺寸（`rect`）

- 子控件的`rect(left, top, width, height)`采用相对于**父容器左上角**的逻辑像素坐标；
- `window`自身的`rect.left`与`rect.top`不用于决定3D空间位置，仅`width`和`height`生效（窗口标题栏高度约44~56px，因此第一个子控件通常从`top = 76`附近开始放置）。
- 在默认缩放（`physical_scale = 1.0`）下，**1000逻辑像素对应1米**（即1逻辑像素约1毫米），`520 × 260`的窗口物理宽度约为0.52米。

### 3. 绑定强类型事件（`on_click += ...`）

```python
def button_hello_click(source, event):
    label_status.text = "你好，VR世界！"

button_hello.on_click += button_hello_click
```

所有事件回调均采用统一的双参数签名：**`(source, event)`**。
- `source`：触发事件的控件实例（此处为`button_hello`）；
- `event`：强类型事件参数对象。普通点击事件为`event_args`（C++为`easyvrui::event_args_t`）；键盘、关闭拦截等事件则会传入包含`key`、`cancel`等专用字段的事件参数类型。

### 4. 将控件添加到窗口（`control_list.add`）

新创建的`label`和`button`必须通过`window_main.control_list.add(...)`（C++为`window_main->get_control_list().add(...)`）加入`window`的控件集合后，才会参与布局、渲染和激光命中检测。

### 5. `show()`与`run("my_first_vr_app")`

- `window_main.show()`：向Engine提交显示请求，默认以居中策略放置在用户前方并自动错开已有窗口的深度。
- `run("my_first_vr_app")`：注册会话名称并进入主消息循环，持续处理激光事件、键盘输入和增量绘制，直到所有窗口关闭后退出。

::: info C++字符串前缀`U"..."`说明
C++ SDK统一使用`std::u32string`（UTF-32编码）表示界面文本与控件名称，以准确处理多语言字符与Unicode码点。使用`U"..."`字面量即可直接构造`std::u32string`。
:::

下一章将介绍如何使用可视化**Form Designer**通过拖拽快速构建界面并导出代码。

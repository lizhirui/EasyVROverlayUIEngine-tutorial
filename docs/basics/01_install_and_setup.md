# 环境准备、构建与安装

本章介绍如何在Windows环境下编译源码并安装EasyVROverlayUIEngine的运行目录。

::: tip 说明
顶层`build.bat`负责构建各组件，`install.bat`将产物安装到运行目录。使用**Python**开发VR应用时，安装后可直接使用已编译的原生扩展。
:::

---

## 第一步：环境要求

开始构建前，请确认系统满足以下条件：

|项目|最低要求|说明|
|---|---|---|
|**操作系统**|Windows 10 / 11（64位）|引擎原生基于Windows与Direct3D 11实现，暂不支持Linux/macOS|
|**显卡与VR环境**|支持Direct3D 11的显卡 + SteamVR + VR头显|满足常规SteamVR运行要求即可|
|**Python**|64位CPython 3.11或更高版本|安装时请勾选 **Add python.exe to PATH**，确保在CMD中可直接调用`python`|
|**C++构建工具**|支持C++20的MSVC x64工具链、Windows SDK、CMake 3.24或更高版本、Ninja|在Visual Studio中选择“使用C++的桌面开发”工作负载，并安装CMake与Ninja组件|

::: warning 仅使用CMD，不要使用PowerShell
在本项目的构建与脚本执行过程中，请一律使用Windows自带的**命令提示符（CMD）**（按`Win+R`输入`cmd`回车即可）。PowerShell对引号、参数转发和环境变量的处理方式与CMD存在差异，可能导致构建或安装脚本出现异常。
:::

---

## 第二步：构建Engine、SDK和内置应用

在CMD中进入源码仓库根目录并运行`build.bat`。

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
build.bat
```

默认使用Release配置并行执行8个构建任务。可用`--configuration`和`--parallel`指定配置和并行数。

```cmd
build.bat --configuration Release --parallel 8
```

### 各组件的构建目录

顶层`build.bat`在CMD中初始化一次MSVC x64环境，再依次调用13个组件的`build.bat`。每个组件使用自己的`build/`配置并编译。以下产物路径均相对于所在组件。

|组件目录|构建产物|
|---|---|
|`sdk/engine_interface`|`build/lib/`中的静态库、DLL导入库与CMake包，`build/bin/`中的DLL，以及`build/include/`中的公开头文件|
|`sdk/api/python`|`build/bin/`中的Python SDK包、`engine_interface_native.pyd`和`engine_interface_native.json`|
|`engine`|`build/bin/`中的`easyvrui_engine.exe`、`easyvrui_service.exe`、`easyvrui_screen_helper.exe`和SteamVR动作资源|
|`app/desktop`、`app/easyvrscreen`、`app/form_designer`、`app/file_manager`、`app/task_manager`、`app/demo/cpp`|各自`build/bin/`中的应用程序与构建生成的运行资源（`app/easyvrscreen`生成`easyvrui_screen.exe`与`easyvrscreen.easyvrui`，`app/file_manager`同时生成`easyvrui_volume_query.exe`）|
|`app/layout/standard_104`、`app/ime/cn/easyvrui_pinyin`、`app/ime/en/easyvrui_english`、`app/ime/jp/easyvrui_japanese`|各自`build/bin/`中的组件程序。拼音和日文IME在`build/bin/rime/`中生成预编译词库|

### 单独构建一个组件

可进入组件目录，直接运行该组件的`build.bat`。单独构建Python原生扩展或C++应用前，先用相同配置构建`sdk/engine_interface`，以便使用`sdk/engine_interface/build/`中的预编译SDK。下面先构建SDK，再单独构建Desktop。

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo\sdk\engine_interface"
build.bat --configuration Release
cd /d "D:\program\project\EasyVROverlayUIEngine\repo\app\desktop"
build.bat --configuration Release
```

成功构建的组件会写入`build/configuration.txt`。第三方源码、Rime方案及词库随仓库提供，配置好本机工具链后即可离线构建。

---

## 第三步：安装到运行目录

完成13个组件的构建后，在源码仓库根目录运行`install.bat`。CMD安装脚本读取各组件自身的`build/`，并确认全部13个组件使用相同构建配置。Python Demo与C++ API头文件从各自的源码目录复制。安装目录必须显式指定且与源码仓库分开；省略目录时脚本向标准错误输出用法并返回退出码2。

服务安装（默认模式，要求受管理员保护的目录，经UAC确认注册并启动`EasyVROverlayUIEngine`服务，并设置系统环境变量`EASYVROVERLAYUIENGINE_HOME`）：

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
install.bat "%ProgramFiles%\EasyVRUI"
```

便携安装（跳过Windows服务注册和系统环境变量写入，适合本地自定义目录手动运行）：

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
install.bat "D:\Tools\EasyVRUI" --no-service
```

以下是全新安装生成的目录（`--no-service`同样复制服务工具与抓屏Helper，但由Engine本进程执行桌面捕获）。各应用的相对路径沿用`repo/app/`中的目录结构。

```text
<安装根目录>\
├── installation.json
├── bin\
│   ├── easyvrui_engine.exe
│   ├── easyvrui_service.exe        # Windows服务托管与管理工具
│   ├── easyvrui_screen_helper.exe  # 服务模式下的跨输入桌面抓屏与键鼠Helper
│   ├── actions\                    # SteamVR动作清单与各手柄默认绑定JSON（actions.json、bindings_*.json）
│   └── config.json
├── app\
│   ├── desktop\
│   │   ├── easyvrui_desktop.exe
│   │   └── config.json
│   ├── easyvrscreen\
│   │   ├── easyvrui_screen.exe     # 多显示器VR屏幕查看器
│   │   └── easyvrscreen.easyvrui
│   ├── form_designer\
│   │   ├── easyvrui_form_designer.exe
│   │   ├── easyvrui_form_designer.easyvrui
│   │   └── resources\             # 窗体设计器资源
│   ├── file_manager\
│   │   ├── easyvrui_file_manager.exe
│   │   ├── easyvrui_file_manager.easyvrui
│   │   ├── easyvrui_volume_query.exe # 磁盘卷查询辅助程序
│   │   └── file_manager.json         # 文件关联与视图配置
│   ├── task_manager\
│   │   ├── easyvrui_task_manager.exe
│   │   └── easyvrui_task_manager.easyvrui
│   ├── demo\
│   │   ├── cpp\
│   │   │   ├── easyvrui_demo_cpp.exe
│   │   │   ├── easyvrui_demo_cpp.easyvrui
│   │   │   └── resources\          # C++ Demo资源
│   │   └── python\
│   │       ├── main.py
│   │       ├── demo\               # Python Demo内部窗口模块与图片资源
│   │       ├── requirements.txt
│   │       └── easyvrui_demo_python.easyvrui
│   ├── layout\standard_104\easyvrui_layout_standard_104.exe
│   └── ime\
│       ├── cn\easyvrui_pinyin\
│       │   ├── easyvrui_ime_chinese_pinyin.exe
│       │   └── rime\chinese_pinyin\ # 拼音IME专属Rime词库与万象LTS文法模型
│       ├── en\easyvrui_english\easyvrui_ime_english.exe
│       └── jp\easyvrui_japanese\
│           ├── easyvrui_ime_japanese.exe
│           └── rime\japanese\      # 日语IME专属Rime词库与方案数据
└── sdk\
    ├── api\
    │   ├── cpp\
    │   │   ├── include\            # C++公开头文件
    │   │   └── third_party\json\    # C++ API所附JSON头文件
    │   └── python\
    │       ├── easyvrui\           # Python SDK封装包
    │       ├── engine_interface_native.pyd
    │       ├── engine_interface_native.json
    │       └── requirements.txt
    └── engine_interface\
        ├── include\                # 原生接口公开头文件与json.hpp
        ├── lib\
        │   ├── engine_interface_static.lib
        │   ├── engine_interface.lib
        │   └── cmake\EngineInterface\ # CMake find_package导出配置
        └── bin\engine_interface.dll
```

首次安装时，`install.bat`创建`bin/config.json`。独立运行的Engine首次启动时生成并保存接入凭据；服务托管的Engine读取配置中的凭据，缺省时为本次运行生成凭据。服务安装成功后，脚本通过`setx /M`将系统环境变量`EASYVROVERLAYUIENGINE_HOME`设为规范化的安装根目录（写入失败时回滚安装），新打开的CMD可通过`%EASYVROVERLAYUIENGINE_HOME%\bin`定位引擎；便携模式保留现有系统环境变量。`installation.json`标识安装根目录，并记录构建配置、Python版本和应用清单路径。`bin/config.json`中的`desktop`及`provider_list`以该文件所在的`bin/`为基准，通过`../app/...`引用程序。`app/desktop/config.json`以Desktop目录为基准，登记6个内置应用清单（C++ Demo、Python Demo、EasyVRScreen、File Manager、Form Designer、Task Manager）。每份[应用清单](/reference/application_manifest)再以自己的目录解析`launch.executable`或`launch.script`和子进程工作目录。

内置C++应用和Python原生扩展默认链接`engine_interface_static`。`engine_interface.lib`是DLL导入库，`engine_interface.dll`供选择共享链接的应用使用。Engine、SDK和应用各自将内置语言包编入二进制。应用也可调用SDK的`language_pack.load_directory()`加载自定义语言包。

Desktop在内存中按应用ID合并系统配置和`%USERPROFILE%\easyvrui\desktop\config.json`中的用户配置。重复安装会重新生成系统配置，并保留已有`bin/config.json`与`app/file_manager/file_manager.json`。Desktop界面上的添加和移除只写用户配置。

安装目录中的Python SDK集中在`sdk/api/python/`。Desktop或File Manager通过SDK启动Python清单时，将该目录前置到子进程的`PYTHONPATH`并保留原值。

---

## 第四步：启动验证

首先启动**SteamVR**并确认头显与手柄处于就绪状态（Engine可先于SteamVR启动并在检测到SteamVR进程与管道就绪后自动以`VRApplication_Background`连接）。

**服务安装模式**：在新开的CMD中查询服务状态（启停与卸载命令见[Engine协议参考](/reference/engine_protocol)），并启动C++示例：

```cmd
"%EASYVROVERLAYUIENGINE_HOME%\bin\easyvrui_service.exe" --status
start "" /D "%EASYVROVERLAYUIENGINE_HOME%\app\demo\cpp" "%EASYVROVERLAYUIENGINE_HOME%\app\demo\cpp\easyvrui_demo_cpp.exe"
```

**便携安装模式**：手动启动Engine与C++示例程序：

```cmd
start "" "D:\Tools\EasyVRUI\bin\easyvrui_engine.exe"
start "" /D "D:\Tools\EasyVRUI\app\demo\cpp" "D:\Tools\EasyVRUI\app\demo\cpp\easyvrui_demo_cpp.exe"
```

在SteamVR中确认示例`window`已显示，可验证Engine和SDK连接。

Python Demo可从Desktop启动。直接在CMD运行时，使用与安装目录中原生扩展版本和架构相同的CPython。以下命令安装Demo声明的依赖，前置共享SDK目录并从应用目录启动主脚本（服务模式可将`D:\Tools\EasyVRUI`替换为`%EASYVROVERLAYUIENGINE_HOME%`）。

```cmd
python -m pip install -r "D:\Tools\EasyVRUI\app\demo\python\requirements.txt"
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
cd /d "D:\Tools\EasyVRUI\app\demo\python"
python -B main.py
```

### 常见问题：启动后VR中没有看到窗口

如果未在视野中看到窗口，通常由以下两个原因导致：

1. **启动时参考姿态或来源窗口位置与当前朝向不一致**：SDK窗口默认采用`center`首次定位（优先与当前可见来源窗口平行居中，无有效来源时按头显前方居中）；`none`保留指定位姿。按下键盘快捷键 **`Ctrl + Alt + Pause`**，引擎会重置`body`参考中心与`world`空间偏移，并在新的World原点显示15秒红色十字提示。
2. **SteamVR尚未就绪**：确认SteamVR已由用户启动并识别头显。若SteamVR在运行中退出或崩溃，可保持Engine与应用运行，待旧SteamVR进程完全退出后重新启动SteamVR。Engine会自动重连并恢复窗口显示。

下一章将介绍VR空间内的窗口交互操作与内置应用的功能用法。

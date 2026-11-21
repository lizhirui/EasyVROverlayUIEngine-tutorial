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

顶层`build.bat`在CMD中初始化一次MSVC x64环境，再依次调用12个组件的`build.bat`。每个组件使用自己的`build/`配置并编译。以下产物路径均相对于所在组件。

|组件目录|构建产物|
|---|---|
|`sdk/engine_interface`|`build/lib/`中的静态库、DLL导入库与CMake包，`build/bin/`中的DLL，以及`build/include/`中的公开头文件|
|`sdk/api/python`|`build/bin/`中的Python SDK包和`engine_interface_native*.pyd`|
|`engine`|`build/bin/`中的`easyvrui_engine.exe`和SteamVR动作资源|
|`app/desktop`、`app/form_designer`、`app/file_manager`、`app/task_manager`、`app/demo/cpp`|各自`build/bin/`中的应用程序与构建生成的运行资源|
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

完成12个组件的构建后，在源码仓库根目录运行`install.bat`。CMD安装脚本读取各组件自身的`build/`，并确认已完成的构建使用相同配置。Python Demo与C++ API头文件从各自的源码目录复制。安装目录应与源码仓库分开。

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
install.bat "D:\Tools\EasyVRUI"
```

省略目标路径时，`install.bat`会提示输入安装目录。


以下是全新安装生成的目录。各应用的相对路径沿用`repo/app/`中的目录结构。

```text
D:\Tools\EasyVRUI\
├── installation.json
├── bin\
│   ├── easyvrui_engine.exe
│   ├── actions\                    # SteamVR动作清单与各手柄默认绑定JSON（actions.json、bindings_*.json）
│   └── config.json
├── app\
│   ├── desktop\
│   │   ├── easyvrui_desktop.exe
│   │   └── config.json
│   ├── form_designer\
│   │   ├── easyvrui_form_designer.exe
│   │   ├── easyvrui_form_designer.easyvrui
│   │   └── resources\             # 窗体设计器资源
│   ├── file_manager\
│   │   ├── easyvrui_file_manager.exe
│   │   ├── easyvrui_file_manager.easyvrui
│   │   ├── easyvrui_volume_query.exe # 磁盘卷查询辅助程序
│   │   └── file_manager.json         # 文件关联配置
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
│       │   └── rime\chinese_pinyin\ # 拼音IME专属Rime词库与方案数据
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
    │       ├── engine_interface_native*.pyd
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

首次安装时，`install.bat`创建`bin/config.json`，Engine首次启动时生成接入凭据。`installation.json`标识安装根目录，并记录构建配置、Python版本和应用清单路径。`bin/config.json`中的`desktop`及`provider_list`以该文件所在的`bin/`为基准，通过`../app/...`引用程序。`app/desktop/config.json`以Desktop目录为基准，登记内置应用清单，例如`../demo/cpp/easyvrui_demo_cpp.easyvrui`。每份[应用清单](/reference/application_manifest)再以自己的目录解析`launch.executable`或`launch.script`和子进程工作目录。

内置C++应用和Python原生扩展默认链接`engine_interface_static`。`engine_interface.lib`是DLL导入库，`engine_interface.dll`供选择共享链接的应用使用。Engine、SDK和应用各自将内置语言包编入二进制。应用也可调用SDK的`language_pack.load_directory()`加载自定义语言包。

Desktop在内存中按应用ID合并系统配置和`%USERPROFILE%\easyvrui\desktop\config.json`中的用户配置。重复安装会重新生成系统配置，并保留已有Engine配置和接入凭据。Desktop界面上的添加和移除只写用户配置。

安装目录中的Python SDK集中在`sdk/api/python/`。Desktop或File Manager通过SDK启动Python清单时，将该目录前置到子进程的`PYTHONPATH`并保留原值。

---

## 第四步：启动验证

首先启动**SteamVR**并确认头显与手柄处于就绪状态，随后在CMD中依次启动Engine和C++示例程序：

```cmd
start "" "D:\Tools\EasyVRUI\bin\easyvrui_engine.exe"
start "" /D "D:\Tools\EasyVRUI\app\demo\cpp" "D:\Tools\EasyVRUI\app\demo\cpp\easyvrui_demo_cpp.exe"
```

在SteamVR中确认示例`window`已显示，可验证Engine和SDK连接。

Python Demo可从Desktop启动。直接在CMD运行时，使用与安装目录中原生扩展版本和架构相同的CPython。以下命令安装Demo声明的依赖，前置共享SDK目录并从应用目录启动主脚本。

```cmd
python -m pip install -r "D:\Tools\EasyVRUI\app\demo\python\requirements.txt"
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
cd /d "D:\Tools\EasyVRUI\app\demo\python"
python -B main.py
```

### 常见问题：启动后VR中没有看到窗口

如果未在视野中看到窗口，通常由以下两个原因导致：

1. **启动时头显朝向与当前佩戴朝向不一致**：窗口默认在程序启动时刻头显正前方生成。按下键盘快捷键 **`Ctrl + Alt + Pause`**，引擎会将`body`参考中心与`world`空间偏移重置到当前头显正前方。
2. **SteamVR尚未就绪**：确认SteamVR已启动并识别头显。若SteamVR在运行中退出或崩溃，可保持Engine与应用运行，待旧SteamVR进程完全退出后重新启动SteamVR。Engine会自动重连并恢复窗口显示。

下一章将介绍VR空间内的窗口交互操作与内置应用的功能用法。

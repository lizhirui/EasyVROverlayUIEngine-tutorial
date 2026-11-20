# 环境准备、构建与安装

本章介绍如何在Windows环境下编译源码并安装EasyVROverlayUIEngine的运行目录。

::: tip 说明
项目仓库已内置一键脚本`build.bat`和`install.bat`，无需手动编写CMake或编译命令。如果后续仅使用**Python**开发VR应用，只需在首次部署时完成一次构建安装，之后无需再配置或调用C++编译器。
:::

---

## 第一步：环境要求

开始构建前，请确认系统满足以下条件：

|项目|最低要求|说明|
|---|---|---|
|**操作系统**|Windows 10 / 11（64位）|引擎原生基于Windows与Direct3D 11实现，暂不支持Linux/macOS|
|**显卡与VR环境**|支持Direct3D 11的显卡 + SteamVR + VR头显|满足常规SteamVR运行要求即可|
|**Python**|64位CPython 3.11或更高版本|安装时请勾选 **Add python.exe to PATH**，确保在CMD中可直接调用`python`|
|**C++构建工具**|Visual Studio（勾选“使用C++的桌面开发”工作负载 + Windows SDK）|用于编译Engine、原生SDK及内置应用；Visual Studio会附带CMake和Ninja，无需单独安装|

::: warning 仅使用CMD，不要使用PowerShell
在本项目的构建与脚本执行过程中，请一律使用Windows自带的**命令提示符（CMD）**（按`Win+R`输入`cmd`回车即可）。PowerShell对引号、参数转发和环境变量的处理方式与CMD存在差异，可能导致构建或安装脚本出现异常。
:::

---

## 第二步：获取源码并执行构建

假设仓库位于`D:\program\project\EasyVROverlayUIEngine\repo`（可根据需要放置在其他目录，路径包含中文或空格亦可）。

打开**CMD**，进入仓库目录并运行`build.bat`：

```cmd
cd /d D:\program\project\EasyVROverlayUIEngine\repo
build.bat
```

如需加快编译速度，可指定Release配置与并行线程数（例如8线程）：

```cmd
build.bat --configuration Release --parallel 8
```

### 构建脚本执行流程

`build.bat`会自动完成以下步骤：
1. 自动定位本机的Visual Studio x64工具链、CMake和Ninja；
2. 编译**Engine**（`easyvrui_engine.exe`，负责GPU渲染与SteamVR交互的核心服务进程）；
3. 编译**原生SDK**（静态库`engine_interface_static.lib`、动态库`engine_interface.dll`以及Python原生扩展`engine_interface_native*.pyd`）；
4. 编译Desktop、Form Designer、File Manager、Task Manager、C++ Demo、标准104虚拟键盘和中英日IME，并准备Python Demo与各应用资源。

::: info 离线构建支持
所有第三方依赖源码（包括中文拼音与日语输入法所需的Rime引擎及词库）均已完整内置在仓库中，**构建过程不依赖外部网络下载**。首次全量编译通常需要几分钟，后续增量修改只需数秒即可完成。
:::

::: tip 编译报错排查建议
如果因本地环境差异（如缺少Windows SDK组件、PATH环境变量冲突或Visual Studio工作负载未勾选完整）导致`build.bat`报错，可将CMD末尾的错误信息复制到AI辅助工具（如Gemini / GPT / Claude）中协助定位缺失组件。
:::

默认构建目录为源码仓库外层的`../build/easyvrui_distribution`。使用`--build-directory`指定其它目录时，安装命令须传入相同的目录。

---

## 第三步：安装到运行目录

构建完成后，运行`install.bat`将可执行文件与SDK部署到目标目录（例如`D:\Tools\EasyVRUI`）：

```cmd
install.bat "D:\Tools\EasyVRUI"
```

如果省略路径参数直接执行`install.bat`，脚本会在命令行提示输入安装路径。

以下是全新安装生成的目录。各应用的相对路径沿用`repo/app/`中的目录结构。

```text
D:\Tools\EasyVRUI\
├── installation.json
├── bin\
│   ├── easyvrui_engine.exe
│   ├── actions\
│   └── config.json
├── app\
│   ├── desktop\
│   │   ├── easyvrui_desktop.exe
│   │   └── config.json
│   ├── form_designer\
│   │   ├── easyvrui_form_designer.exe
│   │   └── easyvrui_form_designer.easyvrui
│   ├── file_manager\
│   │   ├── easyvrui_file_manager.exe
│   │   └── easyvrui_file_manager.easyvrui
│   ├── task_manager\
│   │   ├── easyvrui_task_manager.exe
│   │   └── easyvrui_task_manager.easyvrui
│   ├── demo\
│   │   ├── cpp\
│   │   │   ├── easyvrui_demo_cpp.exe
│   │   │   └── easyvrui_demo_cpp.easyvrui
│   │   └── python\
│   │       ├── main.py
│   │       ├── demo\
│   │       ├── requirements.txt
│   │       └── easyvrui_demo_python.easyvrui
│   ├── layout\standard_104\easyvrui_layout_standard_104.exe
│   └── ime\
│       ├── cn\easyvrui_pinyin\
│       │   ├── easyvrui_ime_chinese_pinyin.exe
│       │   └── rime\chinese_pinyin\
│       ├── en\easyvrui_english\easyvrui_ime_english.exe
│       └── jp\easyvrui_japanese\
│           ├── easyvrui_ime_japanese.exe
│           └── rime\japanese\
└── sdk\
    ├── api\
    │   ├── cpp\include\
    │   └── python\
    │       ├── easyvrui\
    │       ├── engine_interface_native*.pyd
    │       ├── engine_interface_native.json
    │       └── requirements.txt
    └── engine_interface\
        ├── include\
        ├── lib\
        │   ├── engine_interface_static.lib
        │   ├── engine_interface.lib
        │   └── cmake\EngineInterface\
        └── bin\engine_interface.dll
```

`installation.json`标识安装根目录，并记录构建配置、Python版本和应用清单路径。`bin/config.json`中的`desktop`及`provider_list`以该文件所在的`bin/`为基准，通过`../app/...`引用程序。`app/desktop/config.json`以Desktop目录为基准，登记内置应用清单，例如`../demo/cpp/easyvrui_demo_cpp.easyvrui`。每份[应用清单](/reference/application_manifest)再以自己的目录解析`launch.executable`或`launch.script`和子进程工作目录。

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

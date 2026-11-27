# Prerequisites, Build, and Installation

This chapter explains how to compile the source code and install the running directory of EasyVROverlayUIEngine in a Windows environment.

::: tip Build once to use the Python SDK
The top-level `build.bat` builds the components, and `install.bat` copies the output into a runtime directory. If you develop VR apps in **Python**, you can use the prebuilt native extension after installation.
:::

---

## Step 1: System Requirements

Before starting the build, please ensure that the system meets the following conditions:

|Project|Minimum Requirements|Description|
|---|---|---|
|**Operating System**|Windows 10 / 11 (64-bit)|The engine is natively based on Windows and Direct3D 11. It does not support Linux/macOS for now.|
|**Graphics Card and VR Environment**|Graphics card supporting Direct3D 11 + SteamVR + VR headset|Meeting the usual SteamVR running requirements is sufficient.|
|**Python**|64-bit CPython 3.11 or higher version|When installing, please check **Add python.exe to PATH** to ensure that `python` can be directly invoked in CMD.|
|**C++ build tools**|MSVC x64 with C++20 support, Windows SDK, CMake 3.24 or later, and Ninja|Select the "Desktop development with C++" workload in Visual Studio and install its CMake and Ninja components.|

::: warning Use Windows Command Prompt
During the construction and execution of scripts in this project, please always use Windows’ built-in **Command Prompt (CMD)**. Press `Win+R`, type `cmd`, and press Enter. PowerShell handles quotes, parameter passing, and environment variables differently from CMD. This could lead to errors during script construction or installation.
:::

---

## Step 2: Build Engine, the SDK, and the built-in apps

In CMD, change to the source repository root and run `build.bat`.

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
build.bat
```

The default is a Release build with 8 parallel jobs. Use `--configuration` and `--parallel` to set the build configuration and job count.

```cmd
build.bat --configuration Release --parallel 8
```

### Component build directories

The top-level `build.bat` initializes the MSVC x64 environment once in CMD and calls the `build.bat` of each of the 13 components in order. Each script configures and builds its component in its own `build/` directory. The output paths below are relative to the component.

|Component directory|Build output|
|---|---|
|`sdk/engine_interface`|Static library, DLL import library, and CMake package in `build/lib/`. DLL in `build/bin/` and public headers in `build/include/`.|
|`sdk/api/python`|Python SDK package, `engine_interface_native.pyd`, and `engine_interface_native.json` in `build/bin/`.|
|`engine`|`easyvrui_engine.exe`, `easyvrui_service.exe`, `easyvrui_screen_helper.exe`, and SteamVR action resources in `build/bin/`.|
|`app/desktop`, `app/easyvrscreen`, `app/form_designer`, `app/file_manager`, `app/task_manager`, `app/demo/cpp`|Each app's executable and generated runtime resources in its `build/bin/` (`app/easyvrscreen` produces `easyvrui_screen.exe` and `easyvrscreen.easyvrui`; `app/file_manager` also produces `easyvrui_volume_query.exe`).|
|`app/layout/standard_104`, `app/ime/cn/easyvrui_pinyin`, `app/ime/en/easyvrui_english`, `app/ime/jp/easyvrui_japanese`|Each component's executable in its `build/bin/`. The Pinyin and Japanese IMEs also generate precompiled dictionaries in `build/bin/rime/`.|

### Build a single component

You can run `build.bat` directly from a component directory. Before building the native Python extension or a C++ app on its own, build `sdk/engine_interface` with the same configuration. The component uses the prebuilt SDK in `sdk/engine_interface/build/`. This example builds the SDK, then builds Desktop separately.

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo\sdk\engine_interface"
build.bat --configuration Release
cd /d "D:\program\project\EasyVROverlayUIEngine\repo\app\desktop"
build.bat --configuration Release
```

A successful build records its configuration in `build/configuration.txt`. Third-party sources, Rime schemas, and dictionaries are bundled with the repository. You can build offline once the toolchain is installed.

---

## Step three: Install the runtime

After building all 13 components, run `install.bat` from the source repository root. The CMD installer reads each component's `build/` directory and checks that all 13 builds use the same configuration. You must pass an explicit local absolute path separate from the source repository (omitting the path prints usage and exits with code `2`).

Service install (default mode; requires an administrator-protected directory, registers and starts `EasyVROverlayUIEngine`, and sets the system variable `EASYVROVERLAYUIENGINE_HOME` via `setx /M`):

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
install.bat "%ProgramFiles%\EasyVRUI"
```

Portable install (skips service registration and system environment variable writes; start `bin\easyvrui_engine.exe` manually):

```cmd
cd /d "D:\program\project\EasyVROverlayUIEngine\repo"
install.bat "D:\Tools\EasyVRUI" --no-service
```


Below are the directories generated by a fresh installation. The relative paths of each application follow the directory structure in `repo/app/`.

```text
D:\Tools\EasyVRUI\
├── installation.json
├── bin\
│   ├── easyvrui_engine.exe
│   ├── actions\                    # SteamVR action manifest and default controller bindings (actions.json, bindings_*.json)
│   └── config.json
├── app\
│   ├── desktop\
│   │   ├── easyvrui_desktop.exe
│   │   └── config.json
│   ├── form_designer\
│   │   ├── easyvrui_form_designer.exe
│   │   ├── easyvrui_form_designer.easyvrui
│   │   └── resources\             # Form Designer resources
│   ├── file_manager\
│   │   ├── easyvrui_file_manager.exe
│   │   ├── easyvrui_file_manager.easyvrui
│   │   ├── easyvrui_volume_query.exe # Volume query helper
│   │   └── file_manager.json         # File association configuration
│   ├── task_manager\
│   │   ├── easyvrui_task_manager.exe
│   │   └── easyvrui_task_manager.easyvrui
│   ├── demo\
│   │   ├── cpp\
│   │   │   ├── easyvrui_demo_cpp.exe
│   │   │   ├── easyvrui_demo_cpp.easyvrui
│   │   │   └── resources\          # C++ Demo resources
│   │   └── python\
│   │       ├── main.py
│   │       ├── demo\               # Python Demo internal UI modules and image assets
│   │       ├── requirements.txt
│   │       └── easyvrui_demo_python.easyvrui
│   ├── layout\standard_104\easyvrui_layout_standard_104.exe
│   └── ime\
│       ├── cn\easyvrui_pinyin\
│       │   ├── easyvrui_ime_chinese_pinyin.exe
│       │   └── rime\chinese_pinyin\ # Pinyin IME Rime schemas and dictionary data
│       ├── en\easyvrui_english\easyvrui_ime_english.exe
│       └── jp\easyvrui_japanese\
│           ├── easyvrui_ime_japanese.exe
│           └── rime\japanese\      # Japanese IME Rime schemas and dictionary data
└── sdk\
    ├── api\
    │   ├── cpp\
    │   │   ├── include\            # C++ public headers
    │   │   └── third_party\json\    # JSON headers bundled with the C++ API
    │   └── python\
    │       ├── easyvrui\           # Python SDK wrapper package
    │       ├── engine_interface_native*.pyd
    │       ├── engine_interface_native.json
    │       └── requirements.txt
    └── engine_interface\
        ├── include\                # Native interface public headers and json.hpp
        ├── lib\
        │   ├── engine_interface_static.lib
        │   ├── engine_interface.lib
        │   └── cmake\EngineInterface\ # CMake find_package export configs
        └── bin\engine_interface.dll
```

On a fresh installation, `install.bat` creates `bin/config.json`. Engine generates an access credential on its first launch. `installation.json` marks the installation root directory and records the build configuration, Python version, and application list paths. In `bin/config.json`, `desktop` and `provider_list` are based on the `bin/` where the file is located, and the programs are referenced through `../app/...`. `app/desktop/config.json` is based on the Desktop directory, registering the built-in application list, such as `../demo/cpp/easyvrui_demo_cpp.easyvrui`. Each [application list](/en/reference/application_manifest) then parses `launch.executable` or `launch.script` and sub-process working directories using its own directory.

Built C++ applications and Python native extensions are linked to `engine_interface_static` by default. `engine_interface.lib` is the DLL import library, and `engine_interface.dll` is used by selected shared-linked applications. Engine, SDK, and applications each embed the built-in language packs in binary. Applications can also call `language_pack.load_directory()` of the SDK to load custom language packs.

Desktop combines system configurations and those in `%USERPROFILE%\easyvrui\desktop\config.json` with application IDs in memory. A reinstallation will regenerate the system configurations and retain existing Engine configurations and access credentials. Additions and removals on the Desktop interface only affect user configurations.

The Python SDK in the installation directory is located at `sdk/api/python/`. When the Desktop or File Manager launches Python scripts using the SDK, this directory is prefixed to the sub-process’s path, which is set to `PYTHONPATH`, while the original value is retained.

---

## Step four: Startup verification

First, start **SteamVR** and confirm that the headset and controller are ready. Then, start the Engine and C++ example programs in sequence in CMD:

```cmd
start "" "D:\Tools\EasyVRUI\bin\easyvrui_engine.exe"
start "" /D "D:\Tools\EasyVRUI\app\demo\cpp" "D:\Tools\EasyVRUI\app\demo\cpp\easyvrui_demo_cpp.exe"
```

In SteamVR, confirm that the example `window` is displayed, allowing for verification of Engine and SDK connections.

The Python Demo can be launched from the Desktop. When running directly in CMD, use CPython that matches the original extension version and architecture in the installation directory. The following command installs the dependencies declared by the Demo, prepending the shared SDK directory and launching the main script from the application directory.

```cmd
python -m pip install -r "D:\Tools\EasyVRUI\app\demo\python\requirements.txt"
set "PYTHONPATH=D:\Tools\EasyVRUI\sdk\api\python;%PYTHONPATH%"
cd /d "D:\Tools\EasyVRUI\app\demo\python"
python -B main.py
```

### Common issue: No window appears in VR after startup.

If the window is not visible in the field of view, it is usually caused by two reasons:

1. **The headset orientation during startup does not match the current wearing orientation**: The window is defaulted to be generated directly in front of the headset at the moment the program starts. Press the keyboard shortcut **`Ctrl + Alt + Pause`** to reset the engine's `body` reference center and `world` spatial offset to directly in front of the current headset.
2. **SteamVR is not ready**: Ensure that SteamVR has started and recognized the headset. If SteamVR exits or crashes while running, keep the Engine and application running until the old SteamVR process completely exits, then restart SteamVR. The Engine will automatically reconnect and restore window display.

The next chapter will introduce window interactions in the VR space and the functional usage of built-in applications.
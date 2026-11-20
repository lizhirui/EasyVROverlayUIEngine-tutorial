# SteamVR操作与应用导览

完成安装并启动Engine后，本篇将介绍VR空间内的基本交互操作、输入法与快捷键，以及随Engine一同安装的标准内置应用。

![VR空间工作区全景](/images/zh/vr_hero_workspace.png)

---

## SteamVR空间操作

在EasyVROverlayUIEngine中，每个`window`都是悬浮在3D空间中的独立交互表面，可以直接使用VR手柄进行操作：

### 激光点击与双面交互

- **激光点按（扳机键Trigger）**：左右手柄均会投射激光射线，指向按钮、输入框或菜单并扣下扳机即可触发点击。
- **正反面均可交互**：当窗口旋转至背面朝向用户时，背面同样支持激光点击与拖拽操作。
- **重叠窗面**：未捕获指针时，激光止于最近的可见窗面。禁用或被模态对话框阻塞的窗面仍遮挡后方窗口。要操作后方窗口，可移动遮挡物、改变指向，或先结束前方的模态交互。
- **摇杆平滑滚动**：将激光指向带有滚动条的`listbox`、多行`textbox`或`scrollpanel`时，上下推动对应手柄的**摇杆（Thumbstick）**即可平滑滚动，推动幅度越大速度越快。

### 单手抓取、双手控制环与边角调节

窗口四周提供了多个空间交互区域用于调整位置、角度与弯曲度：

![窗口曲率调节角与双手控制环](/images/zh/vr_curvature_and_handles.png)

|操作部位|操作方式|功能说明|
|---|---|---|
|**窗口空白区域（侧握键Grip）**|在`world`/`body`参考模式下单手按住侧握键|执行**6DoF空间移动与旋转**，可将窗口自由拖动至合适位置|
|**控制环控制块（侧握键Grip）**|双手各抓住窗口外围控制环上的一个控制块|触发**双手约束旋转**。系统会根据选中的控制块组合自动锁定旋转轴（`X`/`Y`/`Z`等），避免单手旋转时的抖动偏差|
|**左下角曲率柄 / 右下角缩放柄**|激光指向对应角并按住**扳机键（Trigger）**，同时推动手柄摇杆|左下角配合**摇杆左右**调整水平柱面弯曲角度（交互上限160°，**双击左下角可恢复平面**）；右下角配合**摇杆上下**调整窗口的`physical_scale`（物理缩放）|

::: tip 切换跟踪参考系
窗口标题栏右上角关闭按钮旁设有**`⊕`跟踪模式切换按钮**，点击可在`world`/`body`/`head`/`left`/`right`之间切换。例如切换为`left`后，窗口会固定跟随左手柄移动。
:::

---

## 文本输入与全局快捷键

EasyVROverlayUIEngine同时支持**VR虚拟键盘输入**和**实体键盘接管**两种模式。

### 输入条、候选窗与虚拟键盘

在VR中点击任意`textbox`或可编辑`combobox`时，引擎会自动在输入框正下方居中对齐并展开输入界面栈：

![输入条、候选框与虚拟键盘三层界面栈](/images/zh/vr_input_stack.png)

1. **输入条（最上层）**：显示当前输入语言、活跃IME名称以及**“输入法切换”**按钮。点击可打开模态窗口切换语言、IME和虚拟键盘布局。
2. **IME候选界面（中间层）**：显示拼音或假名组合串及候选词列表，可通过数字键、空格或激光点击选词上屏（英文直通IME无需候选词时可仅显示输入条）。
3. **虚拟键盘（最底层）**：独立的104键虚拟键盘。虚拟模式显示键盘。通过`Pause`切换到实体键盘模式后，输入条和IME候选窗继续工作。

### 实体键盘模式与全局快捷键

|快捷键|适用条件|功能说明|
|---|---|---|
|**`Pause`**|存在有效当前VR窗口|开启/关闭**实体键盘模式**。开启后实体键盘按键由Engine路由至当前VR窗口，不干扰桌面应用|
|**`Alt+Shift`**|实体键盘模式且存在当前窗口|切换输入语言，恢复该语言上次使用的IME并保留`textbox`焦点|
|**`Alt`**|实体键盘模式且当前窗口有可用的`menubar`|按住时显示助记符下划线。单独按下再松开时进入或退出菜单键盘导航|
|**`Ctrl + Shift`**|实体键盘模式 + 存在当前窗口|在当前语言内切换不同的IME|
|**`Tab` / `Shift + Tab`**|存在当前窗口|在窗口内各控件之间按Tab序向前/向后切换焦点|
|**`PrintScreen`**|实体键盘模式 + 存在当前窗口|截取当前VR视角画面并复制到Windows剪贴板|
|**`Ctrl + Pause`**|**全局有效**（无需先选中窗口）|显示或隐藏**Desktop（VR桌面启动器）**|
|**`Ctrl + Alt + Pause`**|**全局有效**|重置**`body`跟踪中心**与**`world`空间偏移**，将窗口基准拉回当前头显正前方|

::: warning 按下`Pause`无效时的排查方法
开启实体键盘模式前，请先用激光点击目标VR窗口，确保Engine已建立有效当前窗口。退出实体键盘模式后，按键将恢复发送给Windows桌面。
:::

---

## 随安装提供的应用

随安装提供的应用和输入组件位于`app/`。Engine依据`bin/config.json`启动Desktop、layout和IME。以下路径均相对于[安装根目录](/basics/01_install_and_setup)。

### 1. Desktop（VR桌面启动器）

![Desktop应用启动器](/images/zh/desktop.png)

图中是空白用户配置下的Desktop。五个图标对应系统配置中的C++演示、Python演示、文件管理器、窗体设计器和任务管理器。

- **呼出方式**：按`Ctrl+Pause`。Engine使用配置中的`app/desktop/easyvrui_desktop.exe`。
- **主要功能**：每次呼出时以`world`参考定位到当前头显前方。Desktop在内存中按应用ID合并`app/desktop/config.json`登记的内置应用与`%USERPROFILE%\easyvrui\desktop\config.json`登记的自定义应用。添加和移除只写用户配置。
- **关闭行为**：点击右上角关闭按钮仅隐藏Desktop窗口，后台进程保持运行，再次按`Ctrl + Pause`即可立即重新显示。

### 2. File Manager（VR文件管理器）

![File Manager文件管理器](/images/zh/file_manager.png)

- **打开方式**：从Desktop启动，或直接运行`app/file_manager/easyvrui_file_manager.exe`。
- **主要功能**：在VR内直接浏览本地磁盘与目录、查看路径并启动应用，支持同时打开多个窗口实例。

### 3. Task Manager（VR任务管理器）

![Task Manager任务管理器](/images/zh/task_manager.png)

- **打开方式**：从Desktop启动，或直接运行`app/task_manager/easyvrui_task_manager.exe`。
- **主要功能**：实时查看连接到Engine的所有应用会话、各窗口的`name`与`title`、内存占用以及CPU/GPU使用率，并支持关闭指定窗口或终止应用进程（Desktop与输入组件受系统保护）。

### 4. 独立虚拟键盘（`standard_104`）

![标准104虚拟键盘](/images/zh/layout_keyboard.png)

- 可执行文件位于`app/layout/standard_104/easyvrui_layout_standard_104.exe`。
- 作为独立进程通过标准协议接入Engine，开发者也可自行编写并替换自定义键盘布局。

### 5. 中/英/日三语输入法（IME）

![IME拼音与日语候选窗](/images/zh/ime_candidates.png)

图中上方是拼音候选窗，下方是日文候选窗。拼音候选窗固定使用中文，日文候选窗固定使用日文。各自上方的输入条由SDK按界面语言显示，因此两处都可显示中文“输入法切换”。

- **EasyVRUI拼音**位于`app/ime/cn/easyvrui_pinyin/easyvrui_ime_chinese_pinyin.exe`。Rime运行词库在该应用目录的`rime/chinese_pinyin/`，用户词典及动态词频在`%USERPROFILE%\easyvrui\chinese_pinyin`。单按`Shift`可切换中英文。源码中的`import_user_dictionary.py`可导入搜狗`.scel`或`.tsv`。
- **EasyVRUI English**位于`app/ime/en/easyvrui_english/easyvrui_ime_english.exe`，提供英文直通输入。
- **EasyVRUI日本語**位于`app/ime/jp/easyvrui_japanese/easyvrui_ime_japanese.exe`。Rime运行词库在该应用目录的`rime/japanese/`，用户数据在`%USERPROFILE%\easyvrui\japanese`。它支持空格转换、回车提交、`F6`至`F10`转换，以及通过`Alt+Backquote`或`Ctrl/Alt/Shift+CapsLock`切换模式。

接着运行[第一个window示例](/basics/03_first_window)，按初始外观与点击后的截图核对输入和事件分发。

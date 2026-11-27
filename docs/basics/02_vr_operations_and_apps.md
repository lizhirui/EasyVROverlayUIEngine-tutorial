# SteamVR操作与应用导览

完成安装并启动Engine后，本篇将介绍VR空间内的基本交互操作、输入法与快捷键，以及随Engine一同安装的标准内置应用。

![VR空间工作区全景](/images/zh/vr_hero_workspace.png)

---

## SteamVR空间操作

在EasyVROverlayUIEngine中，每个`window`都是悬浮在3D空间中的独立交互表面，可以直接使用VR手柄进行操作：

### 激光点击与双面交互

- **激光点按（扳机键Trigger）**：左右手柄各自独立投射激光射线与捕获状态；`world`/`body`/`head`窗口可双手操作，固定在`left`手柄的窗口由右手交互，固定在`right`手柄的窗口由左手交互（关联辅助输入表面遵循同一规则）。有效交点处沿窗面切平面显示命中圆点，按下时通过滤波稳定落点，按住跨窗后需松开再按。处于命中或捕获状态的交互手会单独提升SteamVR动作集优先级以屏蔽冲突动作，离开后恢复。
- **正反面均可交互**：当窗口旋转至背面朝向用户时，背面同样支持激光点击与拖拽操作。
- **重叠窗面**：未捕获指针时，激光止于最近的可见窗面。禁用或被模态对话框阻塞的窗面仍遮挡后方窗口。要操作后方窗口，可移动遮挡物、改变指向，或先结束前方的模态交互。
- **摇杆平滑滚动**：将激光指向带有滚动条的`listbox`、多行`textbox`或`scrollpanel`时，上下推动对应手柄的**摇杆（Thumbstick）**即可平滑滚动，推动幅度越大速度越快。

### 单手抓取、双手控制环与边角调节

窗口四周的空间交互区域受`movable`、`rotatable`、`resizable`、`scalable`和`curvature_adjustable`五个属性独立控制：

![窗口曲率调节角与双手控制环](/images/zh/vr_curvature_and_handles.png)

|操作部位|操作方式|功能说明|
|---|---|---|
|**窗口空白区域（侧握键Grip）**|在`world`/`body`参考模式下单手按住侧握键（需启用`movable`）|执行**6DoF空间移动与旋转**，可将窗口自由拖动至合适位置|
|**控制环控制块（侧握键Grip）**|双手各抓住窗口外围控制环上的一个控制块（需启用`rotatable`）|触发**双手约束旋转**。系统会根据选中的控制块组合自动锁定旋转轴（`X`/`Y`/`Z`等），避免单手旋转时的抖动偏差|
|**控制环四边 / 四角（扳机键Trigger）**|激光指向外围控制块并按住扳机拖动（需启用`resizable`）|调整窗口**客户区逻辑尺寸**（四边单轴缩放，四角等比缩放，对侧锚点保持原位）|
|**左下角曲率柄 / 右下角缩放柄**|激光指向对应角并按住**扳机键（Trigger）**，同时推动手柄摇杆|左下角（`curvature_adjustable`）配合**摇杆左右**调整水平柱面弯曲角度（交互上限160°，**双击左下角可恢复平面**）；右下角（`scalable`）配合**摇杆上下**调整窗口的`physical_scale`（物理缩放）|

::: tip 切换跟踪参考系
窗口标题栏右上角关闭按钮旁设有**`⊕`跟踪模式切换按钮**，点击可在`world`/`body`/`head`/`left`/`right`之间切换。例如切换为`left`后，窗口会固定跟随左手柄移动。
:::

---

## 文本输入与全局快捷键

EasyVROverlayUIEngine同时支持**VR虚拟键盘输入**和**实体键盘接管**两种模式。

### 输入条、候选窗与虚拟键盘

在VR中点击可编辑的`textbox`、可编辑`combobox`或启用了键盘/IME的`screen`时，SDK按控件开关唤起输入界面。输入区开启且启用IME时按键先经IME路由，输入区关闭或IME关闭时按键直接投递给当前窗口所属SDK。虚拟键盘模式下，三层辅助界面在输入区正下方横向居中堆叠；实体键盘模式下，输入条右上角贴合当前窗口右下角，IME候选窗仍在输入区下方居中：

![输入条、候选框与虚拟键盘三层界面栈](/images/zh/vr_input_stack.png)

1. **输入条（最上层）**：启用IME时显示当前输入语言、活跃IME名称以及**“输入法切换”**按钮。点击可打开模态窗口切换语言、IME和虚拟键盘布局。
2. **IME候选界面（中间层）**：显示拼音或假名组合串及候选词列表，可通过数字键、空格或激光点击选词上屏（英文直通IME无需候选词时可仅显示输入条）。
3. **虚拟键盘（最底层）**：独立的104键虚拟键盘。虚拟模式显示键盘。通过`Pause`切换到实体键盘模式后，输入条和IME候选窗继续工作。

### 实体键盘模式与全局快捷键

|快捷键|适用条件|功能说明|
|---|---|---|
|**`Pause`**|全局切换模式，存在有效当前VR窗口时启用拦截|开启/关闭**实体键盘模式**。开启后实体键盘按键由Engine按输入路径路由至当前VR窗口，不干扰桌面应用|
|**`Alt+Shift`**|实体键盘模式且存在当前窗口|切换输入语言，恢复该语言上次使用的IME并保留`textbox`焦点|
|**`Alt`**|实体键盘模式且当前窗口有可用的`menubar`|按住时显示助记符下划线。单独按下再松开时进入或退出菜单键盘导航|
|**`Ctrl + Shift`**|实体键盘模式 + 存在当前窗口|在当前语言内切换不同的IME|
|**`Tab` / `Shift + Tab`**|存在当前窗口|在窗口内各控件之间按Tab序向前/向后切换焦点|
|**`PrintScreen`**|实体键盘模式 + 存在当前窗口|截取当前VR视角画面，以PNG和Windows位图格式复制到剪贴板，并在视野中央显示约2秒输入穿透提示|
|**`Alt + PrintScreen`**|实体键盘模式 + 存在当前窗口|复制当前选中普通窗口的展开平面渲染纹理，写入剪贴板并显示约2秒居中输入穿透提示|
|**`Ctrl + Pause`**|**全局有效**（无需先选中窗口）|显示或隐藏**Desktop（VR桌面启动器）**|
|**`Ctrl + Alt + Pause`**|**全局有效**|重置**`body`跟踪中心**与**`world`空间偏移**，并在新的World原点显示15秒红色十字提示|

::: warning 按下`Pause`无效时的排查方法
开启实体键盘模式前，请先用激光点击目标VR窗口，确保Engine已建立有效当前窗口。退出实体键盘模式后，按键将恢复发送给Windows桌面。
:::

---

## 随安装提供的应用

随安装提供的应用和输入组件位于`app/`。Engine依据`bin/config.json`启动Desktop、layout和IME（安装脚本默认将Desktop的`run_as_administrator`设为`true`）。Desktop、File Manager、Task Manager、Form Designer、EasyVRScreen及Demo在界面操作失败时通过SDK错误对话框（`messagebox` / `show_messagebox`）在VR内反馈，关闭提示后返回原窗口；无头输入组件（layout与IME）的启动异常写入标准错误。以下路径均相对于[安装根目录](/basics/01_install_and_setup)。

### 1. Desktop（VR桌面启动器）

![Desktop应用启动器](/images/zh/desktop.png)

安装器生成的系统配置包含6个内置应用：C++演示、Python演示、EasyVRScreen（屏幕查看器）、文件管理器、窗体设计器和任务管理器。

- **呼出方式**：按`Ctrl+Pause`。Engine使用配置中的`app/desktop/easyvrui_desktop.exe`。
- **主要功能**：每次呼出时以`world`参考定位到当前头显前方。Desktop在内存中按应用ID合并`app/desktop/config.json`登记的内置应用与`%USERPROFILE%\easyvrui\desktop\config.json`登记的自定义应用。添加和移除只写用户配置；支持识别清单中的`run_as_administrator`并显示管理员盾牌与管理员启动操作（详见[应用清单参考](/reference/application_manifest)）。
- **关闭行为**：点击右上角关闭按钮仅隐藏Desktop窗口，后台进程保持运行，再次按`Ctrl + Pause`即可立即重新显示。

### 2. EasyVRScreen（多显示器VR屏幕查看器）

- **打开方式**：从Desktop启动，或直接运行`app/easyvrscreen/easyvrui_screen.exe`（清单`app/easyvrscreen/easyvrscreen.easyvrui`）。
- **主要功能**：自动枚举全部Windows显示器并为每个显示器创建独立的无边框可弯曲VR窗口，支持显示器热插拔自动同步。鼠标/激光悬停对应屏幕底部呼出工具栏，可切换指针输入、实体键盘转发、虚拟键盘与IME开关，查看实时捕获FPS与渲染FPS，并支持位置重置、固定工具栏和退出。配置保存在`%LOCALAPPDATA%\easyvrui\easyvrscreen\config.json`（参见[screen控件指南](/guide/controls/command-and-display/screen)）。

### 3. File Manager（VR文件管理器）

![File Manager文件管理器](/images/zh/file_manager.png)

- **打开方式**：从Desktop启动，或直接运行`app/file_manager/easyvrui_file_manager.exe`。
- **主要功能**：在VR内浏览本地磁盘、映射网络驱动器（显示UNC目标）及网络共享，支持同时打开多个窗口实例。地址栏支持面包屑导航与路径编辑，可输入`\\server`枚举磁盘共享或输入`\\server\share\dir`直接进入目录（可见性取决于当前Windows账号权限），并通过后台卷查询助手`easyvrui_volume_query.exe`避免阻塞主界面。支持直接启动`.easyvrui`清单、按`file_manager.json`关联打开文件及在具备权限时以管理员身份运行。

### 4. Task Manager（VR任务管理器）

![Task Manager任务管理器](/images/zh/task_manager.png)

- **打开方式**：从Desktop启动，或直接运行`app/task_manager/easyvrui_task_manager.exe`。
- **主要功能**：应用列表页实时展示连接到Engine的所有应用会话、各窗口的`name`与`title`、内存占用以及CPU/GPU会话指标，支持关闭指定窗口或终止应用进程（Desktop与输入组件受系统保护）。独立的**GPU标签页**支持切换本机显卡适配器、按PID或程序分组、按列排序并查看专用/共享显存、3D/Copy利用率及复制通道，可对选中的可操作PID行执行确认后结束进程。

### 5. 独立虚拟键盘（`standard_104`）

![标准104虚拟键盘](/images/zh/layout_keyboard.png)

- 可执行文件位于`app/layout/standard_104/easyvrui_layout_standard_104.exe`。
- 作为独立进程通过标准协议接入Engine，开发者也可自行编写并替换自定义键盘布局。

### 6. 中/英/日三语输入法（IME）

![IME拼音与日语候选窗](/images/zh/ime_candidates.png)

图中上方是拼音候选窗，下方是日文候选窗。拼音候选窗固定使用中文，日文候选窗固定使用日文。各自上方的输入条由SDK按界面语言显示，因此两处都可显示中文“输入法切换”。

- **EasyVRUI拼音**位于`app/ime/cn/easyvrui_pinyin/easyvrui_ime_chinese_pinyin.exe`。Rime运行词库及万象LTS简体文法模型位于该应用目录的`rime/chinese_pinyin/`，用户词典及动态词频在`%USERPROFILE%\easyvrui\chinese_pinyin`。单按`Shift`可切换中英文。源码中的`import_user_dictionary.py`可导入`.scel`或`.tsv`词库。
- **EasyVRUI English**位于`app/ime/en/easyvrui_english/easyvrui_ime_english.exe`，提供英文直通输入。
- **EasyVRUI日本語**位于`app/ime/jp/easyvrui_japanese/easyvrui_ime_japanese.exe`。Rime运行词库在该应用目录的`rime/japanese/`，用户数据在`%USERPROFILE%\easyvrui\japanese`。它支持空格转换、回车提交、`F6`至`F10`转换，以及通过`Alt+Backquote`或`Ctrl/Alt/Shift+CapsLock`切换模式。

接着运行[第一个window示例](/basics/03_first_window)，按初始外观与点击后的截图核对输入和事件分发。

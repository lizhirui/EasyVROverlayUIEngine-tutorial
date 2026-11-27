# SteamVR Controls and Built-in Applications

After completing the installation and launching the Engine, this article will introduce basic interactive operations, input methods, and shortcuts within the VR space, as well as the standard built-in applications installed with the Engine.

![Panoramic View of the VR Space Working Area](/images/en/vr_hero_workspace.png)

---

## SteamVR Space Operations

In the EasyVROverlayUIEngine, each `window` is an independent interactive surface suspended in the 3D space, which can be operated directly with the VR controller:

### Laser Clicking and Double-Sided Interaction

- **Laser Pointing (Trigger):** Both left and right controllers emit laser beams that point to buttons, input fields, or menus. Pulling the trigger triggers a click.
- **Interaction on Both Sides:** When the window rotates to the back side facing the user, laser clicking and dragging are also supported on the back side.
- **Overlapping Window Surfaces:** When the pointer is not captured, the laser stops at the nearest visible window surface. Windows that are disabled or blocked by modal dialog boxes still block the rear window. To operate the rear window, you can move the obstruction, change the direction, or end the modal interaction in front.
- **Smooth Rolling with Thumbstick:**When the laser is directed at a `listbox` with a scroll bar, a multi-line `textbox`, or `scrollpanel`, pushing the**thumbstick** of the corresponding controller allows smooth rolling. The greater the push, the faster the speed.

### One-Hand Grabbing, Two-Hand Control Rings, and Corner Adjustment

Multiple spatial interaction areas are provided around the window to adjust position, angle, and curvature:

![Window Curvature Adjustment Angle and Two-Hand Control Rings](/images/en/vr_curvature_and_handles.png)

|Operation Points|Operation Methods|Function Descriptions|
|---|---|---|
|**Blank Area of the Window (Side Grip Key)**|In the `world`/`body` reference mode, hold the side grip key with one hand.|Performing **6DoF spatial movement and rotation** allows the window to be freely dragged to the appropriate position.|
|**Control Ring Block Control (Side Grip Key)**|Hold one control block on each of the control rings around the window with both hands.|Trigger **Two-Hand Restricted Rotation.** The system automatically locks the rotation axis based on the selected control block combination (`X`/`Y`/`Z`, etc.), preventing jitter and deviation during one-handed rotation.|
|**Left Bottom Corner Curvature Handle / Right Bottom Corner Zoom Handle**|Point the laser at the corresponding corner and press the **Trigger**, while pushing the thumbstick.|At the bottom left corner, adjust the bending angle of the horizontal surface by moving the **joystick left and right**(maximum interaction angle is 160°;**double-clicking the bottom left corner restores to the flat position**). At the bottom right corner, adjust the `physical_scale` of the window by moving the **joystick up and down** (physical scaling).|

::: tip Switch the tracking reference
Next to the close button in the upper right corner of the window title bar, there is a **`⊕` tracking mode switch button**. Clicking this button allows switching between `world`, `body`, `head`, `left`, and `right`. For example, after switching to `left`, the window will automatically follow the movement of the left handle.
:::

---

## Text input and global shortcuts

EasyVROverlayUIEngine supports both **VR virtual keyboard input**and**physical keyboard override** modes.

### Input bar, candidate window, and virtual keyboard

In VR, when clicking any `textbox` or editable `combobox`, the engine will automatically align and expand an input interface stack directly below the input box:

Three-tier interface stack: ![input bar, candidate box, and virtual keyboard for](/images/en/vr_input_stack.png)

1. **Input bar (topmost)**: Displays the current input language, active IME name, and the **“Input Method Switch”** button. Clicking this button opens a modal window to switch languages, IME, and virtual keyboard layout.
2. **IME candidate interface (middle tier)**: Displays a pinyin or kana combination string and a list of candidate words. You can select a word using numeric keys, space, or laser click. For English, direct IME mode only shows the input bar when no candidate words are needed.
3. **Virtual keyboard (bottommost)**: A separate 104-key virtual keyboard. The keyboard is displayed in virtual mode. After switching to physical keyboard mode via `Pause`, the input bar and IME candidate window continue to function.

### Physical keyboard mode and global shortcuts

|Shortcuts|Conditions of application|Function Descriptions|
|---|---|---|
|**`Pause`**|There must be a valid current VR window.|**Physical keyboard mode** must be enabled/disabled. When enabled, physical keyboard keys are routed to the current VR window without interfering with desktop applications.|
|**`Alt+Shift`**|Physical keyboard mode and current window present|Switch input language, restore the last used IME for that language, and maintain focus on `textbox`.|
|**`Alt`**|Physical keyboard mode and the current window has an available `menubar`|Show mnemonics underlines when held. Pressing separately and releasing switches between menu keyboard navigation.|
|**`Ctrl + Shift`**|Physical keyboard mode + current window present|Switch between different IMEs within the current language|
|**`Tab` / `Shift + Tab`**|Current window present|Switch focus forward/backward in Tab order among controls within the window|
|**`PrintScreen`**|Physical keyboard mode + current window present|Capture the current VR view as PNG and Windows bitmap to the clipboard, then show a ~2s centered pass-through toast|
|**`Alt + PrintScreen`**|Physical keyboard mode + current window present|Capture the flat D3D render texture of the active normal window to the clipboard, then show a ~2s centered pass-through toast|
|**`Ctrl + Pause`**|**Global** (no active window required)|Show or hide **Desktop (VR Desktop Launcher)**|
|**`Ctrl + Alt + Pause`**|**Global**|Reset the **`body` tracking center** and **`world` offset**, displaying a red cross at the new World origin for 15 seconds|

::: warning Troubleshooting the Pause shortcut
Before enabling the physical keyboard mode, please use a laser to click on the target VR window to ensure that the Engine has established a valid current window. After exiting the physical keyboard mode, the key presses will be sent back to the Windows desktop.
:::

---

## Applications provided with the installation

The applications and input components provided with the installation are located at `app/`. The Engine launches the Desktop, layout, and IME based on `bin/config.json`. All paths are relative to the [installation root directory,](/en/basics/01_install_and_setup).

### 1. Desktop (VR Desktop Launcher)

![Desktop application launcher](/images/en/desktop.png)

The installer registers six built-in applications in `app/desktop/config.json`: C++ Demo, Python Demo, EasyVRScreen (Screen Viewer), File Manager, Form Designer, and Task Manager. Built-in GUI apps report operational errors via VR `messagebox` / `show_messagebox` dialogs.

- **Show / Hide**: Press `Ctrl+Pause`. Engine uses `app/desktop/easyvrui_desktop.exe` (installed with `run_as_administrator: true` by default).
- **Main functions**: Each time it is shown, Desktop positions itself in front of the current headset in `world` space. It merges system entries from `app/desktop/config.json` with user entries from `%USERPROFILE%\easyvrui\desktop\config.json` by application ID, and supports manifest `run_as_administrator` badges and elevated launch.
- **Close behavior**: Clicking the close button in the upper right corner hides the Desktop window while keeping the process running; pressing `Ctrl + Pause` shows it again immediately.

### 2. EasyVRScreen (Multi-Monitor VR Screen Viewer)

- **Open method**: Launch from Desktop or run `app/easyvrscreen/easyvrui_screen.exe` (`app/easyvrscreen/easyvrscreen.easyvrui`).
- **Main functions**: Creates an independent frameless, curvable VR window per Windows monitor with hot-plug synchronization. Hovering near the bottom edge reveals a toolbar with Pointer, Keyboard, Virtual Keyboard, and IME toggles, live Capture/Render FPS readouts, Reset/Pin controls, and Exit. Settings are stored in `%LOCALAPPDATA%\easyvrui\easyvrscreen\config.json`.

### 3. File Manager (VR File Manager)

![File Manager](/images/en/file_manager.png)

- **Open method**: Launch from Desktop or run `app/file_manager/easyvrui_file_manager.exe` directly.
- **Main functions**: Browse local drives, mapped network drives (showing UNC targets), and `\\server` / `\\server\share` network paths with a breadcrumb/editable address bar, background volume query pool (`easyvrui_volume_query.exe`), `.easyvrui` launching, file associations (`file_manager.json`), and elevated launch when permitted.

### 4. Task Manager (VR Task Manager)

![Task Manager](/images/en/task_manager.png)

- **Open method**: Launch from Desktop or run `app/task_manager/easyvrui_task_manager.exe` directly.
- **Main functions**: View connected application sessions, window `name`/`title`, memory, and CPU/GPU metrics, plus a dedicated **GPU** tab supporting adapter selection, PID/program grouping, sorting, dedicated/shared VRAM, 3D/Copy utilization, and confirmed process termination.

### 4. Independent Virtual Keyboard (`standard_104`)

![Standard 104 Virtual Keyboard](/images/en/layout_keyboard.png)

- The executable file is located at `app/layout/standard_104/easyvrui_layout_standard_104.exe`.
- It connects to the Engine as an independent process through standard protocols. Developers can also write and replace custom keyboard layouts themselves.

### 5. Three-language input methods: Chinese/English/Japanese (IME)

![IME Pinyin and Japanese candidate windows:](/images/en/ime_candidates.png)

Above is the Pinyin candidate window, and below is the Japanese candidate window. The input bar above each window is displayed in the interface language by the SDK, so “Input Method Switch” can be shown in Chinese in both places.

- **EasyVRUI Pinyin** is located at `app/ime/cn/easyvrui_pinyin/easyvrui_ime_chinese_pinyin.exe`. The Rime dictionary is stored in `rime/chinese_pinyin/` of this application directory, while the user dictionary and dynamic word frequencies are in `%USERPROFILE%\easyvrui\chinese_pinyin`. Pressing `Shift` switches between Chinese and English. The source code in `import_user_dictionary.py` can be imported into Sogou’s `.scel` or `.tsv`.
- **EasyVRUI English** is located at `app/ime/en/easyvrui_english/easyvrui_ime_english.exe` and provides direct English input.
- **EasyVRUI Japanese** is located at `app/ime/jp/easyvrui_japanese/easyvrui_ime_japanese.exe`. The Rime dictionary is stored in `rime/japanese/` of this application directory, and user data is in `%USERPROFILE%\easyvrui\japanese`. It supports space conversion, Enter submission, conversion between `F6` and `F10`, as well as mode switching through `Alt+Backquote` or `Ctrl/Alt/Shift+CapsLock`.

Then run the first window example of [Create and run your first window](/en/basics/03_first_window). Compare the input and event distribution with the initial appearance and the screenshot after clicking.
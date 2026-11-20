# menubar

`menubar` organizes the commands into a hierarchical menu at the top of the window. The root `menuitem` serves as the top entry, while the child `menuitem` represents individual commands or sub-menus. `menubar` is assigned to `window.menu`, and `window` manages the layout, focus, and command access. For inherited members, see the [container interface and](/en/guide/controls/common-api#container-control).

## Default appearance

The default line height is 32 logical pixels, using SDK fonts. Screenshots add two `menuitem`s for "Task" and "View", maintaining standard positions and off states.

The default appearance of the ![menubar is](/images/en/menubar_default.png).

## Property comparison

The comparison image uses 42 logical pixels line height and custom fonts. In the above image, holding down `Alt` shows `T` and `V` with underlined text. In the following image, pressing `Alt` once and using the direction key to expand "Task" shows underlined mnemonics for sub-items, as well as the shortcut keys, selected states, and disabled states of `Ctrl+R`.

Comparison of ![menubar properties with](/images/en/menubar_comparison.png).

## Mnemonic keys and keyboard navigation.

In `menuitem.text`, mark the next character with `&`; for example, `任务(&T)` is displayed as "Task(T)". Holding down `Alt` or using keyboard navigation in the menu, `T` is underlined. Pressing `Alt` separately and then releasing allows entry or exit from menu navigation. You can move with the direction keys, select with mnemonic keys, or execute the current command using `Enter`. When the character `&` needs to be displayed, it is written as `&&`.

In entity keyboard mode, `Alt+Shift` switches the IME language while retaining the current editing focus of `textbox`. Different mnemonic keys are assigned to `menuitem` of the same level. `shortcut` provides direct shortcut keys for commonly used commands.

## Interface reference

C++ reads and writes attributes using the methods in the table. In Python, access is done through attributes with the same name. Callbacks receive `source` and `event`. Each strong-type parameter in the table inherits from `event_args_t`; basic parameters do not have additional fields. Python type names are omitted in `_t`.

### Property

|Property|C++ access methods|Types, default values, and uses|
|---|---|---|
|`font`、`row_height`|`get_font`、`set_font`、`get_row_height`、`set_row_height`|Font and positive logical pixel line height, with a default line height of 32.|
|`open`|`get_is_open`|Python read-only property, representing the menu navigation state.|
|`owning_menubar`|`get_menubar`|Read-only, querying the associated `menubar`.|
|`control_list`|`get_control_list`|The collection of the root `menuitem`. Submenu content is placed in the corresponding item's `control_list`.|
|`visible`、`enabled`|`get_visible`、`set_visible`、`get_enabled`、`set_enabled`|Inherited switch. Turning visibility or interactivity off will affect the active menu branches.|
|`focusable`|`is_focusable`|Read-only, supporting menu focus.|

### Method

|Method|Purpose|
|---|---|
|`menubar(name)`|Constructing menu objects and assigning them to `window.menu`.|
|`open_menu()`、`close(restore_focus=True)`|Python enters or exits the menu state. The entry method for C++ is `open()`, and you can also choose to restore focus when closing.|
|`is_submenu_open(item)`|Querying whether a specified sub-menu is open. The method for C++ is `get_is_submenu_open(item)`.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_font_changed`、`on_row_height_changed`|`event_args_t`|Changes in font size or line height configuration.|
|`on_opening`、`on_closed`|`event_args_t`|Notifications when the menu starts and closes.|
|`on_item_added`、`on_item_removed`|`menu_item_event_args_t`|Collection operations for sub-items, including `item` and `index`.|

## menuitem

|Property|Purpose|
|---|---|
|`text`|Displaying text. You can specify mnemonic keys using `&`.|
|`icon`|Optional `drawing_image`.|
|`shortcut`|Command shortcut keys, such as `Ctrl+R`.|
|`checkable`、`checked`|Control whether it can be selected and the current selection state.|
|`separator`|Display separators.|
|`open`|Python read-only property, checks if the submenu of this item is open. C++ is queried through its associated `menubar`.|
|`control_list`|Manage the sub-`menuitem` to form a nested menu.|

Created using `menuitem(name)`. The properties of C++ are accessed via `get_` and `set_`. Item events include `on_text_changed`, `on_icon_changed`, `on_shortcut_changed`, `on_checkable_changed`, `on_checked_changed`, `on_separator_changed`, `on_opening`, `on_closed`, and inherited `on_click`, with parameter `event_args_t`. Subsets also provide `on_item_added` and `on_item_removed`.

## Independent routine

Open “Tasks” and select “Refresh Records”. The command processing function updates the status text. You can also press `Alt` directly in the window where keyboard input is received, use the direction keys to expand the menu, then execute the command with `Enter`, or directly press `Ctrl+R`.

Prepare, build, and install the](/en/basics/01_install_and_setup) Engine according to the [environment. Execute the command in the x64 Developer CMD of the tutorial root directory, and replace the SDK installation path in the example.

### C++

```bat
cmake -S examples/guide/controls/command-and-display/menubar/cpp -B .work/example_menubar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_menubar --config Release
.work\example_menubar\Release\tutorial_menubar.exe
```

When using a single-configured Ninja, run the executable directly from the build directory.

<<< ../../../../../examples/guide/controls/command-and-display/menubar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\menubar\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/menubar/python/menubar_demo.py

### Run the effect

The ![menubar runs independently with](/images/en/menubar_demo.png).

## Common problems and layout practices

- The top area is laid out with `window.menu`. The text control must reserve space for the title bar and the height where the menu is located.
- Centralize the same business commands in `on_click`, allowing shared logic for laser, mnemonic keys, and shortcut keys.
- Command names should be suitable for the length of each language. Leave margins for the shortcut trigger text and icons in the submenu.
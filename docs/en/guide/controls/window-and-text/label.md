# label

`label` is used to display page descriptions, status, and field titles. By default, it has a transparent background, text is left-aligned, and does not take up tab focus order. The status color should be paired with clear text to ensure users can distinguish between connected, successful, and failed states.

Inherit the public control interface [, as well as the text style interfaces](/en/guide/controls/common-api#control) and [from](/en/guide/controls/common-api#text-control).

## Default appearance

By default, `text` is empty. The following figure only sets example text and a rectangle, retaining the SDK font, color, and transparent background.

The default appearance of ![label is](/images/en/label_default.png).

## Property comparison

The same text is retained from top to bottom, showing the default appearance, bold font, green text on solid background, and the text color after being disabled. `label` does not have independent alignment properties; adjustments are needed when changing its placement, using `rect` accordingly. For precise alignment, custom drawing is required.

A comparison of the label properties of ![and](/images/en/label_comparison.png).

## Interface reference

C++ properties can be read and written through the access methods in the table; Python accesses them through the same-named properties. The event parameters in the table use C++ type names, with the corresponding Python types omitting the `_t` suffix. Common members are found in the basic interface of [,](/en/guide/controls/common-api).

### Property

|Property|C++|Purpose and default values|
|---|---|---|
|`text`|`get_text`、`set_text`|Text for reading, writing, and displaying, initially a empty string.|
|`font`、`foreground_color`、`background_color`|`get_font`、`set_font`、`get_foreground_color`、`set_foreground_color`、`get_background_color`、`set_background_color`|It inherits style properties. The default font size is 18, and the background is transparent.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`label(name)`|`label(name)`|Create a `label`.|

### Event

|Event|Triggering conditions and parameters.|
|---|---|
|`on_text_changed`|The text actually changes, with the parameter being `event_args_t`.|

## Independent routine

The routine displays the connection page title, connection results with foreground and background colors, and next-step prompts. The three `label` elements are responsible for the first-level title, status, and supplementary explanations, respectively.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Open an x64 CMD with MSVC configured in the root directory of the tutorial repository, using the actual installed SDK path.

### C++

```bat
cmake -S examples/guide/controls/window-and-text/label/cpp -B .work/example_label -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_label --config Release
.work\example_label\Release\tutorial_label.exe
```

The above executable file path corresponds to the Visual Studio generator. When using single-configuration Ninja, the executable file is directly located in the build directory.

<<< ../../../../../examples/guide/controls/window-and-text/label/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\label\python\run.cmd
```

<<< ../../../../../examples/guide/controls/window-and-text/label/python/label_demo.py

### Run the effect

The running effect of the independent routine for ![label is](/images/en/label_demo.png).

## Common issues and practices.

- Reserve width for text that may become longer or be localized. When zooming in on `font`, check the rectangle height and top and bottom margins simultaneously.
- Update `text` when the status changes in real time to avoid duplicate control creation. Background tasks use `begin_invoke()` to distribute updates to the UI thread.
- When users need to copy long text, use [textbox](./textbox) for `read_only`.
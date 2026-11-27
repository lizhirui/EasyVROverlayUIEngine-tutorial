# screen

`screen` is used to draw the display output captured on the engine side onto the spatial interface. The application selects `screen_id` and subscribes to the source status; the rendering backend is responsible for capturing and submitting textures. Common uses include side-by-side viewing of desktop output within the headset, monitoring application status, and observing temporary reference images. For inherited members, see the [common control interface and](/en/guide/controls/common-api#control).

## Default appearance

`screen_id` defaults to 0, with `screen_available` initially set to false. The following image shows the default appearance with an invalid capture number, illustrating the background and border when there is no image for the first time.

![screen default appearance](/images/en/screen_default.png)

## Property comparison

Compare different sizes of capture areas and their available/ unavailable status. The left side shows a restored event sent by the test host, while the right side remains unavailable. Both sides feature controls and placeholder text actually rendered by WARP.

![screen property comparison](/images/en/screen_comparison.png)

## Interface reference

C++ reads and writes attributes using the methods in the table. In Python, access is done through attributes with the same name. Callbacks receive `source` and `event`. Each strong-type parameter in the table inherits from `event_args_t`; basic parameters do not have additional fields. Python type names are omitted in `_t`.

### Property

|Property|C++ access methods|Types, default values, and uses|
|---|---|---|
|`screen_id`|`get_screen_id`、`set_screen_id`|`uint64_t`, with a default value of 0, selects the display output number recognized by the engine.|
|`screen_available`|`get_screen_available`|Read-only, initially false, follows the current window and display output status message.|
|`rect`、`background_color`|`get_rect`、`set_rect`、`get_background_color`、`set_background_color`|Inherited target rectangle and background color. The control background is still drawn when the screen is unavailable.|

### Method

|Method|Purpose|
|---|---|
|`screen(name)`|Construct the control and add it to `window` or a container.|
|`set_screen_id(value)`|C++ switches the capture number. Python assigns a value to `screen_id`.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_screen_id_changed`|`event_args_t`|The number actually changes.|
|`on_screen_unavailable`|`event_args_t`|: From Available to Unavailable. Switching IDs will also reset the current available status.|
|`on_screen_restored`|`event_args_t`|Changes from unavailable to available.|

## Headless and actual capture

WARP test host uses an invalid display number to maintain no desktop input in the capture background and sends the test status to the SDK. The status text is updated by the real-time event handler of the routine. The placeholder area in the screenshot does not contain actual desktop frames. When the actual engine is connected and a valid display number is selected, the capture image is rendered by the engine onto the `screen` rectangle.

## Independent routine

Run "Display Output Monitoring," with the control defaulting to 0. The status area updates based on the recovery or interruption of the capture. The demo image shows that after a recovery event occurs, the status text is updated, and the no-headshot environment retains the drawn area.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Execute the command in the x64 Developer CMD of the tutorial root directory, and replace the SDK installation path in the example.

### C++

```bat
cmake -S examples/guide/controls/command-and-display/screen/cpp -B .work/example_screen -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_screen --config Release
.work\example_screen\Release\tutorial_screen.exe
```

When using a single-configured Ninja, run the executable directly from the build directory.

<<< ../../../../../examples/guide/controls/command-and-display/screen/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\screen\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/screen/python/screen_demo.py

### Run the effect

![screen independent routine operation effect](/images/en/screen_demo.png)

## Common problems and layout practices

- What users see is the image of the capture source on the engine side. When a remote engine is selected, it is based on the display output number of that host.
- Use `screen_available` and two status events to maintain notifications. Initially, provide a waiting state when unavailable.
- During layout, design `rect` according to the proportion of the display output; the notification text can be placed below the capture area.
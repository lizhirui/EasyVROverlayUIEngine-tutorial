# progressbar

`progressbar` presents the known completion amount in a filling ratio, such as the number of processed files or synchronized entries. The values and task names can be displayed via the adjacent `label`.

Inherits the common control interface of [from](/en/guide/controls/common-api#control).

## Default appearance

The default range is 0 to 100, with the current value being 0. The filling percentage starting from the left side is zero, still showing the track and border.

The default appearance of ![progressbar is](/images/en/progressbar_default.png).

## Property comparison

Four lines sequentially display the default value, 42% completion, a range of 20 to 80 with the current value at 65 (75% filled), as well as the disabled color and custom background. The filling color is determined by the SDK style, and `background_color` changes the track. The current SDK only provides a definite progress; when the total amount is unknown, `label` can be used to show the current stage. After the total amount is determined, `progressbar` will be displayed.

Comparison of ![progressbar properties with](/images/en/progressbar_comparison.png).

## Interface reference

C++ properties can be read and written through the access methods in the table; Python accesses them through the same-named properties. The event parameters in the table use C++ type names, with the corresponding Python types omitting the `_t` suffix. Common members are found in the basic interface of [,](/en/guide/controls/common-api).

### Property

|Property|C++|Purpose and default values|
|---|---|---|
|`minimum`|`get_minimum`、`set_minimum`|There is a signed 64-bit integer lower limit, defaulting to 0, which must be less than the current upper limit.|
|`maximum`|`get_maximum`、`set_maximum`|There is a signed 64-bit integer upper limit, defaulting to 100, which must be greater than the current lower limit.|
|`value`|`get_value`、`set_value`|Current value, defaulting to 0. If it exceeds the range, it will be clipped to the nearest endpoint, and the current value will also be adjusted when the range is narrowed.|
|`background_color`、`enabled`|`get_background_color`、`set_background_color`、`get_enabled`、`set_enabled`|Inherits properties. The background color is used for the track, and the filling color changes when the disabled state is changed.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`progressbar(name)`|`progressbar(name)`|Creates a definite progress indicator.|

### Event

|Event|Triggering conditions and parameters.|
|---|---|
|`on_minimum_changed`、`on_maximum_changed`|Changes the lower or upper limit, with the parameter being `event_args_t`.|
|`on_value_changed`|The actual change in the current value, including boundary adjustments that cause clipping, with the parameter being `event_args_t`.|

## Independent routine

The total amount is 8 items, with 2 initially completed. Each click on "Complete the Next Item" updates the filling and completion numbers. The diagram shows the state of completing 5 items; once 8 items are reached, the operation entrance is disabled.

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). Open an x64 CMD with MSVC configured in the root directory of the tutorial repository, using the actual installed SDK path.

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/progressbar/cpp -B .work/example_progressbar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_progressbar --config Release
.work\example_progressbar\Release\tutorial_progressbar.exe
```

The above executable file path corresponds to the Visual Studio generator. When using single-configuration Ninja, the executable file is directly located in the build directory.

<<< ../../../../../examples/guide/controls/selection-and-status/progressbar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\progressbar\python\run.cmd
```

<<< ../../../../../examples/guide/controls/selection-and-status/progressbar/python/progressbar_demo.py

### Run the effect

Independent execution of ![progressbar results in](/images/en/progressbar_demo.png).

## Common issues and practices.

- When changing the entire range, choose the appropriate setting order. For example, switching from `[0, 100]` to `[200, 500]`, first set `maximum = 500`, then set `minimum = 200`.
- The displayed ratio is `(value - minimum) / (maximum - minimum)`. The original unit and status text are displayed together with the filling.
- Updates the progress on the UI thread. Frequent progress changes can be merged and then refreshed via `begin_invoke()`.
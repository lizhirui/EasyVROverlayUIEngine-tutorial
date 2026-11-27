# splitter

`splitter` arranges two direct child controls with a draggable separator bar, suitable for navigation and details, editing areas and previews, as well as upper and lower output areas. The direction indicates the separator bar itself. `vertical` divides the content into left and right sections, while `horizontal` divides it into upper and lower sections.

The inherited general members are found in the [container interface](/en/guide/controls/common-api#container-control).

## Default appearance

Default values for `orientation = vertical` and `split_position = 0.5`. Screenshots include two `panel`s of different colors to distinguish the areas. The separator bar and proportions remain default.

Default appearance of ![splitter for](/images/en/splitter_default.png).

## Property comparison

The left side is `vertical`, with the two sections evenly divided into usable width. The right side is `horizontal`, where the first `panel` occupies 38% of the usable height after deducting the separator bar. The direction and proportions can be configured independently.

Comparison of ![splitter properties with](/images/en/splitter_comparison.png).

## Interface reference

Property names in the Python usage table. C++ is read and written through corresponding methods, and uses `control_base &source` and type references in the table to subscribe to events. `event_args_t` without additional fields indicates that the state has been updated, and the callback reads the new value through `source`. The Python event type names are omitted for `_t`.

### Property

|Property|C++|Types, default values, and uses|
|---|---|---|
|`orientation`|`get_orientation`、`set_orientation`|Default value for `vertical`. C++ uses `orientation_t`, while Python uses `orientation`.|
|`split_position`|`get_split_position`、`set_split_position`|Default value is 0.5. The valid range is for `[0.0, 1.0]`, which must be finite. The calculation subtracts the total axial length from the separator bar.|
|`control_list`|`get_control_list`|A maximum of two direct child controls. The order of the controls corresponds to the first and second sections.|
|`active_item_list`|`get_active_item_list`|List of inherited read-only active child controls.|

### Method

|Python|C++|Purpose|
|---|---|---|
|`splitter(name)`|`splitter(name)`|Construct a two-section container.|
|`control_list.add(item)`|`get_control_list().add(item)`|Add controls in the order of the sections.|
|`control_list.remove(item)`|`get_control_list().remove(item)`|Remove a control from one section.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_orientation_changed`、`on_split_position_changed`|`event_args_t`|Actual changes in direction or proportion. Proportion events can be triggered multiple times with one drag.|
|`on_split_start`|`event_args_t`|Start interactive dragging of the separator bar.|
|`on_split_end`|`interaction_end_event_args_t`|End dragging. The current implementation sends default event values, with `cancelled` being false.|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|Addition or removal of section controls.|

## Independent routine

The two-section workspace starts from 42% of the first section's width. After dragging the separator bar to the right, the left and right `panel`s are rearranged, and the bottom status changes to "Layout proportion updated".

First start Engine as described in [Prerequisites, build, and installation](/en/basics/01_install_and_setup). The following command is executed in the x64 developer CMD at the root directory of the tutorial repository. Change the example SDK path to the actual installation location.

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/splitter/cpp -B .work/example_splitter -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_splitter --config Release
.work\example_splitter\Release\tutorial_splitter.exe
```

The Visual Studio generator places the executable file in the `Release` subdirectory. The single-config Ninja generator directly outputs to the build directory.

<<< ../../../../../examples/guide/controls/layout-and-container/splitter/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\splitter\python\run.cmd
```

<<< ../../../../../examples/guide/controls/layout-and-container/splitter/python/splitter_demo.py

### Run the effect

Independent routine effect of ![splitter for](/images/en/splitter_demo.png).

## Common problems and layout practices

- Use `panel` to wrap multiple controls in each section. `splitter` manages the rectangles of two direct child controls, while the internal layout continues to use their respective local coordinates.
- The separator bar defaults to 8 logical pixels, with the proportion based on the length after deducting the separator bar. When placed near 0 or 1, a section may shrink to the point where text cannot be displayed.
- Continuous feedback uses `on_split_position_changed`. After dragging is completed, the user's layout can be saved using `on_split_end`.
- When allowing direction switching, check the minimum readable sizes in both left-right and top-bottom layouts.
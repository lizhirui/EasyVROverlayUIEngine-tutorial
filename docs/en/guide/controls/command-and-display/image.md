# image

`image` displays `drawing_image` in a rectangle, suitable for application icons, album previews, and status graphics. The SDK calculates the scaling and cropping between the source image and the target rectangle based on `stretch_mode`. See [for inherited members of the public control interface](/en/guide/controls/common-api#control).

## Default appearance

The default source is empty, `stretch_mode = contain`. The screenshot only shows the background and boundaries of the target rectangle.

The default appearance of ![image is](/images/en/image_default.png).

## Property comparison

Four identical target rectangles use `contain`, `cover`, `fill`, and `none`, respectively. The original image has a 2:1 ratio. You can observe the margins, cropping, stretching, and original dimensions.

Comparison of ![image properties with](/images/en/image_comparison.png).

## Interface reference

C++ reads and writes attributes using the methods in the table. In Python, access is done through attributes with the same name. Callbacks receive `source` and `event`. Each strong-type parameter in the table inherits from `event_args_t`; basic parameters do not have additional fields. Python type names are omitted in `_t`.

### Property

|Property|C++ access methods|Types, default values, and uses|
|---|---|---|
|`source`|`get_source`、`set_source`|`drawing_image` resources can be empty; the default is empty. C++ uses `shared_ptr<const drawing_image>`.|
|`stretch_mode`|`get_stretch_mode`、`set_stretch_mode`|`image_stretch_mode_t`, with the default being `contain`. The Python enumeration name is `image_stretch_mode`.|

### Method

|Method|Purpose|
|---|---|
|`image(name)`|Construct the control.|
|`drawing_image(width,height,rgba)`|Construct resources as RGBA bytes with a specified size, with a buffer length of width×height×4.|
|`drawing_image.load_file(path)`|Supportable image formats can be loaded when file resources are needed.|

### Event

|Event|Parameter types|Trigger conditions|
|---|---|---|
|`on_source_changed`、`on_stretch_mode_changed`|`event_args_t`|Notification is received when the source resource or scaling mode changes.|
|`on_source_unavailable`|`event_args_t`|Notification is received when the source resource is unavailable.|

## Scaling rules

|Mode|Display rules|
|---|---|
|`contain`|Proportional scaling, fully displaying the original image, with the remaining area showing the background.|
|`cover`|Fill the target rectangle proportionally, cropping the excess part.|
|`fill`|Match the target width and height separately, allowing for changes in aspect ratio.|
|`none`|Draw from the top-left corner of the target according to the original logical size, cropping when exceeding the display range.|

## Independent routine

“Material preview” generates a two-color pattern; click “Switch Proportional Fill” to switch between `contain` and `cover`. `cover` is shown in the image.

Prepare, build, and install the](/en/basics/01_install_and_setup) Engine according to the [environment. Execute the command in the x64 Developer CMD of the tutorial root directory, and replace the SDK installation path in the example.

### C++

```bat
cmake -S examples/guide/controls/command-and-display/image/cpp -B .work/example_image -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_image --config Release
.work\example_image\Release\tutorial_image.exe
```

When using a single-configured Ninja, run the executable directly from the build directory.

<<< ../../../../../examples/guide/controls/command-and-display/image/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\image\python\run.cmd
```

<<< ../../../../../examples/guide/controls/command-and-display/image/python/image_demo.py

### Run the effect

Independent execution of ![image results with](/images/en/image_demo.png).

## Common problems and layout practices

- Use `contain` to retain all content; use `cover` when the thumbnail card needs to fill the target area.
- Arrange the RGBA bytes by line, confirming the size and channel order. Pure graphics can reuse the same shared resource.
- Reserve a rectangle for text and action items outside the image. Changing the image mode only affects the image itself.
# image

`image`在矩形中显示`drawing_image`，适合应用图标、相册预览和状态图形。SDK根据`stretch_mode`计算源图与目标矩形之间的缩放和裁剪。 继承成员见[公共控件接口](/guide/controls/common-api#control)。

## 默认外观

默认源为空，`stretch_mode = contain`。截图只显示目标矩形的背景与边界。

![image默认外观](/images/zh/image_default.png)

## 属性对比

四个相同目标矩形分别使用`contain`、`cover`、`fill`和`none`。原图为2:1。可以观察留边、裁剪、拉伸和原始尺寸。

![image属性对比](/images/zh/image_comparison.png)

## 接口参考

C++用表中的方法读写属性，Python按同名属性访问。回调接收`source`与`event`。表中各强类型参数继承`event_args_t`，基础参数本身没有附加字段。Python类型名省略`_t`。

### 属性

|属性|C++访问方法|类型、默认值与用途|
|---|---|---|
|`source`|`get_source`、`set_source`|可空`drawing_image`资源，默认空。C++使用`shared_ptr<const drawing_image>`。|
|`stretch_mode`|`get_stretch_mode`、`set_stretch_mode`|`image_stretch_mode_t`，默认`contain`。Python枚举名为`image_stretch_mode`。|

### 方法

|方法|用途|
|---|---|
|`image(name)`|构造控件。|
|`drawing_image(width,height,rgba)`|以指定尺寸的RGBA字节构造资源，缓冲长度为宽×高×4。|
|`drawing_image.load_file(path)`|需要文件资源时可加载支持的图像格式。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_source_changed`、`on_stretch_mode_changed`|`event_args_t`|源资源或缩放模式变化。|
|`on_source_unavailable`|`event_args_t`|源资源不可用时接收通知。|

## 伸缩规则

|模式|显示规则|
|---|---|
|`contain`|等比缩放，完整显示原图，剩余区域显示背景。|
|`cover`|等比填满目标矩形，超出部分裁剪。|
|`fill`|分别匹配目标宽高，允许改变纵横比例。|
|`none`|从目标左上角按原图逻辑尺寸绘制，超出显示范围时裁剪。|

## 独立例程

“素材预览”生成双色图案，单击“切换等比填充”在`contain`和`cover`之间切换。图中展示`cover`。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程根目录的x64开发者CMD中执行命令，并替换示例中的SDK安装路径。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/image/cpp -B .work/example_image -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_image --config Release
.work\example_image\Release\tutorial_image.exe
```

使用单配置Ninja时，从构建目录直接运行可执行文件。

<<< ../../../../examples/guide/controls/command-and-display/image/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\image\python\run.cmd
```

<<< ../../../../examples/guide/controls/command-and-display/image/python/image_demo.py

### 运行效果

![image独立例程运行效果](/images/zh/image_demo.png)

## 常见问题与布局实践

- 要保留所有内容时用`contain`，缩略图卡片要填满目标区域时用`cover`。
- 准备RGBA字节时按行排列，确认尺寸和通道顺序。纯图形可复用同一共享资源。
- 为图片外的文字和操作项预留矩形。改变图像模式只影响图像自身。

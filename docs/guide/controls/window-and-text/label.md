# label

`label`用于显示页面说明、状态和字段标题。默认采用透明背景，文字左对齐，不进入Tab焦点顺序。状态颜色宜搭配明确文字，确保用户能区分连接中、成功和失败。

继承[公共控件接口](/guide/controls/common-api#control)和[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

默认`text`为空。下图仅设置示例文字与矩形，保留SDK字体、颜色和透明背景。

![label默认外观](/images/zh/label_default.png)

## 属性对比

从上至下保留同一文字，依次展示默认外观、大号粗体、绿色文字与实色背景、禁用后的文字颜色。`label`没有独立的对齐属性，需要改变摆放时调整`rect`。需要精确对齐时使用自定义绘图。

![label属性对比](/images/zh/label_comparison.png)

## 接口参考

C++属性通过表中的访问方法读写，Python通过同名属性访问。表中的事件参数采用C++类型名，Python对应类型省略`_t`后缀。公共成员见[基础接口](/guide/controls/common-api)。

### 属性

|属性|C++|用途与默认值|
|---|---|---|
|`text`|`get_text`、`set_text`|读写显示文字，默认空字符串。|
|`font`、`foreground_color`、`background_color`|`get_font`、`set_font`、`get_foreground_color`、`set_foreground_color`、`get_background_color`、`set_background_color`|继承样式属性。默认字号18，背景为透明。|

### 方法

|Python|C++|用途|
|---|---|---|
|`label(name)`|`label(name)`|创建一个`label`。|

### 事件

|事件|触发条件与参数|
|---|---|
|`on_text_changed`|文字实际改变，参数为`event_args_t`。|

## 独立例程

例程显示连接页标题、带前景色和背景色的连接结果，以及下一步提示。三个`label`分别负责一级标题、状态和补充说明。

先按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程仓库根目录打开已配置MSVC的x64 CMD，使用实际安装的SDK路径。

### C++

```bat
cmake -S examples/guide/controls/window-and-text/label/cpp -B .work/example_label -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_label --config Release
.work\example_label\Release\tutorial_label.exe
```

上面的可执行文件路径对应Visual Studio生成器。使用单配置Ninja时，可执行文件直接位于构建目录。

<<< ../../../../examples/guide/controls/window-and-text/label/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\window-and-text\label\python\run.cmd
```

<<< ../../../../examples/guide/controls/window-and-text/label/python/label_demo.py

### 运行效果

![label独立例程运行效果](/images/zh/label_demo.png)

## 常见问题与实践

- 给可能变长或本地化的文字预留宽度。放大`font`后同时检查矩形高度与上下内边距。
- 状态实时变化时更新`text`，避免重复创建控件。后台任务使用`begin_invoke()`把更新派发到UI线程。
- 用户需要选择复制长文本时，使用`read_only`的[textbox](./textbox)。

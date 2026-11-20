# slider

`slider`在有限整数区间内提供连续拖动的操作体验，适合音量百分比、亮度级别、速度档位等即时设置。SDK把指针位置换算为区间比例，再舍入为整数。横向从左到右递增，纵向从下到上递增。键盘焦点在`slider`内时，方向键→和↑增加1，←和↓减少1。

继承的通用成员见[公共控件接口](/guide/controls/common-api#control)。

## 默认外观

默认范围为`[0, 100]`，初始值为0，方向为`horizontal`。指针滑块显示在左端，轨道沿控件横轴排列。

![slider默认外观](/images/zh/slider_default.png)

## 属性对比

左上为`horizontal`且值为65。右侧以同一数值显示`vertical`，上端代表最大值。左下将范围设为`[-20, 20]`，值10对应75%的位置，禁用时轨道和滑块使用弱化配色。

![slider属性对比](/images/zh/slider_comparison.png)

## 接口参考

Python使用表中的属性名。C++通过对应方法读写，并使用`control_base &source`和表中类型的引用订阅事件。无附加字段的`event_args_t`表示状态已更新，回调通过`source`读取新值。Python对应事件类型名省略`_t`。

### 属性

|属性|C++|类型、默认值与用途|
|---|---|---|
|`minimum`|`get_minimum`、`set_minimum`|`int64_t`，默认0。新下限须小于当前上限。|
|`maximum`|`get_maximum`、`set_maximum`|`int64_t`，默认100。新上限须大于当前下限。|
|`value`|`get_value`、`set_value`|`int64_t`，默认0。设值超出范围时夹取到端点，边界调整也会修正当前值。|
|`orientation`|`get_orientation`、`set_orientation`|默认`orientation_t::horizontal`。Python使用`orientation.horizontal`或`orientation.vertical`。|
|`focusable`|`is_focusable`|继承的只读能力，返回真。|

### 方法

|Python|C++|用途|
|---|---|---|
|`slider(name)`|`slider(name)`|构造控件。用继承的`focus()`请求焦点。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_minimum_changed`、`on_maximum_changed`|`event_args_t`|范围端点实际改变。|
|`on_value_changed`|`event_args_t`|整数值实际改变，包括指针、方向键、程序赋值或边界夹取。|
|`on_orientation_changed`|`event_args_t`|轨道方向改变。|
|`on_drag_start`|`event_args_t`|按下指针并开始拖动。|
|`on_drag_end`|`interaction_end_event_args_t`|拖动结束。可通过`cancelled`识别被取消的拖动。|

## 独立例程

监听音量从35开始。拖动`slider`时，`on_value_changed`同步更新`progressbar`和说明文字。截图展示将滑块拖到高音量区域后的状态。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。以下命令在教程仓库根目录的x64开发者CMD中执行。把示例SDK路径改为实际安装位置。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/slider/cpp -B .work/example_slider -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_slider --config Release
.work\example_slider\Release\tutorial_slider.exe
```

Visual Studio生成器把可执行文件放在`Release`子目录。单配置Ninja生成器直接输出到构建目录。

<<< ../../../../examples/guide/controls/selection-and-status/slider/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\slider\python\run.cmd
```

<<< ../../../../examples/guide/controls/selection-and-status/slider/python/slider_demo.py

### 运行效果

![slider独立例程效果](/images/zh/slider_demo.png)

## 常见问题与布局实践

- 纵向布局应把高度留给轨道，宽度留给滑块和激光命中区域。只切换`orientation`时，原有`rect`尺寸保持原样。
- 用`on_value_changed`更新即时反馈，以`on_drag_end`作为指针拖动完成的信号。需要覆盖键盘调节时，在数值变化路径中统一处理业务状态。
- 需要精确小数输入可使用[numericupdown](./numericupdown)。联动[progressbar](./progressbar)时先对齐两者的取值范围。

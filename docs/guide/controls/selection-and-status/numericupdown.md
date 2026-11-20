# numericupdown

`numericupdown`接受有限小数值，适合增益、倍率、时间间隔和其他需要精确输入或固定增量的参数。内部编辑区接收数字。按Enter或移出编辑焦点时提交输入。右侧上下区域按`step`调节数值，操作前会先提交正在编辑的内容。

继承的通用成员见[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

默认`value = 0.0`、`minimum = 0.0`、`maximum = 100.0`、`step = 1.0`、`decimal_places = 0`。显示区以整数形式绘制0，右侧绘制上下两个操作区。

![numericupdown默认外观](/images/zh/numericupdown_default.png)

## 属性对比

第一行显示默认值0。第二行加入负数范围，显示下限−2.00。第三行从1.00增加一个0.25步长后显示1.25，第四行保留相同数值并禁用控件。`decimal_places`决定显示的小数位数。

![numericupdown属性对比](/images/zh/numericupdown_comparison.png)

## 接口参考

Python使用表中的属性名。C++通过对应方法读写，并使用`control_base &source`和表中类型的引用订阅事件。无附加字段的`event_args_t`表示状态已更新，回调通过`source`读取新值。Python对应事件类型名省略`_t`。

### 属性

|属性|C++|类型、默认值与用途|
|---|---|---|
|`value`|`get_value`、`set_value`|`double`，默认0.0。须为有限数，越界值夹取到当前范围。|
|`minimum`|`get_minimum`、`set_minimum`|`double`，默认0.0。有限且小于当前上限。|
|`maximum`|`get_maximum`、`set_maximum`|`double`，默认100.0。有限且大于当前下限。|
|`step`|`get_step`、`set_step`|`double`，默认1.0。正有限数，用于上下调节。|
|`decimal_places`|`get_decimal_places`、`set_decimal_places`|`uint32_t`，默认0，支持0至17。控制固定小数位显示，启用小数位后接受英文小数点。|
|`focusable`|`is_focusable`|只读。编辑区、增加区、减少区是同一控件的不同焦点位置。|

### 方法

|Python|C++|用途|
|---|---|---|
|`numericupdown(name)`|`numericupdown(name)`|构造控件。用`value`或`set_value()`设置初始数值。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_value_changed`|`event_args_t`|已提交值实际改变。编辑缓冲的每次键入未必产生数值变化。|
|`on_minimum_changed`、`on_maximum_changed`|`event_args_t`|范围端点实际改变。变更范围可能紧接着触发值变化。|
|`on_step_changed`、`on_decimal_places_changed`|`event_args_t`|步长或小数位实际改变。|

## 独立例程

本例把增益限制在0.00至2.00，初值0.75。单击上方调节区后显示1.00，状态文字随之更新。激活编辑区也可以直接输入数值并按Enter提交。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。以下命令在教程仓库根目录的x64开发者CMD中执行。把示例SDK路径改为实际安装位置。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/numericupdown/cpp -B .work/example_numericupdown -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_numericupdown --config Release
.work\example_numericupdown\Release\tutorial_numericupdown.exe
```

Visual Studio生成器把可执行文件放在`Release`子目录。单配置Ninja生成器直接输出到构建目录。

<<< ../../../../examples/guide/controls/selection-and-status/numericupdown/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\numericupdown\python\run.cmd
```

<<< ../../../../examples/guide/controls/selection-and-status/numericupdown/python/numericupdown_demo.py

### 运行效果

![numericupdown独立例程效果](/images/zh/numericupdown_demo.png)

## 常见问题与布局实践

- 为负号、小数点、所需数字位数和右侧调节区预留宽度。提高`font`大小时同时增加`rect.height`。
- `decimal_places`控制格式和字符过滤，业务精度应单独约定。直接设置`value`也允许输入不在`step`序列上的有限值。
- 调整范围时先设置能够保持`minimum < maximum`的一侧。应用保存数据时读取`value`，无效输入会恢复当前值的格式化显示。
- 在编辑区焦点内可用Up或Down调节，焦点位于增加或减少区时可用Enter或Space。

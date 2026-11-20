# progressbar

`progressbar`以填充比例呈现已知范围内的完成量，例如文件处理数或同步条目数。数值和任务名称可通过旁边的`label`显示。

继承[公共控件接口](/guide/controls/common-api#control)。

## 默认外观

默认范围为0到100，当前值为0。左端起始的填充占比为零，仍显示轨道与边框。

![progressbar默认外观](/images/zh/progressbar_default.png)

## 属性对比

四行依次展示默认值、42%完成、范围20至80且当前值65（填充75%），以及禁用颜色和自定义背景。填充颜色由SDK样式决定，`background_color`改变轨道。当前SDK只提供确定进度，未知总量时可用`label`展示当前阶段，在总量确定后显示`progressbar`。

![progressbar属性对比](/images/zh/progressbar_comparison.png)

## 接口参考

C++属性通过表中的访问方法读写，Python通过同名属性访问。表中的事件参数采用C++类型名，Python对应类型省略`_t`后缀。公共成员见[基础接口](/guide/controls/common-api)。

### 属性

|属性|C++|用途与默认值|
|---|---|---|
|`minimum`|`get_minimum`、`set_minimum`|有符号64位整数下限，默认0，须小于当前上限。|
|`maximum`|`get_maximum`、`set_maximum`|有符号64位整数上限，默认100，须大于当前下限。|
|`value`|`get_value`、`set_value`|当前值，默认0。超出范围会夹到最近的端点，收窄范围时也会调整当前值。|
|`background_color`、`enabled`|`get_background_color`、`set_background_color`、`get_enabled`、`set_enabled`|继承属性。背景色用于轨道，禁用状态改变填充色。|

### 方法

|Python|C++|用途|
|---|---|---|
|`progressbar(name)`|`progressbar(name)`|创建确定进度指示。|

### 事件

|事件|触发条件与参数|
|---|---|
|`on_minimum_changed`、`on_maximum_changed`|下限或上限变化，参数为`event_args_t`。|
|`on_value_changed`|当前值实际变化，包含边界调整导致的夹取，参数为`event_args_t`。|

## 独立例程

总量为8项，初始完成2项。每次单击“完成下一项”更新填充与完成数。效果图展示完成5项的状态，达到8项后操作入口禁用。

先按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程仓库根目录打开已配置MSVC的x64 CMD，使用实际安装的SDK路径。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/progressbar/cpp -B .work/example_progressbar -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_progressbar --config Release
.work\example_progressbar\Release\tutorial_progressbar.exe
```

上面的可执行文件路径对应Visual Studio生成器。使用单配置Ninja时，可执行文件直接位于构建目录。

<<< ../../../../examples/guide/controls/selection-and-status/progressbar/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\progressbar\python\run.cmd
```

<<< ../../../../examples/guide/controls/selection-and-status/progressbar/python/progressbar_demo.py

### 运行效果

![progressbar独立例程运行效果](/images/zh/progressbar_demo.png)

## 常见问题与实践

- 变更整个范围时选择合适的设置顺序。例如从`[0, 100]`切换到`[200, 500]`，先设置`maximum = 500`，再设置`minimum = 200`。
- 显示的比例是`(value - minimum) / (maximum - minimum)`。将原始计量单位和状态文字与填充一起展示。
- 在UI线程更新进度，大量高频进度变化可合并后再通过`begin_invoke()`刷新。

# splitter

`splitter`按一个可拖动的分隔条布局两个直接子控件，适合导航与详情、编辑区与预览、上下两个输出区。方向表示分隔条本身，`vertical`把内容分成左右两区，`horizontal`分成上下两区。

继承的通用成员见[容器接口](/guide/controls/common-api#container-control)。

## 默认外观

默认`orientation = vertical`、`split_position = 0.5`。截图加入两块颜色不同的`panel`以区分区域，分隔条与比例保持默认。

![splitter默认外观](/images/zh/splitter_default.png)

## 属性对比

左侧为`vertical`，两区平分可用宽度。右侧为`horizontal`，第一块`panel`占扣除分隔条后可用高度的38%。方向和比例可独立配置。

![splitter属性对比](/images/zh/splitter_comparison.png)

## 接口参考

Python使用表中的属性名。C++通过对应方法读写，并使用`control_base &source`和表中类型的引用订阅事件。无附加字段的`event_args_t`表示状态已更新，回调通过`source`读取新值。Python对应事件类型名省略`_t`。

### 属性

|属性|C++|类型、默认值与用途|
|---|---|---|
|`orientation`|`get_orientation`、`set_orientation`|默认`vertical`。C++使用`orientation_t`，Python使用`orientation`。|
|`split_position`|`get_split_position`、`set_split_position`|默认0.5。有效范围为`[0.0, 1.0]`，必须有限。计算时从轴向总长度扣除分隔条。|
|`control_list`|`get_control_list`|最多两个直接子控件。集合顺序对应第一、第二分区。|
|`active_item_list`|`get_active_item_list`|继承的只读活动子控件列表。|

### 方法

|Python|C++|用途|
|---|---|---|
|`splitter(name)`|`splitter(name)`|构造双区容器。|
|`control_list.add(item)`|`get_control_list().add(item)`|按分区顺序加入控件。|
|`control_list.remove(item)`|`get_control_list().remove(item)`|移除一个分区中的控件。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_orientation_changed`、`on_split_position_changed`|`event_args_t`|方向或比例实际变化。比例事件可在一次拖动中多次触发。|
|`on_split_start`|`event_args_t`|开始交互拖动分隔条。|
|`on_split_end`|`interaction_end_event_args_t`|结束拖动。当前实现发送默认事件值，`cancelled`为假。|
|`on_control_added`、`on_control_removed`|`control_collection_event_args_t`|分区控件增加或移除。|

## 独立例程

双区工作台从42%的第一分区宽度开始。向右拖动分隔条后，左右`panel`重新布局，底部状态变为“布局比例已更新”。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。以下命令在教程仓库根目录的x64开发者CMD中执行。把示例SDK路径改为实际安装位置。

### C++

```bat
cmake -S examples/guide/controls/layout-and-container/splitter/cpp -B .work/example_splitter -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_splitter --config Release
.work\example_splitter\Release\tutorial_splitter.exe
```

Visual Studio生成器把可执行文件放在`Release`子目录。单配置Ninja生成器直接输出到构建目录。

<<< ../../../../examples/guide/controls/layout-and-container/splitter/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\layout-and-container\splitter\python\run.cmd
```

<<< ../../../../examples/guide/controls/layout-and-container/splitter/python/splitter_demo.py

### 运行效果

![splitter独立例程效果](/images/zh/splitter_demo.png)

## 常见问题与布局实践

- 用`panel`包装每个分区的多个控件。`splitter`管理两块直接子控件的矩形，内部布局继续使用各自的局部坐标。
- 分隔条默认占8逻辑像素，比例基于扣除分隔条后的长度。放到0或1附近时，一个分区可能收缩到无法显示文字。
- 连续反馈使用`on_split_position_changed`，拖动完成后保存用户布局可用`on_split_end`。
- 允许切换方向时，检查左右和上下两种布局下的最小可读尺寸。

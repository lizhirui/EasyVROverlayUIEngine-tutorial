# blank

`blank`是可存储名称、矩形和集合位置的占位控件。设计器可以用它预留未来要插入的自定义控件位置。应用加载内容时读取它的局部`rect`，再以真实控件替换该集合项。 继承成员见[公共控件接口](/guide/controls/common-api#control)。

## 默认外观

`blank`自身透明且不绘制。图中可见的边框来自父级`panel`，用于说明占位矩形所在的内容区。

![blank默认外观](/images/zh/blank_default.png)

## 属性对比

左侧`panel`包含`blank`，右侧在相同局部位置使用`label`。实际文字和交互能力来自替换后的控件。

![blank属性对比](/images/zh/blank_comparison.png)

## 接口参考

C++用表中的方法读写属性，Python按同名属性访问。回调接收`source`与`event`。表中各强类型参数继承`event_args_t`，基础参数本身没有附加字段。Python类型名省略`_t`。

### 属性

|属性|C++访问方法|类型、默认值与用途|
|---|---|---|
|`name`、`type`、`id`、`parent`、`disposed`|`get_name`、`get_type`、`get_id`、`get_parent`、`get_disposed`|读写规则与`control_base`一致，`type`为`blank`。|
|`rect`、`tag`|`get_rect`、`set_rect`、`get_tag`、`set_tag`|继承的局部矩形和应用标记。|
|`absolute_rectangle`、`owning_window`|`get_absolute_rectangle`、`get_owning_window`|继承的表面矩形与所属窗口查询。|
|`focused`|`get_focused`|只读，`blank`无法获得焦点。|

### 方法

|方法|用途|
|---|---|
|`blank(name)`|创建占位项，通过容器的`control_list`增删或替换。|
|`dispose()`、`invalidate()`、`begin_invoke(callback)`|继承的生命周期和所属线程调度方法。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_moved`、`on_size_changed`、`on_viewport_changed`|`event_args_t`|继承的几何和视口通知。|
|`on_tag_changed`、`on_disposed`|`event_args_t`|继承的标记和释放事件。|
|`on_property_changed`|`property_changed_event_args_t`|可公开配置的属性变化，携带`property_name`。|

## 公开成员限制

`blank`保留布局与所有权功能。其可见、启用、焦点、输入、背景、悬停提示与Tab属性不属于此类型的公开接口。在Python访问被隐藏的成员会得到`AttributeError`。应用应把可见效果和交互事件交给替换后的控件。

## 独立例程

单击“加载内容”后，程序复制占位矩形、按原索引插入`label`并禁用加载操作。图中展示替换后的状态。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程根目录的x64开发者CMD中执行命令，并替换示例中的SDK安装路径。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/blank/cpp -B .work/example_blank -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_blank --config Release
.work\example_blank\Release\tutorial_blank.exe
```

使用单配置Ninja时，从构建目录直接运行可执行文件。

<<< ../../../../examples/guide/controls/command-and-display/blank/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\blank\python\run.cmd
```

<<< ../../../../examples/guide/controls/command-and-display/blank/python/blank_demo.py

### 运行效果

![blank独立例程运行效果](/images/zh/blank_demo.png)

## 常见问题与布局实践

- 先记录`rect`和集合位置，再移除原占位项。将替换工作放在所属UI线程。
- 保留稳定标识时，可使用设计文件中的名称来查找位置，但集合内名称必须唯一。
- 预留尺寸要考虑最终控件的字体、内边距和焦点样式。

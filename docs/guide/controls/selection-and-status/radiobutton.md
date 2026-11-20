# radiobutton

`radiobutton`适合从同一组选项中选择一个，例如通知策略。同一直接父容器内的`radiobutton`构成一组。为多个互不影响的组分别创建`panel`。

继承[公共控件接口](/guide/controls/common-api#control)和[文字样式接口](/guide/controls/common-api#text-control)。

## 默认外观

初始未选中、可聚焦，且使用空心圆显示。默认文字为空，截图只填写示例文字和矩形。

![radiobutton默认外观](/images/zh/radiobutton_default.png)

## 属性对比

第一、第二行展示空心圆和实心选中点。第三行展示禁用未选中的文字与圆标，第四行改变字体、前景色与背景色。

![radiobutton属性对比](/images/zh/radiobutton_comparison.png)

## 接口参考

C++属性通过表中的访问方法读写，Python通过同名属性访问。表中的事件参数采用C++类型名，Python对应类型省略`_t`后缀。公共成员见[基础接口](/guide/controls/common-api)。

### 属性

|属性|C++|用途与默认值|
|---|---|---|
|`text`|`get_text`、`set_text`|选项说明，默认空字符串。|
|`checked`|`get_checked`、`set_checked`|布尔选中状态，默认假。设为真时清除同一直接父容器内已选中的其他`radiobutton`。|
|`focusable`|`is_focusable`|可进入焦点顺序。|

### 方法

|Python|C++|用途|
|---|---|---|
|`radiobutton(name)`|`radiobutton(name)`|创建一个互斥选项。加入父容器后设置默认项。|

### 事件

|事件|触发条件与参数|
|---|---|
|`on_checked_changed`|选中或取消选中时触发，参数为`event_args_t`。组内切换可先收到旧项取消的事件。|
|`on_text_changed`|显示文字实际变化，参数为`event_args_t`。|
|`on_click`|继承的激活事件。跟踪组当前值宜使用`on_checked_changed`。|

## 独立例程

两个`radiobutton`属于同一个`panel`。初始为“仅接收重要通知”，选择“接收全部通知”后可观察旧项取消和状态文字更新。

先按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程仓库根目录打开已配置MSVC的x64 CMD，使用实际安装的SDK路径。

### C++

```bat
cmake -S examples/guide/controls/selection-and-status/radiobutton/cpp -B .work/example_radiobutton -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_radiobutton --config Release
.work\example_radiobutton\Release\tutorial_radiobutton.exe
```

上面的可执行文件路径对应Visual Studio生成器。使用单配置Ninja时，可执行文件直接位于构建目录。

<<< ../../../../examples/guide/controls/selection-and-status/radiobutton/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\selection-and-status\radiobutton\python\run.cmd
```

<<< ../../../../examples/guide/controls/selection-and-status/radiobutton/python/radiobutton_demo.py

### 运行效果

![radiobutton独立例程运行效果](/images/zh/radiobutton_demo.png)

## 常见问题与实践

- 先把选项全部添加到共同的父容器，再设置默认选中项，确保组规则能检查其他选项。
- 处理状态变化时检查来源的`checked`，选中事件适合提交业务枚举，取消事件适合清理旧项状态。
- 如果业务要求始终有选项，初始化时明确设置默认项，并避免将当前项程序化设为假。

# screen

`screen`将Engine侧指定显示输出的采集画面绘制到空间界面。应用选择`screen_id`并订阅来源状态，渲染后端负责采集与纹理提交。典型用途包括头显内并排查看桌面输出、监视应用状态和观察临时参考画面。 继承成员见[公共控件接口](/guide/controls/common-api#control)。

## 默认外观

`screen_id`默认0，`screen_available`初始为假。下图使用无效采集编号保留默认外观，展示首次无画面时的背景和边框。

![screen默认外观](/images/zh/screen_default.png)

## 属性对比

对比不同大小的采集区域及可用、不可用状态。左侧通过测试宿主发送恢复事件，右侧保持不可用。两侧均是WARP实际绘制的控件和占位文字。

![screen属性对比](/images/zh/screen_comparison.png)

## 接口参考

C++用表中的方法读写属性，Python按同名属性访问。回调接收`source`与`event`。表中各强类型参数继承`event_args_t`，基础参数本身没有附加字段。Python类型名省略`_t`。

### 属性

|属性|C++访问方法|类型、默认值与用途|
|---|---|---|
|`screen_id`|`get_screen_id`、`set_screen_id`|`uint64_t`，默认0，选择Engine识别的显示输出编号。|
|`screen_available`|`get_screen_available`|只读，初始假，跟随匹配当前窗口和显示输出的状态消息。|
|`rect`、`background_color`|`get_rect`、`set_rect`、`get_background_color`、`set_background_color`|继承的目标矩形和背景色。画面不可用时仍绘制控件背景。|

### 方法

|方法|用途|
|---|---|
|`screen(name)`|构造控件并加入`window`或容器。|
|`set_screen_id(value)`|C++切换采集编号。Python为给`screen_id`赋值。|

### 事件

|事件|参数类型|触发条件|
|---|---|---|
|`on_screen_id_changed`|`event_args_t`|编号实际变化。|
|`on_screen_unavailable`|`event_args_t`|从可用转为不可用。切换编号也会重置现有可用状态。|
|`on_screen_restored`|`event_args_t`|从不可用转为可用。|

## 无头截图与实际采集

WARP测试宿主使用无效显示编号保持采集后台无桌面输入，并向SDK投递测试状态。状态文字由例程的真实事件处理函数更新。截图中的占位区域不含实际桌面帧。连接实际Engine并选用有效显示编号时，采集画面由Engine渲染到`screen`矩形。

## 独立例程

运行“显示输出监视”，控件默认选择0。状态区根据采集恢复或中断更新。Demo图展示恢复事件到达后，状态文字更新且无头环境保留绘制区域。

按[环境准备、构建与安装](/basics/01_install_and_setup)启动Engine。在教程根目录的x64开发者CMD中执行命令，并替换示例中的SDK安装路径。

### C++

```bat
cmake -S examples/guide/controls/command-and-display/screen/cpp -B .work/example_screen -DEASYVRUI_ENGINE_INTERFACE_ROOT=D:/Tools/EasyVRUI/sdk
cmake --build .work/example_screen --config Release
.work\example_screen\Release\tutorial_screen.exe
```

使用单配置Ninja时，从构建目录直接运行可执行文件。

<<< ../../../../examples/guide/controls/command-and-display/screen/cpp/main.cpp

### Python

```bat
set "EASYVRUI_SDK_ROOT=D:\Tools\EasyVRUI\sdk"
examples\guide\controls\command-and-display\screen\python\run.cmd
```

<<< ../../../../examples/guide/controls/command-and-display/screen/python/screen_demo.py

### 运行效果

![screen独立例程运行效果](/images/zh/screen_demo.png)

## 常见问题与布局实践

- 用户看到的是采集源在Engine侧的画面。选择远程Engine时，以该主机的显示输出编号为准。
- 用`screen_available`和两个状态事件维护提示。初始不可用时先提供等待状态。
- 布局时根据显示输出的比例设计`rect`，可把提示文字放在采集区域下方。

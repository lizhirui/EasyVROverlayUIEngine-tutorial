# 中文配图生成

从工作区根目录在CMD运行以下命令。先准备带运行时资源的发行目录，并提供一个已有的Ninja原生构建缓存，用于定位MSVC、Ninja和CMake。截图工具在`repo_tutorial/.work/capture`中独立编译，WARP在离屏表面上渲染真实控件。

```bat
python -m pip install -r repo_tutorial\tools\requirements.txt
python repo_tutorial\tools\capture_ui_screenshots.py --locale zh --role controls --role demo --role dialog --role designer --role ime --distribution build\easyvrui_distribution\bin
python repo_tutorial\tools\capture_ui_screenshots.py --locale zh --role controls_second --distribution build\easyvrui_distribution\bin
python repo_tutorial\tools\capture_ui_screenshots.py --locale zh --role controls_third --distribution build\easyvrui_distribution\bin
python repo_tutorial\tools\capture_ui_screenshots.py --locale zh --role project_story --role designer --distribution build\easyvrui_distribution\bin
python repo_tutorial\tools\render_3d_mockups.py --locale zh
python repo_tutorial\tools\check_tutorial.py --inventory
```

`--toolchain-build`指定只读的原生构建缓存目录，默认`build\native`。`--native-build`可选择教程目录内的独立构建目录。复用同一目录已编译的截图程序时可加`--reuse-binaries`。省略`--role`时生成指定语言的全部离屏截图。

`controls`生成`window`、`label`、`button`、`textbox`、`checkbox`、`radiobutton`、`progressbar`的`*_default.png`、`*_comparison.png`与`*_demo.png`。例程效果图调用教程C++源码中的同一个构建函数，并通过测试宿主分发点击。图片发布到`docs/public/images/zh`。`render_3d_mockups.py`使用离屏截图及区域数据生成带`vr_`前缀的空间示意图。

`controls_second`按同一套文件名规则生成`slider`、`numericupdown`、`combobox`、`listbox`、`panel`、`scrollpanel`、`splitter`和`tabcontrol`的截图。测试宿主通过点击、拖动和设置视口偏移取得章节所用状态。

`controls_third`为`treeview`、`listview`、`grid`、`menubar`、`toolbar`、`image`、`screen`和`blank`生成截图，并补齐`inputbox`、`file_save_dialog`、参考对象配置与自定义绘图图片。无头测试通过模拟状态事件展示`screen`的状态回调，使用占位区呈现布局。

截图后打开原尺寸PNG检查文字边界、示例选中状态、图注与控件间距。运行`npm run docs:build`验证站点。

`project_story`使用原例程取得第一个`window`和导出窗体的交互状态，并用离屏夹具重现5个工程的输入、确认和状态变化。`designer`同时捕获实际的基础篇设计文件。工程图中的日志、图片、远程会话和采样状态采用可复现的本地数据。

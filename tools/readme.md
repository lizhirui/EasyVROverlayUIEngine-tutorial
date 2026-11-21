# 中文配图生成

从工作区根目录在CMD运行以下命令。先用`repo/build.bat`构建各组件的`build/`，再生成截图。截图工具通过仓库的CMD入口初始化MSVC x64、CMake和Ninja，在`repo_tutorial/.work/capture`中编译WARP测试宿主，并调用`repo/install.bat`把组件资源安装到临时目录。WARP在离屏表面上渲染真实控件。

```bat
python -m pip install -r repo_tutorial\tools\requirements.txt
call repo\build.bat --configuration Release --parallel 8
python repo_tutorial\tools\capture_ui_screenshots.py --locale zh --role controls --role demo --role dialog --role designer --role ime
python repo_tutorial\tools\capture_ui_screenshots.py --locale zh --role controls_second
python repo_tutorial\tools\capture_ui_screenshots.py --locale zh --role controls_third
python repo_tutorial\tools\capture_ui_screenshots.py --locale zh --role project_story --role designer
python repo_tutorial\tools\render_3d_mockups.py --locale zh
python repo_tutorial\tools\check_tutorial.py --inventory
```

`--repository`指定用于临时安装的源码仓库，默认是工作区中的`repo`。该仓库的各组件须已使用相同配置完成构建。`--native-build`可选择教程目录内的WARP测试宿主构建目录。复用已编译的截图程序时可加`--reuse-binaries`。省略`--role`时生成指定语言的全部离屏截图。

英文和日文配图脚本使用相同的CMD构建及临时安装入口。英文脚本用`--build-directory`选择教程目录内的WARP构建目录，默认`repo_tutorial/.work/capture_en`。两个脚本均可通过`--guide`生成对应语言的应用篇配图。

`controls`生成`window`、`label`、`button`、`textbox`、`checkbox`、`radiobutton`、`progressbar`的`*_default.png`、`*_comparison.png`与`*_demo.png`。例程效果图调用教程C++源码中的同一个构建函数，并通过测试宿主分发点击。图片发布到`docs/public/images/zh`。`render_3d_mockups.py`使用离屏截图及区域数据生成带`vr_`前缀的空间示意图。

`controls_second`按同一套文件名规则生成`slider`、`numericupdown`、`combobox`、`listbox`、`panel`、`scrollpanel`、`splitter`和`tabcontrol`的截图。测试宿主通过点击、拖动和设置视口偏移取得章节所用状态。

`controls_third`为`treeview`、`listview`、`grid`、`menubar`、`toolbar`、`image`、`screen`和`blank`生成截图，并补齐`inputbox`、`file_save_dialog`、参考对象配置与自定义绘图图片。无头测试通过模拟状态事件展示`screen`的状态回调，使用占位区呈现布局。

截图后打开原尺寸PNG检查文字边界、示例选中状态、图注与控件间距。运行`npm run docs:build`验证站点。

`project_story`使用原例程取得第一个`window`和导出窗体的交互状态，并用离屏夹具重现5个工程的输入、确认和状态变化。`designer`同时捕获实际的基础篇设计文件。工程图中的日志、图片、远程会话和采样状态采用可复现的本地数据。

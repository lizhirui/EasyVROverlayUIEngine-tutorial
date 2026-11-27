# 窗体设计、预览与代码导出

在Form Designer中可布局控件、编辑属性、预览窗体并导出SDK代码。

![窗体设计器界面区域标注](/images/zh/vr_designer_annotated.png)

---

## 设计器界面

启动SteamVR和Engine后，从Desktop打开Form Designer，或运行`D:\Tools\EasyVRUI\app\form_designer\easyvrui_form_designer.exe`。Desktop从`app/desktop/config.json`找到安装好的`app/form_designer/easyvrui_form_designer.easyvrui`。设计器界面分为四个区域。

1. **顶部`menubar`与`toolbar`**：
   - **文件 / 视图 / 布局 / 运行 / 导出**：支持新建/打开`.easyvruifrm`设计文件、网格吸附、画布缩放、对齐/等宽等高/层次调整、**启动或停止VR实时预览**，以及**导出Python / 导出C++**。
2. **左侧控件栏（Toolbox）与对象树（Object Tree）**：
   - **控件栏**：按注册表提供全部已注册的内置控件，例如`label`、`rich_label`、`button`、`textbox`、`combobox`、`datetime_selector`、`listbox`、`listview`、`grid`、`checkbox`、`radiobutton`、`numericupdown`、`slider`、`progressbar`、`panel`、`scrollpanel`、`tabcontrol`、`treeview`、`image`、`screen`、`splitter`、`menubar`、`toolbar`、`blank`。
   - **对象树**：展示完整的父子层级结构，控件重叠时可在对象树中直接选中目标控件。
3. **中间设计画布**：
   - 对应VR窗口的可视化编辑区，支持网格吸附、框选多选、拖拽调整尺寸以及撤销/重做（`Ctrl+Z` / `Ctrl+Y`）。
   - 对于`tabcontrol`，点击画布页签或在对象树中选择页签只切换设计态当前可见页，便于向不同页拖放和编辑子控件；窗体运行时的初始选中页通过属性面板的`selected_index`配置。
4. **右侧属性栏**：
   - `name`固定在最顶部，其余属性按字母顺序排列，可直接修改文本、颜色、字体、曲率、`tooltip_text`、`tag`和`datetime`等属性。编辑`datetime_selector`的`datetime`属性时，点击属性值直接打开内嵌原生`datetime_selector`控件的编辑对话框（支持日历选日期、时间微调、Clear清空与确定写回），设计文件保存为`YYYY-MM-DD HH:MM:SS`字符串或`null`。

---

## 短语发送界面的设计与预览

示例使用`label`显示提示、`textbox`收集短语、`button`执行发送。

### 1. 新建并保存设计文件

点击菜单 **文件 → 新建窗体**（或使用默认新建的空窗体），然后点击 **文件 → 保存**，保存为`quick_shout_window.easyvruifrm`。

::: tip 窗体类名的生成规则与外部文件监测
属性栏中窗体的`name`为**只读**，直接对应`.easyvruifrm`的文件名（不包含扩展名）。通过导出菜单生成布局代码时，文件与类名统一附加`_ui`后缀（已有`_ui`后缀时保留单个后缀）：例如`quick_shout_window.easyvruifrm`导出为`quick_shout_window_ui.py`或`quick_shout_window_ui.h`与`quick_shout_window_ui.cpp`，布局类名为`quick_shout_window_ui`，构造函数默认`name`参数仍为`quick_shout_window`。如需重命名，可通过文件菜单中的“移动设计文件”完成。

设计器同时监测已打开文件在磁盘上的外部变化或删除：检测到外部修改时弹出重载确认（本地有未保存改动时另行提示，确认重载会重建画布并停止当前预览）；拒绝重载后继续编辑并在保存时遇到外部更新会弹出覆盖确认。
:::

### 2. 添加控件到画布

从左侧**控件栏**依次将以下三个控件拖入中间画布：
1. 在上方放置一个`label`；
2. 在中间放置一个`textbox`；
3. 在下方放置一个`button`。

可以通过边框拖拽调整尺寸，或按住`Ctrl`多选控件后使用顶部**布局**工具栏中的“左对齐”“统一宽度”快速对齐。

### 3. 设置控件属性

依次选中窗体与各控件，在右侧**属性栏**中修改以下字段：

|目标对象|属性名|设置值|说明|
|---|---|---|---|
|**窗体本身**（点击画布空白处）|`title`|`静音快捷喊话条`|窗口标题栏显示的文字|
|**`label`**|`name`|`label_hint`|导出代码中的成员变量名，建议采用`类型_用途`格式|
|**`label`**|`text`|`输入想说的话：`|显示的提示文本|
|**`textbox`**|`name`|`textbox_message`|业务代码中通过`self.ui.textbox_message`或`ui->textbox_message`访问|
|**`textbox`**|`tag`|`chatbox_input`|供程序逻辑识别的自定义字符串标记|
|**`button`**|`name`|`button_send`|按钮成员名|
|**`button`**|`text`|`发送`|按钮显示文本|
|**`button`**|`tooltip_text`|`把文本框里的内容发出去`|按钮悬停提示文本|

### 4. 在VR中实时预览

下图是设计器打开本章示例`quick_shout_window.easyvruifrm`后的画布。对象树、画布与属性栏对应同一份设计。

![本章设计文件的画布排版](/images/zh/basics_form_design.png)

确认`easyvrui_engine.exe`正在运行后，点击工具栏上的 **运行 → 启动**：
- 若存在未保存更改，设计器会提示“保存并启动”；
- 启动后窗体会在SteamVR中实时运行，可以直接测试点击`textbox`以及将激光悬停在`button`上查看`tooltip_text`效果；
- 预览期间属性栏切换为只读显示大纲中主选控件的运行时属性；点击属性栏顶部锁按钮可冻结快照，带差异的属性行或结构体字段可通过右侧应用按钮写回设计文档（支持撤销/重做）；
- 预览完成后，再次点击**停止**即可返回设计期编辑状态。

---

## 代码导出与业务逻辑

界面设计完成后，点击菜单 **导出 → 导出Python** 或 **导出 → 导出C++**：
- 导出Python会在`.easyvruifrm`同目录生成`quick_shout_window_ui.py`（类`quick_shout_window_ui`继承`easyvrui.window`）；
- 导出C++会在同目录生成`quick_shout_window_ui.h`与`quick_shout_window_ui.cpp`（类`quick_shout_window_ui`继承`easyvrui::window`，构造函数中完成全部控件初始化）。

### 在应用代码中实现事件

导出的文件**仅包含界面布局代码**（创建控件、设置属性、加入`control_list`），所有子控件均以`name`作为公开成员暴露。

**推荐采用组合或派生模式**：新建自己的业务类（如`my_shout_app`），持有或派生导出的布局类（当前导出器生成`quick_shout_window_ui`，下方随仓示例工程中的预置布局类为`quick_shout_window`），再通过成员绑定按钮点击事件。点击后，业务方法读取`textbox`内容并更新`label`文本。

::: code-group
```python [Python（my_shout_app.py）]
from easyvrui import run
from quick_shout_window import quick_shout_window

class my_shout_app:
    def __init__(self):
        self.ui = quick_shout_window()
        self.ui.button_send.on_click += self.button_send_click

    def button_send_click(self, source, event):
        message = self.ui.textbox_message.text
        self.ui.label_hint.text = f"已发送：{message}"

    def show(self):
        self.ui.show()

def main():
    app_main = my_shout_app()
    app_main.show()
    run("quick_shout_app")

if __name__ == "__main__":
    main()
```

<<< ../../examples/basics/04_form_designer/cpp/main.cpp
:::

采用组合模式的最大优势在于：**重新导出界面不会覆盖业务代码**。后续在`.easyvruifrm`中调整控件大小、颜色或新增控件并重新导出时，仅`quick_shout_window.py`（或`quick_shout_window.h`与`quick_shout_window.cpp`）会被更新，而`my_shout_app`中的事件绑定和业务逻辑完全保留。

---

## 导出前后的交互核验

C++应用持有生成的`quick_shout_window`实例，并订阅该实例公开的`on_click`。Python的`my_shout_app.ui`承担相同职责。重新导出布局后，业务代码仍通过公开成员和事件操作窗口实例。

![运行导出代码后的初始window](/images/zh/basics_form_initial.png)

测试宿主在`textbox_message`输入`Ready for sync`。激活`button_send`后，业务回调读取输入并更新`label_hint`。

![输入文本并触发发送后的label反馈](/images/zh/basics_form_sent.png)

从[控件目录](/guide/)可查阅控件属性、事件和例程。需要在导出后安装程序化内容时，可参考[blank](/guide/controls/command-and-display/blank)的占位替换示例。
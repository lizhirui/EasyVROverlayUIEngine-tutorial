# Form Design, Preview, and Code Export

In Form Designer, you can arrange controls, edit properties, preview the form, and export SDK code.

![Form Designer Interface Area Annotation](/images/en/vr_designer_annotated.png)

---

## Designer Interface

After starting SteamVR and Engine, open Form Designer from Desktop, or run `D:\Tools\EasyVRUI\app\form_designer\easyvrui_form_designer.exe`. The Desktop finds the installed `app/form_designer/easyvrui_form_designer.easyvrui` from `app/desktop/config.json`. The designer interface is divided into four areas.

1. **Top `menubar` and `toolbar`**:
   - **File / View / Layout / Run / Export**: Supports creating/opening `.easyvruifrm` design files, grid snapping, canvas zooming, alignment/equal width and level adjustment, **starting or stopping VR real-time preview**, and **exporting Python / C++**.
2. **Left Control Panel (Toolbox) and Object Tree (Object Tree)**:
   - **Control Panel**: Provides all built-in controls such as `label`, `button`, `textbox`, `combobox`, `listbox`, `listview`, `grid`, `checkbox`, `radiobutton`, `numericupdown`, `slider`, `progressbar`, `panel`, `scrollpanel`, `tabcontrol`, `treeview`, `image`, `screen`, `splitter`, `menubar`.
   - **Object Tree**: Displays a complete parent-child hierarchy. When controls overlap, you can directly select the target control in the object tree.
3. **Middle Design Canvas**:
   - It is the visual editing area corresponding to the VR window. It supports grid snapping, multiple selections by box selection, dragging to adjust size, and undo/redo (`Ctrl+Z` / `Ctrl+Y`).
4. **Right Property Bar**:
   - `name` is fixed at the top, and the remaining properties are arranged in alphabetical order. You can directly modify text, color, font, curvature, `tooltip_text`, and `tag` properties.

---

## Design and Preview of the Phrase Sending Interface

Example: Use `label` to display prompts, `textbox` to collect phrases, and `button` to perform sending.

### 1. Create and save a design file

Click on the menu **File → New Form**(or use the default empty form for creation), then click**File → Save**, and save as `quick_shout_window.easyvruifrm`.

::: tip How class names are generated
The `name` of the form in the property bar is **read-only**, directly corresponding to the file name of `.easyvruifrm` (without the extension). For example, if saved as `quick_shout_window.easyvruifrm`, the exported class name will be `quick_shout_window`. If you need to rename it, you can do so through the "Move Design File" option in the file menu, and the designer will automatically synchronize the form name.
:::

### 2. Add Controls to the Canvas

Drag the following three controls from the left **Control Panel** into the middle canvas in sequence:
1. Place one `label` above;
2. Place one `textbox` in the middle;
3. Place a `button` below.

You can adjust the size by dragging the border, or hold down the `Ctrl` and select multiple controls, then use the **Layout** toolbar in the top to quickly align them with "Left Aligned" or "Uniform Width".

### 3. Set control properties

Select the form and each control in turn, and modify the following fields in the **Property Bar** on the right:

|Target object|Property name|Set value|Description|
|---|---|---|---|
|**Form itself** (click the blank area of the canvas)|`title`|`静音快捷喊话条`|Text displayed in the window title bar|
|**`label`**|`name`|`label_hint`|The names of member variables in the exported code, recommended to use `类型_用途` format|
|**`label`**|`text`|`输入想说的话：`|Displayed prompt text|
|**`textbox`**|`name`|`textbox_message`|Accessed in business code through `self.ui.textbox_message` or `ui->textbox_message`|
|**`textbox`**|`tag`|`chatbox_input`|Custom string markers for program logic recognition|
|**`button`**|`name`|`button_send`|Button member name|
|**`button`**|`text`|`发送`|Button display text|
|**`button`**|`tooltip_text`|`把文本框里的内容发出去`|Button hover prompt text|

### 4. Real-time preview in VR

The following image shows the canvas after the designer opens the example `quick_shout_window.easyvruifrm` of this chapter. The object tree, canvas, and Property Bar correspond to the same design.

Canvas layout of the ![design file of this chapter:](/images/en/basics_form_design.png)

After confirming that `easyvrui_engine.exe` is running, click **Run → Start** on the toolbar:
- If there are unsaved changes, the designer will prompt "Save and Start";
- After starting, the form will run in real time in SteamVR. You can directly test by clicking on `textbox` and hovering a laser pointer over `button` to see the effect of `tooltip_text`;
- After the preview is complete, click **Stop** again to return to the editing state.

---

## Code export and business logic

After the interface design is completed, click on the menu **Export → Export Python**or**Export → Export C++**:
- Exporting Python will generate `quick_shout_window.py` in the same directory as `.easyvruifrm`;
- Exporting C++ will generate both `quick_shout_window.h` and `quick_shout_window.cpp` in the same directory, and all controls will be initialized in the constructor.

### Implement events in the application code

The exported file **only contains interface layout code** (creating controls, setting properties, adding `control_list`), with all sub-controls exposed as public members using `name`.

**It is recommended to use the composite pattern**: Create your own business classes (such as `my_shout_app`), hold instances of `quick_shout_window` in them, and bind button click events through `ui` members. After clicking, the business method reads the content of `textbox` and updates the text in `label`.

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
        self.ui.label_hint.text = f"Sent: {message}"

    def show(self):
        self.ui.show()

def main():
    app_main = my_shout_app()
    app_main.show()
    run("quick_shout_app")

if __name__ == "__main__":
    main()
```

<<< ../../../examples/basics/04_form_designer/cpp/main.cpp
:::

The greatest advantage of using the composite pattern is that **re-exporting the interface does not overwrite the business code**. When adjusting control sizes, colors, or adding new controls in `.easyvruifrm` and re-exporting, only `quick_shout_window.py` (or `quick_shout_window.h` and `quick_shout_window.cpp`) will be updated, while the event bindings and business logic in `my_shout_app` remain intact.

---

## Interaction verification before and after export

C++ application holds the generated `quick_shout_window` instance and subscribes to the public `on_click` of that instance. Python's `my_shout_app.ui` performs the same function. After re-exporting the layout, business code still operates on the window instance through public members and events.

The initial window](/images/en/basics_form_initial.png) after ![runs the exported code

Test the host by entering `Ready for sync` in `textbox_message`. After activating `button_send`, the business callback reads the input and updates `label_hint`.

The label feedback](/images/en/basics_form_sent.png) after ![enters text and triggers sending

From the control directory of [,](/en/guide/) allows access to control properties, events, and routines. When installing programmatic content after export, refer to the placeholder replacement examples in [blank](/en/guide/controls/command-and-display/blank).
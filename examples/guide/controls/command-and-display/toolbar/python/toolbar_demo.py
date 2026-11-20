from easyvrui import drawing_image, label, rect, run, toolbar, toolbar_button, window

def main():
    window_main = window("window_main")
    window_main.title = "预览操作"
    window_main.set_size(680, 310)
    toolbar_main = toolbar("toolbar_main")
    toolbar_main.rect = rect(36, 85, 608, 67)
    toolbar_main.tool_size = 52
    toolbar_main.spacing = 10.0
    button_preview = toolbar_button("button_preview")
    button_preview.icon = drawing_image(1, 1, bytes((104, 194, 241, 255)))
    button_preview.tooltip_text = "预览结果"
    toolbar_main.button_list.add(button_preview)
    toolbar_main.button_list.add_separator("separator_preview")
    label_state = label("label_state")
    label_state.rect = rect(36, 194, 608, 46)
    label_state.text = "单击蓝色操作项"

    def button_preview_click(source, event):
        label_state.text = "已请求预览"

    button_preview.on_click += button_preview_click
    window_main.control_list.add(toolbar_main)
    window_main.control_list.add(label_state)
    window_main.show()
    run("tutorial_toolbar")

if __name__ == "__main__":
    main()
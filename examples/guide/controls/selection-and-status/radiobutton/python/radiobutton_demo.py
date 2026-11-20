from easyvrui import label, panel, radiobutton, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "通知模式"
    window_main.set_size(650, 320)
    panel_mode = panel("panel_mode")
    panel_mode.rect = rect(32, 82, 586, 126)
    window_main.control_list.add(panel_mode)
    radiobutton_all = radiobutton("radiobutton_all")
    radiobutton_all.rect = rect(16, 8, 554, 46)
    radiobutton_all.text = "接收全部通知"
    panel_mode.control_list.add(radiobutton_all)
    radiobutton_important = radiobutton("radiobutton_important")
    radiobutton_important.rect = rect(16, 68, 554, 46)
    radiobutton_important.text = "仅接收重要通知"
    panel_mode.control_list.add(radiobutton_important)
    label_state = label("label_state")
    label_state.rect = rect(32, 226, 586, 50)
    label_state.text = "当前模式：仅接收重要通知"
    window_main.control_list.add(label_state)
    radiobutton_important.checked = True

    def radiobutton_mode_checked_changed(source, event):
        if source.checked:
            label_state.text = "当前模式：" + source.text

    radiobutton_all.on_checked_changed += radiobutton_mode_checked_changed
    radiobutton_important.on_checked_changed += radiobutton_mode_checked_changed
    window_main.show()
    run("tutorial_radiobutton")

if __name__ == "__main__":
    main()
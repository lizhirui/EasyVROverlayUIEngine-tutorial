from easyvrui import checkbox, label, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "通知偏好"
    window_main.set_size(650, 315)
    checkbox_sound = checkbox("checkbox_sound")
    checkbox_sound.rect = rect(32, 80, 586, 48)
    checkbox_sound.text = "播放通知声音"
    window_main.control_list.add(checkbox_sound)
    checkbox_badge = checkbox("checkbox_badge")
    checkbox_badge.rect = rect(32, 143, 586, 48)
    checkbox_badge.text = "显示未读状态"
    window_main.control_list.add(checkbox_badge)
    label_state = label("label_state")
    label_state.rect = rect(32, 219, 586, 46)
    label_state.text = "通知声音已关闭"
    window_main.control_list.add(label_state)
    checkbox_badge.checked = True

    def checkbox_sound_checked_changed(source, event):
        label_state.text = "通知声音已开启" if source.checked else "通知声音已关闭"

    checkbox_sound.on_checked_changed += checkbox_sound_checked_changed
    window_main.show()
    run("tutorial_checkbox")

if __name__ == "__main__":
    main()
from easyvrui import button, label, progressbar, rect, run, window

def main():
    window_main = window("window_main")
    window_main.title = "同步进度"
    window_main.set_size(650, 310)
    label_state = label("label_state")
    label_state.rect = rect(32, 79, 586, 47)
    label_state.text = "已同步2/8项"
    window_main.control_list.add(label_state)
    progressbar_sync = progressbar("progressbar_sync")
    progressbar_sync.rect = rect(32, 140, 586, 31)
    window_main.control_list.add(progressbar_sync)
    button_next = button("button_next")
    button_next.rect = rect(32, 204, 212, 49)
    button_next.text = "完成下一项"
    window_main.control_list.add(button_next)
    progressbar_sync.maximum = 8
    progressbar_sync.value = 2

    def progressbar_sync_value_changed(source, event):
        complete = source.value == source.maximum
        label_state.text = "同步完成" if complete else f"已同步{source.value}/8项"
        button_next.enabled = not complete

    def button_next_click(source, event):
        progressbar_sync.value += 1

    progressbar_sync.on_value_changed += progressbar_sync_value_changed
    button_next.on_click += button_next_click
    window_main.show()
    run("tutorial_progressbar")

if __name__ == "__main__":
    main()
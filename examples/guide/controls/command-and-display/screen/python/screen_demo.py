from easyvrui import label, rect, run, screen, window

def main():
    window_main = window("window_main")
    window_main.title = "显示输出监视"
    window_main.set_size(680, 357)
    screen_preview = screen("screen_preview")
    screen_preview.rect = rect(36, 86, 608, 168)
    label_state = label("label_state")
    label_state.rect = rect(36, 267, 608, 48)
    label_state.text = "等待显示器画面"

    def screen_preview_screen_restored(source, event):
        label_state.text = "采集源可用"

    def screen_preview_screen_unavailable(source, event):
        label_state.text = "采集源不可用"

    screen_preview.on_screen_restored += screen_preview_screen_restored
    screen_preview.on_screen_unavailable += screen_preview_screen_unavailable
    window_main.control_list.add(screen_preview)
    window_main.control_list.add(label_state)
    window_main.show()
    run("tutorial_screen")

if __name__ == "__main__":
    main()